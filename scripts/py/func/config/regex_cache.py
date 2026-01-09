# import re

# Centralized cache to prevent circular imports
REGEX_COMPILE_CACHE = {}

def clear_regex_cache():
    # global REGEX_COMPILE_CACHE
    REGEX_COMPILE_CACHE.clear()

