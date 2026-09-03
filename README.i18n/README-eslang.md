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

### Opción A: 1 clic e instalador web (recomendado)

Comando de una sola línea o instalador independiente para Linux, macOS y Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-eslang.md)**

---

### Opción B: Instalación manual (Desarrolladores/Git)

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

---

### Desinstalación
Para eliminar los servicios en segundo plano, las entradas de inicio automático y los entornos virtuales de SL5 Aura:
- **Linux/macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -Configuración de archivos/uninstall.ps1`
*(Sus reglas personalizadas en `config/maps/` se mantienen seguras de forma predeterminada a menos que especifique `--purge`).*

---


**⚠️ Requisitos del sistema y compatibilidad**

* **Windows:** ✅ Totalmente compatible (usa AutoHotkey/PowerShell).
* **macOS:** ✅ Totalmente compatible (usa AppleScript).
* **Linux (X11/Xorg):** ✅ Totalmente compatible.

* **Linux (versión continua basada en CachyOS/Arch):** ✅ Totalmente compatible.
Requiere mimalloc (`sudo pacman -S mimalloc`) debido a la compatibilidad con glibc 2.43.
* **Linux (NixOS):** 🧪 Experimental: configuración aportada por la comunidad, aún no probada.
Si lo prueba, abra un problema o PR con sus hallazgos.    
* **Linux (Manjaro):** Nuevo: una tecla de acceso rápido para todo el sistema abre una interfaz controlada por teclado similar a fzf para que pueda ejecutar comandos de Aura desde cualquier lugar del escritorio (completamente desacoplado de la ventana activa). Este iniciador controlado por teclas de acceso rápido está actualmente implementado y probado en Linux (Manjaro); Otras distribuciones pueden funcionar pero requieren configuración. Ver en 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-eslang.md)   




  



Nota: Muchos textos son traducciones generadas automáticamente de la documentación original en inglés y están destinados únicamente a proporcionar orientación general. En caso de discrepancias o ambigüedades, siempre prevalecerá la versión en inglés. ¡Agradecemos la ayuda de la comunidad para mejorar esta traducción!

</detalles>



















































































































































































































































































































































https://translate.google.com/translate?hl=en&sl=en&tl=es&u=https://glogg.bonnefon.org/     