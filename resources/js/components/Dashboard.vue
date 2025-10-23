<template>
  <div class="text-center mt-10">
    <h1 class="text-3xl font-bold mb-4">Bienvenido, {{ user.name }}</h1>
    <p class="mb-4">Tu correo: {{ user.email }}</p>
    <button @click="logout" class="bg-red-600 text-white px-4 py-2 rounded">Cerrar sesión</button>
  </div>
</template>

<script setup>
import axios from 'axios'
const props = defineProps({ user: Object })
const emit = defineEmits(['logout'])

async function logout() {
  await axios.post('/logout')
  emit('logout')
}
</script>
