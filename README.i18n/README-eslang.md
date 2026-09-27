> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo"> 

# ⬟ SL5 Aura – Tu Voz. Tus reglas

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> Marco de asistente de voz 100% fuera de línea y que prioriza la privacidad.  
> Define exactamente lo que hace tu voz, a partir de una sola palabra  
> a scripts completos de Python. Ninguna nube. No salen datos de su máquina.  
> Se ejecuta en terminal, navegador o como servicio en segundo plano (en Linux, macOS y Windows).

| 👵 Principiante | 🎓 Estudiante | 🧑‍💻 Desarrollador |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-eslang.md#the-oma-modus-beginner-shortcut): solo escribe una palabra, Aura hace el resto | Aprende con Koans — un concepto a la vez | Script completo en Python, complementos, llamadas API |
| 🗄️ Gestión del estado | Trino + orquestación de Airflow, fzf, CopyQ, comandos de voz/terminal, interfaces de navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** por prueba (39 pruebas sin LanguageTool en más de 800 mapas @ 0,07 s en caliente / 0,36 s en frío 🌿 medido con [Eco-CI](https://metrics.green-coding.io/index.html)) · sin computación en la nube

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Suite de pruebas completa:** 94 pruebas con LanguageTool en más de 800 mapas @ 0,07 s en caliente / 0,46 s en frío · sin computación en la nube

<details>
<summary>Inicio rápido</summary>

## Inicio rápido

### Opción A: Instalador web y de 1 clic (Recomendado)

Comando de una línea o instalador independiente para Linux, macOS y Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-eslang.md)**

---

### Opción B: Instalación manual (Developers / Git)

1. Descargar o clonar este repositorio
2. Ejecute el script de configuración para su sistema operativo (ver carpeta `setup/`):
   - Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - Linux (openSUSE): `bash setup/suse_setup.sh`
   - Linux (NixOS): `nix-shell setup/shell.nix` luego `bash setup/nixos_setup.sh`
   ====] ︎י Experimental — no testado por los autores, retroalimentación bienvenida!   
   - macOS: `bash setup/macos_setup.sh`
   - Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Inicio Aura: `./scripts/restart_venv_and_run-server.sh`
4. Presione su hotkey y hable — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-eslang.md) * *

---

### Desinstalación
Para eliminar los servicios de fondo SL5 Aura, las entradas de autostart y entornos virtuales:
- **Linux / macOS: ** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Sus reglas personalizadas en `config/maps/` se mantienen seguras por defecto a menos que especifique `--purge`). *

---


Requisitos del sistema y compatibilidad *

*   **Windows:** ✅ Fully supported (uses AutoHotkey/PowerShell).
*   **macOS:** Identificar el soporte completo (utiliza AppleScript).
*   **Linux (X11/Xorg):** Totalmente apoyado.
*   **Linux (Wayland):** ✅ Fully supported (tested on KDE Plasma 6 / Wayland).
*   **Linux (CachyOS / versión rodante arqueada):** Totalmente apoyado.
    Requiere mimalloc (`sudo pacman -S mimalloc`) debido a la compatibilidad glibc 2.43.
*   **Linux (NixOS):** 🧪 Experimental — configuración contribuida por la comunidad, aún no probada.
    Si lo intentas, por favor abre un problema o PR con tus hallazgos!    
*   **Linux (Manjaro):** Nuevo : Un hotkey a nivel de todo el sistema abre una interfaz tipo fzf, con teclado para que pueda ejecutar comandos Aura desde cualquier lugar en el escritorio (completamente decoupled desde la ventana activa). Este lanzador impulsado por teclas calientes está actualmente implementado y probado en Linux (Manjaro); Otras distribuciones pueden funcionar pero requieren la configuración. Ver en latitud [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-eslang.md)    


    
SL5 Aura es un completo asistente de voz **offline** construido en **Vosk** (para Speech-to-Text) y **LanguageTool** (para Grammar/Style), con un opcional **Local LLM (Ollama) Fallback** para las respuestas creativas y el emparejado avanzado. Transforma su voz en acciones y texto precisos, diseñados para la máxima personalización a través de un sistema de reglas pluggable y un motor de scripting dinámico.
    
