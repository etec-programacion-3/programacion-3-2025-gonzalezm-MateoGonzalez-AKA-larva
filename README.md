Proyecto Full-Stack: Gestión de Stock

1. Descripción del Proyecto

Este proyecto implementa un sistema integral de gestión de inventario (CRUD de productos) con autenticación de usuarios.

La arquitectura es Full-Stack:

    Backend: API REST construida con FastAPI (Python).

    Frontend: Interfaz de usuario reactiva construida con React y Vite.

2. Requisitos Previos

    Git

    Python 3.10+

    Node.js 18.x+ (LTS)

    npm (incluido con Node.js)

3. Instrucciones de Ejecución (Paso a Paso)

La ejecución del proyecto requiere dos terminales activas simultáneamente.

Paso 1: Clonar el Repositorio

Bash

git clone https://github.com/etec-programacion-3/programacion-3-2025-gonzalezm-MateoGonzalez-AKA-larva.git
cd AAMATEO

Paso 2: Ejecutar el Backend (Terminal 1)

2.1. Dependencias y Entorno Virtual

Bash

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual (Linux/macOS)
source venv/bin/activate

# Instalar dependencias de Python
pip install fastapi uvicorn sqlalchemy python-jose "passlib[bcrypt]" bcrypt python-multipart

2.2. Base de Datos (SQLite)

Este proyecto utiliza SQLite (una base de datos basada en archivos).

    No se requiere docker-compose ni un servidor de base de datos externo.

    El archivo products.db (que contiene todas las tablas, incluidos los usuarios) se creará automáticamente en la raíz del proyecto (AAMATEO/) al ejecutar el siguiente paso.

2.3. Configurar Clave Secreta (¡CRÍTICO!)

El backend requiere una SECRET_KEY para firmar los tokens de autenticación. Esta variable debe ser configurada antes de iniciar el servidor.

A. Generar una clave (Recomendado): (Ejecuta esto para obtener una clave aleatoria. No necesitas memorizarla, solo guárdala en un lugar seguro para reutilizarla).
Bash

openssl rand -hex 32

B. Establecer la variable de entorno: (Reemplaza <TU_CLAVE_GENERADA> con la clave que acabas de generar o la que hayas elegido).
Bash

export SECRET_KEY="<TU_CLAVE_GENERADA>"

2.4. Iniciar Servidor Backend

Ahora sí, inicia el servidor. El host 0.0.0.0 es requerido para aceptar conexiones desde otras máquinas de la red.
Bash

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Dejar esta terminal en ejecución.

Paso 3: Ejecutar el Frontend (Terminal 2)

Abrir una segunda terminal.

3.1. Dependencias de Node.js

Bash

cd frontend
npm install

3.2. Configuración de Variables de Entorno (API URL)

El frontend necesita saber la dirección IP del backend.

A. Obtener la IP del Backend: En la Terminal 1 (donde corre el backend), obtén la IP de la red local:
Bash

ip addr show

(Identifica la IP de tu interfaz de red principal, ej: 192.168.46.11)

B. Configurar la Variable de Entorno: En la Terminal 2 (dentro de frontend/), reemplaza <TU_IP_DE_RED> con la IP real del paso anterior:
Bash

# Configurar la URL de la API REST (Linux/macOS)
export VITE_API_BASE_URL=http://<TU_IP_DE_RED>:8000

3.3. Iniciar Servidor Frontend

Bash

npm run dev

Dejar esta terminal en ejecución.

Paso 4: Configuración de Red Adicional (Firewall)

Si el frontend (desde otra PC) no puede conectarse (Error CORS con Status code: (null)), el firewall del backend (PC Servidor) está bloqueando el puerto 8000.

Solución (Linux/ufw): En la Terminal 1 (servidor Backend), ejecuta:
Bash

sudo ufw allow 8000

4. Acceso a la Aplicación

Con ambos servidores activos y configurados:

    Acceso Frontend (App): http://<TU_IP_DE_RED>:5173

    Acceso Backend (Docs): http://<TU_IP_DE_RED>:8000/docs

Primeros Pasos:

    Accede a la URL del Frontend.

    Usa el enlace "Regístrate aquí" para crear un usuario.

    Inicia sesión.

5. Pruebas del Backend (con REST Client)

Este proyecto incluye un archivo requests.http para probar la API del backend directamente.

    Asegúrate de que el backend (Paso 2) esté corriendo.

    Instala la extensión "REST Client" en VS Code.

    Abre el archivo requests.http (ubicado en la raíz del proyecto).

    Haz clic en "Send Request" sobre cada petición, en orden (primero "Registrar", luego "Iniciar sesión", y finalmente las rutas CRUD). El token se manejará automáticamente.

activar el entorno virtual: source venv/bin/activate
levanatr el servidor (backend): ./venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
levantar el frontend: npm run dev
swagger: http://127.0.0.1:8000/docs
frontend: http://localhost:5173/
