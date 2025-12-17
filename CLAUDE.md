# Contexto del Proyecto para Código Claude

## Contexto general
- Este es un proyecto desarrollado como parte del curso de Ed "AI in Production"
- Ed está escribiendo este código que miles de estudiantes clonarás; posteriormente seguirán los pasos para desplegar
- Los estudiantes pueden estar en Windows PC, Mac o Linux; las instrucciones deben funcionar en todos los sistemas
- Este proyecto se llama Cybersecurity Analyzer - ejecuta un Agent
- El proyecto se desplegará localmente con npm y uv run (funcionando), también localmente como un solo contenedor Docker (funcionando), en Azure Container App (funcionando), y en GCP Cloud Run (aún sin empezar)
- La raíz del proyecto es ~/projects/cyber
- Hay un archivo .env en la raíz del proyecto; puede que no puedas verlo por motivos de seguridad, pero está allí, con OPENAI_API_KEY y SEMGREP_APP_TOKEN

## Resumen del Proyecto
Cybersecurity Analyzer - Una aplicación web para analizar código Python en busca de vulnerabilidades de seguridad usando análisis con IA a través de OpenAI y Semgrep.

**Propósito educativo**: Este proyecto sirve como herramienta didáctica para estudiantes aprendiendo a desplegar en la nube en Azure y Google Cloud Platform. Los estudiantes obtendrán experiencia práctica desplegando aplicaciones contenerizadas usando plataformas modernas serverless.

## Arquitectura
- **Frontend**: Next.js (React) con TypeScript, Tailwind CSS
  - Ubicado en `frontend/`
  - Corre en el puerto 3000 en desarrollo
  - Se construye como exportación estática para producción
- **Backend**: FastAPI con Python 3.12
  - Ubicado en `backend/`
  - Corre en el puerto 8000
  - Usa OpenAI Agents SDK con el servidor Semgrep MCP

## Decisiones técnicas clave

### Despliegue Docker (31 de julio de 2025)
- Simplificado de un enfoque supervisor de varias etapas a despliegue de una sola etapa
- El frontend se construye como exportación estática (`next export`) y es servido directamente por FastAPI
- Un solo contenedor expone el puerto 8000 tanto para la API como para los archivos estáticos
- Optimizado para Google Cloud Run y Azure Container Instances

### Fijación de versión MCP (31 de julio de 2025)
- **Problema**: La librería MCP se actualizó de la 1.12.2 a la 1.12.3 el 31 de julio de 2025
- **Cambio incompatible**: FastMCP ya no acepta el parámetro `version` en el constructor
- **Solución**: Fijar MCP a la versión 1.12.2 en `pyproject.toml` y usar `uvx --with mcp==1.12.2` al lanzar semgrep-mcp
- **Razón**: semgrep-mcp v0.4.1 todavía pasa el parámetro `version`, causando TypeError con MCP 1.12.3

## Configuración de Desarrollo

### Variables de entorno
Requeridas en el archivo `.env`:
- `OPENAI_API_KEY` - Para acceso a la API de OpenAI
- `SEMGREP_APP_TOKEN` - Para análisis con Semgrep

### Desarrollo local
```bash
# Backend
cd backend
uv run server.py

# Frontend (en terminal separada)
cd frontend
npm run dev
```

### Comandos Docker
```bash
# Construir
docker build -t cyber-analyzer .

# Ejecutar con archivo env
docker run --rm -d --name cyber-analyzer -p 8000:8000 --env-file .env cyber-analyzer

# Ver logs
docker logs cyber-analyzer

# Detener
docker stop cyber-analyzer
```

## Detalles importantes de implementación

1. **Servicio de archivos estáticos**: FastAPI sirve la exportación estática de Next.js desde el directorio `static`. El endpoint `/health` debe definirse antes de montar archivos estáticos para evitar conflictos de rutas.

2. **Rutas de la API**: Todos los endpoints de API están bajo el prefijo `/api/` (ejemplo: `/api/analyze`)

3. **Configuración del frontend**: 
   - `next.config.ts` usa `output: 'export'` para generación estática
   - `trailingSlash: true` para un enrutado adecuado
   - `images.unoptimized: true` para compatibilidad con la exportación estática

## Problemas conocidos y soluciones

1. **Compatibilidad de versión MCP**: Se debe usar MCP 1.12.2 hasta que semgrep-mcp se actualice para quitar el parámetro `version` del inicializador de FastMCP.

## Pruebas y calidad
- Ejecuta `npm run lint` en frontend para linting
- Ejecuta `npm run typecheck` en frontend para verificación de tipos
- El backend usa `uv` para la gestión de dependencias

