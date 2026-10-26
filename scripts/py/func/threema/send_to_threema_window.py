
"""Module for sending text to the Threema Beta window via X11 tools."""
import logging
import subprocess
import time
from typing import Optional

LOGGER = logging.getLogger(__name__)

THREEMA_WINDOW_CLASS = "threema beta.Threema Beta"


def validate_message_text(text: Optional[str]) -> str:
    """Validate and sanitize message text functionally without side effects."""
    if not text:
        raise ValueError("Message text must not be empty.")
    sanitized = text.strip()
    if not sanitized:
        raise ValueError("Message text must contain non-whitespace characters.")
    return sanitized


def send_to_threema_window(
    text: str,
    press_enter: bool = True,
    window_class: str = THREEMA_WINDOW_CLASS,
    focus_delay_seconds: float = 0.15,
) -> bool:
    """
    Focus the Threema Beta window and paste text via clipboard.

    Side effects:
    - Updates system clipboard.
    - Changes window focus.
    - Emulates keystrokes via xdotool.
    """
    sanitized_text = validate_message_text(text)

    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=sanitized_text.encode("utf-8"),
            check=True,
        )

        subprocess.run(
            ["wmctrl", "-x", "-a", window_class],
            check=True,
        )

        time.sleep(focus_delay_seconds)

        subprocess.run(
            ["xdotool", "key", "ctrl+v"],
            check=True,
        )

        if press_enter:
            time.sleep(0.05)
            subprocess.run(
                ["xdotool", "key", "Return"],
                check=True,
            )

        return True

    except subprocess.SubprocessError as exc:
        LOGGER.error("Subprocess execution failed while sending to Threema: %s", exc)
        return False
    except OSError as exc:
        LOGGER.error("System error while sending to Threema: %s", exc)
        return False
