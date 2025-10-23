<template>
  <div class="max-w-sm mx-auto mt-10 bg-white p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4">Crear cuenta</h2>

    <form @submit.prevent="register">
      <input v-model="name" type="text" placeholder="Nombre completo" class="border p-2 w-full mb-3" required />
      <input v-model="email" type="email" placeholder="Correo" class="border p-2 w-full mb-3" required />
      <input v-model="password" type="password" placeholder="Contraseña" class="border p-2 w-full mb-3" required />
      <input v-model="password_confirmation" type="password" placeholder="Repetir contraseña" class="border p-2 w-full mb-3" required />
      <button type="submit" class="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 w-full">Registrarse</button>
    </form>

    <p v-if="error" class="text-red-600 mt-3">{{ error }}</p>
    <p class="mt-3 text-sm">¿Ya tenés cuenta? 
      <a href="#" class="text-blue-500" @click="$emit('change-view', 'login')">Iniciá sesión</a>.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const name = ref('')
const email = ref('')
const password = ref('')
const password_confirmation = ref('')
const error = ref('')

const emit = defineEmits(['register-success', 'change-view'])

async function register() {
  error.value = ''
  try {
    await axios.get('/sanctum/csrf-cookie')
    await axios.post('/register', {
      name: name.value,
      email: email.value,
      password: password.value,
      password_confirmation: password_confirmation.value
    })
    const { data } = await axios.get('/api/user')
    emit('register-success', data)
  } catch (err) {
    error.value = 'Error al registrar el usuario'
  }
}
</script>
