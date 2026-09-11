import os

from ..config.dynamic_settings import settings
from .scratchpad_manager import (
    # append_scratchpad,
    open_scratchpad,
)


from ..config.dynamic_settings import settings
from .scratchpad_manager import is_scratchpad_open, open_scratchpad
def route_to_scratchpad(text: str, active_lt_url: str, language: str) -> bool:
    """
    Routes text to the Scratchpad buffer if Review Mode is enabled.
    Returns True if handled, False otherwise.
    """
    # with open('datei.txt', 'r', encoding='utf-8') as f:
    with open("/tmp/aura_overlay_debug.log", "a", encoding='utf-8') as f:
        f.write(f"route_to_scratchpad received: {text.encode('unicode_escape')!r}\n")
        f.flush()
    
    if not getattr(settings, "SCRATCHPAD_REVIEW_MODE_ENABLED", False):
        return False
    if is_scratchpad_open():
        # type_watcher already types dictated text into the focused
        # window (the open scratchpad); <<Modified>> binding triggers
        # the debounced LT refresh, so nothing more to do here.
        return True
    server_url = active_lt_url or getattr(
        settings,
        "LANGUAGETOOL_BASE_URL",
        f"http://127.0.0.1:{getattr(settings, 'LANGUAGETOOL_PORT', 8082)}",
    )
    os.environ['LANG'] = 'de_DE.UTF-8'
    os.environ['PYTHONUTF8'] = '1'

    open_scratchpad(server_url, language, initial_text=text)
    return True
