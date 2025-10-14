# File: scripts/py/func/notify.py
import logging
import subprocess
import platform
from pathlib import Path

# Assuming these are defined in your project's config
# from config.settings import NOTIFY_SEND_PATH, NOTIFICATION_LEVEL
from config.dynamic_settings import settings

logger = logging.getLogger(__name__)

def notify(summary: str, body: str = "", urgency: str = "low", icon: str = None, duration: int = 3000, replace_tag: str = None) -> None:
    """
    Sends a desktop notification, adapting to the host operating system.
    """
    logger.info("Attempting to send notification...")
    if not settings.NOTIFICATION_LEVEL:
        logger.info(f"Notifications are disabled (NOTIFICATION_LEVEL={settings.NOTIFICATION_LEVEL}). Aborting.")
        return

    system = platform.system()
    summary = str(summary)
    body = str(body)

    try:
        if system == "Darwin":  # macOS
            logger.debug("Using macOS (osascript) notification method.")
            # Sanitize input to prevent breaking the AppleScript string
            safe_summary = summary.replace('"', '\\"')
            safe_body = body.replace('"', '\\"')

            # Build and execute the AppleScript command
            applescript_command = f'display notification "{safe_body}" with title "{safe_summary}"'
            command = ["osascript", "-e", applescript_command]
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
            logger.info(f"Successfully sent macOS notification: '{summary}'")

        elif system == "Linux":
            logger.debug(f"Using Linux (notify-send) notification method with path: {settings.NOTIFY_SEND_PATH}")
            if not settings.NOTIFY_SEND_PATH or not Path(settings.NOTIFY_SEND_PATH).exists():
                logger.warning(f"notify-send path not found or invalid: {settings.NOTIFY_SEND_PATH}. Aborting notification.")
                return

            command = [settings.NOTIFY_SEND_PATH, "-u", urgency, summary, body, "-t", str(duration)]
            if icon:
                command.extend(["-i", icon])
            if replace_tag:
                command.extend(["-h", f"string:x-dunst-stack-tag:{replace_tag}"])

            subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
            logger.info(f"Successfully sent Linux notification: '{summary}'")

        elif system == "Windows":
            logger.debug("Windows notifications are not yet implemented.")
            # Placeholder for future Windows notification logic
            # This could call the notification_watcher.ahk script
            pass

    except subprocess.TimeoutExpired:
        logger.error(f"Notification command timed out for summary: '{summary}'")
    except subprocess.CalledProcessError as e:
        logger.error(f"{system} notification failed for '{summary}'. Return code: {e.returncode}")
        logger.error(f"Stderr: {e.stderr.strip()}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during notification for '{summary}': {e}")
