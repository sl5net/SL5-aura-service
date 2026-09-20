<img src="data/image/logo.svg" align="right" width="150" alt="⬟ Logotipo de SL5 Aura">

# ⬟ SL5 Aura – Tu Voz. Tus Reglas.

<!-- Insignias de Stack Overflow y la Comunidad -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% fuera de línea, marco de asistente de voz centrado en la privacidad.  
> Define exactamente lo que hace tu voz — desde una sola palabra
> a scripts completos de Python. Sin nube. Ningún dato sale de tu máquina.  
> Se ejecuta en la terminal, navegador o como un servicio en segundo plano, en Linux, macOS y Windows.

| 👵 Principiante | 🎓 Estudiante | 🧑‍💻 Desarrollador |
|---|---|---|
| [grandma-mode](../docs/GettingStarted-eslang.md#the-oma-modus-beginner-shortcut): solo escribe una palabra, Aura hace el resto | Aprende con Koans — un concepto a la vez | Script completo en Python, complementos, llamadas API |
| 🗄️ Gestión del Estado | Orquestación Trino + Airflow, fzf, CopyQ, comandos de voz/terminal, interfaces de usuario del navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** por prueba (39 pruebas sin LanguageTool en más de 800 mapas @ 0,07 s en caliente / 0,36 s en frío 🌿 medido con [Eco-CI](https://metrics.green-coding.io/index.html)) · sin computación en la nube

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Suite de pruebas completa:** 94 pruebas con LanguageTool en más de 800 mapas @ 0,07 s en caliente / 0,46 s en frío · sin computación en la nube

<detalles>
<resumen>Inicio Rápido</resumen>## Quick Start

### Option A: 1-Click & Web Installer (Recommended)

One-liner command or standalone installer for Linux, macOS, and Windows:
- **[→ Installer Guide & Direct Downloads](docs/OneClickInstaller.md)**

---

### Option B: Manual Installation (Developers / Git)

1. Download or clone this repository
2. Run the setup script for your OS (see `setup/` folder):
   - Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - Linux (openSUSE): `bash setup/suse_setup.sh`
   - Linux (NixOS): `nix-shell setup/shell.nix` then `bash setup/nixos_setup.sh`
   ===> ⚠️ Experimental — untested by authors, feedback welcome!   
   - macOS: `bash setup/macos_setup.sh`
   - Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Start Aura: `./scripts/restart_venv_and_run-server.sh`
4. Press your hotkey and speak — **[full guide →](docs/GettingStarted.md)**

---

### Uninstallation
To remove SL5 Aura background services, autostart entries, and virtual environments:
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


**⚠️ System Requirements & Compatibility**

*   **Windows:** ✅ Fully supported (uses AutoHotkey/PowerShell).
*   **macOS:** ✅ Fully supported (uses AppleScript).
*   **Linux (X11/Xorg):** ✅ Fully supported.
*   **Linux (Wayland):** ✅ Fully supported (tested on KDE Plasma 6 / Wayland).
*   **Linux (CachyOS / Arch-based rolling release):** ✅ Fully supported.
    Requires mimalloc (`sudo pacman -S mimalloc`) due to glibc 2.43 compatibility.
*   **Linux (NixOS):** 🧪 Experimental — community-contributed setup, not yet tested.
    If you try it, please open an issue or PR with your findings!    
*   **Linux (Manjaro):** New : A system-wide hotkey opens an fzf-like, keyboard-driven interface so you can run Aura commands from anywhere on the desktop (completely decoupled from the active window). This hotkey-driven launcher is currently implemented and tested on Linux (Manjaro); other distributions may work but require the setup . See in 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md)    


    
SL5 Aura is a complete, **offline voice assistant** built on **Vosk** (for Speech-to-Text) and **LanguageTool** (for Grammar/Style), featuring an optional **Local LLM (Ollama) Fallback** for creative responses and advanced fuzzy matching. It transforms your voice into precise actions and text, designed for ultimate customization through a pluggable rule system and a dynamic scripting engine.
    
Translations: This document also exists in [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Note: Many texts are machine-generated translations of the original English documentation and are intended for general guidance only. In case of discrepancies or ambiguities, the English version always prevails. We welcome help from the community to improve this translation!

</details>

<details>
<summary>Demo</summary>

### 📺 Terminal Demo 

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Tip:** For a better terminal experience, see [Zsh Integration](docs/linux/zsh-integration.md).

### 🎥 Video Tutorial
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>Key Features</summary>

## Características clave

*   **Desconectado y privado:** 100% local. Ningún dato sale jamás de tu equipo.
*   **Motor de Scripting Dinámico:** Ve más allá de la sustitución de texto. Las reglas pueden ejecutar scripts personalizados en Python (`on_match_exec`) para realizar acciones avanzadas como llamar a APIs (por ejemplo, buscar en Wikipedia), interactuar con archivos (por ejemplo, gestionar una lista de tareas) o generar contenido dinámico (por ejemplo, un saludo por correo electrónico consciente del contexto).
*   **Reglas conscientes del contexto:** Restringe las reglas a aplicaciones específicas. Usando `only_in_windows`, puedes asegurarte de que una regla solo se active si un título de ventana específico (por ejemplo, "Terminal", "VS Code" o "Browser") está activo. Esto funciona en todas las plataformas (Linux, Windows, macOS).
*  **Motor de Transformación de Alto Control:** Implementa un flujo de procesamiento altamente personalizable y dirigido por configuración. La prioridad de las reglas, la detección de comandos y las transformaciones de texto se determinan únicamente por el orden secuencial de las reglas en los Mapas Difusos, requiriendo **configuración, no codificación**.
*   **Uso conservador de RAM:** Gestiona la memoria de manera inteligente, precargando los modelos solo si hay suficiente RAM disponible, asegurando que otras aplicaciones (como tus juegos de PC) siempre tengan prioridad.
*   **Multiplataforma:** Funciona en Linux, macOS y Windows.
*   **Totalmente Automatizado:** Gestiona su propio servidor de LanguageTool (pero también puedes usar uno externo).
*   **Rápido como un rayo:** La memoria caché inteligente garantiza notificaciones de "Escuchando..." instantáneas y un procesamiento rápido.
*   **Gestión Dinámica del Estado a través de Trino:** Motor de configuración consciente de la interfaz
    separa la configuración para `speech`, `terminal` y `web` — cambia uno sin 
    afectando a los demás. Incluye un **Panel de Administración** en tiempo real (puerto 8084).
</detalles>

<detalles>
<summary> 🔌 Integraciones Listas para Usar</summary>
  XESPACIOPAUSAX## 🔌 Integraciones Listas para Usar

SL5-Aura viene con un vasto ecosistema de más de **100+ plugins preconfigurados**. Aquí hay algunos aspectos destacados:

### Control de Voz del IDE OculiX / SikuliX
SL5-Aura ofrece soporte de voz de primera clase para **OculiX** y **SikuliX IDE**. Esta integración te permite "hablar" tu código de automatización.

*   **De voz a fragmento:** Di "click", "wait" o "find all", y el servicio escribe instantáneamente el código Python correcto (por ejemplo, `click("image.png")`) en el IDE.
*   **Consciente de la ventana:** El complemento es sensible al contexto; solo se activa cuando la ventana de OculiX/SikuliX está enfocada.
*   **Soporte Inteligente de Inglés:** Optimizado para `en-US` con un enfoque especial en acentos no nativos (por ejemplo, fonética alemán-inglés), asegurando una alta precisión de reconocimiento para la comunidad global.
*   **Extensible:** Utiliza el formato `FUZZY_MAP_pre.py`, fácil de editar.

> **Estado:** Reconocido como un plugin comunitario por el equipo de OculiX (ver [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Control por Voz del IDE de LibreOffice

### 0 A.D. Control por Voz

---

</detalles>


<detalles>
<summary>Documentación</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)## Documentación

Para una referencia técnica completa, incluyendo todos los módulos y scripts, por favor visite nuestra página oficial de documentación. Se genera automáticamente y siempre está actualizada.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### Destacados de Funciones
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run-eslang.md) — Búsqueda de reglas `fzf` de doble panel, vistas previas de contexto en vivo, ejecución instantánea de comandos mediante `Enter`/`Ctrl+R` e integración con el editor mediante `Ctrl+E`. Soportado por una tecla de acceso global (`Super+S`) y múltiples entornos de búsqueda dedicados preconfigurados mediante comandos de voz.

### Estado de la compilación

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Observadores de estrellas">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="Licencia">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentación">
</a>
</div>

</detalles>

👉 **Leer esto en otros idiomas:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-eslang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-eslang.md) | [🇪🇸 Español](../README.i18n/README-eslang.md) | [🇫🇷 Français](../README.i18n/README-frlang-eslang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-eslang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-eslang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-eslang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-eslang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-eslang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-eslang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-eslang.md)

---

<detalles>
<summary>Instalación</summary>## Installation

### 🎥 Quick Installation without moderation (Manjaro/Arch Video)
Watch the full 6-minute setup process:
* **Download:** ~3 minutes
* **Setup & First Start:** ~3 minutes (including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


The setup is a two-step process:
1.  Download the latest Release or master ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) or clone this repository to your computer.
2.  Run the one-time setup script for your operating system.

The setup scripts handle everything: system dependencies, Python environment, and downloading the necessary models and tools (~4GB) directly from our GitHub Releases for maximum speed.


#### For Linux, macOS, and Windows (with Optional Language Exclusion)

To save disk space and bandwidth, you can exclude specific language models (`de`, `en`) or all optional models (`all`) during setup. **Core components (LanguageTool, lid.176) are always included.**

Open a terminal in the project's root directory and run the script for your system:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

`sudo pacman -S mimalloc`


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

#### For Windows
Run the setup script with administrator privileges.

**Install a tool to read and run, e.g., [CopyQ](https://github.com/hluk/CopyQ) or [AutoHotkey v2](https://www.autohotkey.com/)**. This is required for the text-typing watcher.

The installation is fully automated and takes about **8-10 minutes** when using 2 Models on a fresh system.

1. Navigate to the `setup` folder.
2. Double-click on **`windows11_setup_with_ahk_copyq.bat`**.
   * *The script will automatically prompt for Administrator privileges.*
   * *It installs the Core System, Language Models, **AutoHotkey v2**, and **CopyQ**.*
3. Once the installation is complete, **Aura Dictation** will launch automatically.

> **Note:** You do not need to install Python or Git beforehand; the script handles everything.

---

#### Advanced / Custom Installation
If you prefer not to install the client tools (AHK/CopyQ) or want to save disk space by excluding specific languages, you can run the core script via the command line:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>Usage</summary>

## Uso

### 1. Iniciar los Servicios

#### En Linux y macOS
Un único script maneja todo. Inicia el servicio principal de dictado y el monitor de archivos automáticamente en segundo plano.
__BLOQUE_DE_CÓDIGO_0__

#### En Windows
Iniciar el servicio es un **proceso manual de dos pasos**:

1.  **Inicia el Servicio Principal:** Ejecuta `start_aura.bat`. o inicia el servicio desde `.venv` con `python3`

### 2. Configura tu tecla de acceso rápido

Para activar la dictado, necesitas un atajo de teclado global que cree un archivo específico. Recomendamos encarecidamente la herramienta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nuestra recomendación: CopyQ

Crea un nuevo comando en CopyQ con un atajo global.

**Comando para Linux/macOS:**
__BLOQUE_DE_CÓDIGO_1__

**Comando para Windows al usar [CopyQ](https://github.com/hluk/CopyQ):**
__BLOQUE_DE_CÓDIGO_2__


**Comando para Windows al usar [AutoHotkey](https://AutoHotkey.com):**
__BLOQUE_DE_CÓDIGO_3__


### 3. ¡Comienza a dictar!
Haga clic en cualquier campo de texto, presione su tecla de acceso rápido y aparecerá una notificación de "Escuchando...". Hable claramente, luego haga una pausa. El texto corregido se escribirá por usted.

</detalles>

---


<detalles>
<summary>Configuración avanzada (Opcional)</summary>## Configuración Avanzada (Opcional)

Puedes personalizar el comportamiento de la aplicación creando un archivo de configuración local.

1. Navega al directorio `config/`.
2. Crea una copia de `config/settings_local.py_Example.txt` y cámbiale el nombre a `config/settings_local.py`.
3. Edita `config/settings_local.py` (este sobrescribe cualquier configuración del archivo principal `config/settings.py`).

Este archivo `config/settings_local.py` es ignorado por Git por defecto, por lo que tus cambios personales no serán sobrescritos por actualizaciones.

### Estructura y lógica del complemento

La modularidad del sistema permite una ampliación robusta a través del directorio plugins/.

El motor de procesamiento se adhiere estrictamente a una **Cadena de Prioridad Jerárquica**:

1. **Orden de Carga de Módulos (Alta Prioridad):** Las reglas cargadas desde los paquetes de idioma principales (de-DE, en-US) tienen prioridad sobre las reglas cargadas desde el directorio plugins/ (que se cargan al final alfabéticamente).
  XESPACIOPAUSAX
2. **Orden dentro del archivo (Prioridad micro):** Dentro de cualquier archivo de mapa dado (FUZZY_MAP_pre.py), las reglas se procesan estrictamente por **número de línea** (de arriba hacia abajo).
  XESPACIOINTERRUMPIRX

Esta arquitectura asegura que las reglas principales del sistema estén protegidas, mientras que las reglas específicas del proyecto o conscientes del contexto (como las de CodeIgniter o los controles de juegos) pueden añadirse fácilmente como extensiones de baja prioridad a través de complementos.

</detalles>

<detalles>
<summary>Scripts clave para usuarios de Windows</summary>## Scripts clave para usuarios de Windows

Aquí hay una lista de los scripts más importantes para configurar, actualizar y ejecutar la aplicación en un sistema Windows.

### Configuración y Actualización

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: El script principal para la **configuración inicial única** del entorno.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Ejecutar powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Ejecuta esto desde la carpeta del proyecto para **obtener el código y las dependencias más recientes**.

### Ejecutando la Aplicación
*   `start_aura.bat`: Un script principal para **iniciar el servicio de dictado**.

### Scripts Principales y Auxiliares
*   `aura_engine.py`: El servicio central de Python (generalmente iniciado por uno de los scripts mencionados arriba).
*   `get_suggestions.py`: Un script auxiliar para funcionalidades específicas.

</detalles>## 🚀 Key Features & OS Compatibility

<details>
<summary>Legend for OS Compatibility</summary>

Legend for OS Compatibility:  
*   🐧 **Linux** (e.g., Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **Windows**  
*   📱 **Android** (for mobile-specific features)  

---

</details>



### **Core Speech-to-Text (Aura) Engine**
    Our primary engine for offline speech recognition and audio processing.

    
<details>
<summary>Aura-Core</summary>
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Main Python service orchestrating Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config & Maps) 🐧 🍏 🪟  
│├ **Secure Private Map Loading (Integrity-First)** 🔒  🐧 🍏 🪟  
││ * **Workflow:** Loads password-protected ZIP archives.   
│├ **Text Processing & Correction/** Grouped by Language ( e.g. `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardizes punctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **Intelligent Pre-Correction** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules.md)) 🐧 🍏 🪟  
││ * **Dynamic Script Execution:** Rules can trigger custom Python scripts (`on_match_exec`) to perform advanced actions like API calls, file I/O, or generate dynamic responses.  
││ * **Cascading Execution:** Rules are processed sequentially and their effects are **cumulative**. Later rules apply to text modified by earlier rules.  
││ * **Highest Priority Stop Criterion:** If a rule achieves a **Full Match** (^...$), the entire processing pipeline for that token stops immediately. This mechanism is critical for implementing reliable voice commands.  
│├ 3. `correct_text_by_languagetool.py` (Integrates LanguageTool for grammar/style correction) 🐧 🍏 🪟  
│├ **4. Hierarchical RegEx-Rule-Engine with Ollama AI Fallback** 🐧 🍏 🪟  
││ * **Deterministic Control:** Uses RegEx-Rule-Engine for precise, high-priority command and text control.  
│├ **Vector-Search Plugin** (Lazy loading): Enables Semantic Search by connecting local Vector embeddings with the Ollama/LLM fallback layer 🐧  
││ * **Ollama AI (Local LLM) Fallback:** Serves as an optional, low-priority check for **creative answers, Q&A, and advanced Fuzzy Matching** when no deterministic rule is met.  
││ * **Status:** Local LLM integration.
│└ 5. **Intelligent Post-Correction** (`FuzzyMap`)**– Post-LT Refinement** 🐧 🍏 🪟  
││ * Applied after LanguageTool to correct LT-specific outputs. Follows the same strict cascading priority logic as the Pre-Correction layer.  
││ * **Dynamic Script Execution:** Rules can trigger custom Python scripts ([on_match_exec](docs/advanced-scripting.md)) to perform advanced actions like API calls, file I/O, or generate dynamic responses.  
││ * **Fuzzy Fallback:** The **Fuzzy Similarity Check** (controlled by a threshold, e.g., 85%) acts as the lowest priority error-correction layer. It is only executed if the entire preceding deterministic/cascading rule run failed to find a match (current_rule_matched is False), optimizing performance by avoiding slow fuzzy checks whenever possible.  
├┬ **Model Management/**   
│├─ `prioritize_model.py` (Optimizes model loading/unloading based on usage) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configures the first-time model setup) 🐧 🍏 🪟  
├─ **Adaptive VAD Timeout** 🐧 🍏 🪟  
├─ **Adaptive Hotkey (Start/Stop)** 🐧 🍏 🪟  
├─ **Instant Language Switching** (Experimental via model preloading) 🐧 🍏         
├─ **Airflow Orchestration** (DAG-based workflow automation) 🐧 🍏 🪟
│   Requires Docker · UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino State Engine** (Interface-aware config per speech/terminal/web) 🐧 🍏 🪟
└─  Requires Docker · Admin UI: `http://localhost:8084` 🐧 🍏 🪟  

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_languagetool_server.py` (Initializes the local LanguageTool server) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Shuts down the LanguageTool server) 🐧 🍏 
├─ `monitor_mic.sh` (e.g. for use with Headset without use keyboard and Monitor) 🐧 🍏 🪟  

### **Model & Package Management**  
    Tools for robust handling of large language models.  

**ModelManagement/** 🐧 🍏 🪟  
├─ **Robust Model Downloader** (GitHub Release chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utility for repo owners to split large files and generate checksums) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool for end-users to download, verify, and reassemble multi-part files) 🐧 🍏 🪟  

</details>


<details>
<summary>Development & Deployment Helpers</summary>

### **Development & Deployment Helpers**  
    Scripts for environment setup, testing, and service execution.  

*Tip: glogg enables you to use regular expressions to search for interesting events in your log files.*     
Please check the checkbox when installing to associate with log-files.    
https://glogg.bonnefon.org/     
    
*Tip: After defining your regex patterns, run `python3 tools/map_tagger.py` to automatically generate searchable examples for the CLI tools. See [Map Maintenance Tools](docs/Developer_Guide/Map_Maintenance_Tools.md) for details.*

Then maybe double-click 
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ **Virtual Environment Management/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **System-wide Dictation Integration/**  
│├ Vosk-System-Listener Integration 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux-specific microphone monitoring) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey listens for recognized text and types it out system-wide) 🪟  
└─ **CI/CD Automation/**  
    └─ Expanded GitHub Workflows (Installation, testing, docs deployment) 🐧 🍏 🪟 *(Runs on GitHub Actions)*  

</details>

<details>
<summary>Experimental Features</summary>
    
### **Upcoming / Experimental Features**  
    Features currently under development or in draft status.  

**ExperimentalFeatures/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Example activation rule "(ExampleAplicationThatNotExist|Pi, your personal AI)" 🐧  
├┬Plugins  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)  
│ ├ **git commands** (Voice control for send git commands) 🐧 🍏 🪟  
│ ├ **wannweil** (Map for Location Germany-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Voice control for poker applications) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Voice control for 0 A.D. game) 🐧   
├─ **Sound Output when Start or End a Session** (Description pending) 🐧   
├─ **Speech Output for Visually Impaired** (Description pending) 🐧 🍏 🪟  
└─ **SL5 Aura Android Prototype** (Not fully offline yet) 📱  

---

*(Note: Specific Linux distributions like Arch (ARL) or Ubuntu (UBT) are covered by the general Linux 🐧 symbol. Detailed distinctions might be covered in installation guides.)*
</details>

<details>
<summary>Click to see the command used to generate this script list</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A graphical overview of the architecture</summary>

### A graphical overview of the architecture:

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)
</details>

<details>
<summary>Used Models</summary>

## Modelos Utilizados:

Recomendación: use modelos de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probablemente más rápido)

Estos modelos comprimidos deben guardarse en la carpeta `models/`

`mv vosk-model-*.zip models/`


| Modelo                                                                                 | Tamaño | Tasa de error de palabras/Velocidad                                                     | Notas                                     | Licencia    |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter)                       | Modelo genérico preciso de inglés estadounidense         | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)       | 1.9G | 9.83 (prueba Tuda)<br/>24.00 (podcast)<br/>12.82 (prueba cv)<br/>12.42 (mls)<br/>33.26 (mtedx) | Gran modelo alemán para telefonía y servidor | Apache 2.0 |

Esta tabla proporciona una visión general de los diferentes modelos de Vosk, incluyendo su tamaño, tasa de error de palabras o velocidad, notas e información sobre la licencia.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licencia de LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</detalles>## Apoya el Proyecto
Si encuentras útil esta herramienta, ¡por favor considera comprarnos un café! Tu apoyo ayuda a impulsar futuras mejoras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)