Traducciones: Este documento también existe en [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Nota: Muchos textos son traducciones generadas por máquina de la documentación original en inglés y están destinados únicamente a la orientación general. En caso de discrepancias o ambigüedades, siempre prevalece la versión en inglés. Damos la bienvenida a la ayuda de la comunidad para mejorar esta traducción!

</details>

<details>
<summary>Demo</summary>

### 📺 Demo de Terminal

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Consejo:** Para una mejor experiencia en el terminal, consulte [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-eslang.md).

### 🎥 Tutorial en video
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Enlace alternativo: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>Características clave</summary>

## Características clave

*   **Offline &quot; Private:** 100% local. Ningún dato deja tu máquina.
*   ** Motor de scripting Dinámico:** Ir más allá de la sustitución de texto. Las reglas pueden ejecutar scripts Python personalizados (`on_match_exec`) para realizar acciones avanzadas como llamar API (por ejemplo, buscar Wikipedia), interactuar con archivos (por ejemplo, gestionar una lista de tareas), o generar contenido dinámico (por ejemplo, un saludo de correo electrónico con conocimiento de contexto).
*   **Reglas de Contexto:** Restringir reglas a aplicaciones específicas. Utilizando `only_in_windows`, puedes asegurar que una regla sólo activa si un título de ventana específico (por ejemplo, "Terminal", "VS Code" o "Browser") es activo. Esto funciona multiplataforma (Linux, Windows, macOS).
*  **High-Control Transformation Engine:** Implementa un oleoducto de procesamiento basado en la configuración, altamente personalizable. La prioridad de reglas, la detección de comandos y las transformaciones de texto se determinan únicamente por el orden secuencial de reglas en los mapas borrosos, lo que requiere **configuración, no codificación**.
*   **Conservative RAM Usage:** Gestiona inteligentemente la memoria, precargando modelos sólo si hay suficiente RAM gratuita disponible, asegurando que otras aplicaciones (como tus juegos de PC) siempre tengan prioridad.
*   **Cross Platform:** Funciona en Linux, macOS y Windows.
*   ** Totalmente Automatizado:** Gestiona su propio servidor LanguageTool (pero también puede utilizar uno externo).
*   **Blazing Fast:** El caché inteligente garantiza notificaciones instantáneas "Listening..." y procesamiento rápido.
*   **Dynamic State Management via Trino:** Motor de configuración de interfaz
    separa la configuración de `speech`, `terminal` y `web` — cambiar uno sin
    Afectando a los otros. Incluye un Dashboard **A tiempo real** (puerto 8084).
</details>

<details>
<summary>Integraciones listas a uso</summary>
    
## 🔌 Integraciones listas para usar

SL5-Aura viene con un vasto ecosistema de más de **100+ plugins preconfigurados**. Aquí hay algunos aspectos destacados:

OculiX / SikuliX Control de voz IDE
SL5-Aura proporciona soporte de voz de primera clase para el **OculiX** y **SikuliX IDE**. Esta integración le permite "hablar" su código de automatización.

*   **Voice-to-Snippet:** Diga "click", "espera", o "encuentre todo", y el servicio instantáneamente escribe el código Python correcto (por ejemplo, `click("image.png")`) en el IDE.
*   **Window-Aware:** El plugin es sensible al contexto; sólo se activa cuando la ventana OculiX/SikuliX está enfocada.
*   **Apoyo inteligente en inglés:** Optimizado para `en-US` con un enfoque especial en acentos no nativos (por ejemplo, fonética alemana-inglés), garantizando una alta precisión de reconocimiento para la comunidad mundial.
*   *Extensible* Utiliza el formato `FUZZY_MAP_pre.py` fácil de editar.

> **Status:** Reconocido como un campo comunitario por el equipo OculiX (ver [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Control de voz de LibreOffice IDE

### 0 A.D. Control por Voz

---

</details>


<details>
<summary>Documentación</summary>

## Documentación

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

Para una referencia técnica completa, incluyendo todos los módulos y scripts, por favor visite nuestra página oficial de documentación. Se genera automáticamente y siempre está actualizada.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### Características Destacadas
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-eslang.md) — Búsqueda de reglas `fzf` de doble panel, vistas previas de contexto en vivo, ejecución instantánea de comandos a través de `Enter`/`Ctrl+R`, e integración con el editor a través de `Ctrl+E`. Compatible con una tecla de acceso rápido global (`Super+S`) y múltiples entornos de búsqueda dedicados preconfigurados mediante comandos de voz.

### Estado de la compilación

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

👉 **Leer esto en otros idiomas:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-eslang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-eslang.md) | [🇪🇸 Español](../README.i18n/README-eslang.md) | [🇫🇷 Français](../README.i18n/README-frlang-eslang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-eslang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-eslang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-eslang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-eslang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-eslang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-eslang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-eslang.md)

---

<details>
<summary>Instalación</summary>

## Instalación

### 🎥 Instalación rápida sin moderación (Manjaro/Arch Video)
Vea el proceso completo de configuración de 6 minutos:
* **Descargar: ~3 minutos
* **Setup & First Start:** ~3 minutos (incluyendo el asistente de bienvenida)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


La configuración es un proceso de dos pasos:
1.  Descargar el último Release o master ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) o clonar este repositorio a su computadora.
2.  Ejecute el script de configuración única para su sistema operativo.

