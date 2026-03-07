import re
from collections import OrderedDict

MAX_CACHE_SIZE = 500
REGEX_COMPILE_CACHE = OrderedDict()

def clear_regex_cache():
    REGEX_COMPILE_CACHE.clear()

def get_cached_regex(pattern, flags=0):
    key = (pattern, flags)
    if key not in REGEX_COMPILE_CACHE:
        if len(REGEX_COMPILE_CACHE) >= MAX_CACHE_SIZE:
            REGEX_COMPILE_CACHE.popitem(last=False)  # ältesten entfernen (LRU)
        REGEX_COMPILE_CACHE[key] = re.compile(pattern, flags=flags)
    return REGEX_COMPILE_CACHE[key]
