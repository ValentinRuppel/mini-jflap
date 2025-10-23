<template>
  <div class="bg-white p-6 rounded shadow-md max-w-3xl mx-auto mt-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">Crear nuevo Autómata</h2>

    <!-- NOMBRE -->
    <div class="mb-4">
      <label class="font-semibold">Nombre:</label>
      <input
        v-model="nombre"
        type="text"
        class="border p-2 rounded w-full"
        placeholder="Ej: DFA de 0s pares"
      />
    </div>

    <!-- TIPO -->
    <div class="mb-4">
      <label class="font-semibold">Tipo:</label>
      <select v-model="tipo" class="border p-2 rounded w-full">
        <option value="DFA">DFA (Determinista)</option>
        <option value="NFA">NFA (No determinista)</option>
      </select>
    </div>

    <!-- ESTADOS -->
    <div class="mb-4">
      <label class="font-semibold">Estados (separados por coma):</label>
      <input
        v-model="estadosTexto"
        type="text"
        class="border p-2 rounded w-full"
        placeholder="q0,q1,q2"
      />
    </div>

    <!-- ALFABETO -->
    <div class="mb-4">
      <label class="font-semibold">Alfabeto (separado por coma):</label>
      <input
        v-model="alfabetoTexto"
        type="text"
        class="border p-2 rounded w-full"
        placeholder="0,1"
      />
    </div>

    <!-- ESTADO INICIAL -->
    <div class="mb-4">
      <label class="font-semibold">Estado inicial:</label>
      <select v-model="estadoInicial" class="border p-2 rounded w-full">
        <option disabled value="">Seleccione...</option>
        <option v-for="estado in estados" :key="estado" :value="estado">
          {{ estado }}
        </option>
      </select>
    </div>

    <!-- ESTADOS FINALES -->
    <div class="mb-4">
      <label class="font-semibold">Estados finales:</label>
      <div class="flex flex-wrap gap-3 mt-2">
        <label
          v-for="estado in estados"
          :key="estado"
          class="flex items-center gap-1"
        >
          <input
            type="checkbox"
            :value="estado"
            v-model="estadosFinales"
            class="accent-blue-600"
          />
          {{ estado }}
        </label>
      </div>
    </div>

    <!-- TRANSICIONES -->
    <div v-if="estados.length && alfabeto.length" class="mb-4">
      <h3 class="font-semibold text-lg mb-2">Transiciones:</h3>
      <div v-for="estado in estados" :key="estado" class="mb-3">
        <h4 class="font-bold mb-1">{{ estado }}</h4>
        <div
          v-for="simbolo in alfabeto"
          :key="simbolo"
          class="flex items-center mb-1 gap-2"
        >
          <span>{{ simbolo }} →</span>
          <select v-model="transiciones[estado][simbolo]" class="border p-1 rounded flex-1">
            <option disabled value="">Seleccione...</option>
            <option v-for="dest in estados" :key="dest" :value="dest">
              {{ dest }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- BOTÓN GUARDAR -->
    <button
      @click="guardarAutomata"
      class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded w-full"
    >
      Guardar Autómata
    </button>

    <p v-if="mensaje" class="text-green-600 mt-3">{{ mensaje }}</p>
    <p v-if="error" class="text-red-600 mt-3">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const nombre = ref('')
const tipo = ref('DFA')
const estadosTexto = ref('')
const alfabetoTexto = ref('')
const estadoInicial = ref('')
const estadosFinales = ref([])
const transiciones = ref({})
const mensaje = ref('')
const error = ref('')

const estados = ref([])
const alfabeto = ref([])

// actualizar listas y estructura de transiciones
watch([estadosTexto, alfabetoTexto], () => {
  estados.value = estadosTexto.value.split(',').map(e => e.trim()).filter(Boolean)
  alfabeto.value = alfabetoTexto.value.split(',').map(a => a.trim()).filter(Boolean)
  transiciones.value = {}
  estados.value.forEach(e => {
    transiciones.value[e] = {}
    alfabeto.value.forEach(s => transiciones.value[e][s] = '')
  })
})

async function guardarAutomata() {
  mensaje.value = ''
  error.value = ''

  const json_definicion = {
    estados: estados.value,
    alfabeto: alfabeto.value,
    estado_inicial: estadoInicial.value,
    estados_finales: estadosFinales.value,
    transiciones: transiciones.value,
  }

  try {
    await axios.post('/api/automatas', {
      nombre: nombre.value,
      tipo: tipo.value,
      json_definicion
    })
    mensaje.value = 'Autómata guardado correctamente 🎉'
  } catch (err) {
    error.value = 'Error al guardar el autómata'
    console.error(err)
  }
}
</script>