## Consideraciones futuras
- Monitorear actualizaciones de semgrep-mcp para compatibilidad con MCP 1.12.3+
- Considerar añadir pruebas automatizadas
- Puede ser necesario ajustar el timeout de healthcheck de Docker para despliegues en la nube

## Proyecto de despliegue en la nube (Iniciado el 31 de julio de 2025)

### Objetivos educativos
- Enseñar habilidades prácticas de despliegue en la nube en Azure y GCP a estudiantes
- Comparar y contrastar plataformas serverless de contenedores (Azure Container Apps vs Cloud Run)
- Experiencia práctica con Terraform para infraestructura como código
- Comprender seguridad en la nube, gestión de secretos y optimización de costes

### Estrategia de despliegue
1. **Fase 1 - Despliegue en Azure**
   - Azure Container Apps (plataforma serverless de contenedores)
   - Azure Container Registry para almacenamiento de imágenes
   - Azure Key Vault para gestión de secretos
   - Cuentas estudiantiles mediante Azure for Students (crédito de $100)

2. **Fase 2 - Despliegue en GCP**
   - Google Cloud Run (equivalente a Azure Container Apps)
   - Artifact Registry para imágenes de contenedores
   - Secret Manager para variables de entorno
   - Cuentas estudiantiles mediante GCP Free Tier + crédito de $300

3. **Infraestructura como código**
   - Terraform con workspaces para gestionar ambas nubes
   - Diseño modular para componentes reutilizables
   - Separación clara entre las configuraciones de Azure y GCP

### Enfoque didáctico
- Comenzar por Azure (es menos familiar para la mayoría de estudiantes)
- Avanzar a GCP para comparar
- Enfoque en habilidades prácticas: creación de cuentas, gestión de costes, seguridad
- Énfasis en comprender los compromisos y diferencias entre plataformas

### Prerrequisitos cubiertos en clases anteriores
- Despliegue en AWS App Runner
- Conceptos básicos de Terraform
- Fundamentos de contenedores

### Estado actual (Actualizado 31 de julio de 2025)
- ✅ **Despliegue en Azure completado** - Aplicación desplegada exitosamente en Azure Container Apps
- ✅ **Imagen Docker optimizada** - Build multi-etapa con compilación cruzada ARM64→AMD64 para compatibilidad en la nube
- ✅ **Pipeline de despliegue Terraform** - Infraestructura como código funcionando con workspace de Azure
- ✅ **CORS y routing API resueltos** - El frontend usa URLs relativas en producción, localhost en desarrollo
- ✅ **Problema con servidor MCP RESUELTO** - Incrementar memoria a 2.0Gi solucionó el problema de Semgrep y SIGKILL

### Problema de memoria del servidor MCP - RESUELTO (31 de julio de 2025)
**Problema**: El servidor Semgrep MCP recibía SIGKILL (-9) en Azure al cargar el registro de reglas
- `list_tools` funcionaba pero `semgrep_scan` fallaba con código de salida -9
- El proceso se mataba justo después de "Loading rules from registry..."
- **Causa raíz**: Asignación insuficiente de memoria (1.0Gi) 
- **Solución**: Incrementar la memoria del contenedor de 1.0Gi a 2.0Gi y la CPU de 0.5 a 1.0
- **Verificado**: Funciona en tanto Azure Container Apps como Azure Container Instances con 2GB de RAM
- **Estado**: Recursos de prueba de ACI destruidos, pero la configuración de terraform se mantiene en `azure-aci/` para referencia futura

**Lección clave**: Cargar el registro de reglas de Semgrep es intensivo en memoria y requiere al menos 2GB de RAM en entornos cloud

### Lecciones clave aprendidas en el despliegue
1. **Limitaciones del proveedor Docker de Terraform**: 
   - No detecta automáticamente cambios en el código fuente
   - Se debe usar `terraform taint` para forzar reconstrucciones cuando cambia el código
   - Usar tags únicos para las imágenes puede ayudar a evitar problemas de caché

2. **Configuración de la URL de la API en el frontend**:
   - La exportación estática de Next.js necesita URLs relativas para despliegue en el mismo dominio
   - Lógica basada en entorno: localhost en desarrollo, URLs relativas en producción
   - CORS debe permitir orígenes wildcard al servir el frontend desde el mismo dominio

3. **Comportamiento de Azure Container Apps**:
   - El FQDN cambia con cada revisión nueva (--0000001, --0000002, etc.)
   - Las apps escalan a cero automáticamente, ahorrando costes
   - Los logs son accesibles vía `az containerapp logs show`

4. **Builds Docker multiplataforma**:
   - M1 Mac construye por defecto sobre ARM64, Azure necesita AMD64
   - Solución: `platform = "linux/amd64"` en el build Docker de Terraform
   - Ligera penalización en rendimiento en M1 Mac pero asegura compatibilidad