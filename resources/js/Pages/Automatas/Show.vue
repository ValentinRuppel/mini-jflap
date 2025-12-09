<template>
  <div class="h-screen flex flex-col bg-gray-50 overflow-hidden font-sans">
    
    <header class="bg-white border-b border-gray-200 relative z-20 shadow-sm">
        <div class="absolute inset-0 opacity-[0.03] pointer-events-none" 
             style="background-image: radial-gradient(#4f46e5 1px, transparent 1px); background-size: 20px 20px;">
        </div>

        <div class="max-w-full mx-auto px-6 py-4 relative z-10 flex justify-between items-center">
            
            <div class="flex items-center gap-4">
                <div>
                    <h1 class="text-xl font-bold text-gray-900 leading-none">{{ automata.nombre }}</h1>
                    <div class="flex items-center gap-2 mt-1">
                         <span :class="automata.tipo === 'DFA' ? 'bg-purple-100 text-purple-700 border-purple-200' : 'bg-orange-100 text-orange-700 border-orange-200'" 
                              class="px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider">
                            {{ automata.tipo }}
                        </span>
                        <span class="text-xs text-gray-400 border-l pl-2 border-gray-300">Modo Visualización</span>
                    </div>
                </div>
            </div>
            
            <div class="flex items-center gap-3">
                 <button 
                    @click="exportarJson"
                    class="inline-flex items-center px-4 py-2 bg-white border border-gray-300 rounded-xl font-semibold text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition shadow-sm"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                    Exportar
                </button>
                
                <div class="h-8 w-px bg-gray-200 mx-1"></div>

                <Link :href="route('automatas.index')" 
                      class="text-gray-500 hover:text-gray-800 font-medium text-sm transition flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Volver
                </Link>
            </div>
        </div>
    </header>

    <div class="flex flex-1 overflow-hidden relative">
        
        <main class="flex-1 relative bg-gray-100/50">
            <div ref="networkContainer" class="w-full h-full cursor-grab active:cursor-grabbing outline-none"></div>
            
            <div class="absolute bottom-6 left-6 bg-white/80 backdrop-blur-md p-4 rounded-2xl shadow-lg border border-white/50 text-xs text-gray-600 pointer-events-none select-none min-w-[150px]">
                <h4 class="font-bold text-gray-800 mb-2 uppercase tracking-wide text-[10px]">Referencias</h4>
                <div class="flex items-center gap-3 mb-1.5">
                    <span class="w-3 h-3 bg-[#d1fae5] border border-[#059669] rounded-full shadow-sm"></span> Inicio
                </div>
                <div class="flex items-center gap-3 mb-1.5">
                    <span class="w-3 h-3 bg-white border border-blue-500 rounded-full shadow-sm"></span> Estado
                </div>
                <div class="flex items-center gap-3">
                    <span class="w-3 h-3 bg-white border-[3px] border-blue-500 rounded-full shadow-sm"></span> Final
                </div>
            </div>
        </main>

        <aside class="w-[400px] bg-white border-l border-gray-200 shadow-[0_0_15px_rgba(0,0,0,0.05)] z-10 flex flex-col">
            
            <div class="p-6 border-b border-gray-100">
                <div class="flex items-center gap-2 mb-1">
                    <span class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                        <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                    </span>
                    <h2 class="font-bold text-lg text-gray-800">Simulador</h2>
                </div>
                <p class="text-xs text-gray-500 ml-10">Ingresa una cadena para validar el recorrido.</p>
            </div>

            <div class="p-6 flex-1 overflow-y-auto">
                
                <div class="bg-gray-50 rounded-2xl p-5 border border-gray-100 mb-6">
                    <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Cadena de Entrada</label>
                    <div class="relative">
                        <input 
                            v-model="inputCadena" 
                            @keyup.enter="probarCadena"
                            type="text" 
                            class="w-full bg-white border border-gray-200 text-gray-900 text-base rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-3 font-mono tracking-widest shadow-sm transition-all" 
                            placeholder="Ej: 01011" 
                        />
                        <button v-if="inputCadena" @click="inputCadena = ''; resultado = null" class="absolute right-3 top-3 text-gray-300 hover:text-gray-500 transition">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                            </svg>
                        </button>
                    </div>

                    <button 
                        @click="probarCadena"
                        :disabled="!inputCadena"
                        class="mt-4 w-full flex justify-center items-center px-6 py-3 bg-blue-600 border border-transparent rounded-xl font-bold text-white hover:bg-blue-700 transition shadow-lg shadow-blue-600/20 disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Verificar Cadena
                    </button>
                </div>

                <transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0 translate-y-2" enter-to-class="opacity-100 translate-y-0">
                    <div v-if="resultado !== null">
                        
                        <div :class="resultado ? 'bg-green-50 border-green-100' : 'bg-red-50 border-red-100'" 
                             class="border rounded-2xl p-6 text-center shadow-sm mb-6 relative overflow-hidden">
                             
                             <div class="absolute -right-4 -top-4 opacity-10">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24" :class="resultado ? 'text-green-600' : 'text-red-600'" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                                </svg>
                             </div>

                            <div class="relative z-10">
                                <div class="inline-flex items-center justify-center w-12 h-12 rounded-full mb-3 shadow-sm"
                                     :class="resultado ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
                                     <span class="text-2xl">{{ resultado ? '✓' : '✕' }}</span>
                                </div>
                                <h3 :class="resultado ? 'text-green-800' : 'text-red-800'" class="font-extrabold text-xl tracking-tight">
                                    {{ resultado ? 'Cadena Aceptada' : 'Cadena Rechazada' }}
                                </h3>
                                <p :class="resultado ? 'text-green-600' : 'text-red-600'" class="text-sm font-medium mt-1">
                                    {{ resultado ? 'El autómata finalizó en un estado válido.' : 'No se alcanzó un estado final.' }}
                                </p>
                            </div>
                        </div>

                        <div>
                            <h4 class="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase mb-3 ml-1">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                                Estados Alcanzados
                            </h4>
                            <div class="bg-gray-900 text-gray-100 font-mono text-xs p-4 rounded-xl shadow-inner border border-gray-700 relative group">
                                <div class="absolute top-2 right-2 flex gap-1">
                                    <div class="w-2 h-2 rounded-full bg-red-500"></div>
                                    <div class="w-2 h-2 rounded-full bg-yellow-500"></div>
                                    <div class="w-2 h-2 rounded-full bg-green-500"></div>
                                </div>
                                
                                <div class="mt-2 space-y-2">
                                    <div><span class="text-blue-400">INPUT:</span> <span class="text-white">"{{ inputCadena }}"</span></div>
                                    <div class="h-px bg-gray-700 my-2"></div>
                                    <div>
                                        <span class="text-purple-400">END_STATES:</span> 
                                        <span class="text-green-300 ml-2">[ {{ estadosFinalesAlcanzados.join(', ') }} ]</span>
                                    </div>
                                    <div v-if="!resultado && estadosFinalesAlcanzados.length === 0" class="text-red-400 mt-1 italic">
                                        // Error: Trap state reached (sin salida)
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
            
            <div class="p-4 bg-gray-50 border-t border-gray-100 text-center">
                <p class="text-[10px] text-gray-400 font-medium">Mini-JFLAP Engine v1.0</p>
            </div>
        </aside>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Link } from '@inertiajs/vue3';
