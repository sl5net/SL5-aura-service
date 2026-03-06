# 💡 Funciones destacadas: almacenamiento en caché persistente para complementos

## 💾 Cache-Nutzung zur Steigerung der Performance und Ausfallsicherheit

El sistema está integrado en el centro, el mecanismo de caché persistente (`simple_plugin_cache`), las API externas activadas (como Wetter, Übersetzungen, etc.) se desactivan y reducen. Der Cache es **persistente**, dh. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel:** Reduzierung der Netzwerklast and Failover auf the letzte bekannte Antwort bei api-Ausfall.

---

### 1. Activación de almacenamiento en caché (Der Standardfall)

Para almacenar una función, debe importar las funciones `get_cached_result` y `set_cached_result`.

#### 1.1 Importaciones y configuración

Utilice este código de complemento para su hogar (por ejemplo, `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 Almacenamiento en caché-Logik im `ejecutar`-Bloque

Debe incluir el código en tres bloques: **Prüfen**, **Ausführen** y **Speichern**.

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

### 2. Spezielle Caching-Fälle

#### A. Almacenamiento en caché permanente (caché de Ewiger)

Cuando no se ablaufen un Ergebnis niemals soll (por ejemplo, una API-URL, die sich nicht ändert), lassen Sie den `ttl_ seconds` Parameter einfach weg.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Wichtige Hinweise zum `key_args`

El parámetro `key_args` debe tener un **Tupel** sein und alle Werte enthalten, die das Ergebnis der Funktion beeinflussen (z.B. `('Berlin', 'de')`).

**El mecanismo funciona automáticamente `pathlib.Path`-Objekte in Strings um, bevor der Cache-Schlüssel generiert wird, um Probleme zu vermeiden.**