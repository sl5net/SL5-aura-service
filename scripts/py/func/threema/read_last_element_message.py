# ---
"""Module for reading the latest message from Element Desktop via X11."""
import logging
import subprocess
import time
from typing import Optional

LOGGER = logging.getLogger(__name__)

ELEMENT_WINDOW_CLASS = "element.Element"


def read_last_element_message(
    window_class: str = ELEMENT_WINDOW_CLASS,
    focus_delay_seconds: float = 0.05,
) -> Optional[str]:
    """
    Extract the latest message from Element Desktop window via X11 keystrokes.

    Side effects:
    - Focuses the Element window via wmctrl.
    - Dispatches Up, Ctrl+A, Ctrl+C, Escape via xdotool.
    - Reads the X11 clipboard via xclip.
    """
    try:
        subprocess.run(
            ["wmctrl", "-x", "-a", window_class],
            check=True,
        )
        time.sleep(focus_delay_seconds)
        subprocess.run(
            ["xdotool", "key", "--clearmodifiers", "Up", "ctrl+a", "ctrl+c", "Escape"],
            check=True,
        )
        result = subprocess.run(
            ["xclip", "-o", "-selection", "clipboard"],
            capture_output=True,
            check=True,
        )
        return result.stdout.decode("utf-8")
    except subprocess.SubprocessError as exc:
        LOGGER.error("Subprocess execution failed while reading Element: %s", exc)
        return None
    except OSError as exc:
        LOGGER.error("System error while reading Element: %s", exc)
        return None
