<template>
    <AuthenticatedLayout>
        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">

                    <h2 class="text-2xl font-bold text-gray-800 mb-6">
                        {{ isEditing ? 'Editar Autómata' : 'Crear nuevo Autómata' }}
                    </h2>

                    <form @submit.prevent="submit">
                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Nombre:</label>
                            <input v-model="form.nombre" type="text" class="border p-2 rounded w-full"
                                placeholder="Ej: AP de paréntesis balanceados" />
                            <div v-if="form.errors.nombre" class="text-red-500 text-sm mt-1">{{ form.errors.nombre }}
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Tipo:</label>
                            
                            <select 
                                v-model="form.tipo" 
                                :disabled="isEditing"
                                class="border p-2 rounded w-full transition-colors"
                                :class="{ 'bg-gray-100 text-gray-500 cursor-not-allowed': isEditing }"
                            >
                                <option value="DFA">DFA (Determinista)</option>
                                <option value="NFA">NFA (No determinista)</option>
                                <option value="AP">AP (Autómata de Pila)</option>
                            </select>

                            <p v-if="isEditing" class="text-xs text-gray-500 mt-1">
                                El tipo de autómata no se puede cambiar durante la edición.
                            </p>

                            <p v-if="form.tipo === 'AP' && !isEditing" class="text-sm text-blue-600 mt-1">
                                Nota: En los Autómatas de Pila definimos qué se saca (Pop) y qué se mete (Push) en la
                                memoria. Usa 'λ' o deja vacío para lambda.
                            </p>
                        </div>
                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Estados (separados por coma):</label>
                            <input v-model="estadosTexto" type="text" class="border p-2 rounded w-full"
                                placeholder="q0,q1,q2" />
                        </div>

                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Alfabeto de Entrada (separado por coma):</label>
                            <input v-model="alfabetoTexto" type="text" class="border p-2 rounded w-full"
                                placeholder="0,1" />
                        </div>

                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Estado inicial:</label>
                            <select v-model="estadoInicial" class="border p-2 rounded w-full">
                                <option disabled value="">Seleccione...</option>
                                <option v-for="estado in estados" :key="estado" :value="estado">{{ estado }}</option>
                            </select>
                        </div>

                        <div class="mb-4">
                            <label class="font-semibold block mb-1">Estados finales:</label>
                            <div class="flex flex-wrap gap-3 mt-2 bg-gray-50 p-3 rounded border">
                                <label v-for="estado in estados" :key="estado"
                                    class="flex items-center gap-2 cursor-pointer">
                                    <input type="checkbox" :value="estado" v-model="estadosFinales"
                                        class="accent-blue-600 w-4 h-4" />
                                    {{ estado }}
                                </label>
                            </div>
                        </div>

                        <div v-if="estados.length && alfabeto.length" class="mb-6 border-t pt-4">
                            <h3 class="font-semibold text-lg mb-3">Función de Transición:</h3>

                            <div class="grid gap-6">
                                <div v-for="estado in estados" :key="estado"
                                    class="bg-gray-50 p-4 rounded border shadow-sm">
                                    <h4 class="font-bold text-blue-700 mb-3 border-b pb-1 flex items-center gap-2">
                                        <span class="w-2 h-2 rounded-full bg-blue-500"></span> {{ estado }}
                                    </h4>

                                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                        <div v-for="simbolo in alfabeto" :key="simbolo" class="relative">
                                            <div class="flex items-center gap-2 mb-1">
                                                <span
                                                    class="font-mono font-bold bg-white border px-2 rounded text-sm min-w-[30px] text-center">{{
                                                    simbolo }}</span>
                                                <span class="text-gray-400 text-xs">➜</span>
                                            </div>

                                            <select v-if="form.tipo === 'DFA'" v-model="transiciones[estado][simbolo]"
                                                class="w-full border p-2 rounded">
                                                <option value="">(Trap)</option>
                                                <option v-for="dest in estados" :key="dest" :value="dest">{{ dest }}
                                                </option>
                                            </select>

                                            <div v-else-if="form.tipo === 'NFA'" class="relative">
                                                <button type="button" @click="toggleDropdown(estado, simbolo)"
                                                    class="w-full border p-2 rounded bg-white text-left text-sm flex justify-between">
                                                    <span class="truncate">{{ transiciones[estado][simbolo]?.length ?
                                                        transiciones[estado][simbolo].join(', ') : '(Seleccionar...)'
                                                        }}</span>
                                                    <span class="text-xs">▼</span>
                                                </button>
                                                <div v-if="dropdownActivo === `${estado}-${simbolo}`"
                                                    class="absolute z-50 top-full w-full bg-white border shadow-xl p-2 max-h-40 overflow-auto">
                                                    <div class="fixed inset-0 z-[-1]" @click="dropdownActivo = null">
                                                    </div>
                                                    <label v-for="dest in estados" :key="dest"
                                                        class="flex gap-2 p-1 hover:bg-gray-50 cursor-pointer">
                                                        <input type="checkbox" :value="dest"
                                                            v-model="transiciones[estado][simbolo]" /> {{ dest }}
                                                    </label>
                                                </div>
                                            </div>

                                            <div v-else-if="form.tipo === 'AP'" class="bg-white border p-2 rounded">
                                                <ul class="mb-2 space-y-1">
                                                    <li v-for="(regla, idx) in transiciones[estado][simbolo]" :key="idx"
                                                        class="text-xs flex justify-between bg-blue-50 p-1 rounded">
                                                        <span>Ir a <b>{{ regla.dest }}</b> | Pop: {{ regla.pop || 'λ'
                                                            }}, Push: {{ regla.push || 'λ' }}</span>
                                                        <button @click="removeApRule(estado, simbolo, idx)"
                                                            class="text-red-500 font-bold px-1">×</button>
                                                    </li>
                                                </ul>

                                                <div class="flex gap-1 items-center">
                                                    <select v-model="apTemp[estado + simbolo].dest"
                                                        class="border text-xs p-1 w-1/3 rounded">
                                                        <option value="" disabled>Dest</option>
                                                        <option v-for="d in estados" :key="d" :value="d">{{ d }}
                                                        </option>
                                                    </select>
                                                    <input v-model="apTemp[estado + simbolo].pop" placeholder="Pop"
                                                        class="border text-xs p-1 w-1/4 rounded" />
                                                    <input v-model="apTemp[estado + simbolo].push" placeholder="Push"
                                                        class="border text-xs p-1 w-1/4 rounded" />
                                                    <button type="button" @click="addApRule(estado, simbolo)"
                                                        class="bg-green-500 text-white text-xs px-2 py-1 rounded hover:bg-green-600">+</button>
                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <button type="submit" :disabled="form.processing"
                            class="mt-6 bg-blue-600 text-white py-3 px-4 rounded w-full font-bold hover:bg-blue-700 transition">
                            {{ isEditing ? 'Actualizar Autómata' : 'Guardar Autómata' }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>

<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { ref, watch, onMounted, reactive } from 'vue';
import { Link, useForm } from '@inertiajs/vue3';

const props = defineProps({
    automata: { type: Object, default: null }
});

const isEditing = !!props.automata;
const def = props.automata?.json_definicion || {};

// Variables reactivas
const estadosTexto = ref(def.estados ? def.estados.join(',') : '');
const alfabetoTexto = ref(def.alfabeto ? def.alfabeto.join(',') : '');
const estados = ref(def.estados || []);
const alfabeto = ref(def.alfabeto || []);
const estadoInicial = ref(def.estado_inicial || '');
const estadosFinales = ref(def.estados_finales || []);
const transiciones = ref(def.transiciones || {});

// Variables auxiliares para la UI
const dropdownActivo = ref(null);
// apTemp: Almacena temporalmente lo que el usuario escribe en los inputs de Pila antes de darle al botón "+"
const apTemp = reactive({});

const form = useForm({
    nombre: props.automata?.nombre || '',
    tipo: props.automata?.tipo || 'DFA',
    json_definicion: {}
});

// Inicializar estructura al montar (importante para edición)
onMounted(() => {
    // Si es AP, asegurar que apTemp tenga estructura para evitar errores
    if (def.estados && def.alfabeto) {
        initApTemp(def.estados, def.alfabeto);
    }

});

watch(() => form.tipo, (nuevoTipo, viejoTipo) => {
    // Evitamos limpiar si es la carga inicial o si no hubo cambio real
    if (nuevoTipo === viejoTipo) return;

    // Reiniciar formulario (Excepto Nombre)
    estadosTexto.value = '';
    alfabetoTexto.value = '';
    estadoInicial.value = '';
    estadosFinales.value = [];
    transiciones.value = {};
    // La limpieza de apTemp ocurre sola al no haber estados
});

// 2. WATCHER DE CONSTRUCCIÓN (Cuando cambian los inputs de texto)
// Nota: Quitamos "() => form.tipo" de este array
watch([estadosTexto, alfabetoTexto], () => {
    const nuevosEstados = estadosTexto.value.split(',').map(e => e.trim()).filter(Boolean);
    const nuevoAlfabeto = alfabetoTexto.value.split(',').map(a => a.trim()).filter(Boolean);
    const nuevasTransiciones = {};

    nuevosEstados.forEach(e => {
        nuevasTransiciones[e] = {};
        nuevoAlfabeto.forEach(s => {
            // Verificamos si existe data previa válida
            if (transiciones.value[e] && transiciones.value[e][s] !== undefined) {
                nuevasTransiciones[e][s] = transiciones.value[e][s];
            } else {
                // Inicializar en blanco según el tipo actual
                if (form.tipo === 'DFA') nuevasTransiciones[e][s] = '';
                else if (form.tipo === 'NFA') nuevasTransiciones[e][s] = [];
                else if (form.tipo === 'AP') nuevasTransiciones[e][s] = [];
            }
        });
    });

    estados.value = nuevosEstados;
    alfabeto.value = nuevoAlfabeto;
    transiciones.value = nuevasTransiciones;

    initApTemp(nuevosEstados, nuevoAlfabeto);
});
function initApTemp(misEstados, misSimbolos) {
    misEstados.forEach(e => {
        misSimbolos.forEach(s => {
            if (!apTemp[e + s]) {
                apTemp[e + s] = { dest: '', pop: '', push: '' };
            }
        });
    });
}

// --- Helpers para UI ---
function toggleDropdown(estado, simbolo) {
    const key = `${estado}-${simbolo}`;
    dropdownActivo.value = dropdownActivo.value === key ? null : key;
}

// Agregar regla de Pila
function addApRule(estado, simbolo) {
    const temp = apTemp[estado + simbolo];
    if (!temp.dest) return; // Validación básica

    // Agregamos al array de transiciones real
    transiciones.value[estado][simbolo].push({
        dest: temp.dest,
        pop: temp.pop || 'λ',
        push: temp.push || 'λ'
    });

    // Limpiar inputs
    apTemp[estado + simbolo] = { dest: '', pop: '', push: '' };
}

function removeApRule(estado, simbolo, idx) {
    transiciones.value[estado][simbolo].splice(idx, 1);
}

function submit() {
    form.json_definicion = {
        estados: estados.value,
        alfabeto: alfabeto.value,
        estado_inicial: estadoInicial.value,
        estados_finales: estadosFinales.value,
        transiciones: transiciones.value
    };

    if (isEditing) form.put(route('automatas.update', props.automata.id));
    else form.post(route('automatas.store'));
}
</script>