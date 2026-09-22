> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Tu Voz. Tus Reglas.

<!-- Stack Overflow & Community Badges -->
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
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-eslang.md#the-oma-modus-beginner-shortcut) : solo escribe una palabra, Aura hace el resto | Aprende con Koans — un concepto a la vez | Script completo en Python, complementos, llamadas API |
| 🗄️ Gestión del Estado | Orquestación Trino + Airflow, fzf, CopyQ, comandos de voz/terminal, interfaces de usuario de navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2.87 J** por prueba (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · sin computación en la nube

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Suite de pruebas completa:** 94 pruebas con LanguageTool en más de 800 mapas @ 0,07 s en caliente / 0,46 s en frío · sin computación en la nube

<details>
<summary>Inicio Rápido</summary>

## Inicio Rápido

### Opción A: Instalador Web y de 1 Clic (Recommended)

Comando de una línea o instalador independiente para Linux, macOS y Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-eslang.md)**

---

### Opción B: Instalación manual (Developers / Git)

1. Descarga o clona este repositorio
2. Ejecute el script de configuración para su sistema operativo (see `setup/` folder):
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` y luego `bash setup/nixos_setup.sh`
===> ⚠️ Experimental: no probado por los autores, ¡recibimos comentarios!   
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Inicie Aura: `./scripts/restart_venv_and_run-server.sh`
4. Presione su tecla de acceso rápido y hable: **[full guide →](../docs/GettingStarted.i18n/GettingStarted-eslang.md)**

---

### Desinstalación
Para eliminar los servicios en segundo plano, las entradas de inicio automático y los entornos virtuales de SL5 Aura:
- **Linux/macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -Configuración de archivos/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


**⚠️ Requisitos del sistema y compatibilidad**

* **Windows:** ✅ Totalmente compatible con (uses AutoHotkey/PowerShell).
* **macOS:** ✅ Totalmente compatible con (uses AppleScript).
* **Linux (X11/Xorg):** ✅ Totalmente compatible.
* **Linux (Wayland):** ✅ Totalmente compatible con (tested on KDE Plasma 6 / Wayland).
* **Linux (CachyOS / Arch-based rolling release):** ✅ Totalmente compatible.
Requiere mimalloc (`sudo pacman -S mimalloc`) debido a la compatibilidad con glibc 2.43.
* **Linux (NixOS):** 🧪 Experimental: configuración aportada por la comunidad, aún no probada.
Si lo prueba, abra un problema o PR con sus hallazgos.    
* **Linux (Manjaro):** Nuevo: una tecla de acceso rápido para todo el sistema abre una interfaz controlada por teclado similar a fzf para que pueda ejecutar comandos de Aura desde cualquier lugar del escritorio (completely decoupled from the active window). Este iniciador controlado por teclas de acceso rápido está actualmente implementado y probado en Linux (Manjaro); Otras distribuciones pueden funcionar pero requieren configuración. Ver en 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-eslang.md)   


    
SL5 Aura es un completo **asistente de voz fuera de línea** integrado en **Vosk** (for Speech-to-Text) y **LanguageTool** (for Grammar/Style), que presenta un **Local LLM (Ollama) Fallback** opcional para respuestas creativas y concordancia difusa avanzada. Transforma su voz en acciones y texto precisos, diseñados para una máxima personalización a través de un sistema de reglas conectable y un motor de secuencias de comandos dinámico.
    
Traducciones: Este documento también existe en [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Nota: Muchos textos son traducciones generadas automáticamente de la documentación original en inglés y están destinados únicamente a proporcionar orientación general. En caso de discrepancias o ambigüedades, siempre prevalecerá la versión en inglés. ¡Agradecemos la ayuda de la comunidad para mejorar esta traducción!

</details>

<details>
<summary>Demostración</summary>

### 📺 Demo de Terminal

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Consejo:** Para una mejor experiencia en la terminal, consulte [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-eslang.md).

### 🎥 Tutorial en Video
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: XMDLINK1X)*

</details>

<details>
<summary>Características principales</summary>

## Características clave

* **Sin conexión y privado:** 100% local. Ningún dato sale nunca de su máquina.
* **Motor de scripting dinámico:** Vaya más allá del reemplazo de texto. Las reglas pueden ejecutar scripts de Python personalizados (`on_match_exec`) para realizar acciones avanzadas como llamar a las API (e.g., search Wikipedia), interactuar con archivos (e.g., manage a to-do list) o generar contenido dinámico (e.g., a context-aware email greeting).
* **Reglas contextuales:** Restringe las reglas a aplicaciones específicas. Al usar `only_in_windows`, puede asegurarse de que una regla solo se active si un título de ventana específico (e.g., "Terminal", "VS Code" or "Browser") está activo. Esto funciona multiplataforma (Linux, Windows, macOS).
* **Motor de transformación de alto control:** Implementa un proceso de procesamiento altamente personalizable y basado en configuración. La prioridad de las reglas, la detección de comandos y las transformaciones de texto están determinadas exclusivamente por el orden secuencial de las reglas en Fuzzy Maps, lo que requiere **configuración, no codificación**.
* **Uso conservador de RAM:** Administra de forma inteligente la memoria, precargando modelos solo si hay suficiente RAM libre disponible, lo que garantiza que otras aplicaciones (like your PC games) siempre tengan prioridad.
* **Multiplataforma:** Funciona en Linux, macOS y Windows.
* **Totalmente automatizado:** Administra su propio servidor LanguageTool (but you can also use an external one).
* **Increíblemente rápido:** El almacenamiento en caché inteligente garantiza notificaciones instantáneas de "escucha..." y un procesamiento rápido.
* **Gestión dinámica del estado a través de Trino:** Motor de configuración compatible con la interfaz
separa las configuraciones para `voz`, `terminal` y `web`; cambie una sin
afectando a los demás. Incluye un **Panel de administración** (port 8084) en tiempo real.
</details>

<details>
<summary> 🔌 Integraciones listas para usar</summary>
  
    
## 🔌 Integraciones listas para usar

SL5-Aura viene con un vasto ecosistema de más de **100+ complementos preconfigurados**. Aquí hay algunos aspectos destacados:

### Control de voz OculiX / SikuliX IDE
SL5-Aura proporciona soporte de voz de primera clase para **OculiX** y **SikuliX IDE**. Esta integración le permite "decir" su código de automatización.

* **Voice-to-Snippet:** Diga "hacer clic", "esperar" o "buscar todo" y el servicio escribirá instantáneamente el código Python correcto ((e.g., `click("image.png")`) en el IDE.
* **Consciente de ventanas:** El complemento es sensible al contexto; solo se activa cuando la ventana de OculiX/SikuliX está enfocada.
* **Soporte inteligente de inglés:** Optimizado para `en-US` con un enfoque especial en acentos no nativos (e.g., German-English phonetics), lo que garantiza una alta precisión de reconocimiento para la comunidad global.
* **Extensible:** Utiliza el formato `FUZZY_MAP_pre.py` fácil de editar.

> **Estado:** Reconocido como complemento comunitario por el equipo de OculiX (see XMDLINK0X).

### Control por voz de LibreOffice IDE

### 0 A.D. Control por Voz

---

</details>


<details>
Documentación de XHTML

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## Documentación

Para obtener una referencia técnica completa, incluidos todos los módulos y scripts, visite nuestra página de documentación oficial. Se genera automáticamente y siempre está actualizado.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### Características Destacadas
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-eslang.md) — Búsqueda de reglas `fzf` de doble panel, vistas previas de contexto en vivo, ejecución instantánea de comandos mediante `Enter`/`Ctrl+R` e integración con el editor a través de `Ctrl+E`. Compatible con un atajo de teclado global (`Super+S`) y múltiples entornos de búsqueda dedicados preconfigurados mediante comandos de voz.

### Estado de compilación

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

👉 **Lea esto en otros idiomas:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-eslang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-eslang.md) | [🇪🇸 Español](../README.i18n/README-eslang.md) | [🇫🇷 Français](../README.i18n/README-frlang-eslang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-eslang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-eslang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-eslang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-eslang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-eslang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-eslang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-eslang.md)

---

<details>
<summary>Instalación</summary>

## Instalación

### 🎥 Instalación rápida y sin moderación (Manjaro/Arch Video)
Vea el proceso de configuración completo de 6 minutos:
* **Descargar:** ~3 minutos
* **Configuración y primer inicio:** ~3 minutos (including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


La configuración es un proceso de dos pasos:
1. Descargue la última versión o masterice ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) o clone este repositorio en su computadora.
2. Ejecute el script de configuración única para su sistema operativo.

Los scripts de configuración manejan todo: dependencias del sistema, entorno Python y descarga de los modelos y herramientas necesarios (~4GB) directamente desde nuestras versiones de GitHub para obtener la máxima velocidad.


#### Para Linux, macOS y Windows (with Optional Language Exclusion)

Para ahorrar espacio en disco y ancho de banda, puede excluir los modelos de idioma específicos (`de`, `en`) o todos los modelos opcionales (`all`) durante la instalación. **Los componentes principales (LanguageTool, lid.176) siempre están incluidos.**

Abra una terminal en el directorio raíz del proyecto y ejecute el script para su sistema:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Ejemplos:
# Instalar todo (Default):
# configuración de bash/manjaro_arch_setup.sh

# Excluir modelos alemanes:
# bash setup/manjaro_arch_setup.sh excluir=de

# Excluir todos los modelos de lenguaje VOSK:
# bash setup/manjaro_arch_setup.sh excluir=todos

# Para Windows en una sesión de Admin-Powershell

setup/windows11_setup.ps1 -Excluir [OPCIÓN]

# Ejemplos:
# Instalar todo (Default):
# configuración/windows11_setup.ps1

# Excluir modelos en inglés:
# setup/windows11_setup.ps1 -Excluir "en"

# Excluir modelos alemanes e ingleses:
# setup/windows11_setup.ps1 -Excluir "de,en"

# O (recommend) - Ejecute el archivo BAT:
windows11_setup.bat -Excluir "en"
__CODE_BLOCK_1__

#### Para Windows
Ejecute el script de configuración con privilegios de administrador.

**Instale una herramienta para leer y ejecutar, por ejemplo, [CopyQ](https://github.com/hluk/CopyQ) o [AutoHotkey v2](https://www.autohotkey.com/)**. Esto es necesario para el observador de escritura de texto.

La instalación es totalmente automatizada y tarda entre **8 y 10 minutos** cuando se utilizan 2 modelos en un sistema nuevo.

1. Navegue hasta la carpeta `setup`.
2. Haga doble clic en **`windows11_setup_with_ahk_copyq.bat`**.
* *El script solicitará automáticamente privilegios de administrador.*
* *Instala el sistema central, los modelos de lenguaje, **AutoHotkey v2** y **CopyQ**.*
3. Una vez que se complete la instalación, **Aura Dictation** se iniciará automáticamente.

> **Nota:** No es necesario instalar Python o Git de antemano; el guión se encarga de todo.

---

#### Instalación avanzada/personalizada
Si prefiere no instalar las herramientas del cliente (AHK/CopyQ) o desea ahorrar espacio en disco excluyendo idiomas específicos, puede ejecutar el script principal a través de la línea de comando:

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
Un solo script maneja todo. Inicia el servicio principal de dictado y el monitor de archivos automáticamente en segundo plano.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### En Windows
Iniciar el servicio es un **proceso manual de dos pasos**:

1. **Inicie el servicio principal:** Ejecute `start_aura.bat`. o iniciar desde `.venv` el servicio con `python3`

### 2. Configura tu tecla de acceso rápido

Para activar la dictado, necesitas un atajo de teclado global que cree un archivo específico. Recomendamos encarecidamente la herramienta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nuestra Recomendación: CopyQ

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


**Comando para Windows al usar [AutoHotkey](https://AutoHotkey.com):**
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
<summary>Configuración avanzada (Optional)</summary>

Configuración avanzada (Optional)

Puede personalizar el comportamiento de la aplicación creando un archivo de configuración local.

1. Navegue al directorio 'config/`.
2. Crear una copia de `config/settings local.py Example.txt` y renombrarla a `config/settings local.py`.
3. Editar `config/settings local.py` (it overrides any setting from the main `config/settings.py` file).

