# 💡 기능 스포트라이트: 플러그인에 대한 영구 캐싱

## 💾 Cache-Nutzung zur Steigerung der Performance und Ausfallsicherheit

Das System bietet einen zentralen, persisten Cache-Mechanismus (`simple_plugin_cache`), der 외부 API-Aufrufe (wie Wetter, Übersetzungen 등) beschleunigt und reduziert. Der Cache는 **지속적**입니다. d.h. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel:** Reduzierung der Netzwerklast 및 Failover auf die letzte bekannte Antwort bei einem API-Ausfall.

---

### 1. 캐싱 활동(Der Standardfall)

기능을 캐시하면 'get_cached_result' 및 'set_cached_result'를 가져올 수 있습니다.

#### 1.1 가져오기 및 구성

Fügen Sie diese Zeilen zu Ihrem 플러그인-스크립트 hinzu(z.B. `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 캐싱-로직 im `execute`-블록

Sie müssen den 코드(drei Blöcke unterteilen): **Prüfen**, **Ausführen** 및 **Speichern**.

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

#### A. 영구 캐싱(Ewiger Cache)

Wenn ein Ergebnis niemals ablaufen soll (z.B. eine API-URL, die sich nicht ändert), lassen Sie den `ttl_seconds` 매개변수 einfach weg.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Wichtige Hinweise zum `key_args`

Der `key_args` 매개변수는 **Tupel** sein und alle Werte enthalten, die das Eergebnis der Funktion beeinflussen (z.B.`('Berlin', 'de')`)입니다.

**Der Mechanismus wandelt automatisch `pathlib.Path`-Object in Strings 음, bevor der Cache-Schlüssel 생성기 wird, 음 Probleme zu vermeiden.**