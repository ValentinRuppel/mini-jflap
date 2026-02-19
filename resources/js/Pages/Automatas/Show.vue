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
                <Link :href="route('automatas.index')" class="text-sm text-gray-500 hover:text-gray-800">Volver</Link>
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
                <div class="p-4 border-t border-gray-100 bg-gray-50 z-20">
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

                        <div class="mb-3">
                            <label
                                class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-1">Método</label>
                            <select v-model="algoritmoSeleccionado"
                                class="w-full text-xs border-gray-200 rounded-lg bg-gray-50 focus:border-purple-500 focus:ring-purple-500">
                                <option value="genetico">🧬 Algoritmo Genético</option>
                                <option value="sa">🔥 Simulated Annealing</option>
                            </select>
                        </div>

                        <button @click="optimizarConIA" :disabled="procesandoIA"
                            class="w-full relative overflow-hidden group bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-3 rounded-xl shadow-md hover:shadow-lg transition-all disabled:opacity-70 disabled:cursor-wait flex justify-center items-center">
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
                </div>

                <div class="p-4 bg-gray-50 border-t border-gray-100">
                    <button @click="reporteModal = null"
                        class="w-full py-3 bg-gray-800 hover:bg-gray-900 text-white rounded-xl font-bold transition">
                        Entendido
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { Link, router, usePage } from '@inertiajs/vue3';
import { Network } from 'vis-network';

const props = defineProps({ automata: Object });
const networkContainer = ref(null);
const inputCadena = ref('');
const resultado = ref(null);
const estadosFinalesAlcanzados = ref([]);
const page = usePage();
const procesandoIA = ref(false);
const algoritmoSeleccionado = ref('genetico');
const reporteModal = ref(null);

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