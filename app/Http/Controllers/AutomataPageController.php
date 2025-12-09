<?php

namespace App\Http\Controllers;

use App\Models\Automata;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Redirect;

class AutomataPageController extends Controller
{
    public function index()
    {
        // Bonus: Ya te dejo listo para que el Index vea los automatas del usuario
        $automatas = Automata::where('user_id', Auth::id())
                        ->orderByDesc('created_at')
                        ->get();

        return Inertia::render('Automatas/Index', [
            'automatas' => $automatas
        ]);
    }
    public function create()
    {
        return Inertia::render('Automatas/Create');
    }

    // Este es el método que te faltaba
    public function store(Request $request)
    {
        $validated = $request->validate([
            'nombre' => 'required|string|max:255',
            'tipo' => 'required|in:DFA,NFA',
            'json_definicion' => 'required|array',
        ]);

        $request->user()->automatas()->create($validated);

        // CON INERTIA: No devolvemos JSON, redirigimos al index
        return Redirect::route('automatas.index');
    }
    public function show(Automata $automata)
    {
        // Seguridad: Verificar que el autómata pertenezca al usuario logueado
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
            'tipo' => 'required|in:DFA,NFA',
            'json_definicion' => 'required|array',
        ]);

        $automata->update($validated);

        return Redirect::route('automatas.index')->with('message', 'Autómata actualizado');
    }

    // Lógica de eliminación
    public function destroy(Automata $automata)
    {
        if ($automata->user_id !== Auth::id()) abort(403);
        
        $automata->delete();

        // Inertia maneja esto y refresca la lista automáticamente
        return Redirect::route('automatas.index');
    }
}
