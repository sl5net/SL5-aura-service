import re
from scripts.py.func.config.regex_cache import REGEX_COMPILE_CACHE

# def get_compiled_regex(logger_instance, pattern, flags=0):
#
#     if pattern not in REGEX_COMPILE_CACHE:
#         try:
#             REGEX_COMPILE_CACHE[pattern] = re.compile(pattern, flags=flags)
#         except re.error as e:
#             logger_instance.error(f"Invalid regex pattern: {pattern} - {e}")
#             return None
#     return REGEX_COMPILE_CACHE.get(pattern)

import re
from scripts.py.func.config.regex_cache import REGEX_COMPILE_CACHE


def get_compiled_regex(pattern, logger_instance, flags=0):
    # Validierung: Ist pattern überhaupt ein String?
    if not isinstance(pattern, (str, re.Pattern)):
        if logger_instance:
            logger_instance.error(f"❌ CRITICAL: pattern ist {type(pattern)} statt string! Wert: {pattern}")
        return None

    if pattern not in REGEX_COMPILE_CACHE:
        try:
            REGEX_COMPILE_CACHE[pattern] = re.compile(pattern, flags=flags)
        except re.error as e:
            if logger_instance:
                logger_instance.error(f"Invalid regex pattern: {pattern} - {e}")
            return None

    return REGEX_COMPILE_CACHE.get(pattern)