import { Network } from 'vis-network';

const props = defineProps({ automata: Object });
const networkContainer = ref(null);

// Variables Reactivas
const inputCadena = ref('');
const resultado = ref(null);
const estadosFinalesAlcanzados = ref([]);

// --- EXPORTAR ---
function exportarJson() {
    const dataStr = JSON.stringify(props.automata.json_definicion, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${props.automata.nombre.replace(/\s+/g, '_')}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// --- ALGORITMO DE SIMULACIÓN ---
function probarCadena() {
    const def = props.automata.json_definicion;
    const cadena = inputCadena.value;
    let estadosActuales = new Set([def.estado_inicial]);

    // Reset visual
    resultado.value = null;

    for (const simbolo of cadena) {
        if (!def.alfabeto.includes(simbolo)) {
            alert(`Símbolo inválido: ${simbolo}`);
            return;
        }

        const siguientesEstados = new Set();
        estadosActuales.forEach(estado => {
            const transicion = def.transiciones[estado]?.[simbolo];
            if (transicion) {
                if (Array.isArray(transicion)) transicion.forEach(dest => siguientesEstados.add(dest));
                else if (transicion !== '') siguientesEstados.add(transicion);
            }
        });

        estadosActuales = siguientesEstados;
        if (estadosActuales.size === 0) break; 
    }

    const estadosAlcanzados = Array.from(estadosActuales);
    estadosFinalesAlcanzados.value = estadosAlcanzados;
    resultado.value = estadosAlcanzados.some(e => def.estados_finales.includes(e));
}

// --- VISUALIZACIÓN ---
onMounted(() => {
    const def = props.automata.json_definicion;
    
    // Nodos
    const nodes = def.estados.map(estado => ({
        id: estado,
        label: estado,
        shape: 'circle',
        color: {
            background: estado === def.estado_inicial ? '#d1fae5' : '#ffffff',
            border: '#2B7CE9',
            highlight: { background: '#f0f0f0', border: '#2B7CE9' }
        },
        borderWidth: def.estados_finales.includes(estado) ? 3 : 1,
        font: { size: 16, face: 'monospace' }
    }));

    // Aristas
    const edges = [];
    if (def.transiciones) {
        Object.keys(def.transiciones).forEach(origen => {
            const destinosPorSimbolo = def.transiciones[origen];
            Object.keys(destinosPorSimbolo).forEach(simbolo => {
                let destinos = destinosPorSimbolo[simbolo];
                if (!Array.isArray(destinos)) destinos = [destinos]; // Normalizar

                destinos.forEach(destino => {
                    if (destino && destino !== "") {
                        const arista = edges.find(e => e.from === origen && e.to === destino);
                        if (arista) {
                            if (!arista.label.includes(simbolo)) arista.label += `, ${simbolo}`;
                        } else {
                            edges.push({
                                from: origen,
                                to: destino,
                                label: simbolo,
                                arrows: 'to',
                                font: { align: 'top' },
                                smooth: { type: 'curvedCW', roundness: 0.2 }
                            });
                        }
                    }
                });
            });
        });
    }

    // Inicializar Vis
    if (networkContainer.value) {
        new Network(networkContainer.value, { nodes, edges }, {
            physics: { 
                enabled: true, 
                solver: 'forceAtlas2Based',
                stabilization: { iterations: 100 }
            },
            interaction: { hover: true, zoomView: true }
        });
    }
});
</script>