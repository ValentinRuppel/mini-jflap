# Changelog

Todos los cambios notables de **FLEXA** se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [2.1.0] - 2026-11-23

### Agregado
- **Modo de Experimento Estadístico Comparativo ($N$ corridas independientes)** entre *Simulated Annealing* (SA) y *Algoritmo Genético* (GA), con cálculo no paramétrico en Python puro (media $\bar{x}$, desviación estándar $\sigma$, cuartiles $Q_1, Q_2, Q_3$, rango intercuartílico $RIC$ y detección de outliers por regla de Tukey $1.5 \times RIC$), gráficos Boxplot en SVG, Test bilateral de **Wilcoxon Rank-Sum / Mann-Whitney U** ($\alpha = 0.05$) con corrección por empates y descarga del reporte completo en JSON.
- **`AutomataDemoSeeder`** con 6 autómatas de demostración precargados (2 DFA, 2 NFA y 2 AP) asignados automáticamente al usuario existente o a un usuario demo inicial (`demo@flexa.edu`).
- **Bloqueo informativo en la UI para Autómatas de Pila (`AP`):** deshabilita la minimización y el experimento comparativo indicando que la equivalencia general de AP es indecidible en la teoría de lenguajes formales.

### Corregido
- **Calibración de hiperparámetros y caché de evaluaciones en `ai_module/optimizer.py`:** se ajustó `AnnealingOptimizer` ($T_0 = 2.0$, $\alpha = 0.92$, $T_{\min} = 0.05$, caché de `f_actual`/`f_mejor`) para reflejar el comportamiento rápido de trayectoria única, y `GeneticOptimizer` (población inicial diversa de 16 individuos, 25 generaciones y operador de cruce basado en fusiones válidas compatibles) para reflejar mayor exploración poblacional y robustez.
- Incorporación de métricas de **evaluaciones del oráculo** y **mejor iteración/generación** en el reporte individual de optimización.
- Corrección tipográfica en la tabla de estadísticos descriptivos para mostrar `(σ)` y `(x̄)` en minúscula.

### Mejorado
- **Rendimiento de navegación:** cambio de drivers de sesión y caché a `file`, consulta ligera en `AutomataPageController@index` (sin cargar blobs `json_definicion`), eliminación del doble montaje en `app.js`, habilitación de `prefetch` en `<Link>` de Inertia y compilación de bundle estático de producción con Vite.
- **Traducción completa al español** de todas las vistas de autenticación (`Login`, `Register`, `ForgotPassword`, `ResetPassword`, `ConfirmPassword`, `VerifyEmail`) y layouts de navegación.

## [2.0.0]

### Agregado
- Incorporación inicial del módulo de optimización IA en Python (`ai_module/optimizer.py`) con **Algoritmo Genético** y **Simulated Annealing**, integración vía `Symfony\Component\Process` en Laravel y modal de reporte de resultados en Vue/Inertia.
