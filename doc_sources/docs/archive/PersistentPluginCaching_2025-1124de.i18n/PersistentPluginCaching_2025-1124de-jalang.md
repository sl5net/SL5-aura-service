# 💡 機能スポットライト: プラグインの永続的なキャッシュ

## 💾 キャッシュに関するパフォーマンスと使用上の注意

システムの詳細は、永続的なキャッシュ メカニズム (`simple_plugin_cache`)、外部 API の使用 (Wetter、Übersetzungen など) を参照してください。 Der Cache は**永続的**です、d.h. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel:** API を使用した場合、Netzwerklast とフェイルオーバーを実行できます。

---

### 1. アクティベーションのキャッシュ (Standardfall から)

関数をキャッシュし、「get_cached_result」と「set_cached_result」をインポートして関数を調べます。

#### 1.1 インポートと構成

Fügen Sie diese Zeilen zu Ihrem Plugin-Skript hinzu (z.B. `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 キャッシュ ロジックの「実行」ブロック

コードの定義: **Prüfen**、**Ausführen**、**Speichern**。

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

### 2. 特別なキャッシングフェレ

#### A. Permanentes キャッシュ (Ewiger キャッシュ)

Wenn ein Ergebnis niemals ablaufen soll (z.B. eine API-URL, die sich nicht ändert), lassen Sie den `ttl_seconds` パラメータ einfach weg.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

#### B. Wichtige Hinweise zum `key_args`

`key_args` パラメーターは、**Tupel** のすべての機能を制御するために使用されます (z.B. `('Berlin', 'de')`)。

**文字列のメカニズムを自動化する「pathlib.Path」オブジェクト、キャッシュ シュリュッセルの生成に問題が発生する可能性があります。**