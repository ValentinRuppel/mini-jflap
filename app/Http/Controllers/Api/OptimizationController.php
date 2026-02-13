<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Process;

class OptimizationController extends Controller
{
    public function optimize(Request $request)
    {
        // 1. Validar
        $request->validate([
            'automata' => 'required|array',
            'algoritmo' => 'required|string|in:genetico,hill_climbing'
        ]);

        // --- CORRECCIÓN AQUÍ ---
        // Empaquetamos AMBOS datos para enviarlos a Python
        $dataParaPython = [
            'algoritmo' => $request->input('algoritmo'),
            'automata'  => $request->input('automata')
        ];
        
        // Ahora codificamos el paquete completo
        $inputJson = json_encode($dataParaPython); 
        // -----------------------
        
        // 2. Definir rutas
        $pythonPath = 'python'; // O 'python3' si estás en Linux/Mac
        $scriptPath = base_path('ai_module/optimizer.py');

        // 3. Ejecutar el proceso enviando el paquete completo
        $result = Process::run([$pythonPath, $scriptPath, $inputJson]);

        // 4. Verificar errores
        if ($result->failed()) {
            return response()->json([
                'error' => 'Error al ejecutar el script de IA',
                'detalle' => $result->errorOutput()
            ], 500);
        }

        // 5. Respuesta
        $output = $result->output();
        $automataOptimizado = json_decode($output, true);

        return response()->json([
            'message' => 'Optimización completada',
            'automata_original' => $request->input('automata'),
            'automata_optimizado' => $automataOptimizado
        ]);
    }
}