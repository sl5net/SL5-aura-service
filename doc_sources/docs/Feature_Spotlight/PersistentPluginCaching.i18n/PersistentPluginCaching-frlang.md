# 💡 Pleins feux sur les fonctionnalités : mise en cache persistante des plugins

## 💾 Mise en cache pour les performances, la fiabilité et l'efficacité du réseau

Le système propose désormais un mécanisme de mise en cache central et persistant (« simple_plugin_cache ») conçu pour réduire la charge du réseau externe (par exemple, la météo, les API de traduction) et accélérer l'exécution. Le cache est **persistant**, ce qui signifie que les entrées survivent aux redémarrages du service.

**Objectif :** Réduire le trafic réseau, prévenir les abus d'API et fournir des réponses de secours rapides en cas de panne de service externe.

---

### 1. Implémentation de base de la mise en cache (pilotée par TTL)

Pour mettre en cache le résultat d'une fonction, vous devez implémenter la logique de base sur trois blocs : **Check**, **Execute** et **Store**.

#### 1.1 Importations et configuration

Ajoutez les importations nécessaires et définissez une constante Time-To-Live (TTL) dans votre script de plugin (par exemple, `weather.py`) :

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 Logique de mise en cache dans le bloc `execute`

La fonction « exécuter » doit d'abord tenter de récupérer le résultat mis en cache avant d'effectuer des appels réseau.

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

### 2. Modes de mise en cache avancés

#### A. Mise en cache permanente (éternelle)

Si un résultat ne doit **jamais expirer** (par exemple, recherche de configuration statique), omettez entièrement le paramètre `ttl_seconds`.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. Exigences relatives à la clé de cache (`key_args`)

* `key_args` doit être un **tuple** contenant toutes les variables qui définissent le résultat (par exemple, `(ville, langue, unit_system)`).
* Le mécanisme de mise en cache convertit automatiquement les objets Python courants non sérialisables JSON, tels que **`pathlib.Path`**, en chaînes pour la génération de clés.