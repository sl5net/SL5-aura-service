"""Element Desktop to Threema Beta GUI relay daemon."""
import logging
import subprocess
import time
from typing import Optional
from scripts.py.func.threema.read_last_element_message import read_last_element_message
from scripts.py.func.threema.send_to_threema_window import send_to_threema_window


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)







LOGGER = logging.getLogger("ElementThreemaRelay")


def is_new_message(last_message: Optional[str], candidate: Optional[str]) -> bool:
    """
    Pure function: verify if candidate is non-empty and differs from last message.

    Benefits of functional programming:
    - Purity: Always produces the same result for the same arguments without side effects.
    - Testability: Can be unit-tested without mock X11 or UI environments.
    """
    if not candidate:
        return False
    cleaned = candidate.strip()
    if not cleaned:
        return False
    previous = last_message.strip() if last_message else None
    return cleaned != previous













def configure_x11_screensaver() -> None:
    """Disable X11 screensaver and DPMS standby to prevent input locks."""
    try:
        subprocess.run(["xset", "s", "off", "-dpms"], check=True)
        LOGGER.info("Disabled X11 screensaver and DPMS.")
    except (subprocess.SubprocessError, OSError) as exc:
        LOGGER.warning("Could not disable X11 screensaver via xset: %s", exc)


def run_relay(poll_interval_seconds: float = 2.0) -> None:
    """Run periodic GUI polling loop from Element to Threema Beta."""
    configure_x11_screensaver()
    LOGGER.info("Starting Element GUI relay (poll interval: %.1fs)...", poll_interval_seconds)

    last_known_message: Optional[str] = read_last_element_message()
    if last_known_message:
        LOGGER.info("Initial Element baseline captured: %r", last_known_message.strip())

    while True:
        try:
            time.sleep(poll_interval_seconds)
            current_candidate = read_last_element_message()
            if is_new_message(last_known_message, current_candidate):
                text_to_forward = current_candidate.strip() if current_candidate else ""
                LOGGER.info("New message detected. Forwarding to Threema: %r", text_to_forward)
                success = send_to_threema_window(text=text_to_forward, press_enter=True)
                if success:
                    last_known_message = current_candidate
                else:
                    LOGGER.error("Failed to forward message to Threema Beta window.")
        except KeyboardInterrupt:
            LOGGER.info("Relay stopped by user.")
            break


if __name__ == "__main__":
    run_relay()

