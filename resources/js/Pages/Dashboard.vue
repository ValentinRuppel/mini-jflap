<template>
  <AuthenticatedLayout>
    <template #header>
      <h2 class="font-semibold text-xl text-gray-800 leading-tight">Dashboard</h2>
    </template>

    <div class="py-12">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
        <div class="p-6 bg-white shadow sm:rounded-lg">
          <p>Bienvenido, estás logueado.</p>
          <a
            href="/automatas"
            class="inline-block mt-4 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
          >
            Ir a mis autómatas
          </a>
        </div>
      </div>
    </div>
  </AuthenticatedLayout>
</template>

<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue'
</script>
