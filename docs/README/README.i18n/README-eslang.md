# Voz a comandos o texto sin conexión en todo el sistema, sistema conectable

**⚠️ Requisitos del sistema y compatibilidad**

* **Windows:** ✅ Totalmente compatible (usa AutoHotkey/PowerShell).
* **macOS:** ✅ Totalmente compatible (usa AppleScript).
* **Linux (X11/Xorg):** ✅ Totalmente compatible. Recomendado para la mejor experiencia.
* **Linux (Wayland):** ⚠️ **Limitado/Experimental.**
* *Las teclas de acceso rápido globales y la escritura automática generalmente no funcionan en Wayland debido a restricciones de seguridad.*
* *Cambie a una **Sesión X11** al iniciar sesión (por ejemplo, "Plasma (X11)" o "Ubuntu en Xorg") para usar todas las funciones.*


¡Bienvenido al Servicio SL5 Aura! Este documento proporciona una descripción general rápida de nuestras funciones clave y su compatibilidad con el sistema operativo.

Aura no es sólo un transcriptor; es un potente motor de procesamiento fuera de línea que transforma su voz en acciones y texto precisos.

Es un completo **asistente de voz sin conexión** creado en **Vosk** (para voz a texto) y **LanguageTool** (para gramática/estilo), que ahora presenta un **Reserva local de LLM (Ollama)** opcional para respuestas creativas y concordancia difusa avanzada. Está diseñado para una máxima personalización a través de un sistema de reglas conectable y un motor de secuencias de comandos dinámico.

  
Traducciones: Este documento también existe en [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs).

Nota: Muchos textos son traducciones generadas automáticamente de la documentación original en inglés y están destinados únicamente a proporcionar orientación general. En caso de discrepancias o ambigüedades, siempre prevalecerá la versión en inglés. ¡Agradecemos la ayuda de la comunidad para mejorar esta traducción!

___

