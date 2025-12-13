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
        except Exception as e:
            logger.warning(f"⚠ Could not encode password candidate: {e}")
            return None

    # patterns to detect assignment-like lines
    assign_re = re.compile(r'^(?:password|pass|secret|key)\s*[:=]\s*(.+)$', re.IGNORECASE)

    # 1) scan for explicit assignment lines (high priority)
    for i, line in enumerate(lines):
        raw = line.rstrip("\n\r")
        m = assign_re.match(raw.strip())
        if m:
            candidate = m.group(1).strip()
            pw = normalise(candidate)
            if pw:
                logger.info("✓ Found password via assignment pattern.")
                return pw

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
                return pw

    # 3) fallback: first non-empty, non-comment line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            pw = normalise(stripped)
            if pw:
                logger.info("✓ Found password in plaintext line.")
                return pw

    logger.warning("⚠ No valid password pattern found in key file.")
    return None


