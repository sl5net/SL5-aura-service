# 💡 Pleins feux sur les fonctionnalités : mise en cache persistante pour les plugins

## 💾 Cache-Nutzung zur Steigerung der Performance and Ausfallsicherheit

Le système dispose d'un centre central, d'un mécanisme de cache persistant (`simple_plugin_cache`), de l'API externe (comme les paramètres plus humides, les options de mise en cache, etc.) optimisées et réduites. Le cache est **persistant**, d.h. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel :** Réduction de la durée de vie du réseau et du basculement auf die bekannte Answer bei an API-Ausfall.

---

### 1. Mise en cache activée (Der Standardfall)

Pour une fonction de cache, vous pouvez importer les fonctions `get_cached_result` et `set_cached_result`.

#### 1.1 Importations et configuration

Vous trouverez ce site dans le script du plug-in (par exemple `weather.py`) :

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 Caching-Logik dans le bloc `execute`

Vous pouvez trouver le code dans trois blocs sous-jacents : **Prüfen**, **Ausführen** et **Speichern**.

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

### 2. Mise en cache spéciale

#### A. Mise en cache permanente (Ewiger Cache)

Lorsqu'un Ergebnis niemals ablaufen solll (par exemple, une URL API, qui n'est pas là), vous pouvez utiliser le paramètre `ttl_seconds` à chaque fois.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Des indications sur `key_args`

Le paramètre `key_args` doit avoir un **Tupel** dans et tous les éléments qui s'appliquent aux paramètres de la fonction (par exemple `('Berlin', 'de')`).

**Le mécanisme utilise automatiquement l'objet `pathlib.Path` dans les chaînes, avant que le système de cache ne génère un problème.**