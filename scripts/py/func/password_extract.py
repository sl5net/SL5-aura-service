# scripts/py/func/password_extract.py
import re
import os
import sys

# scripts/py/func/password_extract.py:5
# def _extract_password(key_path: str, logger, encoding: str = "utf-8") -> Optional[bytes]:
import time

# Global cache to store results and timestamps per key_path
# Structure: { key_path: { 'timestamp': float, 'data': bytes } }

# --- RELOAD-PROOF CACHE SETUP ---
# We attach the cache to the 'sys' module so it survives module reloads.
# TODO: SECURITY RISK - Passwords are currently stored in plain text in this RAM cache.
#       This is a trade-off for performance to prevent I/O spam.
#       In the future, we should investigate safer methods (e.g., encrypted memory,
#       immediate zeroization, or strictly limiting the cache duration).
# (Se, 2025-1215-1432, 15.12.'25 14:32 Mon)

CACHE_ATTR_NAME = "_aura_password_extract_cache"

if not hasattr(sys, CACHE_ATTR_NAME):
    # Initialize the cache if it doesn't exist in sys
    setattr(sys, CACHE_ATTR_NAME, {})

# Reference the persistent cache
#_password_context_cache = getattr(sys, CACHE_ATTR_NAME)
# --------------------------------

from typing import Optional

def _extract_password(key_path: str, logger, encoding: str = "utf-8") -> Optional[bytes]:
    """
    Extracts the password/content from the given key_path.
    Includes a 5-second throttling mechanism per key_path to prevent log spam and excessive I/O.
    """
    #global _password_context_cache

    # Re-fetch the cache reference to be 100% safe
    cache = getattr(sys, CACHE_ATTR_NAME)

    normalized_key = os.path.abspath(key_path)

    current_time = time.time()

    log_everything = False

    # --- CACHE CHECK START ---
    # Check if we have a valid cache entry for this specific key_path
    if normalized_key in cache:
        cached_entry = cache[normalized_key]
        last_time = cached_entry['timestamp']

        # If the request is within 5 seconds of the last successful extraction, return cached result
        if current_time - last_time < 5.0:
            # logger.debug(f"Throttling: Returning cached password for {os.path.basename(key_path)}")
            time.sleep(.005) # not needed but consist how this function is used. eventually helpful
            return cached_entry['pw']
            # return None  # cached_entry['data']
    # --- CACHE CHECK END ---


    """
    Read key file and return password as bytes (or None on failure).

    Heuristics:
    - skip empty lines
    - prefer comment lines starting with '#' (take text after '#')
    - accept common assignment patterns (password=..., key: ..., secret = "...")
    - strip surrounding quotes and whitespace, remove BOM and CR/LF
    - return as bytes using given encoding
    """
    # logger.info(f"📖scripts/py/func/map_reloader.py:453: Reading key file: {key_path}")
    try:
        with open(key_path, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"❌ Error reading key file: {e}")
        return None

    is_fist5are_letters = False
    try:
        is_fist5are_letters = file_first_line_has_ascii5(key_path, logger)
        # logger.info(f"is_fist5are_letters:26 is_fist5are_letters:{is_fist5are_letters} ")
    except Exception as e:
        logger.info(f"❌ Error is_fist5are_letters: {e}")

    # helper to normalise candidate and return bytes if valid



    def normalise(s: str) -> Optional[bytes]:

        if not s:
            return None
        # remove BOM if present
        s = s.lstrip("\ufeff").strip()
        # strip surrounding single/double quotes
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # remove inline comments after value (e.g. secret # comment)
        s = re.split(r"\s+#", s, 1)[0].strip()
        if not s:
            return None
        try:
            raw = line.rstrip("\n\r")

            if raw == 'nopassword':
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                logger.info('found #######################################')
                sys.exit(1)
                return None



            b = s.encode(encoding)
            return b
        except Exception as e2:
            logger.warning(f"⚠ Could not encode password candidate: {e2}")
            return None

    # patterns to detect assignment-like lines
    assign_re = re.compile(r'^(?:password|pass|secret|key)\s*[:=]\s*(.+)$', re.IGNORECASE)

    pw=None
    # 1) scan for explicit assignment lines (high priority)
    for i, line in enumerate(lines):
        raw = line.rstrip("\n\r")
        m = assign_re.match(raw.strip())
        if m:
            candidate = m.group(1).strip()
            pw = normalise(candidate)
            if pw:
                logger.info(f"✓ Found password via assignment pattern. in  ..{key_path[-30:]}")
                # return pw

    # 2) scan for comment lines that contain a candidate (lines starting with '#')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            candidate = stripped.lstrip("#").strip()
            pw = normalise(candidate)
            # if pw:
            #     logger.info(f"scripts/py/func/map_reloader.py:491 ✓ Found password in comment in ..{key_path[-30:]}")
                # return pw

    # 3) fallback: first non-empty, non-comment line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            pw = normalise(stripped)
            if pw:
                if log_everything:
                    logger.info("✓ Found password in plaintext line.")
                # return pw
    if not pw:
        logger.warning(f"⚠ No valid password pattern found in ..{key_path}")
    if pw and not is_fist5are_letters:
        pw = mirror_outside_in_bytes(pw,9)
        # scripts/py/func/password_extract.py:91

        process_id = os.getpid()  # Get the current Process ID

        logger.info(f'⚠️ Extraction of this 🔒 encrypted 📦 ZIP is restricted (fist 5 are not only letters) to Aura only 🏗️ external extraction will fail🛑. Context: .. {key_path} (PID {process_id})')
    else:
        logger.info('🌍 This 🔒 encrypted 📦 ZIP file is portable (fist 5 are letters): External extraction 📤 supported.')

    # Update the persistent cache
    cache[normalized_key] = {
        'timestamp': current_time,
        'pw': pw
        ,
    }


    return pw

_first5_re = re.compile(r'^[A-Za-z]{5}')

def file_first_line_has_ascii5(key_path: str, logger, encoding: str = 'utf-8') -> bool:
    with open(key_path, "r", encoding=encoding, errors="replace") as f:
        line = f.readline()
    if not line:
        return False

    # remove leading whitespace
    line = line.lstrip()

    # remove one or more leading comment markers with optional spaces (e.g. "#  ", "// ", ";", "-- ")
    line = re.sub(r'^(?:(?:#|//|;|--)\s*)+', '', line)

    # test first 5 characters (regex will only match if there are 5 letters at the start)
    return bool(_first5_re.match(line[:5]))



def mirror_outside_in_bytes(s: bytes, mode: int) -> bytes:
    if mode != 9:
        return s

    i, j = 0, len(s) - 1
    out = bytearray()
    while i <= j:
        if i == j:
            out.append(s[i])
        else:
            out.append(s[i])
            out.append(s[j])
        i += 1
        j -= 1
    return bytes(out)

