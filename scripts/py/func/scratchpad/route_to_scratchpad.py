from ..config.dynamic_settings import settings
from .scratchpad_manager import (
    append_scratchpad,
    is_scratchpad_open,
    open_scratchpad,
)


def route_to_scratchpad(text: str, active_lt_url: str, language: str) -> bool:
    """
    Routes text to the Scratchpad buffer if Review Mode is enabled.
    Returns True if handled, False otherwise.
    """
    if not getattr(settings, "SCRATCHPAD_REVIEW_MODE_ENABLED", False):
        return False

    server_url = active_lt_url or getattr(
        settings,
        "LANGUAGETOOL_BASE_URL",
        f"http://127.0.0.1:{getattr(settings, 'LANGUAGETOOL_PORT', 8082)}",
    )

    if not is_scratchpad_open():
        open_scratchpad(server_url, language, initial_text=text)
    else:
        append_scratchpad(text)
    return True

