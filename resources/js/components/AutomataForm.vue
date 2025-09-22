<template>
  <div class="p-4 border rounded mb-6">
    <h2 class="text-xl font-bold mb-4">Crear nuevo Autómata</h2>

    <!-- Nombre -->
    <div class="mb-4">
      <label class="block font-semibold mb-1">Nombre</label>
      <input v-model="nombre" type="text"
             class="border p-2 rounded w-full" placeholder="Ej: DFA de 0s pares"/>
    </div>

    <!-- Estados -->
    <div class="mb-4">
      <label class="block font-semibold mb-1">Estados (separados por coma)</label>
      <input v-model="estadosTexto" type="text"
             class="border p-2 rounded w-full" placeholder="q0,q1,q2"/>
    </div>

    <!-- Alfabeto -->
    <div class="mb-4">
      <label class="block font-semibold mb-1">Alfabeto (separado por coma)</label>
      <input v-model="alfabetoTexto" type="text"
             class="border p-2 rounded w-full" placeholder="0,1"/>
    </div>

    <!-- Estado inicial -->
    <div class="mb-4">
      <label class="block font-semibold mb-1">Estado inicial</label>
      <select v-model="estadoInicial" class="border p-2 rounded w-full">
        <option disabled value="">Seleccione...</option>
        <option v-for="estado in estados" :key="estado" :value="estado">{{ estado }}</option>
      </select>
    </div>

    <!-- Estados finales -->
    <div class="mb-4">
      <label class="block font-semibold mb-1">Estados finales</label>
      <div class="flex flex-wrap gap-2">
        <label v-for="estado in estados" :key="estado" class="flex items-center gap-1">
          <input type="checkbox" :value="estado" v-model="estadosFinales"/>
          {{ estado }}
        </label>
      </div>
    </div>

    <!-- Transiciones -->
    <div v-if="estados.length && alfabeto.length" class="mb-6">
      <h3 class="font-bold mb-2">Transiciones</h3>
      <div v-for="estado in estados" :key="estado" class="mb-4">
        <h4 class="font-semibold mb-1">{{ estado }}</h4>
        <div v-for="simbolo in alfabeto" :key="simbolo" class="flex items-center gap-2 mb-1">
          <span>{{ simbolo }} →</span>
          <select v-model="transiciones[estado][simbolo]" class="border p-1 rounded">
            <option disabled value="">Seleccione...</option>
            <option v-for="dest in estados" :key="dest" :value="dest">{{ dest }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Botón Guardar -->
    <button @click="guardarAutomata"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
      Guardar Autómata
    </button>

    <div v-if="mensaje" class="mt-4 p-2 rounded"
         :class="mensaje.tipo === 'ok' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
      {{ mensaje.texto }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const nombre = ref('');
const estadosTexto = ref('');
const alfabetoTexto = ref('');
const estadoInicial = ref('');
const estadosFinales = ref([]);
const transiciones = ref({});
const mensaje = ref(null);

const estados = ref([]);
const alfabeto = ref([]);

// Cuando cambian los textos, actualizamos arrays
watch(estadosTexto, (val) => {
  estados.value = val.split(',').map(e => e.trim()).filter(e => e);
  inicializarTransiciones();
});

watch(alfabetoTexto, (val) => {
  alfabeto.value = val.split(',').map(a => a.trim()).filter(a => a);
  inicializarTransiciones();
});

function inicializarTransiciones() {
  transiciones.value = {};
  estados.value.forEach(estado => {
    transiciones.value[estado] = {};
    alfabeto.value.forEach(simbolo => {
      transiciones.value[estado][simbolo] = '';
    });
  });
}

async function guardarAutomata() {
  try {
    const json_definicion = {
      estados: estados.value,
      alfabeto: alfabeto.value,
      estado_inicial: estadoInicial.value,
      estados_finales: estadosFinales.value,
      transiciones: transiciones.value
    };

    const res = await axios.post('/api/automatas', {
      nombre: nombre.value,
      tipo: 'DFA',
      json_definicion
    });

    mensaje.value = { tipo: 'ok', texto: 'Autómata creado con éxito ✅' };

    // reset
    nombre.value = '';
    estadosTexto.value = '';
    alfabetoTexto.value = '';
    estadoInicial.value = '';
    estadosFinales.value = [];
    transiciones.value = {};

    // avisar al padre
    emit('automata-creado', res.data);
  } catch (error) {
    console.error(error);
    mensaje.value = { tipo: 'error', texto: 'Error al crear el autómata ❌' };
  }
}
</script>
