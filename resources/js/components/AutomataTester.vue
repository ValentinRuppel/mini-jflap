<template>
  <div v-if="automata" class="p-4">
    <h2 class="text-xl font-bold mb-4">Probar cadenas en: {{ automata.nombre }}</h2>

    <input v-model="cadena" type="text" placeholder="Ingrese una cadena"
           class="border p-2 rounded w-1/2"/>
    <button @click="probarCadena"
            class="ml-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      Probar
    </button>

    <div v-if="resultado" class="mt-4">
      <p class="font-semibold">Resultado: 
        <span :class="resultado.aceptada ? 'text-green-600' : 'text-red-600'">
          {{ resultado.aceptada ? 'Aceptada ✅' : 'Rechazada ❌' }}
        </span>
      </p>
      <p class="mt-2">Recorrido: {{ resultado.recorrido.join(' → ') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
  automata: Object
});

const cadena = ref('');
const resultado = ref(null);

async function probarCadena() {
  if (!cadena.value) return;

  const res = await axios.post(`/api/automatas/${props.automata.id}/probar`, {
    cadena: cadena.value
  });
  resultado.value = res.data;
}
</script>
