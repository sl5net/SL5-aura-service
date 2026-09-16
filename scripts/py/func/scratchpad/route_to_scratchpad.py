import os
from ..config.dynamic_settings import settings
from .scratchpad_manager import deliver_text

LOG_FILE = "/tmp/aura_overlay_debug.log"


def _log(msg: str) -> None:
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
    except Exception:
        pass


def route_to_scratchpad(text: str, active_lt_url: str, language: str) -> bool:
    """
    Routes text to the Scratchpad buffer if Review Mode is enabled.
    Returns True only if the text was CONFIRMED delivered to a live pad.
    Returns False if Review Mode is off, or if delivery failed - the caller
    should then fall back to the normal output path instead of losing text.
    """
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"route_to_scratchpad received: {text.encode('unicode_escape')!r}\n")
        f.flush()

    if not getattr(settings, "SCRATCHPAD_REVIEW_MODE_ENABLED", False):
        return False

    server_url = active_lt_url or getattr(
        settings,
        "LANGUAGETOOL_BASE_URL",
        f"http://127.0.0.1:{getattr(settings, 'LANGUAGETOOL_PORT', 8082)}",
    )
    os.environ['LANG'] = 'de_DE.UTF-8'
    os.environ['PYTHONUTF8'] = '1'

    if deliver_text(text, server_url, language):
        return True

    _log(f"route_to_scratchpad: giving up, pad unavailable for {text.encode('unicode_escape')!r}")
    return False
