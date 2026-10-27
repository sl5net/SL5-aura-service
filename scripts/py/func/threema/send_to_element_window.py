"""Module for pasting text into the Element Desktop window via X11 tools."""
import logging
import subprocess
import time

from scripts.py.func.threema.send_to_threema_window import validate_message_text

LOGGER = logging.getLogger(__name__)

ELEMENT_WINDOW_CLASS = "element.Element"


def send_to_element_window(
    text: str,
    press_enter: bool = True,
    window_class: str = ELEMENT_WINDOW_CLASS,
    focus_delay_seconds: float = 0.2,
) -> bool:
    """
    Focus Element and paste text via clipboard (Ctrl+V), optionally send with Return.

    Side effects: overwrites the clipboard, changes focus, emulates keystrokes.
    The composer must have focus after window activation (it normally does).
    """
    sanitized = validate_message_text(text)
    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard", "-i"],
            input=sanitized.encode("utf-8"),
            check=True,
        )
        subprocess.run(["wmctrl", "-x", "-a", window_class], check=True)
        time.sleep(focus_delay_seconds)
        subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+v"], check=True)
        if press_enter:
            time.sleep(0.25)
            subprocess.run(["xdotool", "key", "--clearmodifiers", "Return"], check=True)
        return True
    except (subprocess.SubprocessError, OSError) as exc:
        LOGGER.error("Sending to Element failed: %s", exc)
        return False
