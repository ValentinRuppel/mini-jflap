<div align="center">

  <h1>🧠 FLEXA — Simulador y Optimizador de Autómatas</h1>

  <p>
    <strong>Diseño, simulación, optimización metaheurística y análisis estadístico de Autómatas Finitos (DFA/NFA) y de Pila (AP).</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Versión-v2.1.0-6366F1?style=for-the-badge" alt="Versión v2.1.0" />
    <img src="https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white" alt="Laravel" />
    <img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  </p>

  <p>
    <a href="#-características">Características</a> •
    <a href="#-novedades--changelog">Novedades (v2.1.0)</a> •
    <a href="#-fundamentos-teóricos">Teoría</a> •
    <a href="#-instalación-y-configuración">Instalación</a>
  </p>

</div>

<br>

## 📖 Descripción

**FLEXA** es una aplicación web que permite a estudiantes y docentes de Teoría de la Computación e Inteligencia Artificial crear, visualizar, simular, optimizar y comparar máquinas de estados. Combina una interfaz interactiva en **Vue 3 + Inertia.js + vis-network**, un backend en **Laravel 12** y un motor de optimización metaheurística y análisis estadístico en **Python**.

## ✨ Novedades / Changelog

La versión **v2.1.0** incorpora:
* **Experimento Estadístico Comparativo ($N$ corridas):** comparación rigurosa entre *Simulated Annealing* y *Algoritmo Genético* con estadísticos no paramétricos ($\bar{x}$, $\sigma$, $Q_1$, Mediana, $Q_3$, $RIC$, outliers por Tukey), gráficos **Boxplot en SVG**, **Test de Wilcoxon Rank-Sum** ($\alpha = 0.05$) y exportación de datos crudos en JSON.
* **Algoritmos recalibrados:** SA de trayectoria única rápido ($T_0=2.0, \alpha=0.92$) vs. GA poblacional con población inicial diversa y cruce por fusiones válidas, además de conteo de evaluaciones del oráculo y mejor iteración/generación.
* **Seeders de demostración y rigor teórico:** 6 autómatas precargados (`AutomataDemoSeeder`: 2 DFA, 2 NFA y 2 AP) y bloqueo explicativo en la UI para AP por indecidibilidad de equivalencia general.
* **UI en español y navegación acelerada:** vistas de autenticación/navegación traducidas, `prefetch` en Inertia, consultas ligeras y bundle de producción con Vite.

Consultá el historial completo de cambios en [CHANGELOG.md](./CHANGELOG.md).

## 🚀 Características

* **Visualizador Gráfico Interactivo:** Representación de estados y transiciones con `vis-network`.
* **Soporte Multitipo:**
    * 🔵 **DFA:** Autómata Finito Determinista.
    * 🟠 **NFA:** Autómata Finito No Determinista.
    * 🟢 **AP:** Autómata de Pila (con gestión visual de operaciones `Pop` y `Push`).
* **Simulación de Cadenas:** Validación de aceptación/rechazo directamente en el navegador con traza de estados alcanzados.
* **Optimización Metaheurística (Python):** Reducción automática de estados en DFA/NFA con **Simulated Annealing** y **Algoritmo Genético**, y modo **Benchmark Comparativo** con validación no paramétrica.
* **Sistema de Archivos JSON:** Exportación e importación híbrida de definiciones completas y reportes estadísticos.

## 📚 Fundamentos Teóricos

1. **Jerarquía de Chomsky:** Soporte para Lenguajes Regulares (Tipo 3) y Libres de Contexto (Tipo 2).
2. **Equivalencia y Minimización:** Minimización aproximada mediante metaheurísticas guiadas por oráculo sobre DFA/NFA, respetando la indecidibilidad de equivalencia general en Autómatas de Pila (AP).
3. **Evaluación Experimental No Paramétrica:** Comparación de algoritmos estocásticos mediante cuartiles, diagramas de caja (Tukey $1.5 \times RIC$) y prueba bilateral de Wilcoxon Rank-Sum ($\alpha = 0.05$).

## 🛠️ Instalación y Configuración

### Opción A — Instalación rápida local (PHP 8.2+, Composer, Node.js, Python 3 y MySQL/SQLite)

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd mini-jflap
   ```
2. **Instalar dependencias:**
   ```bash
   composer install
   npm install
   ```
3. **Configurar entorno, base de datos y datos de demostración:**
   ```bash
   cp .env.example .env
   php artisan key:generate
   php artisan migrate
   php artisan db:seed
   ```
4. **Compilar frontend y levantar el servidor:**
   ```bash
   npm run build
   php artisan serve
   ```
   *(Para desarrollo con hot-reload usá `npm run dev` en una segunda terminal.)*

### Opción B — Con Docker Desktop + Laravel Sail (WSL / Linux)

1. Configurar `.env` con `DB_CONNECTION=mysql`, `DB_HOST=mysql`, `DB_DATABASE=flexa`, `DB_USERNAME=sail`, `DB_PASSWORD=password` (y `SESSION_DRIVER=file`, `CACHE_STORE=file` para mejor rendimiento).
2. Levantar contenedores, migrar, cargar los autómatas demo y compilar el frontend:
   ```bash
   ./vendor/bin/sail up -d
   ./vendor/bin/sail artisan key:generate
   ./vendor/bin/sail artisan migrate
   ./vendor/bin/sail artisan db:seed
   ./vendor/bin/sail npm install
   ./vendor/bin/sail npm run build
   ```
3. Acceder a **http://localhost** *(usuario demo por defecto si la BD estaba vacía: `demo@flexa.edu` / `password`)*.

## 💾 Formato JSON de Autómatas

```json
{
  "nombre": "Ejemplo Pila",
  "tipo": "AP",
  "json_definicion": {
    "estados": ["q0", "q1"],
    "alfabeto": ["a", "b"],
    "estado_inicial": "q0",
    "estados_finales": ["q1"],
    "transiciones": { }
  }
}
```
