# Directorio de inicio y manejo de rutas multiplataforma

Aura está diseñado para ejecutarse en múltiples sistemas operativos. Para garantizar que los comandos de navegación del sistema de archivos funcionen independientemente de si está ejecutando Linux, macOS o Windows, las cadenas de ruta se analizan dinámicamente antes de registrarse en los mapas difusos activos.

---

## Lógica de normalización de ruta (`FUZZY_MAP_pre.py`)

La lógica de asignación de rutas dinámicas se basa en las siguientes prácticas estándar:

### 1. Reducción de tilde (POSIX)
En sistemas compatibles con POSIX (Linux y macOS), las rutas absolutas que coinciden con el directorio de inicio del usuario (por ejemplo, `/home/username/`) se convierten en rutas relativas `~` al inicio. Esto mantiene la longitud de las cadenas más corta y hace que las reglas generadas sean portátiles entre diferentes usuarios en el mismo sistema operativo:

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. Preservación absoluta de la ruta (Windows)
Windows no evalúa de manera confiable el carácter `~` en el símbolo del sistema estándar (`cmd.exe`) o en entornos PowerShell. Por lo tanto, cuando el complemento detecta un entorno Windows (`sys.platform == 'win32'`), conserva la ruta absoluta completa (por ejemplo, `C:\Users\username\...`) para garantizar que la ejecución del comando no falle.

### 3. Normalización de barra diagonal (`as_posix()`)
Aura utiliza barras diagonales de estilo POSIX (`/`) internamente para los mapas de configuración. El script normaliza todos los separadores de ruta dependientes del sistema operativo utilizando el método `pathlib.Path.as_posix()` de Python, que desinfecta automáticamente las barras invertidas (`\`) en entornos Windows.