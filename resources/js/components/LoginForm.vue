<template>
  <div class="max-w-sm mx-auto mt-10 bg-white p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4">Iniciar sesión</h2>

    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Correo" class="border p-2 w-full mb-3" required />
      <input v-model="password" type="password" placeholder="Contraseña" class="border p-2 w-full mb-3" required />
      <button type="submit" class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 w-full">Entrar</button>
    </form>

    <p v-if="error" class="text-red-600 mt-3">{{ error }}</p>
    <p class="mt-3 text-sm">¿No tenés cuenta? 
      <a href="#" class="text-blue-500" @click="$emit('change-view', 'register')">Registrate acá</a>.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const error = ref('')

const emit = defineEmits(['login-success', 'change-view'])

async function login() {
  error.value = ''
  try {
    await axios.get('/sanctum/csrf-cookie')
    await axios.post('/login', {
      email: email.value,
      password: password.value
    })
    const { data } = await axios.get('/api/user')
    emit('login-success', data)
  } catch (err) {
    error.value = 'Credenciales inválidas o error en el servidor'
  }
}
</script>
