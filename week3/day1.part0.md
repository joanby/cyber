# Día 1 Parte 0: Empezando con el Cybersecurity Analyzer

¡Bienvenido a la Semana 3 de IA en Producción! Durante los próximos dos días, desplegarás una aplicación de IA real tanto en Azure como en Google Cloud Platform. Al final del Día 2, tendrás experiencia práctica con prácticas modernas de despliegue en la nube utilizadas en entornos de producción.

## Qué vas a construir

El **Cybersecurity Analyzer** es una aplicación web potenciada por IA que analiza código Python buscando vulnerabilidades de seguridad. Combina:
- Los modelos más recientes de OpenAI para análisis inteligente de código
- Semgrep para escaneo de seguridad estático
- Un frontend en React/Next.js
- Un backend en FastAPI
- Contenerización con Docker
- Despliegue en la nube con Terraform

¡Esta es una arquitectura de aplicación real que verás en entornos de producción!

---

## Sección 1: Configuración del Proyecto

### Clona el Repositorio

Si aún no has clonado el repositorio, hazlo ahora:

```bash
git clone https://github.com/ed-donner/cyber.git
```

### Abrir en Cursor

1. Lanza Cursor
2. Haz clic en **Archivo** → **Nueva ventana**
3. Haz clic en **Abrir carpeta**
4. Navega y selecciona la carpeta `cyber` que acabas de clonar
5. Haz clic en **Abrir**

Ahora deberías ver la estructura del proyecto en el explorador de archivos de Cursor, a la izquierda.

Tómate un momento para explorar la estructura:
- `frontend/` - Aplicación React con Next.js
- `backend/` - Servidor Python con FastAPI
- `terraform/` - Configuraciones de Infraestructura como Código
- `week3/` - ¡Estas guías que estás leyendo!

---

## Sección 2: Configuración de Semgrep

Semgrep es una herramienta poderosa de análisis estático que encuentra vulnerabilidades de seguridad en el código. Vamos a configurar tu cuenta y obtener un token API.

### Crea tu cuenta de Semgrep

1. Visita https://semgrep.dev
2. Haz clic en **"Try Semgrep for free"** 
3. Haz clic en **"Continue with GitHub"**
4. Autoriza a Semgrep para que se conecte con tu cuenta de GitHub

### Genera tu token API

Una vez dentro de Semgrep:

1. Haz clic en **Settings** (abajo a la izquierda del panel)
2. En la navegación principal, haz clic en **Tokens**
3. Haz clic en **"Create New Token"**
4. Configura el token:
   - **Name**: `cyber-analyzer` (o cualquier nombre que prefieras)
   - **Scopes**: Marca ambas:
     - ✅ **Agent (CI)**
     - ✅ **Web API**
5. Haz clic en **"Create"**
6. **IMPORTANTE**: ¡Copia el token inmediatamente! No podrás verlo de nuevo.
   - Se verá algo como: `eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...`

Guarda este token a mano, lo necesitarás en la próxima sección.

---

## Sección 3: Configuración de Entorno

Ahora crea tu archivo `.env` con las claves API necesarias.

### Crea el archivo .env

1. En Cursor, haz clic derecho sobre la raíz del proyecto (la carpeta `cyber` en el explorador)
2. Selecciona **"Nuevo archivo"**
3. Nómbralo exactamente `.env` (sí, empezando con un punto)
4. Agrega el siguiente contenido:

```
OPENAI_API_KEY=your-openai-key-here
SEMGREP_APP_TOKEN=your-semgrep-token-here
```

5. Reemplaza los valores de ejemplo:
   - `your-openai-key-here` - Tu API key de OpenAI de semanas anteriores
   - `your-semgrep-token-here` - El token de Semgrep que acabas de crear
6. Guarda el archivo (`Cmd+S` en Mac, `Ctrl+S` en Windows/Linux)

⚠️ **Nota de Seguridad**: El archivo `.env` ya está en `.gitignore`, así que no se subirá a Git. ¡Nunca compartas estas claves públicamente!

### Verifica tus claves

Tu archivo `.env` debería verse similar a esto (pero con tus claves reales):
```
OPENAI_API_KEY=sk-proj-abc123xyz...
SEMGREP_APP_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## Sección 4: Prueba localmente sin Docker

Verifiquemos que todo funcione ejecutando la aplicación localmente.

### Verifica los prerrequisitos

Primero, asegúrate de tener las herramientas necesarias:

```bash
# Verifica Node.js (debería ser la versión 20 o superior)
node --version

