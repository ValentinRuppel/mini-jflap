<?php

namespace App\Http\Controllers;

use App\Models\Automata;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Redirect;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class AutomataPageController extends Controller
{
    public function index()
    {
        $automatas = Automata::query()
            ->select([
                'id',
                'nombre',
                'tipo',
                'is_optimized',
                'created_at',
                DB::raw("COALESCE(JSON_LENGTH(json_definicion, '$.estados'), 0) as estados_count"),
                DB::raw("COALESCE(JSON_LENGTH(json_definicion, '$.alfabeto'), 0) as alfabeto_count"),
            ])
            ->where('user_id', Auth::id())
            ->orderByDesc('created_at')
            ->paginate(9);

        return Inertia::render('Automatas/Index', [
            'automatas' => $automatas
        ]);
    }
    public function create()
    {
        return Inertia::render('Automatas/Create');
    }
    public function store(Request $request)
    {
        $validated = $request->validate([
            'nombre' => 'required|string|max:255',
            'tipo' => 'required|in:DFA,NFA,AP',
            'json_definicion' => 'required|array',
        ]);
        $request->user()->automatas()->create($validated);
        return Redirect::route('automatas.index');
    }

    public function optimize(Request $request, Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) abort(403);
        // Validar input (Recibir 'algoritmo')
        $request->validate([
            'algoritmo' => 'required|in:genetico,sa'
        ]);
        // Empaquetar todo para Python
        $payload = json_encode([
            'tipo' => $automata->tipo,
            'json_definicion' => $automata->json_definicion,
            'algoritmo' => $request->input('algoritmo')
        ]);

        $scriptPath = base_path('ai_module/optimizer.py');
        $command = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN' ? 'python' : 'python3';

        $process = new Process([$command, $scriptPath]);
        $process->setInput($payload);
        $process->setTimeout(60);

        try {
            $process->mustRun();
            $output = $process->getOutput();
            $result = json_decode($output, true);

            if (!$result || (isset($result['success']) && !$result['success'])) {
                $msg = $result['message'] ?? 'Error desconocido';
                return back()->with('error', 'Fallo IA: ' . $msg);
            }

            // Crear nuevo autómata
            $newAutomata = Automata::create([
                'user_id' => Auth::id(),
                'nombre' => $automata->nombre . ' (' . ucfirst($request->algoritmo) . ')',
                'tipo' => $automata->tipo,
                'json_definicion' => $result['automata'],
                'is_optimized' => true
            ]);
            return Redirect::route('automatas.show', $newAutomata)
                ->with('reporte_ia', $result['reporte']);
        } catch (ProcessFailedException $exception) {
        return back()->withErrors(['error' => 'Error crítico.']);
        }
    }

    public function benchmark(Request $request, Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) abort(403);

        $validated = $request->validate([
            'corridas' => 'nullable|integer|min:5|max:50',
        ]);

        $corridas = (int) ($validated['corridas'] ?? 25);

        $payload = json_encode([
            'modo' => 'benchmark',
            'corridas' => $corridas,
            'tipo' => $automata->tipo,
            'json_definicion' => $automata->json_definicion,
        ]);

        $scriptPath = base_path('ai_module/optimizer.py');
        $command = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN' ? 'python' : 'python3';

        $process = new Process([$command, $scriptPath]);
        $process->setInput($payload);
        $process->setTimeout(120);

        try {
            $process->mustRun();
            $output = $process->getOutput();
            $result = json_decode($output, true);

            if (!$result || (isset($result['success']) && !$result['success'])) {
                $msg = $result['message'] ?? 'Error desconocido al ejecutar el experimento.';
                return response()->json([
                    'success' => false,
                    'message' => 'Fallo IA: ' . $msg,
                ], 422);
            }

            return response()->json($result);
        } catch (ProcessFailedException $exception) {
            return response()->json([
                'success' => false,
                'message' => 'Error crítico al ejecutar el benchmark en Python.',
            ], 500);
        }
    }
    public function show(Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) {
            abort(403, 'No tenés permiso para ver este autómata.');
        }
        return Inertia::render('Automatas/Show', [
            'automata' => $automata
        ]);
    }
    public function edit(Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) abort(403);
        return Inertia::render('Automatas/Create', [
            'automata' => $automata
        ]);
    }

    // Lógica de actualización
    public function update(Request $request, Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) abort(403);
        $validated = $request->validate([
            'nombre' => 'required|string|max:255',
            'tipo' => 'required|in:DFA,NFA,AP',
            'json_definicion' => 'required|array',
        ]);
        $automata->update($validated);
        return Redirect::route('automatas.index')->with('message', 'Autómata actualizado');
    }

    // Lógica de eliminación
    public function destroy(Automata $automata){
        if ($automata->user_id !== Auth::id()) abort(403);
        $automata->delete();
        return Redirect::route('automatas.index');
    }
}
