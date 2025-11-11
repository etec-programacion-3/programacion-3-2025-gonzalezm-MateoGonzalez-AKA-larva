Guía de Instalación y Ejecución 

PROFE TENEME PIEDAD PORFA 🙏🙏🙏

Ejecutar el proyecto requiere dos terminales.

Paso 1: Clonar el Repositorio


git clone https://github.com/etec-programacion-3/programacion-3-2025-gonzalezm-MateoGonzalez-AKA-larva.git
cd AAMATEO

(Todos los comandos subsecuentes asumen que se ejecutan desde la carpeta programacion-3-2025-gonzalezm-MateoGonzalez-AKA-larva o sus subcarpetas).

Paso 2: Configurar y Ejecutar el Backend (Terminal 1)

1. Crear Entorno Virtual (venv)

python3 -m venv venv

2. Activar el Entorno Virtual (Linux/macOS)

source venv/bin/activate

3. Instalar Dependencias de Python

pip install fastapi uvicorn sqlalchemy python-jose "passlib[bcrypt]" bcrypt

4. Iniciar el Servidor Backend

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Nota: Al iniciar, el backend creará el archivo de base de datos products.db en la carpeta raíz del proyecto.

Dejar esta terminal corriendo.

Paso 3: Configurar y Ejecutar el Frontend (Terminal 2)

Abrir una segunda terminal.

1. Navegar a la Carpeta del Frontend

cd frontend

2. Instalar Dependencias de Node.js

npm install

3. Iniciar el Servidor de Desarrollo

npm run dev

Dejar esta terminal corriendo.

Paso 4: Configuración de Red (Requerido)

El frontend debe apuntar a la dirección IP del backend, no a localhost.

1. Obtener la IP de la máquina (Servidor Backend) En la Terminal 1 (Linux/macOS), ejecutar:

ip addr show

Identificar la dirección IP de la red local (ej: 192.168.46.11).

2. Configurar el Frontend Editar los siguientes archivos en frontend/src/ y reemplazar http://localhost:8000 por la IP obtenida (ej: http://192.168.46.11:8000).

    frontend/src/utils/api.js

    frontend/src/context/AuthContext.jsx

Paso 5: Acceder a la Aplicación

Con ambos servidores corriendo y la IP configurada, la aplicación es accesible desde cualquier dispositivo en la misma red.

    URL de Acceso (Frontend): http://<TU_IP_DE_RED>:5173 (Ej: http://192.168.46.11:5173)

    URL de API (Backend Docs): http://<TU_IP_DE_RED>:8000/docs (Ej: http://192.168.46.11:8000/docs)

Primeros Pasos

    Abrir la URL del frontend en un navegador.

    El sistema redirige a /login.

    Hacer clic en "Regístrate aquí" para crear un usuario.

    Iniciar sesión con las credenciales creadas.

    Acceder al dashboard de productos.

activar el entorno virtual: source venv/bin/activate
levanatr el servidor (backend):  ./venv/bin/uvicorn backend.main:app --reload 
levantar el frontend: npm run dev
swagger: http://127.0.0.1:8000/docs
frontend: http://localhost:5173/
