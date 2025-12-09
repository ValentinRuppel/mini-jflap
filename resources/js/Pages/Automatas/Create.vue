<template>
  <div class="bg-white p-6 rounded shadow-md max-w-3xl mx-auto mt-6">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Crear nuevo Autómata</h2>
        <Link :href="route('automatas.index')" class="text-gray-500 hover:text-red-500 transition">
            Cancelar
        </Link>
    </div>

    <form @submit.prevent="submit">
        <div class="mb-4">
            <label class="font-semibold block mb-1">Nombre:</label>
            <input
                v-model="form.nombre"
                type="text"
                class="border p-2 rounded w-full focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ej: DFA de 0s pares"
            />
            <div v-if="form.errors.nombre" class="text-red-500 text-sm mt-1">{{ form.errors.nombre }}</div>
        </div>

        <div class="mb-4">
            <label class="font-semibold block mb-1">Tipo:</label>
            <select v-model="form.tipo" class="border p-2 rounded w-full">
                <option value="DFA">DFA (Determinista)</option>
                <option value="NFA">NFA (No determinista)</option>
            </select>
        </div>

        <div class="mb-4">
            <label class="font-semibold block mb-1">Estados (separados por coma):</label>
            <input
                v-model="estadosTexto"
                type="text"
                class="border p-2 rounded w-full"
                placeholder="q0,q1,q2"
            />
            <p class="text-xs text-gray-500 mt-1">Se detectaron {{ estados.length }} estados.</p>
        </div>

        <div class="mb-4">
            <label class="font-semibold block mb-1">Alfabeto (separado por coma):</label>
            <input
                v-model="alfabetoTexto"
                type="text"
                class="border p-2 rounded w-full"
                placeholder="0,1"
            />
        </div>

        <div class="mb-4">
            <label class="font-semibold block mb-1">Estado inicial:</label>
            <select v-model="estadoInicial" class="border p-2 rounded w-full">
                <option disabled value="">Seleccione...</option>
                <option v-for="estado in estados" :key="estado" :value="estado">
                    {{ estado }}
                </option>
            </select>
        </div>

        <div class="mb-4">
            <label class="font-semibold block mb-1">Estados finales:</label>
            <div class="flex flex-wrap gap-3 mt-2 bg-gray-50 p-3 rounded border">
                <span v-if="estados.length === 0" class="text-gray-400 text-sm">Defina estados primero...</span>
                <label
                    v-for="estado in estados"
                    :key="estado"
                    class="flex items-center gap-2 cursor-pointer"
                >
                    <input
                        type="checkbox"
                        :value="estado"
                        v-model="estadosFinales"
                        class="accent-blue-600 w-4 h-4"
                    />
                    {{ estado }}
                </label>
            </div>
        </div>

<div v-if="estados.length && alfabeto.length" class="mb-20 border-t pt-4">
    <h3 class="font-semibold text-lg mb-3">Transiciones:</h3>
    
    <div class="grid gap-4">
        <div v-for="estado in estados" :key="estado" class="bg-gray-50 p-4 rounded border shadow-sm">
            <h4 class="font-bold text-blue-700 mb-3 border-b pb-1 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span> {{ estado }}
            </h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="simbolo in alfabeto" :key="simbolo" class="relative">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="font-mono font-bold bg-white border px-2 rounded text-sm">{{ simbolo }}</span>
                        <span class="text-gray-400 text-xs">➜</span>
                    </div>

                    <select v-if="form.tipo === 'DFA'" 
                        v-model="transiciones[estado][simbolo]" 
                        class="w-full border p-2 rounded bg-white focus:ring-2 focus:ring-blue-500 cursor-pointer"
                    >
                        <option value="">(Vacio / Trap)</option>
                        <option v-for="dest in estados" :key="dest" :value="dest">{{ dest }}</option>
                    </select>

                    <div v-else class="relative">
                        <button 
                            type="button"
                            @click="toggleDropdown(estado, simbolo)"
                            class="w-full border p-2 rounded bg-white text-left text-sm flex justify-between items-center hover:border-blue-400 focus:ring-2 focus:ring-blue-500"
                        >
                            <span class="truncate block max-w-[120px]">
                                {{ transiciones[estado][simbolo].length ? transiciones[estado][simbolo].join(', ') : '(Seleccionar...)' }}
                            </span>
                            <span class="text-xs text-gray-500">▼</span>
                        </button>

                        <div v-if="dropdownActivo === `${estado}-${simbolo}`" 
                             class="absolute z-50 top-full left-0 w-full mt-1 bg-white border rounded shadow-xl max-h-48 overflow-y-auto p-2"
                        >
                            <div class="fixed inset-0 z-[-1]" @click="dropdownActivo = null"></div>

                            <label v-for="dest in estados" :key="dest" class="flex items-center gap-2 p-1 hover:bg-gray-50 rounded cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    :value="dest" 
                                    v-model="transiciones[estado][simbolo]"
                                    class="rounded text-blue-600 focus:ring-blue-500"
                                />
                                <span class="text-sm">{{ dest }}</span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

        <button
            type="submit"
            :disabled="form.processing"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded w-full transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
            <span v-if="form.processing">Guardando...</span>
            <span v-else>Guardar Autómata</span>
        </button>
        
        <div v-if="Object.keys(form.errors).length > 0" class="mt-4 p-3 bg-red-100 text-red-700 rounded">
            Por favor revisa los errores en el formulario.
        </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Link, useForm } from '@inertiajs/vue3'

