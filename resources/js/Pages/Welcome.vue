<script setup>
import { Head, Link } from '@inertiajs/vue3';

defineProps({
    canLogin: Boolean,
    canRegister: Boolean,
});
</script>

<template>
    <Head title="Bienvenido" />

    <div class="min-h-screen bg-gray-50 text-gray-800 relative overflow-hidden flex flex-col">
        
        <nav class="flex justify-between items-center px-8 py-6 max-w-7xl mx-auto w-full z-20">
            <div class="font-bold text-2xl tracking-tighter text-blue-900 flex items-center gap-2">
                <span class="w-3 h-3 bg-blue-600 rounded-full"></span>
                Mini-JFLAP
            </div>
            <div v-if="canLogin" class="flex gap-4">
                <Link v-if="$page.props.auth.user" :href="route('automatas.index')" 
                      class="font-semibold text-gray-600 hover:text-gray-900">
                    Ir al Dashboard
                </Link>
            </div>
        </nav>

        <main class="flex-1 flex flex-col justify-center items-center text-center px-4 relative z-10 mt-[-50px]">
            
            <div class="mb-6 inline-flex items-center px-3 py-1 rounded-full border border-blue-200 bg-blue-50 text-blue-600 text-xs font-medium uppercase tracking-wide">
                <span>Versión Beta 1.0</span>
            </div>

            <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-6 max-w-4xl">
                Diseña, Prueba y Simula <br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                    Autómatas Finitos
                </span>
            </h1>

            <p class="text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
                Una herramienta universitaria simplificada para crear DFAs y NFAs. 
                Visualiza grafos, prueba cadenas y exporta tus modelos en JSON.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center w-full">
                <Link :href="route('register')" 
                      class="px-8 py-4 bg-blue-600 text-white rounded-xl font-bold text-lg hover:bg-blue-700 transition shadow-xl shadow-blue-600/20 w-full sm:w-auto">
                    Comenzar Ahora 🚀
                </Link>
                <Link :href="route('login')" 
                      class="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-xl font-bold text-lg hover:bg-gray-50 transition w-full sm:w-auto">
                    Ya tengo cuenta
                </Link>
            </div>

            <div class="mt-16 relative w-full max-w-4xl h-64 opacity-60">
                <div class="absolute top-10 left-1/4 w-16 h-16 rounded-full border-4 border-gray-300 bg-white z-10 flex items-center justify-center font-mono text-gray-400">q0</div>
                <div class="absolute top-20 right-1/3 w-16 h-16 rounded-full border-4 border-blue-500 bg-blue-50 z-10 flex items-center justify-center font-mono text-blue-600 font-bold">q1</div>
                <div class="absolute top-40 left-1/2 w-16 h-16 rounded-full border-4 border-gray-300 bg-white z-10 flex items-center justify-center font-mono text-gray-400">q2</div>
                
                <svg class="absolute inset-0 w-full h-full pointer-events-none">
                    <path d="M320 70 Q 550 20, 700 110" stroke="#cbd5e1" stroke-width="2" fill="none" stroke-dasharray="8 8"/>
                    <path d="M700 110 Q 600 200, 520 190" stroke="#cbd5e1" stroke-width="2" fill="none"/>
                </svg>
            </div>
        </main>

        <footer class="py-6 text-center text-gray-400 text-sm">
            Proyecto de Licenciatura en Informática &copy; 2025
        </footer>
    </div>
</template>