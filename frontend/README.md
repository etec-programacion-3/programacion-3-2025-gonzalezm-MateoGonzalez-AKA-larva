Proyecto de Gestión de Stock (Full-Stack)

Este es un sistema integral de gestión de stock, construido con un backend de FastAPI (Python) y un frontend de React (JavaScript).

El sistema permite la autenticación de usuarios, la gestión de productos (CRUD completo) y el registro de movimientos de inventario (entradas y salidas).

Requisitos Previos

    Git

    Python 3.10+

    Node.js 18.x+ (LTS)

    npm

Guía de Instalación y Ejecución

Para ejecutar el proyecto, necesitarás abrir dos terminales por separado.

Paso 1: Clonar el Repositorio

"git clone https://github.com/etec-programacion-3/programacion-3-2025-gonzalezm-MateoGonzalez-AKA-larva.git
cd AAMATEO"

(Todos los comandos asumen que estás en la carpeta raíz AAMATEO o sus subcarpetas).

Paso 2: Configurar y Ejecutar el Backend (Terminal 1)

1. Crear un Entorno Virtual (venv)

"python3 -m venv venv"


2. Activar el Entorno Virtual (Linux/macOS)

"source venv/bin/activate"


3. Instalar Dependencias de Python

"pip install fastapi uvicorn sqlalchemy python-jose "passlib[bcrypt]" bcrypt"


4. Iniciar el Servidor Backend

"python -m uvicorn backend.main:app --reload --port 8000"

Nota: Al iniciar, el backend creará el archivo de base de datos products.db en la carpeta raíz del proyecto.

Dejar esta terminal corriendo.


Paso 3: Configurar y Ejecutar el Frontend (Terminal 2)

Abrir una segunda terminal.

1. Navegar a la Carpeta del Frontend

"cd frontend"


2. Instalar Dependencias de Node.js

"npm install"


3. Iniciar el Servidor de Desarrollo

"npm run dev"

Dejar esta terminal corriendo.

Acceder a la Aplicación


URLs de Acceso

    Frontend (Aplicación Web): http://localhost:5173

    Backend (Documentación API): http://127.0.0.1:8000/docs

    Backend (API): http://127.0.0.1:8000

Primeros Pasos

    Abre http://localhost:5173 en tu navegador.

    Serás redirigido a la página de Login.

    Haz clic en el enlace "Regístrate aquí" para crear una cuenta.

    Inicia sesión con tus nuevas credenciales.

    Podrás ver, crear, editar y eliminar productos.