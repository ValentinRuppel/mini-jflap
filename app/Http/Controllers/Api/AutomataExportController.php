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


public function import(Request $request)
{
    $request->validate([
        'file' => 'required|file|mimes:json,txt',
    ]);

    // Leer el contenido del archivo
    $content = file_get_contents($request->file('file'));
    $json = json_decode($content, true);

    // Validación básica de JSON
    if (json_last_error() !== JSON_ERROR_NONE) {
        return response()->json(['error' => 'El archivo no es un JSON válido'], 422);
    }

    // --- LÓGICA HÍBRIDA (La parte importante) ---
    
    // Variables por defecto
    $definicion = null;
    $tipo = 'DFA'; 
    $nombre = 'Importado';

    // CASO 1: Es el FORMATO NUEVO (tiene la clave json_definicion)
    if (isset($json['json_definicion'])) {
        $definicion = $json['json_definicion'];
        $tipo = $json['tipo'] ?? 'DFA'; // Aquí captura si es NFA o Pila
        $nombre = $json['nombre'] ?? 'Importado';
    } 
    // CASO 2: Es el FORMATO VIEJO (El JSON es directamente la definición con nodos)
    elseif (isset($json['nodos']) || isset($json['enlaces'])) {
        $definicion = $json; // Todo el archivo es la definición
        $tipo = 'DFA'; // Asumimos DFA por defecto si es viejo
        $nombre = 'Automata Antiguo';
    } 
    // CASO 3: Estructura desconocida
    else {
        return response()->json(['error' => 'Archivo inválido: No se reconocen nodos ni enlaces.'], 422);
    }

    // Crear el autómata en Base de Datos
    $automata = Automata::create([
        'nombre' => $nombre,
        'tipo' => $tipo,
        'json_definicion' => $definicion, // Laravel lo convertirá a JSON automáticamente si está casteado en el modelo
        'owner_id' => Auth::id(),
        'visibility' => 'private',
    ]);

    return response()->json([
        'message' => 'Autómata importado con éxito',
        'automata' => $automata,
    ], Response::HTTP_CREATED);
}
}
