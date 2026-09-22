> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../PersistentPluginCaching_2025-1124de.md).*

# 💡 Feature Spotlight: Persistent Caching for Plugins

## 💾 Cache use to increase performance and reliability

The system offers a central, persistent cache mechanism (`simple_plugin_cache`) that speeds up and reduces external API calls (such as weather, translations, etc.). The cache is **persistent**, i.e. it remains even after a restart of the main service.

**Aim:** Reduce network load and failover to the last known response in case of API failure.

---

### 1. Enable caching (The default case)

To cache a function, you need to import the functions `get_cached_result` and `set_cached_result`.

#### 1.1 Imports and Configuration

Add these lines to your plugin script (e.g., `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 Caching Logic in the `execute` Block

You need to divide the code into three blocks: **Check**, **Execute**, and **Save**.

```python
def execute(match_data, logger):
    # ANNAHME: BASE_DIR_FOR_CACHE ist der stabile Pfad (z.B. der TMP-Ordner)
    BASE_DIR_FOR_CACHE = Path(...)
    
    # Der Cache-Key basiert auf allen Argumenten, die das Ergebnis beeinflussen.
    cache_key_args = (city, lang) 
    
    # --- BLOCK A: PRIMÄRER CACHE-ABRUF (TTL-gesteuert) ---
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
        'plugin_get_weather',      # Eindeutiger Name für die Funktion
        cache_key_args,
        WEATHER_TTL,               # Die TTL für diesen Eintrag
        logger=logger
    )
    if cached_response:
        return cached_response # <-- CACHE HIT: Liefere sofort zurück
        
    # --- BLOCK B: NETZWERK-AUFRUF (NUR bei Cache Miss) ---
    try:
        # Führe hier Ihren CURL/Request-Code aus.
        response = "Erfolgreiche Antwort..." 

        # --- ERFOLG: ERGEBNIS SPEICHERN ---
        set_cached_result(BASE_DIR_FOR_CACHE, 'plugin_get_weather', cache_key_args, response)
        
        return response

    # --- BLOCK C: FEHLER & FAILOVER (FALLBACK-Strategie) ---
    except Exception as e:
        logger.warning(f"API-Abruf fehlgeschlagen ({type(e).__name__}). Versuche Fallback...")
        
        # ZWEITER CACHE-ABRUF: Lese den letzten gespeicherten Eintrag, egal wie alt (ttl_seconds=None).
        stale_response = get_cached_result(
            BASE_DIR_FOR_CACHE, 
            'plugin_get_weather', 
            cache_key_args,
            logger=logger # Wichtig: TTL wird hier weggelassen/ist None
        )
        
        if stale_response:
            logger.warning("Liefere ABGELAUFENEN (stale) Cache als Fallback.")
            return stale_response
        
        # KEIN FALLBACK VORHANDEN: Liefere die ursprüngliche Fehlermeldung.
        return f"Fehler: Daten konnten nicht abgerufen werden und kein Fallback verfügbar. Ursache: {e}"

```

---

### 2. Special Caching Cases

#### A. Permanent Caching (Eternal Cache)

If a result should never expire (e.g., an API URL that does not change), simply leave out the `ttl_seconds` parameter.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Important Notes on `key_args`

The `key_args` parameter must be a **tuple** and contain all values that affect the result of the function (e.g., `('Berlin', 'de')`).

**The mechanism automatically converts `pathlib.Path` objects into strings before the cache key is generated to avoid problems.**
