# 💡 기능 스포트라이트: 지속적인 플러그인 캐싱

## 💾 성능, 안정성 및 네트워크 효율성을 위한 캐싱

이제 시스템은 외부 네트워크 부하(예: 날씨, 번역 API)를 줄이고 실행을 가속화하도록 설계된 중앙 집중식 영구 캐싱 메커니즘(`simple_plugin_cache`)을 제공합니다. 캐시는 **지속적**입니다. 즉, 서비스를 다시 시작해도 항목이 유지됩니다.

**목표:** 네트워크 트래픽을 줄이고 API 남용을 방지하며 외부 서비스 중단 시 빠른 대체 응답을 제공합니다.

---

### 1. 기본 캐싱 구현(TTL 기반)

함수 결과를 캐시하려면 **확인**, **실행**, **저장**이라는 세 가지 블록에 걸쳐 핵심 논리를 구현해야 합니다.

#### 1.1 가져오기 및 구성

필요한 가져오기를 추가하고 플러그인 스크립트(예: `weather.py`)에 TTL(Time-To-Live) 상수를 정의합니다.

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 `execute` 블록의 캐싱 로직

'실행' 함수는 네트워크 호출을 하기 전에 먼저 캐시된 결과를 검색하려고 시도해야 합니다.

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

### 2. 고급 캐싱 모드

#### A. 영구(영원한) 캐싱

결과가 **만료되지 않아야** 하는 경우(예: 정적 구성 조회) `ttl_seconds` 매개변수를 완전히 생략하세요.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. 캐시 키(`key_args`) 요구 사항

* `key_args`는 결과를 정의하는 모든 변수(예: `(city, 언어, 단위_시스템)`)를 포함하는 **튜플**이어야 합니다.
* 캐싱 메커니즘은 **`pathlib.Path`**와 같은 일반적인 JSON이 아닌 직렬화 가능 Python 객체를 키 생성을 위한 문자열로 자동 변환합니다.