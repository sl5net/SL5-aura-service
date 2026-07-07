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



## 1. Selección rápida de archivos (comando Aura)

La acción `path_navigator` utiliza el siguiente comando `fzf` compatible con Git. Su propósito es generar una ruta de archivo directamente en el portapapeles del sistema.

**Lógica de comando:**
- Utiliza `git ls-files` dentro de un repositorio Git (excluye archivos ignorados).
- Vuelve a `buscar. -escriba f` fuera de un repositorio Git.
- Envía la ruta seleccionada al portapapeles usando `xclip -selection clipboard`.

## 2. Ejecución rápida de archivos (la función 'k')

Para completar el ciclo, se utiliza la función de shell personalizada `k`. Esta función toma la ruta del portapapeles y abre instantáneamente el archivo en `kate`.

### Implementación

Agregue la siguiente función al archivo de configuración de su shell (por ejemplo, `~/.bashrc`, `~/.zshrc`):

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

### Uso

1. Utilice el comando `path_navigator` (por ejemplo, escriba `buscar archivo` en su herramienta de activación).
2. Busque y seleccione el archivo deseado (por ejemplo, `src/main/config.py`).
3. En su terminal, escriba `k` y presione **ENTER**.
4. El archivo se abre instantáneamente en Kate.
__CODE_BLOCK_2__