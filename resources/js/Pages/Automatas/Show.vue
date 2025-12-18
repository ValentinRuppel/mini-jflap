<template>
  <div class="h-screen flex flex-col bg-gray-50 overflow-hidden font-sans">
    
    <header class="bg-white border-b border-gray-200 relative z-20 shadow-sm px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-4">
             <div class="bg-blue-50 p-2 rounded-lg border border-blue-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
            </div>
            <div>
                <h1 class="text-xl font-bold text-gray-900 leading-none">{{ automata.nombre }}</h1>
                <div class="flex items-center gap-2 mt-1">
                     <span class="px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider bg-blue-100 text-blue-700 border-blue-200">
                        {{ automata.tipo }}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="flex items-center gap-3">
             <button @click="exportarJson" class="text-sm text-gray-600 hover:text-blue-600 font-medium flex items-center gap-1">💾 Exportar</button>
             <div class="h-4 w-px bg-gray-300"></div>
             <Link :href="route('automatas.index')" class="text-sm text-gray-500 hover:text-gray-800">Volver</Link>
        </div>
    </header>
    

    <div class="flex flex-1 overflow-hidden relative">
        <main class="flex-1 relative bg-gray-100/50">
            <div ref="networkContainer" class="w-full h-full outline-none"></div>

            <div class="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-200 z-10 select-none">
                <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3">Referencias</h3>
                
                <div class="space-y-3">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-[#d1fae5] border border-[#2B7CE9] flex items-center justify-center text-xs font-mono text-gray-600 shadow-sm">
                            qi
                        </div>
                        <span class="text-xs font-medium text-gray-600">Estado Inicial</span>
                    </div>

                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-white border border-[#2B7CE9] flex items-center justify-center text-xs font-mono text-gray-600 shadow-sm">
                            qn
                        </div>
                        <span class="text-xs font-medium text-gray-600">Estado Normal</span>
                    </div>

                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-white border-[3px] border-[#2B7CE9] flex items-center justify-center text-xs font-bold font-mono text-gray-800 shadow-sm">
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
                    <input v-model="inputCadena" @keyup.enter="probarCadena" type="text" class="w-full border p-3 rounded-xl font-mono tracking-widest" placeholder="Ej: 0011" />
                    <button @click="probarCadena" :disabled="!inputCadena" class="mt-4 w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition">
                        Verificar
                    </button>
                </div>

                <div v-if="resultado !== null">
                    <div :class="resultado ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'" class="border rounded-2xl p-6 text-center mb-4">
                        <div class="text-4xl mb-2">{{ resultado ? '✓' : '✕' }}</div>
                        <h3 :class="resultado ? 'text-green-800' : 'text-red-800'" class="font-bold text-xl">{{ resultado ? 'Aceptada' : 'Rechazada' }}</h3>
                    </div>
                    
                    <div class="bg-gray-900 text-green-400 font-mono text-xs p-4 rounded-xl overflow-auto">
                        <p class="text-gray-500 mb-1">Traza Final (Estados alcanzados):</p>
                        [ {{ estadosFinalesAlcanzados.join(', ') }} ]
                    </div>
                </div>
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

const inputCadena = ref('');
const resultado = ref(null);
const estadosFinalesAlcanzados = ref([]);

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

            // 1. ¿Terminamos de leer?
            if (indice === cadena.length) {
                // Chequear aceptación
                if (def.estados_finales.includes(estado)) {
                    
                    // --- MODIFICACIÓN AQUÍ ---
                    if (tipo === 'AP') {
                        // Para AP, exigimos Estado Final AND Pila Vacía (o limpia)
                        // Como tu ejemplo no usa Z0 inicial, la pila debe quedar length 0.
                        if (pila.length === 0) {
                            aceptado = true;
                        }
                    } else {
                        // Para DFA / NFA solo importa el estado
                        aceptado = true;
                    }
                    // -------------------------

                    if (aceptado) {
                        if (!estadosFinalesAlcanzados.value.includes(estado)) {
                            estadosFinalesAlcanzados.value.push(estado);
                        }
                    }
                }
            }

            // 2. Buscar transiciones posibles
            // Si ya leímos todo, solo buscamos transiciones lambda que no consuman input?
            // Para simplificar MVP: Solo procesamos si hay caracter o si es lambda explícito (futuro)
            
            if (indice >= cadena.length) continue; 

            const simbolo = cadena[indice];
            const transicionesDelEstado = def.transiciones[estado];
            if (!transicionesDelEstado) continue;

            const reglas = transicionesDelEstado[simbolo];
            
            if (!reglas) continue;

            // Normalizamos reglas a Array para procesar igual DFA/NFA/AP
            let listaReglas = Array.isArray(reglas) ? reglas : (reglas ? [reglas] : []);

            for (let regla of listaReglas) {
                // LOGICA AP (PILA)
                if (tipo === 'AP') {
                    // Regla es objeto: { dest, pop, push }
                    const tope = pila.length > 0 ? pila[pila.length - 1] : '';
                    const popRequerido = regla.pop;
                    
                    // Condición de Pila:
                    // 1. Pop es lambda (vacío o 'λ') -> Siempre pasa
                    // 2. Pop coincide con tope
                    
                    let pilaValida = false;
                    let nuevaPila = [...pila]; // Clonar

                    if (!popRequerido || popRequerido === 'λ') {
                        pilaValida = true; // No saca nada
                    } else if (popRequerido === tope) {
                        pilaValida = true;
                        nuevaPila.pop(); // Sacamos el tope
                    }

                    if (pilaValida) {
                        // Push
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
                    // LOGICA DFA / NFA (Sin pila)
                    // Regla es string (destino)
                    let destino = regla; 
                    if (typeof regla === 'object') destino = regla.dest; // Fallback por si acaso

                    siguientes.push({
                        estado: destino,
                        pila: [],
                        indice: indice + 1
                    });
                }
            }
        }
        
        configuraciones = siguientes;
        if (aceptado) break; // Optimización: Si encontramos un camino exitoso, paramos (salvo que quieras mostrar todos)
    }

    resultado.value = aceptado;
}

// --- VISUALIZADOR ---
onMounted(() => {
    const def = props.automata.json_definicion;
    const nodes = def.estados.map(e => ({
        id: e, label: e, shape: 'circle',
        color: { background: e === def.estado_inicial ? '#d1fae5' : '#fff', border: '#2B7CE9' },
        borderWidth: def.estados_finales.includes(e) ? 3 : 1
    }));

    const edges = [];
    if (def.transiciones) {
        Object.keys(def.transiciones).forEach(origen => {
            Object.keys(def.transiciones[origen]).forEach(simbolo => {
                let reglas = def.transiciones[origen][simbolo];
                if (!Array.isArray(reglas)) reglas = reglas ? [reglas] : [];

                reglas.forEach(r => {
                    let destino = r; 
                    let label = simbolo;

                    // Formato AP: "a, Z; X" (Lee a, Saca Z, Mete X)
                    if (props.automata.tipo === 'AP' && typeof r === 'object') {
                        destino = r.dest;
                        label = `${simbolo}, ${r.pop||'λ'}; ${r.push||'λ'}`;
                    }

                    if (destino) {
                        // Evitar superposición
                        const existing = edges.find(e => e.from === origen && e.to === destino);
                        // En AP no agrupamos labels igual que en DFA porque son largas, mejor dibujar otra flecha o concatenar con \n
                        if (existing) {
                            existing.label += `\n${label}`;
                        } else {
                            edges.push({ from: origen, to: destino, label, arrows: 'to', font: { align: 'top' } });
                        }
                    }
                });
            });
        });
    }

    if (networkContainer.value) {
        new Network(networkContainer.value, { nodes, edges }, { physics: { enabled: true, solver: 'forceAtlas2Based' } });
    }
});
</script>