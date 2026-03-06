# 💡 تسليط الضوء على الميزات: التخزين المؤقت المستمر للمكونات الإضافية

## 💾 حفظ ذاكرة التخزين المؤقت لضبط الأداء وتحسين الأداء

يحتوي النظام على مركز مركزي، وآليات ذاكرة التخزين المؤقت المستمرة (`simple_plugin_cache`)، وواجهة برمجة التطبيقات الخارجية (مثل Wetter، Übersetzungen، وما إلى ذلك) التي يتم تحديثها وتقليصها. Der Cache ist **persistent**, d.h. إنه أكثر من مجرد Neustart des Haupt-Services erhalten.

**الرابط:** Reduzierung der Netzwerklast und Failover auf die Letzte bekannte Antwort bei einem API-Ausfall.

                                                                          ---

             ### 1. تنشيط التخزين المؤقت (Der Standardfall)

للحصول على وظيفة للتخزين المؤقت، يجب عليك استيراد الوظائف `get_cached_result` و`set_cached_result`.

                                   #### 1.1 الواردات والتكوين

    Fügen Sie diese Zeilen zu Ihrem Plugin-Skript hinzu (z.B. `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
# Definieren Sie eine Time-To-Live (TTL) für Ihre Daten
WEATHER_TTL = 300 # 5 Minuten
```

#### 1.2 سجل التخزين المؤقت في "التنفيذ" - الحظر

يجب عليك كتابة الكود في ثلاثة أجزاء: **Prüfen**، **Ausführen** و **Speichrn**.

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

                                            ### 2. تخزين مؤقت خاص

#### أ. التخزين المؤقت الدائم (ذاكرة التخزين المؤقت Ewiger)

إذا لم يتم استخدام أي شيء (z.B. عنوان URL لواجهة برمجة التطبيقات (API-URL) الذي لم يتم تحديده بعد)، فاضغط على المعلمة `ttl_thans` بكل سهولة.

```python
# Abruf (Prüfung)
# Dieser Eintrag läuft nie ab.
cached_result = get_cached_result(BASE_DIR, 'static_config', ('my_key',), logger=logger) 

# Speichern
set_cached_result(BASE_DIR, 'static_config', ('my_key',), 'My static value')
```

                                     #### B. Wichtige Hinweise zum `key_args`

يجب أن تكون معلمة `key_args` **Tupel** sein und alle Werte enthalten، die das Ergebnis der Funktion beeinflussen (z.B. `(\'Berlin', 'de')`).

**تتحرك الآلية بشكل تلقائي `pathlib.Path` - كائن في سلاسل، قبل إنشاء مفتاح ذاكرة التخزين المؤقت، مما يؤدي إلى مشكلة في حل المشكلة.**