[![SL5 Aura (v0.16.1): HowTo crash SL5 Aura? -  seeh Hierarchical and Recursive Rule Engine](https://img.youtube.com/vi/d98ml86u68g/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)
(https://www.youtube.com/watch?v=BZCHonTqwUw o https://skipvids.com/?v=BZCHonTqwUw)

## Características clave

* **Sin conexión y privado:** 100% local. Ningún dato sale nunca de su máquina.
* **Motor de scripting dinámico:** Vaya más allá del reemplazo de texto. Las reglas pueden ejecutar secuencias de comandos Python personalizadas (`on_match_exec`) para realizar acciones avanzadas como llamar a API (por ejemplo, buscar en Wikipedia), interactuar con archivos (por ejemplo, administrar una lista de tareas pendientes) o generar contenido dinámico (por ejemplo, un saludo por correo electrónico contextual).
* **Motor de transformación de alto control:** Implementa un proceso de procesamiento altamente personalizable y basado en configuración. La prioridad de las reglas, la detección de comandos y las transformaciones de texto están determinadas exclusivamente por el orden secuencial de las reglas en Fuzzy Maps, lo que requiere **configuración, no codificación**.
* **Uso conservador de RAM:** Administra de forma inteligente la memoria, precargando modelos solo si hay suficiente RAM libre disponible, lo que garantiza que otras aplicaciones (como los juegos de PC) siempre tengan prioridad.
* **Multiplataforma:** Funciona en Linux, macOS y Windows.
* **Totalmente automatizado:** Administra su propio servidor LanguageTool (pero también puede usar uno externo).
* **Increíblemente rápido:** El almacenamiento en caché inteligente garantiza notificaciones instantáneas de "escucha..." y un procesamiento rápido.

## Documentación

Para obtener una referencia técnica completa, incluidos todos los módulos y scripts, visite nuestra página de documentación oficial. Se genera automáticamente y siempre está actualizado.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### Estado de compilación
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**Lea esto en otros idiomas:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](./README-arlang.md) | [🇩🇪 Deutsch](./README-delang.md) | [🇪🇸 Español](./README-eslang.md) | [🇫🇷 Français](./README-frlang.md) | [🇮🇳 हिन्दी](./README-hilang.md) | [🇯🇵 日本語](./README-jalang.md) | [🇰🇷 한국어](./README-kolang.md) | [🇵🇱 Polski](./README-pllang.md) | [🇵🇹 Português](./README-ptlang.md) | [🇧🇷 Português Brasil](./README-pt-BRlang.md) | [🇨🇳 简体中文](./README-zh-CNlang.md)

---







## Instalación

La configuración es un proceso de dos pasos:
1. Descargue la última versión o master (https://github.com/sl5net/Vosk-System-Listener/archive/master.zip) o clone este repositorio en su computadora.
2. Ejecute el script de configuración única para su sistema operativo.

Los scripts de configuración manejan todo: dependencias del sistema, entorno Python y descarga de los modelos y herramientas necesarios (~4 GB) directamente desde nuestras versiones de GitHub para obtener la máxima velocidad.


#### Para Linux, macOS y Windows (con exclusión de idioma opcional)

Para ahorrar espacio en disco y ancho de banda, puede excluir modelos de idiomas específicos (`de`, `en`) o todos los modelos opcionales (`all`) durante la instalación. **Los componentes principales (LanguageTool, lid.176) siempre están incluidos.**

Abra una terminal en el directorio raíz del proyecto y ejecute el script para su sistema:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

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

# Or (recommend) - Start des BAT: 
windows11_setup.bat -Exclude "en"
```

#### Para Windows
Ejecute el script de configuración con privilegios de administrador.

**Instale una herramienta para leer y ejecutar, p.e. [CopyQ](https://github.com/hluk/CopyQ) o [AutoHotkey v2](https://www.autohotkey.com/)**. Esto es necesario para el observador de escritura de texto.

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
setup\windows11_setup.bat

# Exclude specific language models (saves space):
# Exclude English:
setup\windows11_setup.bat -Exclude "en"

# Exclude German and English:
setup\windows11_setup.bat -Exclude "de,en"
```


---

## Uso

### 1. Iniciar los servicios

#### En Linux y macOS
Un único script se encarga de todo. Inicia el servicio de dictado principal y el observador de archivos automáticamente en segundo plano.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### En Windows
Iniciar el servicio es un **proceso manual de dos pasos**:

1. **Inicie el servicio principal:** Ejecute `start_dictation_v2.0.bat`. o iniciar desde `.venv` el servicio con `python3`

### 2. Configura tu tecla de acceso rápido

Para activar el dictado, necesita una tecla de acceso rápido global que cree un archivo específico. Recomendamos encarecidamente la herramienta multiplataforma [CopyQ](https://github.com/hluk/CopyQ).

#### Nuestra recomendación: CopyQ

Cree un nuevo comando en CopyQ con un acceso directo global.

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


### 3. ¡Empiece a dictar!
Haga clic en cualquier campo de texto, presione la tecla de acceso rápido y aparecerá una notificación "Escuchando...". Habla con claridad y luego haz una pausa. El texto corregido se escribirá por usted.

---


## Configuración avanzada (opcional)

Puede personalizar el comportamiento de la aplicación creando un archivo de configuración local.

1. Navegue hasta el directorio `config/`.
2. Cree una copia de `config/settings_local.py_Example.txt` y cámbiele el nombre a `config/settings_local.py`.
3. Edite `config/settings_local.py` (anula cualquier configuración del archivo principal `config/settings.py`).

Este archivo `config/settings_local.py` es (tal vez) ignorado por Git, por lo que sus cambios personales (tal vez) no serán sobrescritos por las actualizaciones.

### Estructura y lógica del complemento

La modularidad del sistema permite una extensión sólida a través del directorio plugins/.

El motor de procesamiento se adhiere estrictamente a una **Cadena de prioridad jerárquica**:

1. **Orden de carga de módulos (prioridad alta):** Las reglas cargadas desde los paquetes de idiomas principales (de-DE, en-US) tienen prioridad sobre las reglas cargadas desde el directorio plugins/ (que se cargan en último lugar alfabéticamente).
  
2. **Orden en el archivo (microprioridad):** Dentro de cualquier archivo de mapa determinado (FUZZY_MAP_pre.py), las reglas se procesan estrictamente por **número de línea** (de arriba a abajo).
  

Esta arquitectura garantiza que las reglas centrales del sistema estén protegidas, mientras que las reglas específicas del proyecto o contextuales (como las de CodeIgniter o los controles del juego) se pueden agregar fácilmente como extensiones de baja prioridad a través de complementos.
## Scripts clave para usuarios de Windows

Aquí hay una lista de los scripts más importantes para configurar, actualizar y ejecutar la aplicación en un sistema Windows.

### Configuración y actualización
* `setup/setup.bat`: El script principal para la **configuración inicial única** del entorno.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Ejecute powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat`: ejecútelos desde la carpeta del proyecto **obtenga el código y las dependencias más recientes**.

### Ejecutando la aplicación
* `start_dictation_v2.0.bat`: un script principal para **iniciar el servicio de dictado**.

### Scripts principales y auxiliares
* `aura_engine.py`: El servicio principal de Python (generalmente iniciado por uno de los scripts anteriores).
* `get_suggestions.py`: un script auxiliar para funcionalidades específicas.




## 🚀 Funciones clave y compatibilidad con el sistema operativo

Leyenda de compatibilidad del sistema operativo:  
* 🐧 **Linux** (por ejemplo, Arch, Ubuntu)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (para funciones específicas de dispositivos móviles)  

---

### **Motor principal de conversión de voz a texto (Aura)**
Nuestro motor principal para el reconocimiento de voz y el procesamiento de audio sin conexión.

  
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Servicio principal de Python que orquesta Aura) 🐧 🍏 🪟  
├┬ **Recarga en vivo** (Configuración y mapas) 🐧 🍏 🪟  
│├ **Carga segura de mapas privados (integridad primero)** 🔒 🐧 🍏 🪟  
││ * **Flujo de trabajo:** Carga archivos ZIP protegidos con contraseña.   
│├ **Procesamiento y corrección de texto/** Agrupado por idioma (p. ej., `de-DE`, `en-US`, ...)   
│├ 1. `normalize_punctuation.py` (Estandariza la puntuación post-transcripción) 🐧 🍏 🪟  
│├ 2. **Precorrección inteligente** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules-eslang.md)) 🐧 🍏 🪟  
││ * **Ejecución dinámica de secuencias de comandos:** Las reglas pueden activar secuencias de comandos Python personalizadas (on_match_exec) para realizar acciones avanzadas como llamadas API, E/S de archivos o generar respuestas dinámicas.  
││ * **Ejecución en cascada:** Las reglas se procesan secuencialmente y sus efectos son **acumulativos**. Las reglas posteriores se aplican al texto modificado por reglas anteriores.  
││ * **Criterio de detención de prioridad más alta:** Si una regla logra una **Coincidencia completa** (^...$), todo el proceso de procesamiento para ese token se detiene inmediatamente. Este mecanismo es fundamental para implementar comandos de voz confiables.  
│├ 3. `correct_text_by_languagetool.py` (Integra LanguageTool para corrección de gramática/estilo) 🐧 🍏 🪟  
│├ **4. Motor de reglas RegEx jerárquico con respaldo de IA de Ollama** 🐧 🍏 🪟  
││ * **Control determinista:** Utiliza RegEx-Rule-Engine para comandos precisos y de alta prioridad y control de texto.  
││ * **Reserva de Ollama AI (LLM local):** Sirve como una verificación opcional de baja prioridad para **respuestas creativas, preguntas y respuestas y coincidencias aproximadas avanzadas** cuando no se cumple ninguna regla determinista.  
││ * **Estado:** Integración LLM local.
│└ 5. **Postcorrección inteligente** (`FuzzyMap`)**– Refinamiento post-LT** 🐧 🍏 🪟
││ * Se aplica después de LanguageTool para corregir resultados específicos de LT. Sigue la misma lógica estricta de prioridad en cascada que la capa de corrección previa.  
││ * **Ejecución dinámica de secuencias de comandos:** Las reglas pueden activar secuencias de comandos Python personalizadas ([on_match_exec](docs/advanced-scripting-eslang.md)) para realizar acciones avanzadas como llamadas API, E/S de archivos o generar respuestas dinámicas.  
││ * **Refuerzo difuso:** La **Comprobación de similitud difusa** (controlada por un umbral, por ejemplo, 85%) actúa como la capa de corrección de errores de menor prioridad. Solo se ejecuta si toda la ejecución de la regla determinista/en cascada anterior no pudo encontrar una coincidencia (current_rule_matched es False), lo que optimiza el rendimiento evitando comprobaciones difusas lentas siempre que sea posible.  
├┬ **Gestión de modelos/**   
│├─ `prioritize_model.py` (Optimiza la carga/descarga del modelo según el uso) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configura la configuración del modelo por primera vez) 🐧 🍏 🪟  
├─ **Tiempo de espera de VAD adaptable** 🐧 🍏 🪟  
├─ **Tecla de acceso rápido adaptable (Iniciar/Detener)** 🐧 🍏 🪟  
└─ **Cambio instantáneo de idioma** (Experimental mediante precarga del modelo) 🐧 🍏   

**Utilidades del sistema/**   
├┬ **Administración del servidor LanguageTool/**   
│├─ `start_languagetool_server.py` (Inicializa el servidor local de LanguageTool) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Cierra el servidor LanguageTool) 🐧 🍏
├─ `monitor_mic.sh` (por ejemplo, para usar con auriculares sin usar teclado ni monitor) 🐧 🍏 🪟  

### **Gestión de modelos y paquetes**  
Herramientas para un manejo sólido de modelos de lenguaje grandes.  

**Gestión de modelos/** 🐧 🍏 🪟  
├─ **Descargador robusto de modelos** (fragmentos de lanzamiento de GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilidad para que los propietarios de repositorios divida archivos grandes y genere sumas de verificación) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Herramienta para que los usuarios finales descarguen, verifiquen y vuelvan a ensamblar archivos de varias partes) 🐧 🍏 🪟  


### **Ayudantes de desarrollo e implementación**  
Scripts para la configuración, prueba y ejecución del servicio del entorno.  

*Consejo: glogg le permite utilizar expresiones regulares para buscar eventos interesantes en sus archivos de registro.*   
Marque la casilla de verificación durante la instalación para asociar con archivos de registro.    
https://translate.google.com/translate?hl=en&sl=en&tl=es&u=https://glogg.bonnefon.org/     
  
*Consejo: Después de definir sus patrones de expresiones regulares, ejecute `python3 tools/map_tagger.py` para generar automáticamente ejemplos de búsqueda para las herramientas CLI. Consulte [Map Maintenance Tools](docs/Developer_Guide/Map_Maintenance_Tools-eslang.md) para obtener más detalles.*

Entonces tal vez haga doble clic
`log/aura_engine.log`
  
  
**DevHelpers/**  
├┬ **Gestión del entorno virtual/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Integración de dictado en todo el sistema/**  
│├ Integración Vosk-System-Listener 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (monitoreo de micrófono específico de Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey escucha el texto reconocido y lo escribe en todo el sistema) 🪟  
└─ **Automatización CI/CD/**  
└─ Flujos de trabajo de GitHub ampliados (instalación, pruebas, implementación de documentos) 🐧 🍏 🪟 *(Se ejecuta en GitHub Actions)*  

### **Próximas funciones/experimentales**  
Funciones actualmente en desarrollo o en estado de borrador.  

**Características experimentales/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Ejemplo de regla de activación "(ExampleAplicationThatNotExist|Pi, tu IA personal)" 🐧  
├┬Complementos  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Los cambios en la activación/desactivación del complemento y sus configuraciones se aplican en la siguiente ejecución del procesamiento sin reiniciar el servicio.*)  
│ ├ **comandos git** (control de voz para enviar comandos git) 🐧 🍏 🪟  
│ ├ **wannweil** (Mapa de ubicación Alemania-Wannweil) 🐧 🍏 🪟  
│ ├ **Complemento de póquer (Draft)** (Control por voz para aplicaciones de póquer) 🐧 🍏 🪟  
│ └ **Complemento 0 A.D. (borrador)** (control por voz para el juego 0 A.D.) 🐧   
├─ **Salida de sonido al iniciar o finalizar una sesión** (Descripción pendiente) 🐧   
├─ **Salida de voz para personas con discapacidad visual** (Descripción pendiente) 🐧 🍏 🪟  
└─ **Prototipo de Android SL5 Aura** (Aún no está completamente fuera de línea) 📱  

---

*(Nota: Distribuciones de Linux específicas como Arch (ARL) o Ubuntu (UBT) están cubiertas por el símbolo general de Linux 🐧. Es posible que se cubran distinciones detalladas en las guías de instalación).*









<detalles>
<summary>Haga clic para ver el comando utilizado para generar esta lista de scripts</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</detalles>


### bit mira gráficamente para ver qué hay detrás:

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# Modelos usados:

Recomendación: utilice modelos de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probablemente más rápido)

Estos modelos comprimidos deben guardarse en la carpeta `modelos/`

`mv vosk-model-*.zip modelos/`


| Modelo | Tamaño | Tasa de error de palabra/Velocidad | Notas | Licencia |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5.69 (prueba de limpieza de librispeech)<br/>6.05 (tedlium)<br/>29.78 (centro de llamadas) | Modelo genérico preciso en inglés de EE. UU. | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9,83 (prueba Tuda-de)<br/>24,00 (podcast)<br/>12,82 (prueba cv)<br/>12,42 (mls)<br/>33,26 (mtedx) | Gran modelo alemán para telefonía y servidor | Apache 2.0 |

Esta tabla proporciona una descripción general de los diferentes modelos de Vosk, incluido su tamaño, velocidad o tasa de error de palabras, notas e información de licencia.


- **Modelos Vosk:** XMLDLINK34X
- **Herramienta de idioma:**  
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**Licencia de LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Apoye el proyecto
Si encuentra útil esta herramienta, ¡considere invitarnos a un café! Su apoyo ayuda a impulsar mejoras futuras.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)



IgnorarPkg = linux66-nvidia-575xx nvidia-575xx-utils lib32-nvidia-575xx-utils

Configuración-nvidia-575xx mhwd-nvidia-575xx