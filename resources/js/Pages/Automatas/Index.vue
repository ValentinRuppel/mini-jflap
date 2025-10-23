<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-4">Mis Autómatas 🤖</h1>

    <p class="text-gray-600 mb-6">
      Desde aquí vas a poder crear, probar y compartir tus autómatas.
    </p>

    <a
      href="#"
      @click.prevent="irACrear"
      class="inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
    >
      ➕ Crear nuevo autómata
    </a>

    <div class="mt-8 border-t pt-4">
    <p class="text-gray-500">Próximamente: listado de autómatas guardados…</p>
    </div>
    </div>
    <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Mis Autómatas 🤖</h1>
    <AutomataForm />
    </div>
</template>

<script setup>
import { router } from '@inertiajs/vue3'
import AutomataForm from './AutomataForm.vue'
function irACrear() {
  // después podemos cambiarlo a otra página de creación
  alert('acá iría la vista de creación')
}
</script>

