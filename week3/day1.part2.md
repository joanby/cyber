# Día 1 Parte 2: Despliegue en Azure

Esta guía desplegará el Cybersecurity Analyzer en Azure Container Apps usando Terraform. El despliegue construirá automáticamente tu imagen Docker, la subirá al Azure Container Registry y la lanzará como una aplicación serverless en contenedores.

## Requisitos Previos

✅ Completa primero el Día 1 Parte 1  
✅ Terraform CLI instalado (cubierto en módulos anteriores del curso)  
✅ Docker corriendo localmente  
✅ Archivo `.env` en la raíz del proyecto con tus keys de API

## Comprobación Rápida de Terraform

Si te saltaste la instalación de Terraform en módulos previos:

```bash
# Revisa si Terraform está instalado
terraform version

# Si no está instalado:
# Mac: brew install terraform
# Windows: Descargar desde https://terraform.io/downloads
```

---

## Paso 1: Configurar Variables de Entorno

Terraform leerá tus keys de API desde las variables de entorno. Vamos a cargarlas desde tu archivo `.env`:

### Mac/Linux:
```bash
# Cargar variables de entorno desde el archivo .env
export $(cat .env | xargs)

# Verifica que estén cargadas
echo "OpenAI key cargada: ${OPENAI_API_KEY:0:8}..."
echo "Semgrep token cargado: ${SEMGREP_APP_TOKEN:0:8}..."
```

### Windows (PowerShell):
```powershell
# Cargar variables de entorno desde .env
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=', 2)
    Set-Item -Path "env:$name" -Value $value
}

# Verifica que estén cargadas
Write-Host "OpenAI key cargada: $($env:OPENAI_API_KEY.Substring(0,8))..."
Write-Host "Semgrep token cargado: $($env:SEMGREP_APP_TOKEN.Substring(0,8))..."
```

---

## Paso 2: Inicializar Terraform

Navega a la configuración de Terraform para Azure:

```bash
cd terraform/azure
```

Inicializa Terraform y crea un workspace para Azure:

```bash
# Inicializar Terraform
terraform init

# Crear y seleccionar el workspace de Azure
terraform workspace new azure
terraform workspace select azure

# Verifica que estés en el workspace correcto
terraform workspace show
```

Deberías ver un mensaje indicando que el provider de Azure se descarga y el workspace está en `azure`.

---

## Paso 3: Iniciar Sesión en Azure y Registrar Proveedores

Asegúrate de haber iniciado sesión en Azure CLI y registra los resource providers requeridos:

```bash
# Inicia sesión en Azure (se abrirá el navegador)
az login

# Verifica que has iniciado sesión y mira tu suscripción
az account show --output table
```

Asegúrate de que la suscripción mostrada coincida con la que configuraste en la guía de setup de Azure.

### Entendiendo los Resource Providers

En Azure, los "resource providers" son servicios que proveen recursos de Azure. Son la forma en que Azure organiza y habilita distintos servicios en la nube. Es similar a habilitar servicios o APIs en AWS, aunque con una diferencia clave: en AWS, la mayoría de los servicios están disponibles en cuanto tienes permisos IAM adecuados. En Azure, debes registrar explícitamente los resource providers antes de crear recursos de ese tipo en tu suscripción. Esto solo debe hacerse una vez y le indica a Azure: "Quiero poder utilizar Container Apps y Log Analytics en esta suscripción." El registro es gratuito; solo pagas cuando realmente creas los recursos.

Registra ahora los resource providers requeridos por Azure (solo se hace una vez):

```bash
# Registrar el provider para Container Apps
az provider register --namespace Microsoft.App

# Registrar el provider para Log Analytics
az provider register --namespace Microsoft.OperationalInsights

# Comprobar estado de registro (debe decir "Registered")
az provider show --namespace Microsoft.App --query "registrationState" -o tsv
az provider show --namespace Microsoft.OperationalInsights --query "registrationState" -o tsv
```

⏳ **Espera el registro**: Si alguno aparece como "Registering", espera 1-2 minutos y consulta de nuevo. Los dos deben mostrar "Registered" antes de proseguir.

---

## Paso 4: Desplegar en Azure

Ahora vamos a desplegar todo con un solo comando:

```bash
# Planificar el despliegue (ver qué se creará)
terraform plan \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Revisa la salida del plan. Deberías ver:
- ✅ Azure Container Registry (ACR)
- ✅ Log Analytics Workspace
- ✅ Container App Environment
- ✅ Container App
- ✅ Construcción y subida de imagen Docker

Si todo es correcto, aplica los cambios:

En Mac / Linux:

```bash
# Desplegar todo
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

