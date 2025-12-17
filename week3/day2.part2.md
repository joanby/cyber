# Día 2 Parte 2: Google Cloud Platform

Esta guía desplegará el Cybersecurity Analyzer en Google Cloud Run usando Terraform. El despliegue construirá automáticamente tu imagen de Docker, la subirá a Google Container Registry y la desplegará como una aplicación de contenedor sin servidor.

## Prerrequisitos

✅ Completa primero la [Guía de configuración de GCP](./setup_gcp.md)
✅ Terraform CLI instalado (cubierto en módulos previos del curso)
✅ Docker ejecutándose localmente
✅ Archivo `.env` en la raíz del proyecto con tus claves API
✅ Ten a mano tu GCP Project ID (por ejemplo, `cyber-analyzer-123456`)

## Comprobación rápida de Terraform

Si pasaste por alto la instalación de Terraform en módulos anteriores:

```bash
# Comprobar si Terraform está instalado
terraform version

# Si no está instalado:
# Mac: brew install terraform
# Windows: Descargar desde https://terraform.io/downloads
# Linux: Ver https://terraform.io/docs/cli/install/apt.html
```

---

## Paso 1: Obtén tu Project ID

Necesitarás tu GCP Project ID (no el nombre del proyecto). Encuéntralo así:

```bash
# Lista tus proyectos y sus IDs
gcloud projects list

# Debería mostrar algo como:
# PROJECT_ID              NAME            PROJECT_NUMBER
# cyber-analyzer-123456   cyber-analyzer  123456789012
```

Copia tu PROJECT_ID, lo necesitarás en los siguientes pasos.

---

## Paso 2: Configura las variables de entorno

Terraform leerá tus claves API y el project ID de las variables de entorno. Las cargaremos de tu archivo `.env`:

### Mac/Linux:
```bash
# Carga las variables de entorno desde el archivo .env
export $(cat .env | xargs)

# Establece tu GCP Project ID (reemplaza por tu ID real)
export TF_VAR_project_id="cyber-analyzer-123456"

# Verifica que estén cargadas
echo "Project ID: $TF_VAR_project_id"
echo "OpenAI key loaded: ${OPENAI_API_KEY:0:8}..."
echo "Semgrep token loaded: ${SEMGREP_APP_TOKEN:0:8}..."
```

### Windows (PowerShell):
```powershell
# Carga las variables de entorno desde el archivo .env
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=', 2)
    Set-Item -Path "env:$name" -Value $value
}

# Establece tu GCP Project ID (reemplaza por tu ID real)
$env:TF_VAR_project_id = "cyber-analyzer-123456"

# Verifica que estén cargadas
Write-Host "Project ID: $env:TF_VAR_project_id"
Write-Host "OpenAI key loaded: $($env:OPENAI_API_KEY.Substring(0,8))..."
Write-Host "Semgrep token loaded: $($env:SEMGREP_APP_TOKEN.Substring(0,8))..."
```

---

## Paso 3: Inicializa Terraform

Navega hasta la configuración de Terraform de GCP:

```bash
cd terraform/gcp
```

Inicializa Terraform y crea un workspace de GCP:

```bash
# Inicializa Terraform
terraform init

# Crea y selecciona el workspace de GCP
terraform workspace new gcp
terraform workspace select gcp

# Verifica que estés en el workspace correcto
terraform workspace show
```

Deberías ver que se descarga el proveedor de Google y que el workspace está establecido en `gcp`.

---

## Paso 4: Autentícate con Google Cloud

Asegúrate de estar autenticado y de haber seleccionado el proyecto correcto:

```bash
# Inicia sesión en Google Cloud (se abrirá el navegador)
gcloud auth login

# Selecciona tu proyecto
gcloud config set project $TF_VAR_project_id

# Obtén credenciales por defecto para Terraform
gcloud auth application-default login

# Ajusta el proyecto de cuota (evita mensajes de advertencia)
gcloud auth application-default set-quota-project $TF_VAR_project_id

# Configura Docker para usar credenciales de gcloud (requerido para subir imágenes)
gcloud auth configure-docker

# Verifica la autenticación
gcloud config list
```

Asegúrate de que el proyecto mostrado coincide con tu PROJECT_ID.

> **Nota**: Al ejecutar `gcloud auth configure-docker`, se te pedirá actualizar la configuración de Docker. Escribe ‘Y’ para confirmar.

---

## Paso 5: Despliega en Cloud Run

Ahora desplegaremos todo con un solo comando:

En Mac/Linux:

