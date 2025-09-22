<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Mini JFLAP 🚀</h1>

    <!-- Formulario de creación -->
    <AutomataForm @automata-creado="refrescarLista" />

    <div class="grid grid-cols-2 gap-6">
      <!-- Lista de autómatas -->
      <AutomataList ref="lista" @select-automata="seleccionarAutomata" />

      <!-- Tester + Grafo -->
      <div>
        <AutomataTester v-if="automataSeleccionado" :automata="automataSeleccionado"/>
        <AutomataGraph v-if="automataSeleccionado" :jsonDefinicion="automataSeleccionado.json_definicion"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AutomataForm from './AutomataForm.vue';
import AutomataList from './AutomataList.vue';
import AutomataTester from './AutomataTester.vue';
import AutomataGraph from './AutomataGraph.vue';

const automataSeleccionado = ref(null);
const lista = ref(null);

function seleccionarAutomata(a) {
  automataSeleccionado.value = a;
}

function refrescarLista() {
  if (lista.value && lista.value.cargar) {
    lista.value.cargar();
  }
}
</script>
