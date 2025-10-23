<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Automata;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AutomataController extends Controller
{
    public function index()
    {
        $userId = Auth::id();

        $automatas = Automata::where('visibility', 'public')
            ->orWhere('owner_id', $userId)
            ->get();

        return response()->json($automatas);
    }


    public function store(Request $request)
    {
        $data = $request->validate([
            'nombre' => 'required|string|max:100',
            'tipo' => 'required|in:DFA,NFA',
            'json_definicion' => 'required|array',
            'visibility' => 'in:private,public',
        ]);

        $data['owner_id'] = Auth::id();

        $automata = Automata::create($data);

        return response()->json($automata, 201);
    }

    public function show(Automata $automata)
    {
        return $automata;
    }

    public function destroy(Automata $automata)
    {
        $automata->delete();
        return response()->json(null, 204);
    }
    public function probar(Request $request, Automata $automata)
    {
        $request->validate([
            'cadena' => 'required|string'
        ]);

        $dfa = $automata->json_definicion;
        $cadena = str_split($request->cadena);

        $estadoActual = $dfa['estado_inicial'];
        $recorrido = [$estadoActual];

        foreach ($cadena as $simbolo) {
            if (!isset($dfa['transiciones'][$estadoActual][$simbolo])) {
                return response()->json([
                    'aceptada' => false,
                    'recorrido' => $recorrido
                ]);
            }

            $estadoActual = $dfa['transiciones'][$estadoActual][$simbolo];
            $recorrido[] = $estadoActual;
        }

        $aceptada = in_array($estadoActual, $dfa['estados_finales']);

        return response()->json([
            'aceptada' => $aceptada,
            'recorrido' => $recorrido
        ]);
    }

}
