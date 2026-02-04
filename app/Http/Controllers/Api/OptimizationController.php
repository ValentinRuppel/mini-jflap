<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Process;

class OptimizationController extends Controller
{
    public function optimize(Request $request)
    {
        // 1. Validar que nos manden un autómata
        $request->validate([
            'automata' => 'required|array', // El objeto JSON completo
            'algoritmo' => 'required|string|in:genetico,hill_climbing' // Para elegir estrategia después
        ]);

        $automataJson = json_encode($request->input('automata'));
        
        // 2. Definir la ruta al script de Python
        // Ajusta 'python' a 'python3' si estás en Linux/Mac
        $pythonPath = 'python'; 
        $scriptPath = base_path('ai_module/optimizer.py');

        // 3. Ejecutar el proceso
        // Pasamos el JSON como argumento de línea de comandos
        $result = Process::run([$pythonPath, $scriptPath, $automataJson]);

        // 4. Verificar si falló la ejecución del comando
        if ($result->failed()) {
            return response()->json([
                'error' => 'Error al ejecutar el script de IA',
                'detalle' => $result->errorOutput()
            ], 500);
        }

        // 5. Decodificar la respuesta de Python
        $output = $result->output();
        $automataOptimizado = json_decode($output, true);

        return response()->json([
            'message' => 'Optimización completada',
            'automata_original' => $request->input('automata'),
            'automata_optimizado' => $automataOptimizado
        ]);
    }
}