Este archivo 'config/settings local.py` es ignorado por Git por defecto, por lo que sus cambios personales no serán sobrescritos por actualizaciones.

### Plug-in Estructura y lógica

La modularidad del sistema permite una extensión robusta a través de los plugins/ directorio.

El motor de procesamiento se adhiere estrictamente a una cadena de prioridad jerárquica**:

1. **Module Loading Order (High Priority):** Las reglas cargadas de paquetes de lenguaje básico (de-DE, en-US) tienen precedencia sobre las reglas cargadas de los plugins/ directorio (which load last alphabetically).
    
2. ** Orden in-File (Micro Priority):** Dentro de cualquier archivo de mapa dado (FUZZY_MAP_pre.py), las reglas se procesan estrictamente por ** número de línea** (top-to-bottom).
    

Esta arquitectura garantiza que las reglas básicas del sistema estén protegidas, mientras que las reglas específicas para proyectos o contextuales (like those for CodeIgniter or game controls) se pueden añadir fácilmente como extensiones de baja prioridad a través de plug-ins.

</details>

<details>
<summary>Key Scripts para usuarios de Windows</summary>






## Scripts Clave para Usuarios de Windows

Aquí hay una lista de los scripts más importantes para configurar, actualizar y ejecutar la aplicación en un sistema Windows.

