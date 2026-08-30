<img src="data/image/logo.svg" align="right" width="150" alt="⬟ Logotipo de SL5 Aura">

# ⬟ SL5 Aura – Tu Voz. Tus reglas.

> Marco de asistente de voz 100% fuera de línea y que prioriza la privacidad.  
> Defina exactamente lo que hace su voz, a partir de una sola palabra  
> a scripts completos de Python. Ninguna nube. No salen datos de su máquina.  
> Se ejecuta en terminal, navegador o como servicio en segundo plano (en Linux, macOS y Windows).

| 👵 Principiante | 🎓 Aprendiz | 🧑u200d💻 Desarrollador |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-eslang.md#the-oma-modus-beginner-shortcut): sólo escribe una palabra, Aura hace el resto | Aprenda con Koans: un concepto a la vez | Secuencias de comandos Python completas, complementos, llamadas API |
| 🗄️Gestión Estatal | Trino + Orquestación de flujo de aire, fzf, CopyQ, comandos de voz/terminal, interfaces de usuario del navegador |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)
⚡ **~2,87 J** por prueba (39 pruebas en >800 mapas a 0,08 s cálido/0,35 s frío 🌿 medido con [Eco-CI](https://metrics.green-coding.io/index.html)) · sin computación en la nube


<detalles>
<summary>Inicio rápido</summary>

## Inicio rápido

1. Descarga o clona este repositorio
2. Ejecute el script de configuración para su sistema operativo (consulte la carpeta `setup/`):
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` y luego `bash setup/nixos_setup.sh`
===> ⚠️ Experimental: no probado por los autores, ¡recibimos comentarios!   
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Inicie Aura: `./scripts/restart_venv_and_run-server.sh`
4. Presione su tecla de acceso rápido y hable: **[full guide →](../docs/GettingStarted.i18n/GettingStarted-eslang.md)**


**⚠️ Requisitos del sistema y compatibilidad**

* **Windows:** ✅ Totalmente compatible (usa AutoHotkey/PowerShell).
* **macOS:** ✅ Totalmente compatible (usa AppleScript).
* **Linux (X11/Xorg):** ✅ Totalmente compatible.
* **Linux (Wayland):** ✅ Totalmente compatible (probado en KDE Plasma 6/Wayland).
* **Linux (versión continua basada en CachyOS/Arch):** ✅ Totalmente compatible.
Requiere mimalloc (`sudo pacman -S mimalloc`) debido a la compatibilidad con glibc 2.43.
* **Linux (NixOS):** 🧪 Experimental: configuración aportada por la comunidad, aún no probada.
Si lo prueba, abra un problema o PR con sus hallazgos.    
* **Linux (Manjaro):** Nuevo: una tecla de acceso rápido para todo el sistema abre una interfaz controlada por teclado similar a fzf para que pueda ejecutar comandos de Aura desde cualquier lugar del escritorio (completamente desacoplado de la ventana activa). Este iniciador controlado por teclas de acceso rápido está actualmente implementado y probado en Linux (Manjaro); Otras distribuciones pueden funcionar pero requieren configuración. Ver en 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-eslang.md)   


  
SL5 Aura es un completo **asistente de voz fuera de línea** integrado en **Vosk** (para voz a texto) y **LanguageTool** (para gramática/estilo), que presenta un **Reserva local de LLM (Ollama)** opcional para respuestas creativas y concordancia difusa avanzada. Transforma su voz en acciones y texto precisos, diseñados para una máxima personalización a través de un sistema de reglas conectable y un motor de secuencias de comandos dinámico.
  
Traducciones: Este documento también existe en [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Nota: Muchos textos son traducciones generadas automáticamente de la documentación original en inglés y están destinados únicamente a proporcionar orientación general. En caso de discrepancias o ambigüedades, siempre prevalecerá la versión en inglés. ¡Agradecemos la ayuda de la comunidad para mejorar esta traducción!

</detalles>

<detalles>
<summary>Demostración</summary>

### 📺 Demostración de terminal

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Consejo:** Para una mejor experiencia con el terminal, consulte [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-eslang.md).

### 🎥 Vídeotutorial
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Enlace alternativo: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</detalles>

<detalles>
<summary>Características clave</summary>

## Características clave

* **Sin conexión y privado:** 100% local. Ningún dato sale nunca de su máquina.
* **Motor de scripting dinámico:** Vaya más allá del reemplazo de texto. Las reglas pueden ejecutar secuencias de comandos Python personalizadas (`on_match_exec`) para realizar acciones avanzadas como llamar a API (por ejemplo, buscar en Wikipedia), interactuar con archivos (por ejemplo, administrar una lista de tareas pendientes) o generar contenido dinámico (por ejemplo, un saludo por correo electrónico contextual).
* **Reglas contextuales:** Restringe las reglas a aplicaciones específicas. Al usar `only_in_windows`, puede garantizar que una regla solo se active si un título de ventana específico (por ejemplo, "Terminal", "Código VS" o "Navegador") está activo. Esto funciona multiplataforma (Linux, Windows, macOS).
* **Motor de transformación de alto control:** Implementa un proceso de procesamiento altamente personalizable y basado en configuración. La prioridad de las reglas, la detección de comandos y las transformaciones de texto están determinadas exclusivamente por el orden secuencial de las reglas en Fuzzy Maps, lo que requiere **configuración, no codificación**.
* **Uso conservador de RAM:** Administra de forma inteligente la memoria, precargando modelos solo si hay suficiente RAM libre disponible, lo que garantiza que otras aplicaciones (como los juegos de PC) siempre tengan prioridad.
* **Multiplataforma:** Funciona en Linux, macOS y Windows.
* **Totalmente automatizado:** Administra su propio servidor LanguageTool (pero también puede usar uno externo).
* **Increíblemente rápido:** El almacenamiento en caché inteligente garantiza notificaciones instantáneas de "escucha..." y un procesamiento rápido.
* **Gestión dinámica del estado a través de Trino:** Motor de configuración compatible con la interfaz
separa las configuraciones para `voz`, `terminal` y `web`; cambie una sin
afectando a los demás. Incluye un **Panel de administración** en tiempo real (puerto 8084).
</detalles>

<detalles>
<summary> 🔌 Integraciones listas para usar</summary>
  
## 🔌 Integraciones listas para usar

SL5-Aura viene con un vasto ecosistema de más de **100+ complementos preconfigurados**. Aquí hay algunos aspectos destacados:

### Control de voz OculiX / SikuliX IDE
SL5-Aura proporciona soporte de voz de primera clase para **OculiX** y **SikuliX IDE**. Esta integración le permite "decir" su código de automatización.

* **Voice-to-Snippet:** Diga "hacer clic", "esperar" o "buscar todo" y el servicio escribirá instantáneamente el código Python correcto (por ejemplo, `hacer clic("image.png")`) en el IDE.
* **Consciente de ventanas:** El complemento es sensible al contexto; solo se activa cuando la ventana de OculiX/SikuliX está enfocada.
* **Soporte de inglés inteligente:** Optimizado para `en-US` con un enfoque especial en acentos no nativos (por ejemplo, fonética alemán-inglés), lo que garantiza una alta precisión de reconocimiento para la comunidad global.
* **Extensible:** Utiliza el formato `FUZZY_MAP_pre.py` fácil de editar.

> **Estado:** Reconocido como complemento comunitario por el equipo de OculiX (ver [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Control por voz de LibreOffice IDE

### 0 A.D. Control por voz

---

</detalles>


<detalles>
<summary>Documentación</summary>

🔍[Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## Documentación

Para obtener una referencia técnica completa, incluidos todos los módulos y scripts, visite nuestra página de documentación oficial. Se genera automáticamente y siempre está actualizado.

👉[**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### Funciones destacadas


### Estado de compilación

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)








</a>

<a href="https://sl5net.github.io/SL5-aura-service/">
























































































































































































































































https://translate.google.com/translate?hl=en&sl=en&tl=es&u=https://glogg.bonnefon.org/     