En PC (Powershell):

```powershell
terraform apply -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Escribe `yes` cuando se te solicite. Esto toma 5-10 minutos, durante los cuales:
1. Se crea el Azure Container Registry
2. Se construye tu imagen Docker localmente
3. Se sube la imagen al ACR
4. Se crea la infraestructura del Container App
5. Se despliega tu aplicación

**Importante**: Si haces cambios en el código y vuelves a desplegar, Terraform podría no detectar los cambios automáticamente. Si tus actualizaciones no aparecen, fuerza la reconstrucción:

```bash
# Forzar reconstrucción de la imagen Docker cuando cambie el código
terraform taint docker_image.app
terraform taint docker_registry_image.app
```

Luego vuelve a desplegar usando los comandos `terraform apply` del paso anterior.

---

## Paso 5: Obtener la URL de tu Aplicación

Cuando termine el despliegue, Terraform imprimirá la URL de tu aplicación:

```bash
# Obtener la URL de tu aplicación
terraform output app_url
```

Debería mostrar algo así:
```
"https://cyber-analyzer.nicehill-12345678.eastus.azurecontainerapps.io"
```

🎉 **¡Tu aplicación ya está en línea!** Visita la URL para probarla.

---

## Paso 6: Verificar el Despliegue

### Probar la Aplicación
1. Abre la URL del Paso 5 en tu navegador
2. Deberías ver la interfaz de Cybersecurity Analyzer
3. Prueba subiendo un archivo Python para verificar que funciona de extremo a extremo

### Revisar Recursos en Azure
En el Portal de Azure (https://portal.azure.com):
1. Navega hasta tu grupo de recursos: `cyber-analyzer-rg`
2. Deberías ver:
   - Registro de contenedores (cyberanalyzeracr)
   - Log Analytics workspace (cyber-analyzer-logs)
   - Container App Environment (cyber-analyzer-env)
   - Container App (cyber-analyzer)

### Monitorizar Logs
```bash
# Ver logs de la aplicación
az containerapp logs show --name cyber-analyzer --resource-group cyber-analyzer-rg --follow
```

### Revisar Costes Generados
Es buena práctica revisar regularmente los costes. En el Portal de Azure:
1. Busca **"Cost Management"** en la barra de búsqueda superior
2. Haz clic en **"Cost analysis"** en el menú izquierdo
3. Establece el scope en tu suscripción
4. Observa **"Accumulated costs"** del periodo actual de facturación
5. Filtra por grupo de recursos `cyber-analyzer-rg` para ver los costes de este proyecto

Desde la línea de comandos:
```bash
# Consulta consumo actual (puede tardar unas horas en actualizarse)
az consumption usage list \
  --start-date $(date -u -d '7 days ago' '+%Y-%m-%d') \
  --end-date $(date -u '+%Y-%m-%d') \
  --query "[?contains(instanceId, 'cyber-analyzer')].{Resource:instanceName, Cost:pretaxCost, Currency:currency}" \
  --output table
```

**Nota**: Los costes de Azure pueden tardar 24-48 horas en aparecer. El cobro de Container Apps es mínimo cuando está inactivo, pero revisa regularmente para evitar sorpresas.

---

## Paso 7: Limpiar Recursos (¡Importante!)

Cuando termines de experimentar con el despliegue en Azure, es fundamental destruir todos los recursos para evitar costes adicionales. Los Container Apps pueden generar costes incluso estando inactivos, así que limpia siempre tras tus sesiones de práctica.

### Destruir Todos los Recursos de Azure

Ejecuta este comando desde el directorio `terraform/azure`:

Para Mac/Linux:

```bash
# Destruir todos los recursos creados por Terraform
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Para PC:

```powershell
terraform destroy -var ("openai_api_key=" + $Env:OPENAI_API_KEY) -var ("semgrep_app_token=" + $Env:SEMGREP_APP_TOKEN)
```

Terraform mostrará lo que va a destruir. Revisa la lista y escribe `yes` cuando se te pida confirmación.

Esto eliminará:
- El Container App (cyber-analyzer)
- El Container App Environment  
- El Container Registry y todas las imágenes
- El Log Analytics workspace
- Toda la configuración asociada

### Verificar que Todo se Eliminó

Una vez que termine la destrucción:

1. **En el Portal de Azure**:  
   - Ve al grupo de recursos `cyber-analyzer-rg`
   - Debería estar vacío o mostrar "No resources to display"

