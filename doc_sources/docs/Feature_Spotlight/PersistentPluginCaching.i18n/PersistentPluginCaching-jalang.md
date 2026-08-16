# 💡 機能スポットライト: 永続的なプラグイン キャッシュ

## 💾 パフォーマンス、信頼性、ネットワーク効率のためのキャッシュ

このシステムは、外部ネットワーク負荷 (天候、翻訳 API など) を軽減し、実行を高速化するために設計された、中央の永続的なキャッシュ メカニズム (`simple_plugin_cache`) を提供するようになりました。キャッシュは **永続的**です。つまり、エントリはサービスの再起動後に残ります。

**目標:** ネットワーク トラフィックを削減し、API の悪用を防止し、外部サービスの停止時に迅速なフォールバック応答を提供します。

---

### 1. 基本的なキャッシュの実装 (TTL 駆動)

関数の結果をキャッシュするには、**Check**、**Execute**、**Store** の 3 つのブロックにわたってコア ロジックを実装する必要があります。

#### 1.1 インポートと構成

必要なインポートを追加し、プラグイン スクリプト (例: 「weather.py」) で Time-To-Live (TTL) 定数を定義します。

```python
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from pathlib import Path

# Define the Time-To-Live for successful data
WEATHER_TTL = 300 # 5 minutes
```

#### 1.2 `execute` ブロックのキャッシュ ロジック

「実行」関数は、ネットワーク呼び出しを行う前に、まずキャッシュされた結果の取得を試行する必要があります。

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

### 2. 高度なキャッシュ モード

#### A. 永久 (永久) キャッシュ

結果が **決して期限切れにならない**場合 (静的設定ルックアップなど)、`ttl_seconds` パラメータを完全に省略します。

```python
# The entry will be considered valid forever until manually overwritten.
cached_result = get_cached_result(BASE_DIR_FOR_CACHE, 'static_config', ('my_key',), logger=logger) 
```

#### B. キャッシュ キー (`key_args`) の要件

* `key_args` は、結果を定義するすべての変数を含む **タプル** でなければなりません (例: `(city, language, Unit_system)`)。
* キャッシュ メカニズムは、**`pathlib.Path`** などの一般的な非 JSON シリアル化可能 Python オブジェクトをキー生成用の文字列に自動的に変換します。