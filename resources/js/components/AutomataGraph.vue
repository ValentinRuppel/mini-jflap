<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Grafo del Autómata</h2>
    <div ref="cyContainer" class="border w-full h-[400px]"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import cytoscape from 'cytoscape';

const props = defineProps({
  jsonDefinicion: { type: Object, required: true }
});

const cyContainer = ref(null);
let cyInstance = null;

function renderGraph() {
  if (!props.jsonDefinicion) return;

  // Limpiar si ya hay un grafo
  if (cyInstance) {
    cyInstance.destroy();
  }

  const nodes = props.jsonDefinicion.estados.map((estado) => ({
    data: { id: estado, label: estado },
    classes: [
      estado === props.jsonDefinicion.estado_inicial ? 'initial' : '',
      props.jsonDefinicion.estados_finales.includes(estado) ? 'final' : ''
    ].join(' ')
  }));

  const edges = [];
  for (const [origen, trans] of Object.entries(props.jsonDefinicion.transiciones)) {
    for (const [simbolo, destino] of Object.entries(trans)) {
      edges.push({
        data: { source: origen, target: destino, label: simbolo }
      });
    }
  }

  cyInstance = cytoscape({
    container: cyContainer.value,
    elements: { nodes, edges },
    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#4f46e5',
          'label': 'data(label)',
          'text-valign': 'center',
          'color': '#fff',
          'text-outline-width': 2,
          'text-outline-color': '#4f46e5'
        }
      },
      {
        selector: 'node.initial',
        style: {
          'background-color': '#22c55e'
        }
      },
      {
        selector: 'node.final',
        style: {
          'border-width': 3,
          'border-color': '#f59e0b'
        }
      },
      {
        selector: 'edge',
        style: {
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'label': 'data(label)',
          'font-size': 12,
          'text-background-color': '#fff',
          'text-background-opacity': 1,
          'text-background-padding': 2
        }
      }
    ],
    layout: {
      name: 'circle'
    }
  });
}

onMounted(renderGraph);

// Redibujar si cambian los datos
watch(() => props.jsonDefinicion, renderGraph, { deep: true });
</script>

<style scoped>
/* Ajuste visual */
div[ref="cyContainer"] {
  min-height: 400px;
}
</style>
