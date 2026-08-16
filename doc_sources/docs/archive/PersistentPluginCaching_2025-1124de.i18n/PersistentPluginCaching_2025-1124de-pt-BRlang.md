# 💡 Destaque de recursos: cache persistente para plug-ins

## 💾 Cache-Nutzung zur Steigerung der Performance und Ausfallsicherheit

O sistema possui um mecanismo de cache centralizado e persistente (`simple_plugin_cache`), o aumento externo da API (como Wetter, Übersetzungen, etc.) é melhorado e reduzido. O cache é **persistente**, d.h. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel:** Reduz a capacidade de rede e o failover na resposta mais recente em uma API-Ausfall.

---

### 1. Cache ativado (Der Standardfall)

Para armazenar uma função em cache, você deve importar as funções `get_cached_result` e `set_cached_result`.

#### 1.1 Importações e configuração

Verifique este Zeilen para seu script de plug-in (z.B. `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 Lógica de cache no bloco `execute`

Você deve inserir o código em três blocos: **Prüfen**, **Ausführen** e **Speichern**.

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

#### A. Cache Permanente (Ewiger Cache)

Se um único número for ablaufen soll (por exemplo, um URL de API, que não é o mesmo), lasse o parâmetro `ttl_seconds` einfach weg.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Quais são as principais instruções para `key_args`

O parâmetro `key_args` deve ser **Tupel** e todos os lugares envolvidos, a primeira função a ser influída (z.B. `('Berlin', 'de')`).

**O Mecanismo foi automaticamente `pathlib.Path`-Objeto em Strings um, antes que o Cache-Schlüssel gerasse um problema para resolver.**