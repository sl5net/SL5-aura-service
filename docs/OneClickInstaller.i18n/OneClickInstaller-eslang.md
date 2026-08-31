# Instalador de 1 clic (configuración cero)

Ponga **Aura** en funcionamiento en su máquina con un solo clic. No se requieren conocimientos de programación, comandos de terminal ni configuración manual de Python.

---

## Cero requisitos previos

**No** necesitas:
- Python preinstalado
- Git o repositorios de código
- Experiencia en línea de comandos o terminal

---

## Inicio rápido

### Método 1: Web One-Liner (más rápido y recomendado para Linux/macOS)
Ahorra ~30 segundos de manejo manual de archivos y se inicia inmediatamente en tu terminal:

**Linux y macOS:**

```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
```bash

# In development - please use Method 2 (standalone binary) for Windows

irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Método 2: binario independiente (clic en Windows y escritorio)

### 2.1 Descargar el instalador
Descargue el archivo de instalación único que coincida con su sistema operativo desde la [Última versión de GitHub]:

- **Windows:** XMLDLINK0X
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Ejecute el instalador

cambie el nombre de aura-installer-windows.exe.zip a aura-installer-windows.exe

Haga doble clic en el archivo descargado. Aparecerá una ventana de configuración y preparará automáticamente el entorno.

### 2.3. Empezar a dictar
Una vez terminado, Aura crea un acceso directo en el escritorio y comienza a escuchar inmediatamente.

---

## ¿Qué sucede automáticamente?

Cuando ejecutas el instalador, Aura automáticamente:
- Configura el motor de reconocimiento de voz local y privado.
- Descarga los modelos de voz predeterminados.
- Configura todos los accesos directos del sistema y los lanzadores de escritorio necesarios.

---

## Detalles y requisitos de instalación

- **Duración de la instalación:** Aproximadamente 2 a 3 minutos.
- **Espacio en disco requerido:** Mínimo ~1,5 GB (hasta 2,5 GB según los modelos de idioma seleccionados).
- **Directorio de instalación:**
- **Linux y macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Próximos pasos

- **Modo abuela:** Escribe una sola palabra en tu archivo de reglas y observa cómo Aura crea reglas automáticamente.
- **Aprende con Koans:** Explora conceptos paso a paso en [Getting Started](../GettingStarted.i18n/GettingStarted-eslang.md).