# 💡 Funciones destacadas: almacenamiento en caché persistente de complementos

## 💾 Almacenamiento en caché para rendimiento, confiabilidad y eficiencia de la red

El sistema ahora ofrece un mecanismo de almacenamiento en caché central y persistente (`simple_plugin_cache`) diseñado para reducir la carga de la red externa (por ejemplo, clima, API de traducción) y acelerar la ejecución. El caché es **persistente**, lo que significa que las entradas sobreviven a los reinicios del servicio.

**Objetivo:** Reducir el tráfico de red, prevenir el abuso de API y proporcionar respuestas rápidas durante interrupciones del servicio externo.

---

### 1. Implementación básica de almacenamiento en caché (controlada por TTL)

Para almacenar en caché el resultado de una función, debe implementar la lógica central en tres bloques: **Verificar**, **Ejecutar** y **Almacenar**.

#### 1.1 Importaciones y Configuración

Agregue las importaciones necesarias y defina una constante de tiempo de vida (TTL) en el script de su complemento (por ejemplo, `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 Lógica de almacenamiento en caché en el bloque `ejecutar`

La función "ejecutar" primero debe intentar recuperar el resultado almacenado en caché antes de realizar cualquier llamada de red.

```python
def execute(match_data, logger):
    # ASSUMPTION: BASE_DIR_FOR_CACHE points to a stable, persistent directory (e.g., TMP_DIR)
    BASE_DIR_FOR_CACHE = Path(...) 
    
    # The cache key must be a tuple of all arguments that affect the function's result.
    cache_key_args = (city, lang) 
    
    # --- BLOCK A: PRIMARY CACHE CHECK (TTL-Driven) ---
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
        'plugin_get_weather',      # Unique name for this function/operation
        cache_key_args,
        WEATHER_TTL,               # The TTL for this entry
        logger=logger
    )
    if cached_response:
        return cached_response # <-- CACHE HIT: Return immediately
        
    # --- BLOCK B: NETWORK EXECUTION (ONLY on Cache Miss) ---
    try:
        # Execute your CURL/Requests/External API call here.
        response = "Successful API response..." 

        # --- SUCCESS: STORE RESULT ---
        set_cached_result(BASE_DIR_FOR_CACHE, 'plugin_get_weather', cache_key_args, response)
        
        return response

    # --- BLOCK C: EXCEPTION & FAILOVER (Stale Cache Strategy) ---
    except Exception as e:
        logger.warning(f"API call failed ({type(e).__name__}). Attempting stale cache fallback...")
        
        # SECOND CACHE CHECK: Retrieve the last stored entry, ignoring its age (ttl_seconds=None).
        stale_response = get_cached_result(
            BASE_DIR_FOR_CACHE, 
            'plugin_get_weather', 
            cache_key_args,
            logger=logger # Important: TTL is explicitly omitted (None) here
        )
        
        if stale_response:
            logger.warning("Delivering STALE cache as fallback.")
            return stale_response
        
        # NO FALLBACK AVAILABLE: Return the original error message.
        # Ensure you handle all specific exceptions as defined in your plugin.
        if isinstance(e, FileNotFoundError):
             return "Error: 'curl' program not found."
        # ... (other exception handlers) ...
        return f"Error: Could not fetch data and no fallback available. Cause: {e}"
```

---

### 2. Modos de almacenamiento en caché avanzados

#### A. Almacenamiento en caché permanente (eterno)

Si un resultado **nunca caduca** (por ejemplo, búsqueda de configuración estática), omita el parámetro `ttl_segundos` por completo.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. Requisitos de la clave de caché (`key_args`)

* `key_args` debe ser una **tupla** que contenga todas las variables que definen el resultado (por ejemplo, `(ciudad, idioma, sistema_unidad)`).
* El mecanismo de almacenamiento en caché convierte automáticamente objetos comunes de Python no serializables en JSON, como **`pathlib.Path`**, en cadenas para la generación de claves.