<template>
    <div class="h-screen flex flex-col bg-gray-50 overflow-hidden font-sans">

        <header
            class="bg-white border-b border-gray-200 relative z-20 shadow-sm px-6 py-4 flex justify-between items-center">
            <div class="flex items-center gap-4">
                <div class="bg-blue-50 p-2 rounded-lg border border-blue-100">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                    </svg>
                </div>
                <div>
                    <h1 class="text-xl font-bold text-gray-900 leading-none">{{ automata.nombre }}</h1>
                    <div class="flex items-center gap-2 mt-1">
                        <span
                            class="px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider bg-blue-100 text-blue-700 border-blue-200">
                            {{ automata.tipo }}
                        </span>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-3">
                <button @click="exportarJson"
                    class="text-sm text-gray-600 hover:text-blue-600 font-medium flex items-center gap-1">💾
                    Exportar</button>
                <div class="h-4 w-px bg-gray-300"></div>
                <Link :href="route('automatas.index')" prefetch class="text-sm text-gray-500 hover:text-gray-800">Volver</Link>
            </div>
        </header>


        <div class="flex flex-1 overflow-hidden relative">
            <main class="flex-1 relative bg-gray-100/50">
                <div ref="networkContainer" class="w-full h-full outline-none"></div>

                <div
                    class="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-200 z-10 select-none">
                    <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3">Referencias</h3>

                    <div class="space-y-3">
                        <div class="flex items-center gap-3">
                            <div
                                class="w-8 h-8 rounded-full bg-[#d1fae5] border border-[#2B7CE9] flex items-center justify-center text-xs font-mono text-gray-600 shadow-sm">
                                qi
                            </div>
                            <span class="text-xs font-medium text-gray-600">Estado Inicial</span>
                        </div>

                        <div class="flex items-center gap-3">
                            <div
                                class="w-8 h-8 rounded-full bg-white border border-[#2B7CE9] flex items-center justify-center text-xs font-mono text-gray-600 shadow-sm">
                                qn
                            </div>
                            <span class="text-xs font-medium text-gray-600">Estado Normal</span>
                        </div>

                        <div class="flex items-center gap-3">
                            <div
                                class="w-8 h-8 rounded-full bg-white border-[3px] border-[#2B7CE9] flex items-center justify-center text-xs font-bold font-mono text-gray-800 shadow-sm">
                                qf
                            </div>
                            <span class="text-xs font-medium text-gray-600">Estado Final</span>
                        </div>
                    </div>
                </div>
            </main>

            <aside class="w-[400px] bg-white border-l border-gray-200 shadow-xl z-10 flex flex-col">

                <div class="p-6 border-b border-gray-100">
                    <h2 class="font-bold text-lg text-gray-800">Simulador</h2>
                    <p class="text-xs text-gray-500">Prueba cadenas en tu {{ automata.tipo }}.</p>
                </div>

                <div class="p-6 flex-1 overflow-y-auto">
                    <div class="bg-gray-50 rounded-2xl p-5 border border-gray-100 mb-6">
                        <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Cadena de Entrada</label>
                        <input v-model="inputCadena" @keyup.enter="probarCadena" type="text"
                            class="w-full border p-3 rounded-xl font-mono tracking-widest" placeholder="Ej: 0011" />
                        <button @click="probarCadena" :disabled="!inputCadena"
                            class="mt-4 w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition">
                            Verificar
                        </button>
                    </div>

                    <div v-if="resultado !== null">
                        <div :class="resultado ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'"
                            class="border rounded-2xl p-6 text-center mb-4">
                            <div class="text-4xl mb-2">{{ resultado ? '✓' : '✕' }}</div>
                            <h3 :class="resultado ? 'text-green-800' : 'text-red-800'" class="font-bold text-xl">{{
                                resultado ? 'Aceptada' : 'Rechazada' }}</h3>
                        </div>

                        <div class="bg-gray-900 text-green-400 font-mono text-xs p-4 rounded-xl overflow-auto">
                            <p class="text-gray-500 mb-1">Traza Final (Estados alcanzados):</p>
                            [ {{ estadosFinalesAlcanzados.join(', ') }} ]
                        </div>
                    </div>
                </div>

