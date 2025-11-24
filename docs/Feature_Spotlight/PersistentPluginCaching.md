# 💡 Feature Spotlight: Persistent Plugin Caching

## 💾 Caching for Performance, Reliability, and Network Efficiency

The system now offers a central, persistent caching mechanism (`simple_plugin_cache`) designed to reduce external network load (e.g., weather, translation APIs) and accelerate execution. The cache is **persistent**, meaning entries survive service restarts.

**Goal:** Reduce network traffic, prevent API abuse, and provide quick fallback responses during external service outages.

---

### 1. Basic Caching Implementation (TTL-Driven)

To cache a function's result, you need to implement the core logic across three blocks: **Check**, **Execute**, and **Store**.

#### 1.1 Imports and Configuration

Add the necessary imports and define a Time-To-Live (TTL) constant in your plugin script (e.g., `weather.py`):

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 Caching Logic in the `execute` Block

The `execute` function must first attempt to retrieve the cached result before making any network calls.

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

### 2. Advanced Caching Modes

#### A. Permanent (Eternal) Caching

If a result should **never expire** (e.g., static configuration lookup), omit the `ttl_seconds` parameter entirely.

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. Cache Key (`key_args`) Requirements

*   `key_args` must be a **tuple** containing all variables that define the result (e.g., `(city, language, unit_system)`).
*   The caching mechanism automatically converts common non-JSON-serializable Python objects, such as **`pathlib.Path`**, into strings for key generation.
