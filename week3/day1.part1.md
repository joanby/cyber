# Día 1 Parte 1: Guía de Configuración de Azure

Esta guía te mostrará cómo configurar tu cuenta de Azure y prepararla para desplegar aplicaciones contenerizadas. Todas las instrucciones funcionan tanto para usuarios de Windows como de Mac.


## Tabla de Contenidos
1. [Creando tu Cuenta de Azure](#creating-your-azure-account)
2. [Entendiendo la Estructura de Azure](#understanding-azures-structure)
3. [Configurando la Administración de Costos](#setting-up-cost-management)
4. [Creando tu Primer Grupo de Recursos](#creating-your-first-resource-group)
5. [Instalando Azure CLI](#installing-azure-cli)
6. [Verificando tu Configuración](#verifying-your-setup)

---

## Creando tu Cuenta de Azure

### Cuenta gratuita de Azure
1. Navega a https://azure.microsoft.com/en-us/free/
2. Haz clic en **"Start free"**
3. Inicia sesión con tu cuenta de Microsoft (o crea una)
4. Necesitarás proporcionar:
   - Una tarjeta de crédito (solo para verificación de identidad - no se te cobrará)
   - Número de teléfono para verificación
5. Recibirás:
   - $200 de crédito para 30 días
   - 12 meses de servicios populares gratuitos
   - Servicios siempre gratuitos

> **Nota**: Si tienes una dirección de correo .edu, podrías calificar para Azure for Students, que ofrece $100 de crédito por 12 meses sin necesidad de tarjeta de crédito. Visita https://azure.microsoft.com/en-us/free/students/ para más detalles.

⚠️ **Importante**: Después de crear tu cuenta, serás redirigido al Portal de Azure en https://portal.azure.com

---

## Entendiendo la Estructura de Azure

Antes de crear recursos, vamos a entender la jerarquía de Azure:

```
Azure Account (Tu correo)
  └── Subscription (ej: "Azure for Students")
      └── Resource Group (ej: "cyber-analyzer-rg")
          └── Resources (Container Apps, Registry, etc.)
```

Piensa en:
- **Subscription**: Tu límite de facturación (como una tarjeta de crédito)
- **Resource Group**: Una carpeta para organizar recursos relacionados
- **Resources**: Los servicios reales que creas

---

## Configurando la Administración de Costos

Vamos a configurar una alerta de presupuesto para evitar sorpresas:

1. En el Portal de Azure (https://portal.azure.com), usa la barra de búsqueda en la parte superior
2. Escribe **"Cost Management"** y selecciona **"Cost Management + Billing"**
3. En el menú de la izquierda, haz clic en **"Cost Management"**
4. Haz clic en **"Budgets"**
5. Haz clic en **"+ Add"**
6. Configura tu presupuesto:
   - **Name**: `Monthly-Training-Budget`
   - **Reset period**: Monthly
   - **Budget amount**: `10` (mantén los costes mínimos)
   - Haz clic en **"Next"**
7. Configura alertas:
   - **Alert conditions**:
     - 50% del presupuesto → Alerta por email
     - 80% del presupuesto → Alerta por email
     - 100% del presupuesto → Alerta por email
   - Ingresa tu correo electrónico
   - Haz clic en **"Create"**

✅ ¡Ahora recibirás alertas por email antes de gastar demasiado!

---

## Creando tu Primer Grupo de Recursos

Los grupos de recursos organizan tus recursos de Azure. Vamos a crear uno:

1. En el Portal de Azure, haz clic en el icono de menú **"☰"** (arriba a la izquierda)
2. Selecciona **"Resource groups"**
3. Haz clic en **"+ Create"**
4. Rellena los detalles:
   - **Subscription**: Selecciona tu suscripción
   - **Resource group**: `cyber-analyzer-rg`
   - **Region**: Elige una cercana a ti:
     - US: `East US` o `West US 2`
     - Europa: `West Europe` o `North Europe`
     - Asia: `Southeast Asia` o `Japan East`
   
   💡 **Consejo profesional**: ¡Recuerda esta región! Todos los recursos en este grupo deberían usar la misma región para mejor rendimiento y menor costo.

5. Haz clic en **"Review + create"**
6. Haz clic en **"Create"**

🎉 ¡Has creado tu primer grupo de recursos!

---

## Instalando Azure CLI

La Azure CLI es esencial para operaciones de despliegue y trabajar con aplicaciones contenerizadas.

### Usuarios de Windows
1. Descarga el instalador MSI de: https://aka.ms/installazurecliwindows
2. Ejecuta el archivo descargado y sigue el asistente de instalación
3. Reinicia cualquier ventana de terminal que tengas abierta

### Usuarios de Mac
Opción 1 - Usando Homebrew (si lo tienes):
```bash
brew update && brew install azure-cli
```

Opción 2 - Instalación directa:
1. Descarga el instalador de: https://aka.ms/installazureclimacos
2. Ejecuta el archivo .pkg descargado
3. Sigue el asistente de instalación

### Verifica la Instalación (Ambas Plataformas)
Abre una nueva terminal o línea de comandos y ejecuta:
```bash
az --version
```

Deberías ver información de la versión. Si no, reinicia tu terminal.

### Inicia sesión en Azure CLI
Ahora vamos a conectar la CLI con tu cuenta:
```bash
az login
```

Esto abrirá tu navegador. Inicia sesión con tu cuenta de Azure.

---

## Verificando tu Configuración

Vamos a asegurarnos de que todo funcione correctamente:

### Usando el Portal de Azure
1. Ve a https://portal.azure.com
2. En la barra de búsqueda, escribe el nombre de tu grupo de recursos: `cyber-analyzer-rg`
3. Haz clic en él - deberías ver:
   - La localización coincide con la elegida
   - Sin recursos aún (¡esto es correcto!)

### Usando Azure CLI
Ejecuta estos comandos:
```bash
# Lista tus suscripciones
az account list --output table

# Lista tus grupos de recursos
az group list --output table
```

Deberías ver tu suscripción y el grupo de recursos `cyber-analyzer-rg`.

---

## ¿Qué sigue?

¡Felicidades! Tu cuenta de Azure ya está lista. Ahora tienes:
- ✅ Una cuenta de Azure con créditos
- ✅ Alertas de costo configuradas
- ✅ Un grupo de recursos para nuestro proyecto
- ✅ Azure CLI instalada y configurada

En la próxima guía:
1. Crearemos un Azure Container Registry
2. Subiremos nuestra imagen Docker
3. Desplegaremos en Azure Container Apps
4. Configuraremos variables de entorno de forma segura

---

## Resolución de Problemas

### Errores de "Subscription not found"
- Asegúrate de iniciar sesión con la cuenta correcta
- Verifica que hayas completado la configuración de la cuenta
- Prueba cerrar sesión y volver a entrar

### Problemas eligiendo región
- Algunas regiones pueden no tener todos los servicios
- Usa regiones principales (US East, West Europe, etc.)
- Todos los recursos de un grupo deben usar la misma región

### Problemas instalando la CLI
- Windows: Ejecuta el instalador como Administrador
- Mac: Asegúrate de tener permisos de administrador
- Ambos: Reinicia la terminal después de instalar

### ¿Sigues atascado?
- El Portal de Azure tiene un botón de ayuda **"?"** (arriba a la derecha)
- Hay soporte por chat en vivo para la mayoría de los problemas
- Consulta los recursos IT de tu escuela, pueden tener guías de Azure

---

## Consejos de Ahorro de Costos 💰

1. **Elimina siempre los recursos** cuando termines los laboratorios
2. **Usa la tarifa más baja** para aprender (te mostraremos cómo)
3. **Configura alertas de presupuesto** (¡que ya acabas de hacer!)
4. **Revisa Cost Management semanalmente** para entender tus gastos
5. **Usa niveles gratuitos** siempre que sea posible

Recuerda: Los Container Apps sólo cobran mientras están en ejecución, ¡lo cual es perfecto para aprender!