# File: scripts/py/func/notify.py
import logging
import subprocess
import platform
from pathlib import Path

logger = logging.getLogger(__name__)

from config.settings import NOTIFY_SEND_PATH

def notify(summary: object, body: object = "", urgency: object = "low", icon: object = None, duration: object = 3000,replace_tag: str = None) -> None:
    if not NOTIFY_SEND_PATH or not Path(NOTIFY_SEND_PATH).exists():
        logger.warning("Notifier not initialized or path invalid.")
        return

    logger.info(f"DEBUG: Attempting to notify: '{summary}'")
    if platform.system() == "Windows":
        # ... Windows logic ...
        pass
    else:
        if not NOTIFY_SEND_PATH or not Path(NOTIFY_SEND_PATH).exists(): return
        try:
            command = [NOTIFY_SEND_PATH, "-u", urgency, summary, body, "-t", str(duration)]
            if icon: command.extend(["-i", icon])

            if replace_tag:
                command.extend(["-h", f"string:x-dunst-stack-tag:{replace_tag}"])

            subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
        except Exception as e:
            logger.error(f"Linux notification failed for '{summary}': {e}")

