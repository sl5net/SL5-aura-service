import sqlite3
import time
import hashlib
import json
from pathlib import Path
from typing import Optional
import json
from pathlib import Path
from typing import Optional, Any, Tuple

# --- Configuration ---
# NOTE: Using a static name for the cache DB ensures all plugins use the same file.
CACHE_DB_FILE = "plugin_call_cache.sqlite"


def _json_default_converter(obj):
    """Converts non-JSON-serializable objects (like Path) into a serializable type (str)."""
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def get_cache_db_path(base_dir: Path) -> Path:
    """Returns the absolute path to the cache database file."""
    # Assuming the cache should live in a persistent location like the main tmp/log directory
    return base_dir.parent / CACHE_DB_FILE

def get_cached_result(
    base_dir: Path,
    function_name: str,
    key_args: Tuple[Any, ...],
    ttl_seconds: Optional[int] = None,
    logger: Optional[Any] = None
    ) -> (str, None):
    """
    Retrieves a result from the cache if it is valid (not expired).

    Args:
        base_dir: The base directory (e.g., TMP_DIR or a stable path).
        function_name: The name of the function being called (e.g., 'get_current_weather').
        key_args: A tuple of the function arguments (used for hashing).
        ttl_seconds: The Time-To-Live in seconds for this entry.

    Returns:
        The cached result (str) or None if not found or expired.
    """
    db_path = get_cache_db_path(base_dir)


    # 1. Generate Cache Key
    key_data = json.dumps(
        [function_name, key_args],
        default=_json_default_converter,
        sort_keys=True
    )
    cache_key = hashlib.sha256(key_data.encode('utf-8')).hexdigest()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute("CREATE TABLE IF NOT EXISTS plugin_cache (key TEXT PRIMARY KEY, result TEXT, timestamp REAL)")

        # Attempt to retrieve
        cursor.execute("SELECT result, timestamp FROM plugin_cache WHERE key = ?", (cache_key,))
        result = cursor.fetchone()

        if result:
            cached_result_json, cached_timestamp = result

            if logger:
                logger.info(
                    f"CACHE: Found entry for '{function_name}'. Timestamp: {cached_timestamp}. TTL: {ttl_seconds}")

            current_time = time.time()

            # 2. Check TTL validity

            if cached_timestamp is None:
                print(f"DEBUG: Cache entry found but timestamp is None. Treating as expired.")
                logger.warning("CACHE ERROR: Timestamp is None. Treating as expired.")
                return None

            # 2. Check TTL validity
            if ttl_seconds is None:
                if logger:
                    logger.debug("CACHE HIT: Entry is 'eternal' (TTL=None). Skipping time check.")
                return json.loads(cached_result_json)

            # Drittens: Zeitbasierter Check (Wir sind uns sicher: Beide sind Zahlen)
            current_time = time.time()
            time_since_cache = current_time - cached_timestamp

            if time_since_cache < ttl_seconds:
                # Cache Hit: Valid
                logger.info(f"CACHE HIT: Valid for {ttl_seconds - time_since_cache:.2f}s more.")
                return json.loads(cached_result_json)
            # Cache Miss: Expired, falls through to return None


                # Cache Miss: Expired
            if logger:
                logger.debug("CACHE MISS: Entry expired.")

    except Exception as e:
        # In a caching utility, errors should be swallowed or logged without stopping execution
        print(f"Cache read error: {e}")

    finally:
        if conn:
            conn.close()

    return None


def set_cached_result(base_dir: Path, function_name: str, key_args: Tuple[Any, ...], result: str):
    """
    Saves a result to the cache.
    """
    db_path = get_cache_db_path(base_dir)

    # GEÄNDERT: Verwende den 'default' Parameter mit unserer Konverter-Funktion
    key_data = json.dumps(
        [function_name, key_args],
        default=_json_default_converter,
        sort_keys=True
    )
    cache_key = hashlib.sha256(key_data.encode('utf-8')).hexdigest()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        current_time = time.time()

        result_json = json.dumps(result)

        cursor.execute(
            "INSERT OR REPLACE INTO plugin_cache (key, result, timestamp) VALUES (?, ?, ?)",
            (cache_key, result_json, current_time)
        )
        conn.commit()

    except Exception as e:
        print(f"Cache write error: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()
