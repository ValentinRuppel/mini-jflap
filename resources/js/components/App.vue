<template>
  <div class="min-h-screen bg-gray-100">
    <LoginForm 
      v-if="view === 'login'" 
      @login-success="setUser" 
      @change-view="view = $event" 
    />
    <RegisterForm 
      v-if="view === 'register'" 
      @register-success="setUser" 
      @change-view="view = $event" 
    />
    <Dashboard 
      v-if="view === 'dashboard'" 
      :user="user" 
      @logout="logout" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
import Dashboard from './Dashboard.vue'

const view = ref('login')
const user = ref(null)

function setUser(u) {
  user.value = u
  view.value = 'dashboard'
}

function logout() {
  user.value = null
  view.value = 'login'
}
</script>