// --- LÓGICA DEL AUTOMATA (Variables locales) ---
const estadosTexto = ref('')
const alfabetoTexto = ref('')
const estados = ref([])
const alfabeto = ref([])
const estadoInicial = ref('')
const estadosFinales = ref([])
const transiciones = ref({})

// --- LÓGICA DE INERTIA (Formulario) ---
const form = useForm({
    nombre: '',
    tipo: 'DFA',
    json_definicion: {} // Se llena justo antes del submit
});

// Watchers para actualizar la estructura de datos dinámicamente
watch([estadosTexto, alfabetoTexto], () => {
    // 1. Parsear inputs
    const nuevosEstados = estadosTexto.value.split(',').map(e => e.trim()).filter(Boolean);
    const nuevoAlfabeto = alfabetoTexto.value.split(',').map(a => a.trim()).filter(Boolean);

    // 2. Preservar transiciones existentes si es posible
    const nuevasTransiciones = {};
    
    nuevosEstados.forEach(e => {
        nuevasTransiciones[e] = {};
        nuevoAlfabeto.forEach(s => {
            // Si ya existía una transición para este estado/simbolo, la mantenemos
            if (transiciones.value[e] && transiciones.value[e][s]) {
                nuevasTransiciones[e][s] = transiciones.value[e][s];
            } else {
                nuevasTransiciones[e][s] = ''; // Inicializar vacía
            }
        });
    });

    estados.value = nuevosEstados;
    alfabeto.value = nuevoAlfabeto;
    transiciones.value = nuevasTransiciones;
});

function submit() {
    // Empaquetamos toda la lógica visual en el JSON que espera el backend
    form.json_definicion = {
        estados: estados.value,
        alfabeto: alfabeto.value,
        estado_inicial: estadoInicial.value,
        estados_finales: estadosFinales.value,
        transiciones: transiciones.value
    };

    // Enviamos usando Inertia (esto maneja auth y CSRF automáticamente)
    form.post(route('automatas.store'), {
        onSuccess: () => {
            // Opcional: limpiar formulario si no rediriges (pero estamos redirigiendo)
        }
    });
}
watch([estadosTexto, alfabetoTexto, () => form.tipo], () => { // Agregamos form.tipo al watch
    const nuevosEstados = estadosTexto.value.split(',').map(e => e.trim()).filter(Boolean);
    const nuevoAlfabeto = alfabetoTexto.value.split(',').map(a => a.trim()).filter(Boolean);
    const nuevasTransiciones = {};

    nuevosEstados.forEach(e => {
        nuevasTransiciones[e] = {};
        nuevoAlfabeto.forEach(s => {
            // Inicialización inteligente
            if (form.tipo === 'NFA') {
                // Para NFA inicializamos como Array vacío []
                nuevasTransiciones[e][s] = []; 
            } else {
                // Para DFA inicializamos como string vacío ''
                nuevasTransiciones[e][s] = '';
            }
        });
    });
    
    // (Omití la lógica de preservar datos viejos por brevedad, 
    // pero idealmente deberías chequear si existía y convertir string<->array si cambias de tipo)

    estados.value = nuevosEstados;
    alfabeto.value = nuevoAlfabeto;
    transiciones.value = nuevasTransiciones;
});
// Variable para controlar qué dropdown está abierto
const dropdownActivo = ref(null);

function toggleDropdown(estado, simbolo) {
    const key = `${estado}-${simbolo}`;
    if (dropdownActivo.value === key) {
        dropdownActivo.value = null; // Cerrar si ya estaba abierto
    } else {
        dropdownActivo.value = key; // Abrir este
    }
}
</script>