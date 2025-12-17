# Día 2 Parte 1: Guía de Configuración de Google Cloud Platform

Esta guía te llevará paso a paso en la configuración de tu cuenta de Google Cloud Platform (GCP) y en la preparación para desplegar aplicaciones contenerizadas. Todas las instrucciones funcionan para usuarios de Windows, Mac y Linux.

## Tabla de Contenidos
1. [Creando tu Cuenta de GCP](#creating-your-gcp-account)
2. [Entendiendo la Estructura de GCP](#understanding-gcps-structure)
3. [Creando tu Primer Proyecto](#creating-your-first-project)
4. [Configurando la Facturación](#setting-up-billing)
5. [Configurando la Gestión de Costes](#setting-up-cost-management)
6. [Instalando Google Cloud CLI](#installing-google-cloud-cli)
7. [Verificando tu Configuración](#verifying-your-setup)

---

## Creando tu Cuenta de GCP

### Prueba gratuita de GCP
1. Ve a https://cloud.google.com/free
2. Haz clic en **"Get started for free"**
3. Inicia sesión con tu cuenta de Google (o crea una)
4. Deberás proporcionar:
   - País
   - Tipo de cuenta (Individual)
   - Una tarjeta de crédito (solo para verificación de identidad - no se te cobrará)
   - Número de teléfono para verificación
5. Recibirás:
   - $300 de crédito válido por 90 días
   - Servicios del nivel siempre gratis (incluso después de que la prueba termine)
   - No habrá cobros automáticos al terminar la prueba

> **Nota**: A diferencia de Azure, GCP NO cobrará automáticamente tu tarjeta al acabar la prueba gratuita. Debes actualizar manualmente tu cuenta para pasar a paga.

⚠️ **Importante**: Tras crear tu cuenta, serás redirigido a la Consola de Google Cloud en https://console.cloud.google.com

---

## Entendiendo la Estructura de GCP

Antes de crear recursos, vamos a entender la jerarquía de GCP:

```
Cuenta de Google (Tu Gmail)
  └── Organización (opcional, para empresas)
      └── Billing Account (Tu método de pago)
          └── Proyecto (ej: "cyber-analyzer")
              └── Recursos (Cloud Run, Artifact Registry, etc.)
```

Piensa en:
- **Billing Account**: Tu método de pago (puede usarse en varios proyectos)
- **Project**: Un contenedor para todos tus recursos (similar al Resource Group de Azure)
- **Resources**: Los servicios reales que creas

---

## Creando tu Primer Proyecto

GCP requiere un proyecto para organizar los recursos. Vamos a crear uno:

1. En la Consola de Google Cloud (https://console.cloud.google.com)
2. En la parte superior de la página, haz clic en el desplegable de proyectos (quizás diga "My First Project")
3. Haz clic en **"NEW PROJECT"** en el diálogo
4. Completa los detalles:
   - **Project name**: `cyber-analyzer`
   - **Organization**: Deja el valor por defecto
   - **Location**: Deja el valor por defecto
   
   💡 **Nota**: GCP generará automáticamente un Project ID único basado en el nombre de tu proyecto (aparece en gris debajo del campo de nombre). Apúntalo: lo necesitarás en comandos de la CLI.

5. Haz clic en **"CREATE"**
6. Espera unos 30 segundos para la creación
7. Asegúrate de que tu nuevo proyecto está seleccionado en el desplegable superior

🎉 ¡Has creado tu primer proyecto!

---

## Configurando la Facturación

Incluso con créditos gratuitos, necesitas vincular tu cuenta de facturación al proyecto:

1. En la consola, haz clic en el menú **"☰"** (arriba a la izquierda)
2. Navega a **"Billing"**
3. Si se solicita, vincula tu cuenta de facturación al proyecto
4. Verifica que ves tu saldo de $300 en créditos

---

## Configurando la Gestión de Costes

Vamos a configurar alertas de presupuesto para evitar sorpresas:

1. En el menú **"☰"** de la consola, navega a **"Billing"**
2. Haz clic en **"Budgets & alerts"** en el menú de la izquierda
3. Haz clic en **"CREATE BUDGET"**
4. Configura tu presupuesto:
   - **Name**: `Monthly Training Budget`
   - **Projects**: Selecciona `cyber-analyzer`
   - Haz clic en **"Next"**
5. Establece el monto:
   - **Budget type**: Specified amount
   - **Amount**: `$10`
   - **Time period**: Monthly
   - Haz clic en **"Next"**
6. Configura las alertas:
   - Los umbrales por defecto están bien (50%, 90%, 100%)
   - Marca **"Email alerts to billing admins"**
   - Opcional: añade tu correo electrónico bajo "Email recipients"
   - Haz clic en **"Finish"**

✅ ¡Ahora recibirás alertas por correo antes de gastar demasiado!

---

## Instalando Google Cloud CLI

La CLI de gcloud es esencial para operaciones de despliegue y trabajar con aplicaciones contenerizadas.

### Usuarios de Windows

Opción 1 - Usando el instalador:
1. Descarga el instalador desde: https://cloud.google.com/sdk/docs/install#windows
2. Ejecuta el archivo `GoogleCloudSDKInstaller.exe` descargado
3. Sigue el asistente de instalación (acepta todas las opciones por defecto)
4. El instalador abrirá automáticamente una nueva ventana de terminal

Opción 2 - Usando PowerShell (requiere permisos de administrador):
```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

### Usuarios de Mac

Opción 1 - Usando Homebrew (si lo tienes instalado):
```bash
brew install --cask google-cloud-sdk
```

Opción 2 - Instalación directa:
```bash
# Descargar y ejecutar el script de instalación
curl https://sdk.cloud.google.com | bash
# Reinicia tu terminal
exec -l $SHELL
```

### Usuarios de Linux

Para la mayoría de distribuciones:
```bash
# Descargar y ejecutar el script de instalación
curl https://sdk.cloud.google.com | bash
# Reinicia tu terminal
exec -l $SHELL
```

Para Ubuntu/Debian con apt:
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-cli
```

### Inicializar gcloud (Todas las plataformas)

1. Abre una nueva terminal o línea de comandos
2. Ejecuta:
```bash
gcloud init
```

3. Sigue las indicaciones:
   - Elige **"Y"** para iniciar sesión
   - Se abrirá tu navegador, inicia sesión con tu cuenta de Google
   - Elige tu proyecto (`cyber-analyzer`)
   - Elige una región por defecto cuando te lo pregunte:
     - US: `us-central1` o `us-east1`
     - Europa: `europe-west1` o `europe-north1`
     - Asia: `asia-southeast1` o `asia-northeast1`
   
   💡 **Consejo**: ¡Recuerda esta región! La usaremos para Cloud Run.

---

## Verificando tu Configuración

Vamos a asegurar que todo funciona correctamente:

### Usando Google Cloud Console
1. Ve a https://console.cloud.google.com
2. Asegúrate de que `cyber-analyzer` esté seleccionado en el desplegable de proyectos
3. Haz clic en el menú **"☰"** y ve a **"Cloud Run"**
4. Debes ver una lista vacía (¡eso es correcto!)

### Usando gcloud CLI
Ejecuta estos comandos:
```bash
# Muestra la configuración actual
gcloud config list

# Lista los proyectos disponibles
gcloud projects list

# Muestra el proyecto actual
gcloud config get-value project

# Prueba el acceso a la API
gcloud services list --enabled
```

Deberías ver:
- Tu Project ID (`cyber-analyzer-xxxxx`)
- Tu región seleccionada
- Una lista de APIs habilitadas

### Habilitar APIs necesarias
Cloud Run necesita ciertas APIs activadas. Ejecuta:
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

Esto activa:
- Cloud Run API (para despliegues)
- Container Registry API (para almacenar imágenes)
- Cloud Build API (para construir contenedores)

---

## ¿Qué sigue?

¡Felicidades! Tu cuenta de GCP ya está lista. Ahora tienes:
- ✅ Una cuenta de GCP con $300 en créditos
- ✅ Un proyecto configurado para nuestra aplicación
- ✅ Alertas de presupuesto configuradas
- ✅ gcloud CLI instalada y autenticada
- ✅ APIs requeridas habilitadas

En la próxima guía, vamos a:
1. Subir nuestra imagen Docker a Artifact Registry
2. Desplegar en Cloud Run
3. Configurar las variables de entorno de forma segura
4. Configurar un dominio personalizado (opcional)

---

## Solución de Problemas

### Errores de "Permission denied"
- Asegúrate de haber seleccionado el proyecto correcto
- Confirma que las APIs están habilitadas (ver sección de Habilitar APIs necesarias)
- Prueba: `gcloud auth login` para refrescar credenciales

### Problemas con la cuenta de facturación
- La prueba gratuita requiere una tarjeta válida
- La facturación debe estar vinculada al proyecto
- Verifica con: `gcloud beta billing projects describe cyber-analyzer`

### Problemas con la instalación de CLI
- Windows: Ejecuta el instalador como Administrador
- Mac/Linux: Asegúrate de tener instalado curl
- Todos: Reinicia tu terminal tras la instalación

### Project ID vs Project Name
- Project Name: Nombre amigable (ej: "cyber-analyzer")
- Project ID: Identificador globalmente único (ej: "cyber-analyzer-123456")
- Usa el Project ID en los comandos

### ¿Sigues atascado?
- La consola de GCP tiene un botón de ayuda **"?"** (arriba a la derecha)
- Cloud Shell (terminal en el navegador) está disponible como respaldo
- Soporte comunitario en https://cloud.google.com/community

---

## Consejos para Ahorrar Costos 💰

1. **Cloud Run solo cobra mientras está en ejecución**: ¡perfecto para aprender!
2. **Elimina los recursos no usados** inmediatamente después de los labs
3. **Usa instancias mínimas** (configuraremos esto en 0)
4. **Monitorea los costos semanalmente** en la sección de Billing
5. **Configura alertas de presupuesto** (¡lo acabas de hacer!)

### Lo gratis de la capa Always Free
Incluso después de agotar tus $300 de crédito, tienes:
- Cloud Run: 2 millones de requests/mes gratis
- Cloud Storage: 5GB gratis
- Cloud Build: 120 minutos de builds/día gratis

Recuerda: A diferencia de Azure Container Apps, Cloud Run puede escalar realmente a cero, ¡así que no hay costo cuando no está en uso!

---

## Referencia Rápida de Comandos

```bash
# Login
gcloud auth login

# Set project
gcloud config set project cyber-analyzer-xxxxx

# List configurations
gcloud config list

# Get help
gcloud help
gcloud run --help

# View costs
gcloud billing accounts list
```

Ten esta guía a mano: vamos a referenciar estos comandos en la guía de despliegue.