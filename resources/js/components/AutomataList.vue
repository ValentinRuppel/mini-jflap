<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Lista de Autómatas</h2>
    <ul class="space-y-2">
      <li v-for="a in automatas" :key="a.id"
          class="p-2 border rounded hover:bg-gray-100 cursor-pointer"
          @click="$emit('select-automata', a)">
        {{ a.nombre }} ({{ a.tipo }})
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const automatas = ref([]);

onMounted(async () => {
  const res = await axios.get('/api/automatas');
  automatas.value = res.data;
});
</script>
