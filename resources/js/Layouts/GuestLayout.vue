<script setup>
import { Link } from '@inertiajs/vue3';
</script>

<template>
    <div class="min-h-screen flex flex-col sm:justify-center items-center pt-6 sm:pt-0 bg-[#f8fafc] relative overflow-hidden">
        
        <div class="absolute inset-0 z-0 opacity-10" 
             style="background-image: radial-gradient(#4f46e5 1px, transparent 1px); background-size: 24px 24px;">
        </div>

        <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

        <div class="w-full sm:max-w-md mt-6 px-6 py-8 bg-white shadow-2xl overflow-hidden sm:rounded-2xl z-10 border border-gray-100 relative">
            
            <div class="flex flex-col items-center mb-6">
                <Link href="/">
                    <div class="w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg mb-4 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                    </div>
                </Link>
                <h2 class="text-2xl font-bold text-gray-800 tracking-tight">Mini-JFLAP</h2>
                <p class="text-sm text-gray-500 mt-1">Tu laboratorio de autómatas</p>
            </div>

            <slot />
        </div>

        <div class="mt-8 text-center text-xs text-gray-400 z-10">
            &copy; 2025 Facultad de Informática
        </div>
    </div>
</template>

<style scoped>
/* Animación suave para las manchas de fondo */
@keyframes blob {
    0% { transform: translate(0px, 0px) scale(1); }
    33% { transform: translate(30px, -50px) scale(1.1); }
    66% { transform: translate(-20px, 20px) scale(0.9); }
    100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
    animation: blob 7s infinite;
}
.animation-delay-2000 {
    animation-delay: 2s;
}
</style>