# Verifica que uv está instalado (gestor de paquetes de Python)
uv --version
```

Si `uv` no está instalado:
```bash
# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (en PowerShell como administrador)
irm https://astral.sh/uv/install.ps1 | iex
```

### Inicia el servidor backend

Abre una terminal en Cursor (Terminal → Nueva Terminal) y ejecuta:

```bash
cd backend
uv run server.py
```

Deberías ver una salida similar a:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

La API del backend ahora está corriendo en http://localhost:8000

### Inicia el servidor de desarrollo del frontend

Abre **una nueva terminal** en Cursor (mantén el backend corriendo) y ejecuta:

```bash
cd frontend
npm install  # Sólo la primera vez
npm run dev
```

Deberías ver una salida como:
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Environments: .env

✓ Ready in 2.1s
```

### Prueba la aplicación

1. Abre tu navegador en http://localhost:3000
   
   **Importante**: Usa la URL `http://localhost:3000`, NO la Network URL que muestra Next.js. La aplicación está configurada para funcionar con localhost en modo desarrollo.

2. Deberías ver la interfaz de Cybersecurity Analyzer
3. Haz clic en **"Choose File"** y selecciona el archivo `airline.py` de la raíz del proyecto
   - Este archivo contiene vulnerabilidades de seguridad intencionadas para pruebas
4. Haz clic en **"Analyze Code"**
5. ¡Deberías ver múltiples vulnerabilidades de seguridad detectadas!

### Detener los servidores

Cuando termines de probar:
- Backend: presiona `Ctrl+C` en la terminal del backend
- Frontend: presiona `Ctrl+C` en la terminal del frontend

---

## Sección 5: Prueba con Docker

Ahora probemos la versión contenerizada, ¡exactamente lo que desplegaremos en la nube!

### Verifica los prerrequisitos

Asegúrate de tener Docker instalado y corriendo:

```bash
docker --version
docker ps  # No debería mostrar error
```

Si Docker no está instalado, descárgalo desde https://docker.com/get-started

### Construye la imagen de Docker

En una terminal en la raíz del proyecto:

```bash
docker build -t cyber-analyzer .
```

Esto tomará entre 2 y 5 minutos la primera vez, ya que:
- Descarga las imágenes base
- Instala dependencias de Python
- Construye el frontend de Next.js
- Empaqueta todo junto

Deberías ver una salida terminando así:
```
Successfully tagged cyber-analyzer:latest
```

### Ejecuta el contenedor

Inicia la aplicación contenerizada:

```bash
docker run --rm --name cyber-analyzer -p 8000:8000 --env-file .env cyber-analyzer
```

Desglose de este comando:
- `--rm`: Elimina el contenedor al detenerlo
- `--name cyber-analyzer`: Nombre fácil de referenciar
- `-p 8000:8000`: Mapea el puerto 8000
- `--env-file .env`: Carga variables de entorno
- `cyber-analyzer`: Nombre de la imagen

Verás los logs de inicio del servidor:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Prueba el contenedor

1. Abre http://localhost:8000 en tu navegador
2. Prueba subiendo el archivo `airline.py` desde la raíz del proyecto
3. Deberías ver los mismos resultados de análisis de seguridad que antes

### Detén el contenedor

Cuando termines de probar, presiona `Ctrl+C` en la terminal para detener el contenedor. Se eliminará automáticamente (por el flag `--rm`).

---

## Solución de problemas

### "Module not found" o errores de dependencias
- Asegúrate de usar `uv run` para el backend (no sólo `python`)
- Para el frontend, ejecuta `npm install` antes de `npm run dev`

### "Port already in use"
- Comprueba otros procesos: `lsof -i :8000` (Mac/Linux) o `netstat -ano | findstr :8000` (Windows)
- Mata cualquier proceso en conflicto o usa otros puertos

### Falla la construcción con Docker
- Asegúrate de que Docker Desktop esté ejecutándose
- Comprueba espacio libre en disco: `docker system df`
- Limpia si es necesario: `docker system prune -a` (advertencia: elimina todas las imágenes no usadas)

### Las variables de entorno no funcionan
- Verifica que el archivo `.env` esté en la raíz del proyecto (no en backend/ ni frontend/)
- Asegúrate de no dejar espacios alrededor del `=` en tu archivo `.env`
- No pongas comillas a los valores salvo que contengan espacios

---

## ¿Qué sigue?

🎉 **¡Felicidades!** Has logrado:
- ✅ Configurar el proyecto Cybersecurity Analyzer
- ✅ Configurar Semgrep para análisis de seguridad
- ✅ Crear tu configuración de entorno
- ✅ Probar localmente con ambos servidores de desarrollo
- ✅ Construir y ejecutar el contenedor Docker

¡Ya estás listo para desplegar esta aplicación en la nube!

**Próximo paso**: [Día 1 Parte 1: Configuración en Azure](./day1.part1.md) donde crearás tu cuenta de Azure y te prepararás para el despliegue en la nube.

La aplicación que acabas de probar localmente pronto estará corriendo en Azure Container Apps y Google Cloud Run, ¡accesible desde cualquier lugar del mundo!