```bash
# Previsualiza el despliegue (muestra lo que se va a crear)
terraform plan \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

En PC:

```powershell
terraform plan -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Revisa la salida del plan. Deberías ver:
- ✅ Habilitado Cloud Run API
- ✅ Habilitado Container Registry API
- ✅ Habilitado Cloud Build API
- ✅ Imagen de Docker construida y subida
- ✅ Despliegue del servicio Cloud Run
- ✅ Política IAM de acceso público

Si todo se ve bien, aplica los cambios:

En Mac/Linux:

```bash
# Despliega todo
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

En PC:

```powershell
terraform apply -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Escribe `yes` cuando se te pida. Esto tardará 5–10 minutos mientras:
1. Habilita las APIs necesarias de Google Cloud
2. Construye tu imagen de Docker localmente
3. Sube la imagen a Google Container Registry
4. Despliega el servicio en Cloud Run
5. Configura acceso público

**Importante**: Si haces cambios en el código y vuelves a desplegar, Terraform puede que no detecte automáticamente los cambios. Si tus actualizaciones no aparecen, fuerza la reconstrucción:

```bash
# Fuerza la reconstrucción de la imagen de Docker al cambiar el código
terraform taint docker_image.app
terraform taint docker_registry_image.app

# Luego vuelve a desplegar usando los comandos de arriba
```
---

## Paso 6: Obtén la URL de tu aplicación

Cuando termine el despliegue, Terraform mostrará la URL de tu aplicación:

```bash
# Obtén la URL de la aplicación
terraform output service_url
```

Deberías ver algo como:
```
"https://cyber-analyzer-abcdef123-uc.a.run.app"
```

🎉 **¡Tu aplicación ya está en línea!** Visita la URL para probarla.

