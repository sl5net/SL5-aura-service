# FUNCIONES DESTACADAS: Carga segura de mapas privados y empaquetado automático

Este documento describe la arquitectura para administrar complementos de mapas confidenciales (por ejemplo, datos del cliente, comandos propietarios) de una manera que permite la **edición en vivo** mientras se aplican las **mejores prácticas de seguridad** para evitar la exposición accidental de Git.

---

## 1. El concepto: seguridad "Matryoshka"

Para garantizar la máxima privacidad al utilizar herramientas estándar, Aura utiliza una estrategia de anidamiento **Matryoshka (muñeca rusa)** para archivos cifrados.

1. **Capa exterior:** Un archivo ZIP estándar cifrado con **AES-256** (mediante el comando `zip` del sistema).
* *Apariencia:* Contiene solo **un** archivo llamado `aura_secure.blob`.
* *Beneficio:* Oculta los nombres de archivos y la estructura de directorios de miradas indiscretas.
2. **Capa interna (el blob):** Un contenedor ZIP sin cifrar dentro del blob.
* *Contenido:* La estructura de directorios real y los archivos Python.
3. **Estado de funcionamiento:** Cuando están desbloqueados, los archivos se extraen a una carpeta temporal con el prefijo de guión bajo (por ejemplo, `_privado`).
* *Seguridad:* Esta carpeta es estrictamente ignorada por `.gitignore`.

---

## 2. Flujo de trabajo técnico

### A. La puerta de seguridad (puesta en marcha)
Antes de descomprimir cualquier cosa, Aura verifica `scripts/py/func/map_reloader.py` para reglas específicas `.gitignore`.
* **Regla 1:** `config/maps/**/.*` (Protege archivos clave)
* **Regla 2:** `config/maps/**/_*` (Protege los directorios de trabajo)
Si faltan, el sistema **aborta**.

### B. Desembalaje (controlado por excepciones)
1. El usuario crea un archivo de clave (por ejemplo, `.auth_key.py`) que contiene la contraseña (en texto sin formato o en comentarios).
2. Aura detecta este archivo y el ZIP correspondiente (por ejemplo, `private.zip`).
3. Aura descifra el ZIP externo usando la clave.
4. Aura detecta `aura_secure.blob`, extrae la capa interna y mueve los archivos al directorio de trabajo `_private`.

### C. Edición en vivo y empaquetado automático (El ciclo)
Aquí es donde el sistema se vuelve "autocurativo":

1. **Editar:** Modificas un archivo en `_private/` y lo guardas.
2. **Activador:** Aura detecta el cambio y recarga el módulo.
3. **Enganche del ciclo de vida:** El módulo activa su función `on_reload()`.
4. **SecurePacker:** Se ejecuta un script (`secure_packer.py`) en la raíz de la carpeta privada:
* Crea el ZIP (estructura) interior.
* Le cambia el nombre a `.blob`.
* Llama al comando `zip` del sistema para cifrarlo en el archivo externo usando la contraseña del archivo `.key`.

**Resultado:** Su `private.zip` siempre está actualizado con los últimos cambios, pero Git solo ve el cambio del archivo ZIP binario.

---

## 3. Guía de configuración

### Paso 1: Estructura del directorio
Cree una estructura de carpetas como esta:
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### Paso 2: El archivo clave (`.auth_key.py`)
Debe comenzar con un punto.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### Paso 3: El script Packer (`secure_packer.py`)
Coloque este script dentro de su carpeta de mapas privada (antes de comprimirlo inicialmente). Maneja la lógica de cifrado. asegúrese de que sus mapas llamen a este script a través del enlace `on_reload`.

### Paso 4: Implementación del gancho
En sus archivos de mapas (`.py`), agregue este enlace para activar la copia de seguridad en cada guardado:

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Estado y seguridad de Git

Cuando se configura correctamente, `git status` **solo** mostrará:
```text
modified:   config/maps/private/private_maps.zip
```
La carpeta `_private_maps` y el archivo `.auth_key.py` nunca son rastreados.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# Guía para desarrolladores: enlaces del ciclo de vida de los complementos

Aura SL5 permite que los complementos (Mapas) definan "Hooks" específicos que se ejecutan automáticamente cuando cambia el estado del módulo. Esto es esencial para flujos de trabajo avanzados como el sistema **Secure Private Map**.

## El gancho `on_reload()`

La función `on_reload()` es una función opcional que puede definir en cualquier módulo de Mapa.

### Comportamiento
* **Activador:** Se ejecuta inmediatamente después de que un módulo se **recarga en caliente** exitosamente (modificación de archivo + activador de voz).
* **Contexto:** Se ejecuta dentro del hilo principal de la aplicación.
* **Seguridad:** Envuelto en un bloque `try/except`. Los errores aquí se registrarán pero **no bloquearán** la aplicación.

### Patrón de uso: la "cadena tipo margarita"
Para paquetes complejos (como Private Maps), a menudo tienes muchos subarchivos, pero solo un script central (`secure_packer.py`) debe manejar la lógica.

Puedes usar el gancho para delegar la tarea hacia arriba:

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

### Mejores prácticas
1. **Mantenlo rápido:** No ejecutes tareas de bloqueo prolongadas (como descargas enormes) en el enlace principal. Utilice hilos si es necesario.
2. **Idempotencia:** Asegúrese de que su enlace pueda ejecutarse varias veces sin romper cosas (por ejemplo, no lo agregue a un archivo sin cesar; en su lugar, vuelva a escribirlo).