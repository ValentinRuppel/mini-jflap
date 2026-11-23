<?php

namespace Database\Seeders;

use App\Models\Automata;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class AutomataDemoSeeder extends Seeder
{
    public function run(): void
    {
        $users = User::all();

        if ($users->isEmpty()) {
            $demoUser = User::create([
                'name' => 'Demo FLEXA',
                'email' => 'demo@flexa.edu',
                'email_verified_at' => now(),
                'password' => Hash::make('password'),
            ]);
            $users = collect([$demoUser]);
        }

        $demos = [
            // 1. DFA simple ya mínimo: cadenas binarias que terminan en "01" (3 estados)
            [
                'nombre' => 'DFA — Cadenas terminadas en 01',
                'tipo' => 'DFA',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1', 'q2'],
                    'alfabeto' => ['0', '1'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q2'],
                    'transiciones' => [
                        'q0' => ['0' => 'q1', '1' => 'q0'],
                        'q1' => ['0' => 'q1', '1' => 'q2'],
                        'q2' => ['0' => 'q1', '1' => 'q0'],
                    ],
                ],
            ],

            // 2. DFA redundante de 6 estados: paridad par de 1s (mínimo teórico: 2 estados)
            [
                'nombre' => 'DFA Redundante — Paridad de 1s (6 estados)',
                'tipo' => 'DFA',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
                    'alfabeto' => ['0', '1'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q0', 'q2', 'q4'],
                    'transiciones' => [
                        'q0' => ['0' => 'q2', '1' => 'q1'],
                        'q1' => ['0' => 'q3', '1' => 'q2'],
                        'q2' => ['0' => 'q4', '1' => 'q3'],
                        'q3' => ['0' => 'q5', '1' => 'q4'],
                        'q4' => ['0' => 'q0', '1' => 'q5'],
                        'q5' => ['0' => 'q1', '1' => 'q0'],
                    ],
                ],
            ],

            // 3. NFA con bifurcaciones múltiples: cadenas que contienen "101"
            [
                'nombre' => 'NFA — Cadenas que contienen 101',
                'tipo' => 'NFA',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1', 'q2', 'q3'],
                    'alfabeto' => ['0', '1'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q3'],
                    'transiciones' => [
                        'q0' => ['0' => ['q0'], '1' => ['q0', 'q1']],
                        'q1' => ['0' => ['q2'], '1' => []],
                        'q2' => ['0' => [], '1' => ['q3']],
                        'q3' => ['0' => ['q3'], '1' => ['q3']],
                    ],
                ],
            ],

            // 4. NFA redundante de 6 estados: cadenas que terminan en "00" (reduce a 3 estados)
            [
                'nombre' => 'NFA Redundante — Termina en 00 (6 estados)',
                'tipo' => 'NFA',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
                    'alfabeto' => ['0', '1'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q4', 'q5'],
                    'transiciones' => [
                        'q0' => ['0' => ['q0', 'q1', 'q2', 'q3'], '1' => ['q0', 'q1']],
                        'q1' => ['0' => ['q0', 'q2', 'q3'], '1' => ['q0']],
                        'q2' => ['0' => ['q4'], '1' => []],
                        'q3' => ['0' => ['q5'], '1' => []],
                        'q4' => ['0' => [], '1' => []],
                        'q5' => ['0' => [], '1' => []],
                    ],
                ],
            ],

            // 5. AP clásico: lenguaje a^n b^n (n >= 1) con aceptación por estado final + pila vacía
            [
                'nombre' => 'AP — Lenguaje aⁿbⁿ',
                'tipo' => 'AP',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1'],
                    'alfabeto' => ['a', 'b'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q1'],
                    'transiciones' => [
                        'q0' => [
                            'a' => [['dest' => 'q0', 'pop' => 'λ', 'push' => 'A']],
                            'b' => [['dest' => 'q1', 'pop' => 'A', 'push' => 'λ']],
                        ],
                        'q1' => [
                            'a' => [],
                            'b' => [['dest' => 'q1', 'pop' => 'A', 'push' => 'λ']],
                        ],
                    ],
                ],
            ],

            // 6. AP clásico: palíndromos con marca central w c w^R
            [
                'nombre' => 'AP — Palíndromos wcwᴿ',
                'tipo' => 'AP',
                'is_optimized' => false,
                'json_definicion' => [
                    'estados' => ['q0', 'q1'],
                    'alfabeto' => ['a', 'b', 'c'],
                    'estado_inicial' => 'q0',
                    'estados_finales' => ['q1'],
                    'transiciones' => [
                        'q0' => [
                            'a' => [['dest' => 'q0', 'pop' => 'λ', 'push' => 'a']],
                            'b' => [['dest' => 'q0', 'pop' => 'λ', 'push' => 'b']],
                            'c' => [['dest' => 'q1', 'pop' => 'λ', 'push' => 'λ']],
                        ],
                        'q1' => [
                            'a' => [['dest' => 'q1', 'pop' => 'a', 'push' => 'λ']],
                            'b' => [['dest' => 'q1', 'pop' => 'b', 'push' => 'λ']],
                            'c' => [],
                        ],
                    ],
                ],
            ],
        ];

        foreach ($users as $user) {
            foreach ($demos as $demo) {
                Automata::updateOrCreate(
                    [
                        'user_id' => $user->id,
                        'nombre' => $demo['nombre'],
                    ],
                    [
                        'tipo' => $demo['tipo'],
                        'json_definicion' => $demo['json_definicion'],
                        'is_optimized' => $demo['is_optimized'],
                    ]
                );
            }
        }
    }
}
