# 💡 Feature Spotlight: Persistentes Plugin-Caching

## 💾 Caching für Leistung, Zuverlässigkeit und Netzwerkeffizienz

Das System bietet jetzt einen zentralen, dauerhaften Caching-Mechanismus („simple_plugin_cache“), der darauf ausgelegt ist, die externe Netzwerklast (z. B. Wetter, Übersetzungs-APIs) zu reduzieren und die Ausführung zu beschleunigen. Der Cache ist **persistent**, was bedeutet, dass Einträge einen Neustart des Dienstes überdauern.

**Ziel:** Reduzieren Sie den Netzwerkverkehr, verhindern Sie API-Missbrauch und bieten Sie schnelle Fallback-Reaktionen bei Ausfällen externer Dienste.

---

### 1. Grundlegende Caching-Implementierung (TTL-gesteuert)

Um das Ergebnis einer Funktion zwischenzuspeichern, müssen Sie die Kernlogik in drei Blöcken implementieren: **Prüfen**, **Ausführen** und **Speichern**.

#### 1.1 Importe und Konfiguration

Fügen Sie die erforderlichen Importe hinzu und definieren Sie eine Time-To-Live (TTL)-Konstante in Ihrem Plugin-Skript (z. B. „weather.py“):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 Caching-Logik im „execute“-Block

Die Funktion „Ausführen“ muss zunächst versuchen, das zwischengespeicherte Ergebnis abzurufen, bevor sie Netzwerkaufrufe durchführt.

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

### 2. Erweiterte Caching-Modi

#### A. Permanentes (ewiges) Caching

Wenn ein Ergebnis **niemals ablaufen** soll (z. B. statische Konfigurationssuche), lassen Sie den Parameter „ttl_seconds“ vollständig weg.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. Anforderungen an den Cache-Schlüssel („key_args“)

* „key_args“ muss ein **Tupel** sein, der alle Variablen enthält, die das Ergebnis definieren (z. B. „(Stadt, Sprache, Einheitensystem)“).
* Der Caching-Mechanismus konvertiert gängige, nicht JSON-serialisierbare Python-Objekte, wie zum Beispiel **`pathlib.Path`**, automatisch in Strings für die Schlüsselgenerierung.