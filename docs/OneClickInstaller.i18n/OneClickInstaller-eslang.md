> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# Instalador de 1 clic (configuración cero)

Ponga **Aura** en funcionamiento en su máquina con un solo clic. No se requieren conocimientos de programación, comandos de terminal ni configuración manual de Python.

---

## Cero Requisitos Previos

No necesitas:
- Python preinstalado
- Repositorios de Git o de código
- Experiencia en línea de comandos o terminal

---

## Inicio Rápido

### Método 1: Una línea web (Más rápido y recomendado para Linux / macOS)
Ahorra ~30 segundos de manejo manual de archivos y se inicia inmediatamente en tu terminal:

**Linux y macOS:**
#### Código de una línea para Web en CodeBerg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
o
#### GitHub de una sola línea web
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Código de una línea Web en CodeBerg

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
o
#### Línea única web github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Método 2: Binario independiente (Windows y clic de escritorio)

### 2.1 Descargar el instalador
Descargue el archivo único de instalación que coincida con su sistema operativo desde el [Último Lanzamiento en GitHub]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Ejecutar el instalador

renombrar aura-installer-windows.exe.zip a aura-installer-windows.exe

Haga doble clic en el archivo descargado. Aparecerá una ventana de instalación y preparará automáticamente el entorno.

### 2.3. Comenzar a Dictar
Una vez terminado, Aura crea un acceso directo en el escritorio y comienza a escuchar de inmediato.

---

## ¿Qué sucede automáticamente?

Cuando ejecutas el instalador, Aura automáticamente:
- Configura el motor de reconocimiento de voz local y privado.
- Descarga los modelos de voz predeterminados.
- Configura todos los accesos directos del sistema y los lanzadores de escritorio necesarios.

---

## Detalles y Requisitos de Instalación

- **Duración de la instalación:** Aproximadamente 2–3 minutos.
- **Espacio en disco requerido:** Mínimo ~1,5 GB (hasta 2,5 GB dependiendo de los modelos de idioma seleccionados).
- **Directorio de instalación:**
  - **Linux y macOS:** `~/opt/sl5-aura-service`
  - **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Próximos pasos

- **Modo-Abuela:** Escribe una sola palabra en tu archivo de reglas y observa cómo Aura crea reglas automáticamente.
- **Aprende con Koans:** Explora conceptos paso a paso en [Getting Started](../GettingStarted.i18n/GettingStarted-eslang.md).
