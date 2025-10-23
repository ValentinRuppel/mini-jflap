<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Automata;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\Response;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests; 
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Support\Facades\Auth;

class AutomataExportController extends Controller
{
    use AuthorizesRequests, ValidatesRequests;
    /** Exportar el autómata como JSON descargable */
    public function export(Automata $automata)
    {
        $this->authorize('view', $automata);

        $data = [
            'nombre' => $automata->nombre,
            'tipo' => $automata->tipo,
            'json_definicion' => $automata->json_definicion,
        ];

        $filename = 'automata_' . $automata->id . '.json';

        return response()->streamDownload(
            function () use ($data) { // <-- Cambia a 'function'
                echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
            },
            $filename,
            ['Content-Type' => 'application/json']
        );
    }

    /** Importar un autómata desde archivo JSON */
    public function import(Request $request)
    {
        $request->validate([
            'file' => 'required|file|mimes:json,txt',
        ]);

        $json = json_decode(file_get_contents($request->file('file')), true);

        if (!$json || !isset($json['json_definicion'])) {
            return response()->json(['error' => 'Archivo inválido'], 422);
        }

        $automata = Automata::create([
            'nombre' => $json['nombre'] ?? 'Importado',
            'tipo' => $json['tipo'] ?? 'DFA',
            'json_definicion' => $json['json_definicion'],
            'owner_id' => Auth::id(),
            'visibility' => 'private',
        ]);

        return response()->json([
            'message' => 'Autómata importado con éxito',
            'automata' => $automata,
        ], Response::HTTP_CREATED);
    }
}
