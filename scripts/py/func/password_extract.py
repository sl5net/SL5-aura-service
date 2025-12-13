# scripts/py/func/password_extract.py
import re
from typing import Optional
def _extract_password(key_path: str, logger, encoding: str = "utf-8") -> Optional[bytes]:
    """
    Read key file and return password as bytes (or None on failure).

    Heuristics:
    - skip empty lines
    - prefer comment lines starting with '#' (take text after '#')
    - accept common assignment patterns (password=..., key: ..., secret = "...")
    - strip surrounding quotes and whitespace, remove BOM and CR/LF
    - return as bytes using given encoding
    """
    logger.info(f"📖scripts/py/func/map_reloader.py:453: Reading key file: {key_path}")
    try:
        with open(key_path, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"❌ Error reading key file: {e}")
        return None

    is_fist5are_letters = False
    try:
        is_fist5are_letters = file_first_line_has_ascii5(key_path, logger)
        logger.info(f"is_fist5are_letters:26 is_fist5are_letters:{is_fist5are_letters} ")
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
                logger.info("✓ Found password via assignment pattern.")
                # return pw

    # 2) scan for comment lines that contain a candidate (lines starting with '#')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            candidate = stripped.lstrip("#").strip()
            pw = normalise(candidate)
            if pw:
                logger.info("scripts/py/func/map_reloader.py:491 ✓ Found password in comment.")
                # return pw

    # 3) fallback: first non-empty, non-comment line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            pw = normalise(stripped)
            if pw:
                logger.info("✓ Found password in plaintext line.")
                # return pw
    if pw:
        logger.warning("⚠ No valid password pattern found in key file.")
    if pw and not is_fist5are_letters:
        pw = mirror_outside_in_bytes(pw,9)
        logger.info('⚠️ Extraction of this 🔒 encrypted 📦 ZIP is restricted (fist 5 are not only letters) to Aura only 🏗️ external extraction will fail🛑.')
    else:
        logger.info('🌍 This 🔒 encrypted 📦 ZIP file is portable (fist 5 are letters): External extraction 📤 supported.')
    return pw


import re
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