<div v-if="!automata.is_optimized" class="p-4 border-t border-gray-100 bg-gray-50 z-20">
                    <div class="bg-white border border-purple-100 rounded-2xl p-4 shadow-sm">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="bg-purple-100 text-purple-600 p-1.5 rounded-lg">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </span>
                            <div>
                                <h3 class="text-sm font-bold text-gray-800">Optimización IA</h3>
                                <p class="text-[10px] text-gray-500 leading-none">Reducir estados automáticamente</p>
                            </div>
                        </div>

                        <div v-if="automata.tipo === 'AP'"
                            class="mb-3 rounded-xl bg-amber-50 border border-amber-200 p-3 text-xs text-amber-900 space-y-1">
                            <p class="font-bold flex items-center gap-1.5 text-amber-800">
                                <span>⚠️</span> No aplicable a Autómatas de Pila (AP)
                            </p>
                            <p class="text-[11px] leading-relaxed text-amber-800/90">
                                La minimización automática no aplica a Autómatas de Pila porque el problema de
                                <strong>equivalencia general de AP es indecidible</strong> en la teoría de lenguajes
                                formales. Disponible para <strong>DFA</strong> y <strong>NFA</strong>.
                            </p>
                        </div>

                        <div class="mb-3">
                            <label
                                class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-1">Método</label>
                            <select v-model="algoritmoSeleccionado" :disabled="automata.tipo === 'AP'"
                                class="w-full text-xs border-gray-200 rounded-lg bg-gray-50 focus:border-purple-500 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                <option value="genetico">🧬 Algoritmo Genético</option>
                                <option value="sa">🔥 Simulated Annealing</option>
                            </select>
                        </div>

                        <button @click="optimizarConIA" :disabled="procesandoIA || procesandoBenchmark || automata.tipo === 'AP'"
                            class="w-full relative overflow-hidden group bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-3 rounded-xl shadow-md hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center">
                            <span v-if="!procesandoIA">Optimizar Autómata</span>
                            <span v-else class="flex items-center gap-2">
                                <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg"
                                    fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                        stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                    </path>
                                </svg>
                                Procesando...
                            </span>
                        </button>

                        <div class="mt-3 pt-3 border-t border-gray-100">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                                    Corridas (N)
                                </span>
                                <div class="inline-flex rounded-lg bg-gray-100 p-0.5 gap-0.5">
                                    <button v-for="n in [10, 25, 30]" :key="n" type="button"
                                        @click="corridasBenchmark = n" :disabled="procesandoBenchmark || automata.tipo === 'AP'"
                                        :class="corridasBenchmark === n
                                            ? 'bg-white text-indigo-700 shadow-sm font-bold'
                                            : 'text-gray-500 hover:text-gray-700'"
                                        class="px-2.5 py-0.5 text-[11px] rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed">
                                        {{ n }}
                                    </button>
                                </div>
                            </div>

                            <button type="button" @click="ejecutarBenchmark"
                                :disabled="procesandoBenchmark || procesandoIA || automata.tipo === 'AP'"
                                class="w-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold py-2.5 px-3 rounded-xl shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2">
                                <span v-if="!procesandoBenchmark">📊 Comparar SA vs Genético (Experimento)</span>
                                <span v-else class="flex items-center gap-2">
                                    <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg"
                                        fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                        </path>
                                    </svg>
                                    Ejecutando {{ corridasBenchmark }} corridas...
                                </span>
                            </button>

                            <p v-if="errorBenchmark" class="mt-2 text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-lg p-2">
                                {{ errorBenchmark }}
                            </p>
                        </div>
                    </div>
                </div>

            </aside>

        </div>
        <div v-if="reporteModal"
            class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-all">
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-bounce-in">

                
                <div :class="reporteModal.algoritmo === 'genetico' ? 'from-blue-600 to-cyan-500' : 'from-orange-500 to-red-500'"
                    class="bg-gradient-to-r p-6 text-white text-center">
                    <div class="text-5xl mb-2">
                        {{ reporteModal.algoritmo === 'genetico' ? '🧬' : '🔥' }}
                    </div>
                    <h2 class="text-2xl font-bold">Optimización Completada</h2>
                    <p class="text-white/80 text-sm uppercase tracking-widest font-bold">
                        {{ reporteModal.algoritmo === 'genetico' ? 'Algoritmo Genético' : 'Simulated Annealing' }}
                    </p>
                </div>

                <div class="p-6 space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-gray-50 p-3 rounded-xl border border-gray-100 text-center">
                            <p class="text-xs text-gray-500 uppercase">Tiempo</p>
                            <p class="text-xl font-mono font-bold text-gray-800">{{ reporteModal.tiempo_seg }}s</p>
                        </div>
                        <div class="bg-gray-50 p-3 rounded-xl border border-gray-100 text-center">
                            <p class="text-xs text-gray-500 uppercase">Reducción</p>
                            <p class="text-xl font-mono font-bold text-green-600">-{{ reporteModal.reduccion_porcentaje
                            }}%</p>
                        </div>
                    </div>

                    <div
                        class="flex items-center justify-between px-4 py-2 bg-blue-50 rounded-lg border border-blue-100">
                        <div class="flex flex-col items-center">
                            <span class="text-lg font-bold text-gray-400">{{ reporteModal.estados_iniciales }}</span>
                            <span class="text-[10px] text-gray-400">ESTADOS</span>
                        </div>

                        <div class="flex-1 px-4 flex items-center justify-center">
                            <svg class="w-6 h-6 text-blue-400 animate-pulse" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </div>

                        <div class="flex flex-col items-center">
                            <span class="text-2xl font-bold text-blue-700">{{ reporteModal.estados_finales }}</span>
                            <span class="text-[10px] text-blue-600 font-bold">ESTADOS</span>
                        </div>
                    </div>

                    <div v-if="reporteModal.evaluaciones_oraculo !== undefined" class="grid grid-cols-2 gap-4">
                        <div class="bg-purple-50/70 p-3 rounded-xl border border-purple-100 text-center">
                            <p class="text-[10px] font-bold text-purple-500 uppercase tracking-wider">Evaluaciones Oráculo</p>
                            <p class="text-lg font-mono font-bold text-purple-900 mt-0.5">
                                {{ reporteModal.evaluaciones_oraculo }}
                            </p>
                        </div>
                        <div class="bg-indigo-50/70 p-3 rounded-xl border border-indigo-100 text-center">
                            <p class="text-[10px] font-bold text-indigo-500 uppercase tracking-wider">
                                {{ reporteModal.algoritmo === 'genetico' ? 'Mejor Generación' : 'Mejor Iteración' }}
                            </p>
                            <p class="text-lg font-mono font-bold text-indigo-900 mt-0.5">
                                {{ reporteModal.mejor_iteracion > 0 ? `#${reporteModal.mejor_iteracion}` : 'Inicial (0)' }}
                                <span v-if="reporteModal.total_iteraciones" class="text-xs font-normal text-indigo-500">
                                    / {{ reporteModal.total_iteraciones }}
                                </span>
                            </p>
                        </div>
                    </div>
                </div>

                <div class="p-4 bg-gray-50 border-t border-gray-100">
                    <button @click="reporteModal = null"
                        class="w-full py-3 bg-gray-800 hover:bg-gray-900 text-white rounded-xl font-bold transition">
                        Entendido
                    </button>
                </div>
            </div>
        </div>

        <!-- MODAL INFORME ESTADÍSTICO COMPARATIVO (BENCHMARK) -->
        <div v-if="benchmarkModal"
            class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-sm">
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-5xl max-h-[92vh] flex flex-col overflow-hidden">
                <!-- Header -->
                <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 px-6 py-5 text-white flex justify-between items-start gap-4 shrink-0">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2 py-0.5 rounded-md bg-indigo-500/20 border border-indigo-400/30 text-[10px] font-bold uppercase tracking-widest text-indigo-200">
                                Análisis No Paramétrico
                            </span>
                            <span class="text-xs text-slate-300 font-mono">
                                N = {{ benchmarkModal.corridas }} corridas independientes / algoritmo
                            </span>
                        </div>
                        <h2 class="text-2xl font-extrabold tracking-tight mt-1">
                            Informe Estadístico Comparativo: SA vs. Algoritmo Genético
                        </h2>
                        <p class="text-xs text-slate-300 mt-0.5">
                            Autómata: <span class="font-semibold text-white">{{ automata.nombre }}</span> ({{ automata.tipo }})
                            • Estados iniciales: <span class="font-mono font-bold text-indigo-200">{{ benchmarkModal.estados_iniciales }}</span>
                        </p>
                    </div>
                    <button @click="benchmarkModal = null"
                        class="text-slate-300 hover:text-white bg-white/10 hover:bg-white/20 rounded-lg p-2 transition"
                        title="Cerrar">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <!-- Contenido scrollable -->
                <div class="p-6 overflow-y-auto space-y-6 bg-slate-50/50">
                    <!-- 1. Tarjetas Resumen -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- SA -->
                        <div class="bg-white rounded-2xl border border-orange-200 shadow-sm overflow-hidden">
                            <div class="bg-gradient-to-r from-orange-500 to-amber-500 px-4 py-3 text-white flex justify-between items-center">
                                <div class="flex items-center gap-2">
                                    <span class="text-xl">🔥</span>
                                    <div>
                                        <h3 class="font-bold text-sm leading-tight">Simulated Annealing (SA)</h3>
                                        <p class="text-[10px] text-orange-100 uppercase tracking-wider">Trayectoria única • T₀=2.0, α=0.92</p>
                                    </div>
                                </div>
                                <span class="text-[11px] font-mono bg-white/20 px-2 py-0.5 rounded-full">
                                    ~{{ benchmarkModal.sa.evaluaciones_promedio }} evals
                                </span>
                            </div>
                            <div class="p-4 grid grid-cols-2 gap-3">
                                <div class="bg-orange-50/60 rounded-xl p-3 border border-orange-100">
                                    <p class="text-[10px] font-bold text-orange-600 uppercase tracking-wider">Estados Finales</p>
                                    <div class="mt-1 flex items-baseline gap-2">
                                        <span class="text-2xl font-mono font-extrabold text-gray-900">{{ formatNum(benchmarkModal.sa.estados.mediana, 1) }}</span>
                                        <span class="text-[11px] text-gray-500">mediana</span>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1 font-mono">
                                        x̄ = {{ formatNum(benchmarkModal.sa.estados.media, 2) }} <span class="text-gray-400">(σ={{ formatNum(benchmarkModal.sa.estados.desviacion_std, 2) }})</span>
                                    </p>
                                </div>
                                <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
                                    <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Tiempo de Ejecución</p>
                                    <div class="mt-1 flex items-baseline gap-1.5">
                                        <span class="text-2xl font-mono font-extrabold text-gray-900">{{ formatNum(benchmarkModal.sa.tiempo_ms.mediana, 1) }}</span>
                                        <span class="text-xs text-gray-500 font-mono">ms</span>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1 font-mono">
                                        x̄ = {{ formatNum(benchmarkModal.sa.tiempo_ms.media, 2) }} ms
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Genético -->
                        <div class="bg-white rounded-2xl border border-blue-200 shadow-sm overflow-hidden">
                            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-3 text-white flex justify-between items-center">
                                <div class="flex items-center gap-2">
                                    <span class="text-xl">🧬</span>
                                    <div>
                                        <h3 class="font-bold text-sm leading-tight">Algoritmo Genético (GA)</h3>
                                        <p class="text-[10px] text-blue-100 uppercase tracking-wider">Poblacional • 16 ind., 25 gen.</p>
                                    </div>
                                </div>
                                <span class="text-[11px] font-mono bg-white/20 px-2 py-0.5 rounded-full">
                                    ~{{ benchmarkModal.genetico.evaluaciones_promedio }} evals
                                </span>
                            </div>
                            <div class="p-4 grid grid-cols-2 gap-3">
                                <div class="bg-blue-50/60 rounded-xl p-3 border border-blue-100">
                                    <p class="text-[10px] font-bold text-blue-600 uppercase tracking-wider">Estados Finales</p>
                                    <div class="mt-1 flex items-baseline gap-2">
                                        <span class="text-2xl font-mono font-extrabold text-gray-900">{{ formatNum(benchmarkModal.genetico.estados.mediana, 1) }}</span>
                                        <span class="text-[11px] text-gray-500">mediana</span>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1 font-mono">
                                        x̄ = {{ formatNum(benchmarkModal.genetico.estados.media, 2) }} <span class="text-gray-400">(σ={{ formatNum(benchmarkModal.genetico.estados.desviacion_std, 2) }})</span>
                                    </p>
                                </div>
                                <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
                                    <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Tiempo de Ejecución</p>
                                    <div class="mt-1 flex items-baseline gap-1.5">
                                        <span class="text-2xl font-mono font-extrabold text-gray-900">{{ formatNum(benchmarkModal.genetico.tiempo_ms.mediana, 1) }}</span>
                                        <span class="text-xs text-gray-500 font-mono">ms</span>
                                    </div>
                                    <p class="text-xs text-gray-600 mt-1 font-mono">
                                        x̄ = {{ formatNum(benchmarkModal.genetico.tiempo_ms.media, 2) }} ms
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 2. Gráficos Boxplot en SVG -->
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <div v-for="chart in boxplotCharts" :key="chart.id"
                            class="bg-white rounded-2xl border border-gray-200 p-4 shadow-sm">
                            <div class="flex items-center justify-between mb-2">
                                <div>
                                    <h4 class="text-sm font-bold text-gray-800">{{ chart.titulo }}</h4>
                                    <p class="text-[11px] text-gray-500">{{ chart.subtitulo }}</p>
                                </div>
                                <span class="text-[10px] font-mono bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                                    {{ chart.unidad }}
                                </span>
                            </div>

                            <svg viewBox="0 0 360 225" class="w-full h-auto select-none">
                                <!-- Grilla y Eje Y -->
                                <g v-for="(tick, idx) in chart.ticks" :key="idx">
                                    <line x1="54" :y1="tick.y" x2="342" :y2="tick.y" stroke="#e2e8f0" stroke-dasharray="3,3" stroke-width="1" />
                                    <text x="48" :y="tick.y + 3.5" text-anchor="end" fill="#64748b" font-size="10" font-family="monospace">
                                        {{ tick.label }}
                                    </text>
                                </g>
                                <line x1="54" y1="18" x2="54" y2="180" stroke="#94a3b8" stroke-width="1.2" />
                                <line x1="54" y1="180" x2="342" y2="180" stroke="#94a3b8" stroke-width="1.2" />

                                <!-- Series SA y Genético -->
                                <g v-for="s in chart.series" :key="s.key">
                                    <!-- Bigote superior e inferior -->
                                    <line :x1="s.cx" :y1="s.yBigoteSup" :x2="s.cx" :y2="s.yQ3" :stroke="s.stroke" stroke-width="1.8" stroke-dasharray="4,2" />
                                    <line :x1="s.cx" :y1="s.yQ1" :x2="s.cx" :y2="s.yBigoteInf" :stroke="s.stroke" stroke-width="1.8" stroke-dasharray="4,2" />
                                    <!-- Topes de bigotes -->
                                    <line :x1="s.cx - 14" :y1="s.yBigoteSup" :x2="s.cx + 14" :y2="s.yBigoteSup" :stroke="s.stroke" stroke-width="2" />
                                    <line :x1="s.cx - 14" :y1="s.yBigoteInf" :x2="s.cx + 14" :y2="s.yBigoteInf" :stroke="s.stroke" stroke-width="2" />

                                    <!-- Caja Q1 - Q3 -->
                                    <rect :x="s.cx - 28" :y="s.boxY" width="56" :height="s.boxH" rx="4"
                                        :fill="s.fill" :stroke="s.stroke" stroke-width="2">
                                        <title>{{ s.nombre }} — Q1: {{ s.raw.q1 }} | Mediana: {{ s.raw.mediana }} | Q3: {{ s.raw.q3 }} | RIC: {{ s.raw.ric }}</title>
                                    </rect>

                                    <!-- Línea de Mediana -->
                                    <line :x1="s.cx - 28" :y1="s.yMediana" :x2="s.cx + 28" :y2="s.yMediana"
                                        :stroke="s.medianStroke" stroke-width="3" />

                                    <!-- Rombo de Media -->
                                    <polygon :points="`${s.cx},${s.yMedia - 4.5} ${s.cx + 4.5},${s.yMedia} ${s.cx},${s.yMedia + 4.5} ${s.cx - 4.5},${s.yMedia}`"
                                        fill="#0f172a" stroke="#ffffff" stroke-width="1">
                                        <title>Media (x̄): {{ s.raw.media }} {{ chart.unidad }}</title>
                                    </polygon>

                                    <!-- Outliers -->
                                    <circle v-for="(out, oIdx) in s.outliers" :key="oIdx"
                                        :cx="out.x" :cy="out.y" r="3.8"
                                        fill="#ef4444" fill-opacity="0.85" stroke="#991b1b" stroke-width="1">
                                        <title>Outlier: {{ out.val }} {{ chart.unidad }}</title>
                                    </circle>

                                    <!-- Etiqueta eje X -->
                                    <text :x="s.cx" y="198" text-anchor="middle" fill="#1e293b" font-size="11" font-weight="700">
                                        {{ s.nombre }}
                                    </text>
                                    <text :x="s.cx" y="212" text-anchor="middle" fill="#64748b" font-size="9.5" font-family="monospace">
                                        Med: {{ formatNum(s.raw.mediana, chart.esEntero ? 1 : 1) }} | RIC: {{ formatNum(s.raw.ric, chart.esEntero ? 1 : 1) }}
                                    </text>
                                </g>
                            </svg>

                            <div class="mt-1 flex flex-wrap items-center justify-center gap-3 text-[10px] text-gray-500">
                                <span class="flex items-center gap-1"><span class="inline-block w-3 h-2 rounded-sm bg-slate-200 border border-slate-500"></span> Caja Q₁–Q₃</span>
                                <span class="flex items-center gap-1"><span class="inline-block w-3 h-0.5 bg-slate-800"></span> Mediana</span>
                                <span class="flex items-center gap-1"><span class="inline-block w-2 h-2 rotate-45 bg-slate-900"></span> Media (x̄)</span>
                                <span class="flex items-center gap-1"><span class="inline-block w-2 h-2 rounded-full bg-red-500"></span> Outlier</span>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Tabla de Estadísticos Descriptivos -->
                    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
                        <div class="px-5 py-3.5 border-b border-gray-100 flex items-center justify-between">
                            <h4 class="text-sm font-bold text-gray-800">Tabla de Estadísticos Descriptivos</h4>
                            <span class="text-[11px] text-gray-400">Cuartiles y dispersión sobre N = {{ benchmarkModal.corridas }} corridas</span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr class="bg-gray-50 text-gray-500 uppercase text-[10px] tracking-wider border-b border-gray-200">
                                        <th class="py-2.5 px-4 font-bold">Métrica / Algoritmo</th>
                                        <th class="py-2.5 px-3 font-bold text-right">Media <span class="normal-case">(x̄)</span></th>
                                        <th class="py-2.5 px-3 font-bold text-right">Desv. Est. <span class="normal-case">(σ)</span></th>
                                        <th class="py-2.5 px-3 font-bold text-right">Q₁</th>
                                        <th class="py-2.5 px-3 font-bold text-right">Mediana</th>
                                        <th class="py-2.5 px-3 font-bold text-right">Q₃</th>
                                        <th class="py-2.5 px-3 font-bold text-right">RIC</th>
                                        <th class="py-2.5 px-3 font-bold text-right">Mín</th>
                                        <th class="py-2.5 px-3 font-bold text-right">Máx</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-100 font-mono">
                                    <tr v-for="row in tablaEstadisticos" :key="row.label" class="hover:bg-slate-50/80">
                                        <td class="py-2.5 px-4 font-sans font-semibold text-gray-800 flex items-center gap-2">
                                            <span :class="row.dotClass" class="w-2.5 h-2.5 rounded-full shrink-0"></span>
                                            <span>{{ row.label }}</span>
                                        </td>
                                        <td class="py-2.5 px-3 text-right text-gray-700">{{ formatNum(row.stats.media, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-gray-500">{{ formatNum(row.stats.desviacion_std, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-gray-700">{{ formatNum(row.stats.q1, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right font-bold text-gray-900 bg-slate-50/70">{{ formatNum(row.stats.mediana, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-gray-700">{{ formatNum(row.stats.q3, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-indigo-700 font-semibold">{{ formatNum(row.stats.ric, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-gray-600">{{ formatNum(row.stats.min, row.dec) }}</td>
                                        <td class="py-2.5 px-3 text-right text-gray-600">{{ formatNum(row.stats.max, row.dec) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- 4. Panel de Validación Estadística (Test de Wilcoxon Rank-Sum) -->
                    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <div>
                                <h4 class="text-sm font-bold text-gray-800">
                                    Validación Estadística: Test de Wilcoxon Rank-Sum (Mann-Whitney U)
                                </h4>
                                <p class="text-xs text-gray-500">
                                    Prueba no paramétrica bilateral con corrección por empates y nivel de significancia α = 0.05.
                                </p>
                            </div>
                            <span class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-mono text-xs font-bold">
                                α = 0.05
                            </span>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-50 rounded-xl p-3.5 border border-slate-200/80">
                            <div>
                                <span class="font-bold text-slate-700">H₀ (Hipótesis Nula):</span>
                                <span class="text-slate-600"> No existe diferencia estadísticamente significativa entre las distribuciones de SA y Algoritmo Genético.</span>
                            </div>
                            <div>
                                <span class="font-bold text-slate-700">H₁ (Hipótesis Alternativa):</span>
                                <span class="text-slate-600"> Existe una diferencia estadísticamente significativa entre ambos algoritmos.</span>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <!-- Wilcoxon Estados -->
                            <div class="rounded-xl border p-4"
                                :class="benchmarkModal.wilcoxon_estados.significativo ? 'border-emerald-200 bg-emerald-50/40' : 'border-amber-200 bg-amber-50/40'">
                                <div class="flex items-center justify-between gap-2 mb-3">
                                    <h5 class="font-bold text-sm text-gray-800">Calidad (Estados Finales)</h5>
                                    <span v-if="benchmarkModal.wilcoxon_estados.significativo"
                                        class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                        ✓ Significativo (Se rechaza H₀)
                                    </span>
                                    <span v-else
                                        class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-200">
                                        ≈ No significativo (No se rechaza H₀)
                                    </span>
                                </div>
                                <div class="grid grid-cols-3 gap-2 text-center font-mono">
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">U</p>
                                        <p class="text-sm font-bold text-gray-800">{{ formatNum(benchmarkModal.wilcoxon_estados.estadistico_u, 1) }}</p>
                                    </div>
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">Z-Score</p>
                                        <p class="text-sm font-bold text-gray-800">{{ formatNum(benchmarkModal.wilcoxon_estados.z_score, 3) }}</p>
                                    </div>
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">p-value</p>
                                        <p class="text-sm font-extrabold"
                                            :class="benchmarkModal.wilcoxon_estados.significativo ? 'text-emerald-700' : 'text-amber-700'">
                                            {{ formatPValue(benchmarkModal.wilcoxon_estados.p_value) }}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <!-- Wilcoxon Tiempo -->
                            <div class="rounded-xl border p-4"
                                :class="benchmarkModal.wilcoxon_tiempo.significativo ? 'border-emerald-200 bg-emerald-50/40' : 'border-amber-200 bg-amber-50/40'">
                                <div class="flex items-center justify-between gap-2 mb-3">
                                    <h5 class="font-bold text-sm text-gray-800">Eficiencia (Tiempo en ms)</h5>
                                    <span v-if="benchmarkModal.wilcoxon_tiempo.significativo"
                                        class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                        ✓ Significativo (Se rechaza H₀)
                                    </span>
                                    <span v-else
                                        class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-200">
                                        ≈ No significativo (No se rechaza H₀)
                                    </span>
                                </div>
                                <div class="grid grid-cols-3 gap-2 text-center font-mono">
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">U</p>
                                        <p class="text-sm font-bold text-gray-800">{{ formatNum(benchmarkModal.wilcoxon_tiempo.estadistico_u, 1) }}</p>
                                    </div>
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">Z-Score</p>
                                        <p class="text-sm font-bold text-gray-800">{{ formatNum(benchmarkModal.wilcoxon_tiempo.z_score, 3) }}</p>
                                    </div>
                                    <div class="bg-white rounded-lg p-2 border border-gray-100">
                                        <p class="text-[10px] text-gray-400 font-sans uppercase">p-value</p>
                                        <p class="text-sm font-extrabold"
                                            :class="benchmarkModal.wilcoxon_tiempo.significativo ? 'text-emerald-700' : 'text-amber-700'">
                                            {{ formatPValue(benchmarkModal.wilcoxon_tiempo.p_value) }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="px-6 py-4 bg-white border-t border-gray-200 flex flex-wrap justify-between items-center gap-3 shrink-0">
                    <p class="text-xs text-gray-400">
                        Criterio de outliers: Regla de Tukey (1.5 × RIC) • Test bilateral de Wilcoxon Rank-Sum.
                    </p>
                    <div class="flex items-center gap-3">
                        <button type="button" @click="descargarBenchmarkJson"
                            class="px-4 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-xl text-sm font-bold transition flex items-center gap-2">
                            <span>📥</span> Descargar Reporte JSON
                        </button>
                        <button type="button" @click="benchmarkModal = null"
                            class="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-sm font-bold transition">
                            Cerrar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { Link, router, usePage } from '@inertiajs/vue3';
import { Network } from 'vis-network';
import axios from 'axios';

const props = defineProps({ automata: Object });
const networkContainer = ref(null);
const inputCadena = ref('');
const resultado = ref(null);
const estadosFinalesAlcanzados = ref([]);
const page = usePage();
const procesandoIA = ref(false);
const algoritmoSeleccionado = ref('genetico');
const reporteModal = ref(null);

// --- BENCHMARK COMPARATIVO ---
const corridasBenchmark = ref(25);
const procesandoBenchmark = ref(false);
const benchmarkModal = ref(null);
const errorBenchmark = ref(null);

async function ejecutarBenchmark() {
    procesandoBenchmark.value = true;
    errorBenchmark.value = null;

    try {
        const response = await axios.post(
            route('automatas.benchmark', props.automata.id),
            { corridas: corridasBenchmark.value },
            {
                baseURL: '',
                withCredentials: true,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    Accept: 'application/json',
                },
            }
        );

        if (response.data?.success && response.data?.benchmark) {
            benchmarkModal.value = response.data.benchmark;
        } else {
            errorBenchmark.value = response.data?.message || 'No se pudo completar el experimento.';
        }
    } catch (err) {
        errorBenchmark.value =
            err?.response?.data?.message ||
            err?.message ||
            'Error de conexión o servidor al ejecutar el experimento.';
    } finally {
        procesandoBenchmark.value = false;
    }
}

function descargarBenchmarkJson() {
    if (!benchmarkModal.value) return;
    const payload = {
        automata: {
            id: props.automata.id,
            nombre: props.automata.nombre,
            tipo: props.automata.tipo,
        },
        generado_en: new Date().toISOString(),
        benchmark: benchmarkModal.value,
    };
    const dataStr = JSON.stringify(payload, null, 2);
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([dataStr], { type: 'application/json' }));
    const nombreSeguro = (props.automata.nombre || 'automata').replace(/[^a-zA-Z0-9_-]+/g, '_');
    link.download = `benchmark_${nombreSeguro}_N${benchmarkModal.value.corridas}.json`;
    link.click();
}

function formatNum(val, dec = 2) {
    if (val === null || val === undefined || Number.isNaN(Number(val))) return '—';
    const num = Number(val);
    return Number.isInteger(num) && dec <= 1 ? String(num) : num.toFixed(dec);
}

function formatPValue(p) {
    if (p === null || p === undefined || Number.isNaN(Number(p))) return '—';
    const num = Number(p);
    if (num < 0.0001) return '< 0.0001';
    return num.toFixed(4);
}

function construirBoxplotSvg(id, titulo, subtitulo, saStats, gaStats, unidad, esEntero) {
    const plotTop = 20;
    const plotBottom = 178;
    const plotHeight = plotBottom - plotTop;

    const allVals = [
        saStats.min, saStats.max, saStats.bigote_inf, saStats.bigote_sup, ...(saStats.outliers || []),
        gaStats.min, gaStats.max, gaStats.bigote_inf, gaStats.bigote_sup, ...(gaStats.outliers || []),
    ].filter((v) => typeof v === 'number' && !Number.isNaN(v));

    let rawMin = allVals.length ? Math.min(...allVals) : 0;
    let rawMax = allVals.length ? Math.max(...allVals) : 1;

    let yMin;
    let yMax;
    if (Math.abs(rawMax - rawMin) < 1e-9) {
        const pad = esEntero ? 1 : Math.max(0.5, rawMax * 0.25);
        yMin = Math.max(0, rawMin - pad);
        yMax = rawMax + pad;
    } else {
        const pad = (rawMax - rawMin) * 0.12;
        yMin = Math.max(0, rawMin - pad);
        yMax = rawMax + pad;
    }
    if (yMax <= yMin) yMax = yMin + 1;

    const mapY = (v) => plotBottom - ((v - yMin) / (yMax - yMin)) * plotHeight;

    const numTicks = 5;
    const ticks = [];
    for (let i = 0; i < numTicks; i++) {
        const ratio = i / (numTicks - 1);
        const val = yMin + ratio * (yMax - yMin);
        ticks.push({
            y: mapY(val),
            label: esEntero ? val.toFixed(1).replace(/\.0$/, '') : val.toFixed(1),
        });
    }

    const buildSerie = (key, nombre, stats, cx, fill, stroke, medianStroke) => {
        const yQ1 = mapY(stats.q1);
        const yQ3 = mapY(stats.q3);
        const yMediana = mapY(stats.mediana);
        const yMedia = mapY(stats.media);
        const yBigoteInf = mapY(stats.bigote_inf);
        const yBigoteSup = mapY(stats.bigote_sup);
        const rawBoxH = Math.abs(yQ1 - yQ3);
        const boxH = Math.max(rawBoxH, 4);
        const boxY = rawBoxH < 4 ? yMediana - 2 : Math.min(yQ1, yQ3);

        const outliers = (stats.outliers || []).map((val, idx, arr) => {
            const offset = arr.length > 1 ? ((idx % 3) - 1) * 6 : 0;
            return { x: cx + offset, y: mapY(val), val };
        });

        return {
            key,
            nombre,
            cx,
            fill,
            stroke,
            medianStroke,
            yQ1,
            yQ3,
            yMediana,
            yMedia,
            yBigoteInf,
            yBigoteSup,
            boxY,
            boxH,
            outliers,
            raw: stats,
        };
    };

    return {
        id,
        titulo,
        subtitulo,
        unidad,
        esEntero,
        ticks,
        series: [
            buildSerie('sa', 'Simulated Annealing', saStats, 130, '#ffedd5', '#ea580c', '#9a3412'),
            buildSerie('ga', 'Algoritmo Genético', gaStats, 266, '#dbeafe', '#2563eb', '#1e3a8a'),
        ],
    };
}

const boxplotCharts = computed(() => {
    if (!benchmarkModal.value) return [];
    const bm = benchmarkModal.value;
    return [
        construirBoxplotSvg(
            'estados',
            'Distribución de Estados Finales',
            'Menor cantidad de estados = mejor minimización',
            bm.sa.estados,
            bm.genetico.estados,
            'estados',
            true
        ),
        construirBoxplotSvg(
            'tiempo',
            'Distribución de Tiempo de Ejecución',
            'Costo computacional por corrida independiente',
            bm.sa.tiempo_ms,
            bm.genetico.tiempo_ms,
            'ms',
            false
        ),
    ];
});

const tablaEstadisticos = computed(() => {
    if (!benchmarkModal.value) return [];
    const bm = benchmarkModal.value;
    return [
        { label: 'Estados Finales — Simulated Annealing', stats: bm.sa.estados, dec: 2, dotClass: 'bg-orange-500' },
        { label: 'Estados Finales — Algoritmo Genético', stats: bm.genetico.estados, dec: 2, dotClass: 'bg-blue-600' },
        { label: 'Tiempo (ms) — Simulated Annealing', stats: bm.sa.tiempo_ms, dec: 2, dotClass: 'bg-amber-400' },
        { label: 'Tiempo (ms) — Algoritmo Genético', stats: bm.genetico.tiempo_ms, dec: 2, dotClass: 'bg-indigo-500' },
    ];
});

// --- EXPORTAR ---
function exportarJson() {
    const archivoCompleto = {
        nombre: props.automata.nombre || 'Automata Sin Nombre',
        tipo: props.automata.tipo,
        json_definicion: props.automata.json_definicion
    };

    const dataStr = JSON.stringify(archivoCompleto, null, 2);

    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([dataStr], { type: 'application/json' }));
    link.download = `${archivoCompleto.nombre}.json`;
    link.click();
}


// FUNCIÓN PARA LLAMAR AL BACKEND
function optimizarConIA() {
    if (!confirm(`¿Usar ${algoritmoSeleccionado.value} para optimizar?`)) return;

    router.post(route('automatas.optimize', props.automata.id), { algoritmo: algoritmoSeleccionado.value }, {
        onStart: () => { procesandoIA.value = true; },
        onFinish: () => {
            procesandoIA.value = false;
            const flash = page.props.flash;
            if (flash?.message) alert(flash.message);
            if (flash?.error) alert('Error: ' + flash.error);
        },
        onError: (errors) => {
            alert('Error de conexión o servidor: ' + (errors.error || 'Desconocido'));
        }
    });
}

function probarCadena() {
    const def = props.automata.json_definicion;
    const cadena = inputCadena.value;
    const tipo = props.automata.tipo;
    let configuraciones = [
        { estado: def.estado_inicial, pila: [], indice: 0 }
    ];

    let pasos = 0;
    let aceptado = false;
    estadosFinalesAlcanzados.value = [];
    const MAX_PASOS = 2000;

    while (configuraciones.length > 0 && pasos < MAX_PASOS) {
        pasos++;
        let siguientes = [];

        for (let config of configuraciones) {
            const { estado, pila, indice } = config;
            if (indice === cadena.length) {
                if (def.estados_finales.includes(estado)) {
                    if (tipo === 'AP') {
                        if (pila.length === 0) {
                            aceptado = true;
                        }
                    } else {
                        aceptado = true;
                    }
                    if (aceptado) {
                        if (!estadosFinalesAlcanzados.value.includes(estado)) {
                            estadosFinalesAlcanzados.value.push(estado);
                        }
                    }
                }
            }

            if (indice >= cadena.length) continue;
            const simbolo = cadena[indice];
            const transicionesDelEstado = def.transiciones[estado];
            if (!transicionesDelEstado) continue;
            const reglas = transicionesDelEstado[simbolo];
            if (!reglas) continue;
            let listaReglas = Array.isArray(reglas) ? reglas : (reglas ? [reglas] : []);

            for (let regla of listaReglas) {
                // LOGICA AP (PILA)
                if (tipo === 'AP') {
                    const tope = pila.length > 0 ? pila[pila.length - 1] : '';
                    const popRequerido = regla.pop;

                    let pilaValida = false;
                    let nuevaPila = [...pila];

                    if (!popRequerido || popRequerido === 'λ') {
                        pilaValida = true;
                    } else if (popRequerido === tope) {
                        pilaValida = true;
                        nuevaPila.pop();
                    }

                    if (pilaValida) {
                        if (regla.push && regla.push !== 'λ') {
                            nuevaPila.push(regla.push);
                        }

                        siguientes.push({
                            estado: regla.dest,
                            pila: nuevaPila,
                            indice: indice + 1
                        });
                    }

                } else {
                    let destino = regla;
                    if (typeof regla === 'object') destino = regla.dest;

                    siguientes.push({
                        estado: destino,
                        pila: [],
                        indice: indice + 1
                    });
                }
            }
        }

        configuraciones = siguientes;
        if (aceptado) break;
    }

    resultado.value = aceptado;
}

// --- VISUALIZADOR ---
function dibujarRed() {
    if (!networkContainer.value) return;

    const def = props.automata.json_definicion;
    const nodes = def.estados.map(e => ({
        id: e, label: e, shape: 'circle',
        color: { background: e === def.estado_inicial ? '#d1fae5' : '#fff', border: '#2B7CE9' },
        borderWidth: def.estados_finales.includes(e) ? 3 : 1
    }));

    const edges = [];
    if (def.transiciones) {
        Object.keys(def.transiciones).forEach(origen => {
            const reglasOrigen = def.transiciones[origen];
            if (reglasOrigen) {
                Object.keys(reglasOrigen).forEach(simbolo => {
                    let reglas = reglasOrigen[simbolo];
                    if (!Array.isArray(reglas)) reglas = reglas ? [reglas] : [];

                    reglas.forEach(r => {
                        let destino = r;
                        let label = simbolo;

                        // Formato AP
                        if (props.automata.tipo === 'AP' && typeof r === 'object') {
                            destino = r.dest;
                            label = `${simbolo}, ${r.pop || 'λ'}; ${r.push || 'λ'}`;
                        }

                        if (destino) {
                            const existing = edges.find(e => e.from === origen && e.to === destino);
                            if (existing) {
                                existing.label += `\n${label}`;
                            } else {
                                edges.push({ from: origen, to: destino, label, arrows: 'to', font: { align: 'top' } });
                            }
                        }
                    });
                });
            }
        });
    }

    new Network(networkContainer.value, { nodes, edges }, { physics: { enabled: true, solver: 'forceAtlas2Based' } });
}
// --- CICLO DE VIDA ---
onMounted(() => {
    dibujarRed();
});

watch(() => page.props.flash, (flash) => {
    if (flash?.reporte_ia) {
        reporteModal.value = flash.reporte_ia;
        dibujarRed();
    }
}, { deep: true, immediate: true });
</script>