Los scripts de configuración manejan todo: dependencias del sistema, entorno Python, y descargando los modelos y herramientas necesarios (~4GB) directamente desde nuestras versiones GitHub para la máxima velocidad.


#### Para Linux, macOS y Windows (con exclusión opcional de idioma)

Para ahorrar espacio en el disco y ancho de banda, puede excluir modelos de idioma específicos (`de`, `en`) o todos los modelos opcionales (`all`) durante la configuración. **Los componentes principales (LanguageTool, lid.176) siempre están incluidos.**

Abre una terminal en el directorio raíz del proyecto y ejecuta el script para tu sistema:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


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

#### Para Windows
Ejecute el script de configuración con privilegios de administrador.

**Intente una herramienta para leer y ejecutar, por ejemplo, [CopyQ](https://github.com/hluk/CopyQ) o [AutoHotkey v2](https://www.autohotkey.com/)**. Esto es necesario para el reloj de texto.

La instalación es totalmente automatizada y toma alrededor de **8-10 minutos** al utilizar 2 Modelos en un sistema fresco.

1. Navegue a la carpeta `setup`.
2. Haga doble clic en **`windows11_setup_with_ahk_copyq.bat`**.
   * *El script pedirá automáticamente privilegios de Administrador. *
   * *Instala el Sistema Core, Modelos de Lengua, **AutoHotkey v2**, y **CopyQ**. *
3. Una vez que la instalación esté completa, **Aura Dictation** se lanzará automáticamente.

> **Nota:** Usted no necesita instalar Python o Git de antemano; El guión lo maneja todo.

---

#### Instalación avanzada / personalizada
Si prefieres no instalar las herramientas del cliente (AHK/CopyQ) o quieres ahorrar espacio en disco excluyendo idiomas específicos, puedes ejecutar el script principal a través de la línea de comandos:

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
<summary>Uso</summary>

## Uso

### 1. Iniciar los servicios

#### En Linux y macOS
Un solo script lo maneja todo. Inicia el servicio principal de dictado y el observador de archivos automáticamente en segundo plano.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### En Windows
Iniciar el servicio es un **proceso manual de dos pasos**:

1.  **Iniciar el Servicio Principal:** Ejecute `start_aura.bat`. o inicie desde `.venv` el servicio con `python3`

### 2. Configura tu tecla rápida

Para activar la dictado, necesitas un atajo de teclado global que cree un archivo específico. Recomendamos encarecidamente la herramienta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nuestra recomendación: CopyQ

Crea un nuevo comando en CopyQ con un atajo global.

**Comando para Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Comando para Windows cuando se usa [CopyQ](https://github.com/hluk/CopyQ):**
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**Comando para Windows cuando se usa [AutoHotkey](https://AutoHotkey.com):**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3. ¡Comienza a dictar!
Haga clic en cualquier campo de texto, presione su tecla de acceso rápido y aparecerá una notificación de "Escuchando...". Hable claramente, luego haga una pausa. El texto corregido se escribirá por usted.

</details>

---


<details>
<summary>Configuración avanzada (opcional)</summary>

## Configuración avanzada (opcional)

Puede personalizar el comportamiento de la aplicación creando un archivo de configuración local.

1.  Navega al directorio `config/`.
2.  Crear una copia de `config/settings_local.py_Example.txt` y renombrarla a `config/settings_local.py`.
3.  Editar `config/settings_local.py` (que anula cualquier configuración del archivo `config/settings.py` principal).

Este archivo `config/settings_local.py` es ignorado por Git por defecto, por lo que sus cambios personales no serán sobrescritos por actualizaciones.

Estructura de complemento y lógica

La modularidad del sistema permite una extensión robusta a través de los plugins/directorio.

El motor de procesamiento se adhiere estrictamente a una cadena prioritaria jerárquica ***:

1. ** Orden de carga moderada ( alta prioridad):** Las reglas cargadas de paquetes de lenguaje básico (de-DE, en-US) prevalecen sobre las reglas cargadas de los plugins/directorio (que cargan alfabéticamente).
    
2. **Orden In-File (Micro Priority):** Dentro de cualquier archivo de mapa dado (FUZZY MAP pre.py), las reglas se procesan estrictamente por **line number** (top-to-bottom).
    

Esta arquitectura garantiza que las reglas básicas del sistema estén protegidas, mientras que las reglas específicas del proyecto o del software contextual (como las de CodeIgniter o los controles del juego) se pueden añadir fácilmente como extensiones de baja prioridad a través de plug-ins.

</details>

<details>
<summary>Palabras clave para usuarios de Windows</summary>






## Scripts clave para usuarios de Windows

Aquí hay una lista de los scripts más importantes para configurar, actualizar y ejecutar la aplicación en un sistema Windows.

### Configuración y actualización

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: El script principal para la **configuración inicial única** del entorno.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Ejecuta esto desde la carpeta del proyecto para **obtener el código y las dependencias más recientes**.

### Ejecutando la aplicación
*   `start_aura.bat`: Un guion principal para **iniciar el servicio de dictado**.

### Scripts principales y auxiliares
*   `aura_engine.py`: El servicio principal de Python (generalmente iniciado por uno de los scripts mencionados arriba).
*   `get_suggestions.py`: Un script auxiliar para funcionalidades específicas.

</details>



## 🚀 Características clave y compatibilidad del sistema operativo

<details>
<summary>Leyenda para la compatibilidad del sistema operativo</summary>

Leyenda para la compatibilidad del sistema operativo:  
*   🐧 **Linux** (por ejemplo, Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **Ventanas**  
*   📱 **Android** (para funciones específicas de móviles)  

---

</details>



### **Core Speech-to-Text (Aura) Engine* *
    Nuestro motor primario para reconocimiento de voz y procesamiento de audio sin conexión.

    
<details>
<summary>Aura core</summary>

**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Main Python service orquestating Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config &amp; Maps) 🐧 🍏 🪟  
│├ ** Mapa privado seguro Cargando (Integridad-Primero)** 🔒  🐧 🍏 🪟  
││ * ** Flujo de trabajo** Carga archivos ZIP protegidos por contraseña.   
│├ **Procesamiento de texto Corrección/** agrupado por idioma (por ejemplo, `de-DE`, `en-US`, ...)   
│├ 1. `normalize_punctuation.py` (Standardizes punctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **Precorrección inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-eslang.md)) 🐧 🍏 🪟  
││ * **Ejecución del script Dinámico: Las reglas pueden desencadenar scripts Python personalizados (`on_match_exec`) para realizar acciones avanzadas como llamadas de API, archivo I/O, o generar respuestas dinámicas.  
││ * ** Ejecución decadente:** Las reglas se procesan secuencialmente y sus efectos son **cumulativos**. Las reglas posteriores se aplican al texto modificado por reglas anteriores.  
││ * **Críter de alto nivel de prioridad:** Si una regla alcanza un **Full Match** (^...$), toda la tubería de procesamiento para ese token se detiene inmediatamente. Este mecanismo es fundamental para implementar comandos de voz fiables.  
│├ 3. `correct_text_by_languagetool.py` (Integras LanguageTool para corrección de gramática/estilo) 🐧 🍏 🪟  
│├ **4. Motor de reglas de RegEx jerárquico con Ollama AI Fallback * * 🐧 🍏 🪟  
││ * **Control Determinístico:** Usa el motor de reglas RegEx para un control preciso, de alta prioridad y de texto.  
│├ *Vector-Search Plugin** (Carga perezosa): Permite la búsqueda semántica conectando los embeddings vectoriales locales con la capa de retroceso Ollama/LLM 🐧  
││ * **Ollama AI (Local LLM) Fallback:** Sirve como un cheque opcional de baja prioridad para ** respuestas creativas, Q PulA, y avanzado Fuzzy Matching** cuando no se cumple ninguna regla determinista.  
││ * **Estatus:** Integración local de LLM.
│└ 5. **Intelligent Post-Correction** (`FuzzyMap`)**– Refinement post-LT * 🐧 🍏 🪟  
││ * Aplicado después de LanguageTool para corregir las salidas específicas de LT. Sigue la misma lógica de prioridad de cascada estricta que la capa de precorrección.  
││ * *Ejecución de script Dinámica: Las reglas pueden desencadenar scripts Python personalizados ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-eslang.md)) para realizar acciones avanzadas como llamadas API, archivo I/O o generar respuestas dinámicas.  
││ * *Fuzzy Fallback* El **Comprobación de similitud borrosa** (controlado por un umbral, por ejemplo, el 85%) actúa como la capa de corrección de error de prioridad más baja. Sólo se ejecuta si toda la regla determinista/cacading anterior no encontró un partido (la regla actual coincide es falsa), optimizando el rendimiento evitando lentos controles borrosos siempre que sea posible.  
├┬ **Model Management/**   
│├─ `prioritize_model.py` (Optimiza la carga/descarga del modelo basado en el uso) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configures the first-time model setup) 🐧 🍏 🪟  
├─ **Adaptive VAD Timeout * 🐧 🍏 🪟  
├─ **Aditivo Hotkey (Start/Stop)** 🐧 🍏 🪟  
├─ **Instant Language Switching** (Experimental via model preloading) 🐧 🍏         
├─ **Orquestación de Afluencia** (Automatización del flujo de trabajo basado en el ADAG) 🐧 🍏 🪟
│   Requiere Docker · UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino State Engine** (interface-aware config per speech/terminal/web) 🐧 🍏 🪟
└─  Requiere Docker · Admin UI: `http://localhost:8084` 🐧 🍏 🪟  

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_languagetool_server.py` (Inicia el servidor local LanguageTool) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Shuts down the LanguageTool server) 🐧 🍏 
├─ `monitor_mic.sh` (por ejemplo, para uso con auriculares sin teclado y monitor de uso) 🐧 🍏 🪟  

### **Gestión de Modelos y Paquetes**  
    Herramientas para el manejo robusto de grandes modelos de lenguaje.  

**GestiónDeModelos/** 🐧 🍏 🪟  
├─ **Descargador de Modelos Robusto** (fragmentos de la versión de GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilidad para los propietarios del repositorio para dividir archivos grandes y generar sumas de verificación) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Herramienta para que los usuarios finales descarguen, verifiquen y recompongan archivos multipartes) 🐧 🍏 🪟  

</details>


<details>
<summary>Asistentes de Desarrollo y Despliegue</summary>

#### **Development &amp; Deployment Helpers *  
    Scripts para la configuración, pruebas y ejecución de servicios ambientales.  

*Consejo: glogg le permite utilizar expresiones regulares para buscar eventos interesantes en sus archivos de registro. *     
Por favor, compruebe la casilla de verificación cuando se instala para asociar con archivos de registro.    
https://glogg.bonnefon.org/     
    
Consejo: Después de definir los patrones de regex, ejecute `python3 tools/map_tagger.py` para generar automáticamente ejemplos de búsqueda de las herramientas CLI. Ver [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-eslang.md) para más detalles. *

Entonces tal vez doble clic
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ ** Gestión del medio ambiente virtual/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ ** Integración de la dictadoción en todo el sistema/*  
│├ Vosk System Listener Integration 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Control de micrófono específico de Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey escucha el texto reconocido y lo escribe en todo el sistema) 🪟  
└─ **CCI/CD Automation/**  
    └─ Expanded GitHub Workflows (instalación, pruebas, despliegue de docs) 🐧 🪟 *(Runs on GitHub Actions)*  

</details>

<details>
<summary>Características experimentales</summary>
    
#### **Upcoming / Experimental Features * *  
    Características actualmente en desarrollo o en proyecto de estado.  

**Características experimentales/**  
├─ **TER AFTER DICTATION REGEX** Regla de activación del ejemplo "(ExampleAplication ThatNoExist habitPi, your personal AI)" 🐧  
├┬Plugins  
│╰= **Lazy-Reload** (*) 🐧 🍏 🪟  
(*Cambios de activación/desactivación de Plugin, y sus configuraciones, se aplican en la siguiente ejecución de procesamiento sin reiniciar el servicio.*)  
│ ├ **git commands* (Voice control for send git commands) 🐧 🍏 🪟  
│ ├ **wannweil** (Mapa para la ubicación Alemania-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Control de Voz para aplicaciones de poker) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Control de voz para 0 A.D. juego) 🐧   
├─ ** Producto de sonido cuando inicie o termine una sesión** (Descripción pendiente) 🐧   
├─ ** Producto de voz para personas con discapacidad visual** (Descripción pendiente) 🐧 🍏 🪟  
└─ *SL5 Aura Android Prototype** (Todavía no está conectado) 📱  

---

*(Nota: Las distribuciones específicas de Linux como Arch (ARL) o Ubuntu (UBT) están cubiertas por el símbolo general Linux 🐧). Se pueden incluir distinciones detalladas en las guías de instalación. *
</details>

<details>
<summary>Haga clic para ver el comando utilizado para generar esta lista de scripts</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>Una visión gráfica de la arquitectura</summary>

### Una visión gráfica de la arquitectura:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Modelos utilizados</summary>

## Modelos usados:

Recomendación: use modelos de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probablemente más rápido)

Estos modelos comprimidos deben guardarse en la carpeta `models/`.

`mv vosk-model-*.zip models/`


Silencio Modelo Silencioso Tamaño Silencio Word error rate/Speed Silencioso
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
Silencio [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) Silencio 1.8G Silencio 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter)
<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx) TEN Big German model for telephony and server TEN Apache 2.0 TMLTAG5X33.26 (mtedx)

Esta tabla proporciona una visión general de los diferentes modelos de Vosk, incluyendo su tamaño, tasa de error de palabras o velocidad, notas e información sobre la licencia.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licencia de LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## Apoya el proyecto
Si encuentras útil esta herramienta, ¡por favor considera comprarnos un café! Tu apoyo ayuda a impulsar futuras mejoras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