### Configuración y Actualización

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: El script principal para la **configuración inicial única** del entorno.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Ejecutar powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Ejecuta esto desde la carpeta del proyecto para **obtener el código y las dependencias más recientes**.

### Ejecutando la Aplicación
*   `start_aura.bat`: Un script principal para **iniciar el servicio de dictado**.

### Scripts Principales y Auxiliares
*   `aura_engine.py`: El servicio principal de Python (usually started by one of the scripts above).
*   `get_suggestions.py`: Un script auxiliar para funcionalidades específicas.

</details>



## 🚀 Características clave y compatibilidad del sistema operativo

<details>
<summary>Leyenda para la compatibilidad con OS</summary>

Leyenda para la compatibilidad del sistema operativo:  
*   🐧 **Linux** (e.g., Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **Ventanas**
*   📱 **Android** (for mobile-specific features)  

---

</details>



#### **Core Speech-to-Text (Aura) Engine**
Nuestro motor primario para reconocimiento de voz y procesamiento de audio sin conexión.

    
<details>
<summary>Aura-Core</summary>
  
*Aura-Core/*  
🍏 🪟 🪟  
** 🪟 ACE  
* Mapa privado seguro Carga (Integrity-First)**  
* * Flujo de trabajo* Carga archivos ZIP protegidos por contraseña.   
* Procesamiento de texto* Grouped by Language ( e.g. `de-DE`, `en-US`, ... )   
│ 🪟 🪟 🪟  
2. ** Intelligent Pre-Correction** (`FuzzyMap Pre` - XMDLINK0X)  
* * Ejecución diabética del script:** Las reglas pueden activar scripts Python personalizados (`on_match_exec`) para realizar acciones avanzadas como llamadas API, archivo I/O o generar respuestas dinámicas.  
* Ejecución de la causa:** Las reglas se procesan secuencialmente y sus efectos son **cumulativos**. Las reglas posteriores se aplican al texto modificado por reglas anteriores.  
*El más alto nivel de prioridad parar la crisis* Si una regla logra un **Full Match** (^...$), todo el conducto de procesamiento para ese token se detiene inmediatamente. Este mecanismo es fundamental para implementar comandos de voz fiables.   
3. `correct text by languagetool.py` (Integrates LanguageTool for grammar/style correction) 🍏 🪟 🪟 🪟  
** 🍏 🪟 🪟   
* **Control Determinístico:** Utiliza RegEx-Rule-Engine para un control preciso, de alta prioridad y de texto.   
**  
Ollama AI (Local LLM) Fallback:** Sirve como un cheque opcional de baja prioridad para ** respuestas creativas, Q emparejado y avanzado Fuzzy Matching** cuando no se cumple ninguna regla determinista.  
* **Estatus:** Integración local de LLM.  
5. ** Intelligent Post-Correction** (`FuzzyMap`)**– Refinement post-LT**  
* Aplicado después de LanguageTool para corregir las salidas específicas de LT. Sigue la misma lógica de prioridad de cascada estricta que la capa de Precorrección.  
* * Ejecución diabética del script:** Las reglas pueden activar scripts Python personalizados (XMDLINK1X) para realizar acciones avanzadas como llamadas API, archivo I/O o generar respuestas dinámicas.  
* *Fuzzy Fallback* El **Fuzzy Similarity Check** (controlled by a threshold, e.g., 85%) actúa como la capa de corrección de errores de prioridad más baja. Sólo se ejecuta si toda la regla determinista / caduca anterior no encontró un partido (current_rule_matched is False), optimizando el rendimiento evitando controles lentos siempre que sea posible.   
* Gestión de modelos/*   
│ 🪟 🪟 🪟  
└ 🪟 🪟 🪟  
** 🪟  
🍏 🪟 ACE  
🍏 🍏   
** 🪟 ├ ├  
Requiere Docker · UI: http://localhost:8081` 🍏 🪟 🪟 🪟  
* Motor Estatal de Turín*  
─ Requiere a Docker · Admin UI: http://localhost:8084` 🍏 🪟 🪟 🪟  
  
**SystemUtilities/**   
√ **LanguageTool Server Management/**   
🍏 🪟 🪟 🪟  
└  
🍏 🪟 ACE  

### **Gestión de Modelos y Paquetes**  
Herramientas para el manejo robusto de modelos de lenguaje grandes.  

**ModelManagement/** 🐧 🍏 🪟  
├─ **Descargador de Modelos Robusto** (GitHub Release chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utility for repo owners to split large files and generate checksums) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool for end-users to download, verify, and reassemble multi-part files) 🐧 🍏 🪟  

</details>


<details>
<summary>Desarrolladores y Ayudantes de Implementación</summary>

#### **Development &amp; Deployment Helpers**  
Scripts para la configuración, pruebas y ejecución de servicios ambientales.   

*Consejo: glogg le permite utilizar expresiones regulares para buscar eventos interesantes en sus archivos de registro.*   
Por favor, compruebe la casilla de verificación cuando se instala para asociar con los archivos de registro.   
https://glogg.bonnefon.org/   
    
*Consejo: Después de definir sus patrones de regex, ejecute `pithon3 herramientas/map tagger.py` para generar automáticamente ejemplos de búsqueda de las herramientas CLI. Ver [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-eslang.md) para más detalles.*

Entonces tal vez doble clic
`log/aura engine.log`
    
**DevHelpers/**  
** Gestión del medio ambiente virtual/**  
│ 🍏  
│  
* Integración de la dictadora en todo el sistema/**  
│ 🪟 🪟  
│  
└  
─ ¿Quién?  
└ 🪟 *(Runs on GitHub Actions)*  

</details>

<details>
<summary>Experimental Características</summary>
  
    
#### ## Upcoming / Experimental Features**  
Características actualmente en desarrollo o en proyecto de estado.  

**Características/**  
**** Regla de activación de ejemplo "(ExampleAplicationThatNotExist|Pi, your personal AI)" 🐧  
®Plugins  
# Live Lazy-Reload** (*) 🍏 🪟 🪟  
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)  
│ 🪟  
│ 🪟   
* Enchufe de muelles (Draft)** (Voice control for poker applications)  
Plugin A.D. (Draft)** (Voice control for 0 A.D. game)  
─ ** Producto de sonido cuando se inicia o termina una sesión** (Description pending) 🐧   
Out 🪟 🪟 🪟  
─ **SL5 Aura Android Prototipo** (Not fully offline yet) 📱  

---

*(Note: Specific Linux distributions like Arch (ARL) o Ubuntu (UBT) están cubiertos por el símbolo general Linux 🐧. Las distinciones detalladas pueden incluirse en las guías de instalación.)*
</details>

<details>
<summary>Haga clic para ver el comando utilizado para generar este script list</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A panorama gráfico de la arquitectura</summary>

### Una visión gráfica de la arquitectura:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
Modelos usados

## Modelos Utilizados:

Recomendación: use modelos de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probably faster)

Estos modelos comprimidos deben guardarse en la carpeta `models/`

`mv vosk-model-*.zip models/`


Silencio Modelo Silencioso Tamaño Silencio Word error rate/Speed Silencioso
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
(librispeech test-clean)HTMLTAG1X6.05 (tedlium)<br/>29.78 (callcenter) Silencioso genérico de EE.UU.
(Tuda-de test)<br/>24.00 (podcast)HTMLTAG8X12.82 (cv-test)<br/><br/>12.42 (mls)HTMLTAG12XX<br/>33.26 (mtedx)

Esta tabla proporciona una visión general de los diferentes modelos de Vosk, incluyendo su tamaño, tasa de error de palabras o velocidad, notas e información sobre la licencia.


- **Modelos Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licencia de LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## Apoya el Proyecto
Si encuentras útil esta herramienta, ¡por favor considera comprarnos un café! Tu apoyo ayuda a impulsar futuras mejoras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

