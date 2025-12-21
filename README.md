<div align="center">

  <h1>🧠 Simulador de Autómatas y Lenguajes Formales</h1>
  
  <p>
    <strong>Diseño, simulación y persistencia de Autómatas Finitos (DFA/NFA) y de Pila (PDA).</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white" alt="Laravel" />
    <img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  </p>

  <p>
    <a href="#-características">Características</a> •
    <a href="#-fundamentos-teóricos">Teoría</a> •
    <a href="#-instalación">Instalación</a> •
    <a href="#-uso">Uso</a>
  </p>
  
  </div>

<br>

## 📖 Descripción

Esta aplicación web permite a estudiantes y profesores de Teoría de la Computación crear, editar, almacenar y simular el comportamiento de máquinas de estados. El sistema resuelve la complejidad de visualizar y persistir estructuras matemáticas abstractas mediante una interfaz gráfica interactiva y un backend robusto.

El proyecto destaca por su capacidad de manejar **polimorfismo en la definición de autómatas**, soportando desde máquinas simples (DFA) hasta modelos con memoria auxiliar (Pila), garantizando la integridad de los datos mediante validaciones estrictas y algoritmos de importación inteligentes.

## 🚀 Características

* **Editor Gráfico Interactivo:** Creación de estados y transiciones mediante "Drag & Drop".
* **Soporte Multitipo:**
    * 🔵 **DFA:** Autómata Finito Determinista.
    * 🟠 **NFA:** Autómata Finito No Determinista (con soporte para transiciones $\lambda$).
    * 🟣 **PDA:** Autómata de Pila (con gestión visual de operaciones `Pop` y `Push`).
* **Simulación de Cadenas:** Algoritmo de recorrido paso a paso para validar la aceptación o rechazo de hileras de entrada.
* **Sistema de Archivos JSON Inteligente:**
    * Exportación de definiciones completas con metadatos.
    * **Importación Híbrida:** Capacidad de leer archivos "Legacy" (antiguos) y convertirlos al nuevo estándar automáticamente.
    * Validación de estructura en cliente y servidor.
* **Gestión de Proyectos:** Dashboard privado para administrar mis autómatas con opciones de visibilidad.

## 📚 Fundamentos Teóricos

Este software implementa conceptos clave de la jerarquía de lenguajes:

1.  **Jerarquía de Chomsky:** Soporte para lenguajes Regulares (Tipo 3) y Libres de Contexto (Tipo 2).
2.  **Teorema de Kleene:** Equivalencia práctica entre las representaciones visuales y las expresiones regulares subyacentes.
3.  **Equivalencia AFD/AFND:** El sistema permite modelar el no determinismo, demostrando computacionalmente que todo NFA tiene un DFA equivalente.
4.  **Memoria LIFO:** Implementación visual de la pila para demostrar el reconocimiento de lenguajes como $a^n b^n$.

## 🛠️ Instalación y Configuración

Sigue estos pasos para desplegar el proyecto en tu entorno local:

### Prerrequisitos
* PHP >= 8.1
* Composer
* Node.js & NPM
* MySQL

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
    cd nombre-del-repo
    ```

2.  **Instalar dependencias de Backend:**
    ```bash
    composer install
    ```

3.  **Instalar dependencias de Frontend:**
    ```bash
    npm install
    ```

4.  **Configurar variables de entorno:**
    ```bash
    cp .env.example .env
    # Configura tus credenciales de base de datos en el archivo .env
    ```

5.  **Generar key y migrar base de datos:**
    ```bash
    php artisan key:generate
    php artisan migrate
    ```

    > **Nota:** La migración configura la columna `tipo` para aceptar 'DFA', 'NFA' y 'PDA'.

6.  **Ejecutar la aplicación:**
    En una terminal:
    ```bash
    php artisan serve
    ```
    En otra terminal:
    ```bash
    npm run dev
    ```

## 💾 Exportación e Importación (Detalles Técnicos)

El sistema utiliza un formato JSON estandarizado para la portabilidad:

```json
{
  "nombre": "Ejemplo Pila",
  "tipo": "PDA",
  "json_definicion": {
    "estados": ["q0", "q1"],
    "transiciones": { ... }
  }
}