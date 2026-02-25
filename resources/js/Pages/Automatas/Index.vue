<template>
    <AuthenticatedLayout>
        <div class="min-h-screen bg-gray-50/50">

            <div class="bg-white border-b border-gray-200 relative overflow-hidden">
                <div class="absolute inset-0 opacity-[0.03]"
                    style="background-image: radial-gradient(#4f46e5 1px, transparent 1px); background-size: 20px 20px;">
                </div>

                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 relative z-10">
                    <div class="flex flex-col md:flex-row justify-between items-center gap-6">

                        <div>
                            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">
                                Mis Proyectos
                            </h1>
                            <p class="mt-2 text-gray-500">
                                Gestiona, edita y simula tus autómatas finitos.
                            </p>
                        </div>

                        <div class="flex items-center gap-3">
                            <button @click="triggerImport"
                                class="inline-flex items-center px-5 py-2.5 bg-white border border-gray-300 rounded-xl font-semibold text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition shadow-sm">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-400" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                </svg>
                                Importar JSON
                            </button>

                            <input type="file" ref="fileInput" class="hidden" accept=".json"
                                @change="handleFileUpload" />

                            <Link :href="route('automatas.create')"
                                class="inline-flex items-center px-5 py-2.5 bg-blue-600 border border-transparent rounded-xl font-bold text-white hover:bg-blue-700 transition shadow-lg shadow-blue-600/20">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 4v16m8-8H4" />
                                </svg>
                                Nuevo Autómata
                            </Link>
                        </div>
                    </div>
                </div>
            </div>

            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

                <div v-if="automatas.data && automatas.data.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

    <Link v-for="aut in automatas.data" :key="aut.id" :href="route('automatas.show', aut.id)"
                        class="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 relative overflow-hidden">
                        <div
                            class="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">
                        </div>

                        <div class="flex justify-between items-start mb-4">
                            <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-colors"
                                :class="aut.tipo === 'DFA' ? 'bg-purple-50 text-purple-600 group-hover:bg-purple-100' : 'bg-orange-50 text-orange-600 group-hover:bg-orange-100'">
                                <span class="font-bold text-sm tracking-tighter">{{ aut.tipo }}</span>
                            </div>

                            <div class="flex justify-between items-start mb-4">


                                <div class="flex items-center gap-1 z-20 relative" @click.prevent>

                                    <Link :href="route('automatas.edit', aut.id)"
                                        class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                                        title="Editar">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                                            fill="currentColor">
                                            <path
                                                d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                        </svg>
                                    </Link>

                                    <button @click="deleteAutomata(aut)"
                                        class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                                        title="Eliminar">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                                            fill="currentColor">
                                            <path fill-rule="evenodd"
                                                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                                                clip-rule="evenodd" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <h3 class="text-xl font-bold text-gray-800 group-hover:text-blue-600 transition mb-2 truncate">
                            {{ aut.nombre }}
                        </h3>

                        <div class="flex items-center gap-4 text-sm text-gray-500">
                            <span class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z">
                                    </path>
                                </svg>
                                {{ aut.json_definicion?.estados?.length || 0 }} Estados
                            </span>
                            <span class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                                {{ aut.json_definicion?.alfabeto?.length || 0 }} Símbolos
                            </span>
                        </div>
                        

                    </Link>
                </div>

                <div v-else class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
                    <div class="mx-auto w-24 h-24 bg-blue-50 rounded-full flex items-center justify-center mb-6">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-500" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900">No tienes autómatas aún</h3>
                    <p class="mt-1 text-gray-500 max-w-sm mx-auto mb-6">
                        Comienza creando tu primer diagrama de estados o importa un archivo JSON existente.
                    </p>
                    <Link :href="route('automatas.create')"
                        class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition shadow">
                        Crear mi primer autómata
                    </Link>
                </div>

            </div>
                                <div v-if="automatas.links && automatas.links.length > 3" class="mt-12 flex justify-center items-center gap-2">
                    <template v-for="(link, index) in automatas.links" :key="index">
                        <div v-if="link.url === null"
                            class="px-4 py-2 text-sm text-gray-400 border border-gray-200 rounded-lg bg-gray-50 cursor-not-allowed"
                            v-html="link.label">
                        </div>
                        <Link v-else
                            :href="link.url"
                            class="px-4 py-2 text-sm font-medium border rounded-lg transition-colors shadow-sm"
                            :class="link.active 
                                ? 'bg-blue-600 text-white border-blue-600 ring-2 ring-blue-200' 
                                : 'bg-white text-gray-700 border-gray-200 hover:bg-blue-50 hover:text-blue-600'"
                            v-html="link.label">
                        </Link>
                    </template>
                </div>
        </div>
    </AuthenticatedLayout>
</template>

<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { Link, router } from '@inertiajs/vue3';
import { ref } from 'vue';

defineProps({
    automatas: Array
});

// --- LÓGICA DE IMPORTACIÓN (Reutilizada) ---
const fileInput = ref(null);

function triggerImport() {
    fileInput.value.click();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const contenido = JSON.parse(e.target.result);

            // --- LÓGICA DE DETECCIÓN INTELIGENTE (Frontend) ---
            let definicionReal;
            let tipoAutomata = 'DFA';
            let nombreAutomata = file.name.replace('.json', '');

            // CASO 1: Formato Nuevo (Exportado correctamente con tipo)
            if (contenido.json_definicion) {
                definicionReal = contenido.json_definicion;
                tipoAutomata = contenido.tipo || 'DFA';
                nombreAutomata = contenido.nombre || nombreAutomata;
            }
            // CASO 2: Formato Viejo (El JSON es la definición pura)
            else {
                definicionReal = contenido;
                // Si es viejo, asumimos DFA
            }

            // --- VALIDACIÓN ---
            // Ahora validamos sobre la definición real extraída
            // Nota: En tu JSON de ejemplo usas "transiciones", asegúrate si es "enlaces" o "transiciones" en tu código gráfico
            if (!definicionReal.estados || (!definicionReal.transiciones && !definicionReal.enlaces)) {
                alert('Archivo inválido: No se detecta estructura de autómata.');
                return;
            }

            // --- ENVÍO AL STORE ---
            router.post(route('automatas.store'), {
                nombre: nombreAutomata,
                tipo: tipoAutomata, // ¡Ahora sí mandamos NFA o PDA!
                json_definicion: definicionReal
            });

        } catch (error) {
            console.error(error);
            alert('Error al leer el JSON: ' + error.message);
        } finally {
            event.target.value = ''; // Limpiar input
        }
    };
    reader.readAsText(file);
}
function deleteAutomata(aut) {
    if (confirm(`¿Estás seguro de que querés eliminar "${aut.nombre}"?`)) {
        router.delete(route('automatas.destroy', aut.id));
    }
}
</script>