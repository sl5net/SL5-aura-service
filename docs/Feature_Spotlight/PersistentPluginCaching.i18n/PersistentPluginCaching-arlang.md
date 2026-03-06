# 💡 تسليط الضوء على الميزات: التخزين المؤقت المستمر للمكونات الإضافية

## 💾 التخزين المؤقت لتحقيق الأداء والموثوقية وكفاءة الشبكة

يقدم النظام الآن آلية تخزين مؤقت مركزية ومستمرة (`simple_plugin_cache`) مصممة لتقليل حمل الشبكة الخارجية (مثل الطقس وواجهات برمجة تطبيقات الترجمة) وتسريع التنفيذ. ذاكرة التخزين المؤقت **مستمرة**، مما يعني أن الإدخالات تبقى بعد إعادة تشغيل الخدمة.

**الهدف:** تقليل حركة مرور الشبكة ومنع إساءة استخدام واجهة برمجة التطبيقات وتوفير استجابات احتياطية سريعة أثناء انقطاع الخدمة الخارجية.

                                                                          ---

### 1. تنفيذ التخزين المؤقت الأساسي (المعتمد على TTL)

للتخزين المؤقت لنتيجة إحدى الوظائف، تحتاج إلى تنفيذ المنطق الأساسي عبر ثلاث كتل: **التحقق**، **التنفيذ**، و **التخزين**.

                                   #### 1.1 الواردات والتكوين

أضف الواردات اللازمة وحدد ثابت مدة البقاء (TTL) في البرنامج النصي للمكون الإضافي (على سبيل المثال، `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 منطق التخزين المؤقت في كتلة "التنفيذ".

يجب أن تحاول وظيفة "التنفيذ" أولاً استرداد النتيجة المخزنة مؤقتًا قبل إجراء أي مكالمات للشبكة.

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

               ### 2. أوضاع التخزين المؤقت المتقدمة

            #### أ. التخزين المؤقت الدائم (الأبدي).

إذا كانت النتيجة يجب أن **لا تنتهي صلاحيتها أبدًا** (على سبيل المثال، البحث عن التكوين الثابت)، فاحذف المعلمة `ttl_thans` بالكامل.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

 #### ب. متطلبات مفتاح التخزين المؤقت (`key_args`).

* يجب أن يكون `key_args` **tuple** يحتوي على جميع المتغيرات التي تحدد النتيجة (على سبيل المثال، `(city, language,unit_system)`).
* تعمل آلية التخزين المؤقت تلقائيًا على تحويل كائنات Python الشائعة غير القابلة للتسلسل JSON، مثل **`pathlib.Path`**، إلى سلاسل لإنشاء المفاتيح.