> **Nota para usuarios de Google Workspace**: Si obtienes un error sobre políticas de organización bloqueando "allUsers", revisa [Restricciones de Google Workspace](#google-workspace-restrictions) al final de esta guía.

---

## Paso 7: Verifica el despliegue

### Prueba la aplicación
1. Abre la URL del paso 6 en tu navegador
2. Deberías ver la interfaz de Cybersecurity Analyzer
3. Intenta subir un archivo Python para verificar que funciona de extremo a extremo

### Comprueba en la Consola de Google Cloud
En la consola (https://console.cloud.google.com):
1. Selecciona tu proyecto en el desplegable
2. Ve a **Cloud Run** en el menú
3. Deberías ver tu servicio `cyber-analyzer`
4. Haz clic sobre él para ver métricas, logs y configuración

### Monitorea los logs
```bash
# Ver logs de la aplicación
gcloud run services logs read cyber-analyzer \
  --limit=50 \
  --region=$TF_VAR_region

# Ver logs en tiempo real
gcloud alpha run services logs tail cyber-analyzer \
  --region=$TF_VAR_region
```

---

## Paso 8: Limpia los recursos (¡Importante!)

Cuando termines de experimentar con el despliegue en GCP, es fundamental destruir todos los recursos para evitar costes continuos. Cloud Run tiene costes mínimos en reposo, pero el almacenamiento en Container Registry y el tráfico activo pueden generar cargos.

### Elimina todos los recursos de GCP

Ejecuta este comando desde el directorio `terraform/gcp` (todo en una sola línea):

Mac/Linux:

```bash
terraform destroy -var="openai_api_key=$OPENAI_API_KEY" -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

PC:

```powershell
terraform destroy -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Terraform mostrará lo que se eliminará. Revisa la lista y escribe `yes` cuando se te pida.

Esto eliminará:
- El servicio Cloud Run (cyber-analyzer)
- La imagen de Docker en Container Registry
- Todas las políticas IAM y configuraciones asociadas

### Verifica la limpieza en la consola

Cuando termine la destrucción, verifica que todo se haya eliminado:

1. **En Google Cloud Console** (https://console.cloud.google.com):
   - Ve a **Cloud Run** en el menú
   - Tu servicio `cyber-analyzer` ya no debería aparecer
   - Ve a **Container Registry** → **Imágenes**
   - La imagen `cyber-analyzer` debe estar eliminada

2. **Por CLI**:
```bash
# Verifica servicios Cloud Run (debería estar vacío o no mostrar cyber-analyzer)
gcloud run services list --region=us-central1

# Verifica imágenes en Container Registry (no debe aparecer cyber-analyzer)
gcloud container images list
```

3. **Comprueba recursos específicos**:
```bash
# Esto debería devolver un error indicando que el servicio no existe
gcloud run services describe cyber-analyzer --region=us-central1
```

### Opcional: Limpia el almacenamiento que quede en el registro

Si aún quedan imágenes en el registro:

```bash
# Lista todas las imágenes
gcloud container images list

# Elimina una imagen específica si todavía existe
gcloud container images delete gcr.io/$TF_VAR_project_id/cyber-analyzer --quiet --force-delete-tags
```

**💡 Consejo**: Ejecuta siempre `terraform destroy` al terminar cada laboratorio. Puedes volver a desplegar fácilmente con `terraform apply` cuando lo necesites. Cloud Run cobra muy poco en reposo, pero es buena práctica limpiar los recursos de aprendizaje.

---

## Comprendiendo lo que se ha creado

### Desglose de costes (mayormente en capa gratuita):
- **Cloud Run**: 2 millones de peticiones/mes gratis, luego ~$0.40 por millón
- **Container Registry**: 0.5GB de almacenamiento gratis, luego ~$0.05/GB/mes
- **Tráfico saliente**: 1GB/mes gratis a Norteamérica
- **Coste total estimado**: < 1$/mes para aprendizaje

### Arquitectura:
```
Internet → Cloud Run Service → Tu imagen Docker
              ↓
     Google Container Registry
          (almacenamiento de imágenes)
```

### Configuración de recursos:
- **CPU**: 1 vCPU (requerido para el procesamiento de Semgrep)
- **Memoria**: 2Gi (requerido para la carga del registro de reglas de Semgrep)
- **Importante**: Configurar menos memoria provocará que Semgrep falle con SIGKILL

### Escalado:
- **Instancias mínimas**: 0 (escala real a cero = $0 en reposo)
- **Instancias máximas**: 1 (mantiene costes mínimos)
- **Autoscaling**: Según peticiones concurrentes
- **Arranque en frío**: ~5-10 segundos tras estar inactivo

---

## Gestión de tu despliegue

### Ver el estado de la infraestructura
```bash
# Ver lo que está desplegado
terraform show

# Listar todos los recursos
terraform state list
```

### Actualizar la aplicación
Después de hacer cambios en el código:

```bash
# Reconstruye y vuelve a desplegar con una nueva etiqueta
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN" \
  -var="docker_image_tag=v2"
```

### Ver detalles del servicio
```bash
# Obtener información del servicio
gcloud run services describe cyber-analyzer \
  --region=$TF_VAR_region

# Listar todas las revisiones
gcloud run revisions list \
  --service=cyber-analyzer \
  --region=$TF_VAR_region
```

### Limpieza (¡Importante para el control de costes!)
Cuando termines con el laboratorio:

```bash
# Elimina todos los recursos
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Escribe `yes` para confirmar. Esto elimina todo y detiene cualquier cargo.

**También limpia imágenes del Container Registry:**
```bash
# Lista de imágenes
gcloud container images list

# Borra la imagen (opcional, ahorra en costes de almacenamiento)
gcloud container images delete gcr.io/$TF_VAR_project_id/cyber-analyzer --quiet
```

---

## Resolución de problemas

### "Failed to build Docker image" (Fallo al construir la imagen de Docker)
- Asegúrate de que Docker está en marcha: `docker ps`
- Verifica que estás en el directorio correcto: `terraform/gcp`
- Comprueba que Docker tiene suficiente espacio en disco: `docker system df`

### "Permission denied" o errores de API
```bash
# Vuelve a autenticarte
gcloud auth application-default login

# Verifica que las APIs están habilitadas
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### "Project not found" (Proyecto no encontrado)
- Verifica el project ID: `gcloud projects list`
- Asegúrate de que TF_VAR_project_id está bien configurada
- Comprueba que estás en el proyecto correcto: `gcloud config get-value project`

### "Environment variables not set" (Variables de entorno no configuradas)
- Repite los comandos de configuración de variables de entorno del Paso 2
- Comprueba que el archivo `.env` existe y tiene el formato correcto
- En Windows, asegúrate de estar usando PowerShell (no Command Prompt)

### La aplicación devuelve 503 o no carga
- Cloud Run puede tener arranques en frío – espera 10-15 segundos en el primer acceso
- Revisa los logs: `gcloud run services logs read cyber-analyzer --limit=50`
- Verifica que el servicio está desplegado: `gcloud run services list`

### Fallos al subir imágenes a Docker
```bash
# Configura Docker para usar credenciales de gcloud
gcloud auth configure-docker

# Reintenta el despliegue
terraform apply -var="openai_api_key=$OPENAI_API_KEY" -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

---

## Comparando Azure vs GCP

### Similitudes:
- Ambos ofrecen plataformas de contenedores serverless
- Ambos escalan a cero (Cloud Run es más rápido)
- Ambos usan patrones Terraform similares
- Ambos requieren 2GB RAM para Semgrep

### Diferencias clave:

| Característica | Azure Container Apps | Google Cloud Run |
|----------------|---------------------|------------------|
| Arranque en frío | ~30 segundos | ~5-10 segundos |
| Escala real a cero | Algo (procesos en segundo plano) | Sí (se detiene por completo) |
| Modelo de precios | Por vCPU/Memoria asignada | Por petición + tiempo de cómputo |
| Container Registry | Servicio separado (ACR) | Integrado (GCR) |
| Formato URL | Subdominio largo | Más corto y limpio |
| Capa gratuita | Limitada | Generosa (2M peticiones) |

### ¿Cuál es mejor?
- **Para aprender**: Cloud Run (mejor capa gratuita)
- **Para producción**: Depende de tu carga de trabajo
- **En este curso**: ¡Ambas! Compáralas y aprende

---

## Siguientes pasos

🎉 **¡Enhorabuena!** Has desplegado correctamente en Azure y en GCP.

**Has aprendido:**
- Google Cloud Run para contenedores serverless
- Google Container Registry para almacenamiento de imágenes
- Patrones de despliegue multiplataforma en la nube
- Terraform para infraestructura multinube
- Estrategias de optimización de costes

**Habilidades adquiridas:**
- Experiencia con despliegues multinube
- Infraestructura como código con Terraform
- Gestión de registros de contenedores
- Manejo de variables de entorno
- Gestión de costes en la nube

Conserva ambos despliegues para comparar, pero recuerda limpiar al terminar para evitar costes.

---

## Restricciones de Google Workspace

Si usas una cuenta de Google Workspace (correo de dominio propio) en lugar de una Gmail personal, puedes encontrar un error cuando Terraform intente hacer que tu servicio Cloud Run sea público:

```
Error: Error applying IAM policy for cloudrun service...
One or more users named in the policy do not belong to a permitted customer, 
perhaps due to an organization policy.
```

Esto sucede porque las organizaciones de Google Workspace suelen tener políticas de compartición restringidas por dominio por seguridad. Así es cómo solucionarlo:

### Opción 1: Solicitar una excepción en la política de organización (Recomendado)

Si tienes acceso de administrador en Google Workspace:

1. **Comprueba tu rol actual**:
```bash
gcloud organizations list
gcloud organizations get-iam-policy YOUR_ORG_ID | grep -A5 "YOUR_EMAIL"
```

2. **Concede a tu usuario el rol Organization Policy Administrator** (si es necesario):
```bash
gcloud organizations add-iam-policy-binding YOUR_ORG_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/orgpolicy.policyAdmin"
```

3. **Modifica la política en la consola de GCP**:
   - Ve a https://console.cloud.google.com
   - Cambia de tu organización a tu proyecto específico (desplegable arriba a la izquierda)
   - Navega a **IAM & Admin** → **Organization Policies**
   - Busca **"Domain restricted sharing"** (constraints/iam.allowedPolicyMemberDomains)
   - Haz clic en **"MANAGE POLICY"**
   - Añade una regla con **"Allow All"** para tu proyecto
   - Guarda los cambios

4. **Vuelve a ejecutar Terraform**:
```bash
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

### Opción 2: Contacta con tu administrador

Si no tienes acceso de admin:
1. Contacta con el administrador de Google Workspace
2. Solicita una excepción para tu proyecto cyber-analyzer
3. Deben permitir "allUsers" para servicios Cloud Run en tu proyecto

### Opción 3: Usa acceso autenticado (alternativa)

Si no puedes modificar la política, aún puedes acceder a tu servicio desplegado:

```bash
# Esto crea un proxy local a tu servicio Cloud Run
gcloud run services proxy cyber-analyzer --region=us-central1
```

Luego visita http://localhost:8080 en tu navegador.

### Por qué ocurre esto

- **Cuentas personales de Gmail**: No hay organización = sin restricciones
- **Cuentas de Google Workspace**: Las políticas de la organización regulan la seguridad por defecto
- **La solución**: Crear una excepción específica de proyecto manteniendo la seguridad de la organización

Esto se configura una sola vez. Una vez hecho, todos los futuros despliegues a este proyecto funcionarán normalmente.