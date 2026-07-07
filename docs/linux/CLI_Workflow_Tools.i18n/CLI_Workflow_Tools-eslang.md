# Guía de instalación de herramientas de flujo de trabajo CLI

Algunas acciones en el complemento del navegador de ruta dependen de utilidades de línea de comandos externas para realizar búsquedas aproximadas, enumerar archivos y manipular el portapapeles. Si faltan estas herramientas, verá una advertencia en la consola del sistema.

A continuación se encuentran las instrucciones de instalación para cada sistema operativo compatible.

## Utilidades requeridas

* **`fzf`**: Buscador difuso de línea de comandos de uso general.
* **`find`** (o `fd`): utilidad estándar de búsqueda de archivos.
* **Herramienta Portapapeles**: Se utiliza para canalizar la salida directamente al portapapeles de su sistema.
* **Linux:** `xclip` (requiere entorno X11).
* **macOS:** `pbcopy` (preinstalado).
* **Windows:** `clip` (preinstalado).
* **`file`**: Determina los tipos de archivos para vistas previas completas del terminal.

---

## Instrucciones de instalación

### 1. Linux (Arch/Manjaro)
Dado que su sistema se ejecuta en Manjaro, puede instalar los paquetes necesarios usando `pacman`:

```bash
sudo pacman -S fzf findutils xclip file
```

### 2. Linux (Debian/Ubuntu/Mint)
En sistemas basados en Debian, utilice `apt`:

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. MacOS
Utilice el administrador de paquetes [Homebrew](https://brew.sh/) para instalar las herramientas que faltan:

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. Ventanas
Si está utilizando Windows, le recomendamos instalar `fzf` mediante [Scoop](https://scoop.sh/) o [Winget](https://github.com/microsoft/winget-cli):

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
__CODE_BLOCK_4__