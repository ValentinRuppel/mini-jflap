<template>
  <div class="h-screen flex flex-col bg-gray-100 overflow-hidden">
    
    <header class="bg-white border-b px-6 py-3 flex justify-between items-center shadow-sm z-20">
        <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold text-gray-800">{{ automata.nombre }}</h1>
            <span :class="automata.tipo === 'DFA' ? 'bg-purple-100 text-purple-700' : 'bg-orange-100 text-orange-700'" 
                  class="px-2 py-0.5 rounded text-xs font-bold border">
                {{ automata.tipo }}
            </span>
        </div>
        
        <div class="flex items-center gap-3">
             <button @click="exportarJson" class="text-sm text-gray-600 hover:text-blue-600 font-medium flex items-center gap-1">
                💾 Exportar
            </button>
            <div class="h-4 w-px bg-gray-300"></div>
            <Link :href="route('automatas.index')" class="text-sm text-gray-500 hover:text-gray-800 transition">
                Volver al listado
            </Link>
        </div>
    </header>

    <div class="flex flex-1 overflow-hidden relative">
        
        <main class="flex-1 relative bg-gray-50">
            <div ref="networkContainer" class="w-full h-full cursor-grab active:cursor-grabbing"></div>
            
            <div class="absolute bottom-4 left-4 bg-white/90 backdrop-blur p-3 rounded-lg shadow border text-xs text-gray-600 pointer-events-none select-none">
                <div class="flex items-center gap-2 mb-1">
                    <span class="w-3 h-3 bg-[#d1fae5] border border-[#059669] rounded-full"></span> Estado Inicial
                </div>
                <div class="flex items-center gap-2 mb-1">
                    <span class="w-3 h-3 bg-white border-2 border-blue-500 rounded-full"></span> Estado Normal
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-3 h-3 bg-white border-[3px] border-blue-500 rounded-full"></span> Estado Final
                </div>
            </div>
        </main>

        <aside class="w-96 bg-white border-l shadow-xl z-10 flex flex-col overflow-y-auto">
            <div class="p-5 border-b bg-gray-50">
                <h2 class="font-bold text-lg text-gray-800 flex items-center gap-2">
                    🧪 Simulador
                </h2>
                <p class="text-xs text-gray-500 mt-1">Probá si una cadena es aceptada por el autómata.</p>
            </div>

            <div class="p-5 flex-1">
                <div class="mb-4">
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Cadena de Entrada</label>
                    <div class="relative">
                        <input 
                            v-model="inputCadena" 
                            @keyup.enter="probarCadena"
                            type="text" 
                            class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 font-mono tracking-widest" 
                            placeholder="Ej: 01011" 
                        />
                        <span v-if="inputCadena" @click="inputCadena = ''" class="absolute right-3 top-2.5 cursor-pointer text-gray-400 hover:text-gray-600">✕</span>
                    </div>
                </div>

                <button 
                    @click="probarCadena"
                    :disabled="!inputCadena"
                    class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    Verificar Cadena
                </button>

                <div v-if="resultado !== null" class="mt-6 animate-fade-in">
                    <div :class="resultado ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'" class="border rounded-lg p-4 text-center">
                        <div class="text-4xl mb-2">{{ resultado ? '✅' : '❌' }}</div>
                        <h3 :class="resultado ? 'text-green-800' : 'text-red-800'" class="font-bold text-lg">
                            {{ resultado ? 'Cadena Aceptada' : 'Cadena Rechazada' }}
                        </h3>
                    </div>

                    <div class="mt-4">
                        <h4 class="text-xs font-bold text-gray-500 uppercase mb-2">Estados Alcanzados</h4>
                        <div class="bg-gray-800 text-green-400 font-mono text-xs p-3 rounded overflow-x-auto">
                            <span class="text-gray-500">Input:</span> "{{ inputCadena }}"<br>
                            <span class="text-gray-500">Fin :</span> { {{ estadosFinalesAlcanzados.join(', ') }} }
                            <div v-if="!resultado && estadosFinalesAlcanzados.length === 0" class="text-red-400 mt-1">
                                -> Murió en el camino (Trap)
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="p-4 border-t text-center text-xs text-gray-400">
                Mini-JFLAP &copy; 2025
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

<style scoped>
/* Animación suave para el resultado */
.animate-fade-in {
    animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>