2. **Por CLI**:
```bash
# Listar recursos en el grupo (debería estar vacío)
az resource list --resource-group cyber-analyzer-rg --output table
```

3. **Comprobar el Registro de Contenedores**:
```bash
# Verifica que el registro ya no existe (debería arrojar error)
az acr show --name cyberanalyzeracr --resource-group cyber-analyzer-rg
```

### Puedes Mantener el Grupo de Recursos

Puedes dejar el grupo vacío para futuros despliegues; no genera costes. Si lo quieres eliminar también:

```bash
# Opcional: Eliminar completamente el grupo de recursos
az group delete --name cyber-analyzer-rg --yes
```

**💡 Consejo Pro:** Ejecuta siempre `terraform destroy` al final de cada sesión de laboratorio. Puedes volver a desplegar con `terraform apply` cuando lo necesites.

---

## Entendiendo lo que se ha Creado

### Desglose de Costes (todos muy bajos o gratis):
- **Container Registry**: Tier básico (~$5/mes, incluye 10GB de almacenamiento)
- **Container App**: Pago por uso, escala a cero (~$0 mientras no se use)
- **Log Analytics**: 5GB gratis por mes
- **Coste total estimado**: < $5/mes para aprendizaje

### Arquitectura:
```
Internet → Container App → Your Docker Image
              ↓
          Log Analytics (monitoring)
              ↓
      Container Registry (image storage)
```

### Configuración de Recursos:
- **CPU**: 1.0 vCPU (requerido por el procesamiento de Semgrep)
- **Memoria**: 2.0Gi (necesario para cargar el registro de reglas de Semgrep)
- **Importante**: Menos memoria hace que Semgrep falle con SIGKILL

### Escalado:
- **Min replicas**: 0 (escala a cero cuando no se usa = $0)
- **Max replicas**: 1 (para mantener los costes mínimos)
- **Autoescalado**: Basado en peticiones HTTP

---

## Gestión de tu Despliegue

### Ver el Estado de la Infraestructura
```bash
# Ver lo que está desplegado
terraform show

# Listar todos los recursos
terraform state list
```

### Actualizar la Aplicación
Tras hacer cambios en el código:

```bash
# Reconstruir y volver a desplegar
terraform apply \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN" \
  -var="docker_image_tag=v2"
```

### Limpiar (¡Importante para evitar costes!)
Cuando termines el laboratorio:

```bash
# Destruir todos los recursos
terraform destroy \
  -var="openai_api_key=$OPENAI_API_KEY" \
  -var="semgrep_app_token=$SEMGREP_APP_TOKEN"
```

Confirma escribiendo `yes`. Esto elimina todo y detiene cualquier cargo.

---

## Solución de Problemas

### "Failed to build Docker image"
- Asegúrate de que Docker esté corriendo: `docker ps`
- Que estés en la carpeta raíz del proyecto
- Verifica que el Dockerfile exista y sea válido

### Error "MissingSubscriptionRegistration"
Esto indica que los providers de recursos de Azure no están registrados:
```bash
# Registrar los providers requeridos
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# Espera a que el registro finalice
az provider show --namespace Microsoft.App --query "registrationState" -o tsv
```
Repite `terraform apply` cuando ambos indiquen "Registered".

### "Login server could not be found"
- Ejecuta `az login` otra vez
- Verifica que exista el grupo de recursos: `az group show --name cyber-analyzer-rg`

### "Environment variables not set"
- Repite los comandos de variables de entorno del Paso 1
- Verifica que el archivo `.env` exista y tenga el formato correcto

### Problemas con el workspace de Terraform
```bash
# Listar workspaces
terraform workspace list

# Volver a seleccionar azure
terraform workspace select azure
```

### Aplicación no accesible
- Comprueba la URL con `terraform output app_url`
- Espera 2-3 minutos tras el despliegue
- Revisa logs: `az containerapp logs show --name cyber-analyzer --resource-group cyber-analyzer-rg`

---

## Siguientes Pasos

🎉 **¡Felicidades!** Has desplegado exitosamente una aplicación contenerizada en Azure usando Infrastructure as Code.

**Lo que has aprendido:**
- Azure Container Apps para contenedores serverless
- Azure Container Registry para almacenar imágenes
- Workspaces de Terraform para gestionar entornos
- Gestión de variables de entorno en despliegues cloud
- Patrones de arquitectura cloud rentables

**Próximamente:** Vamos a desplegar la misma aplicación en Google Cloud Platform usando Cloud Run y comparar ambos enfoques.