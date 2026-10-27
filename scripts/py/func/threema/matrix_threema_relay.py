"""Bidirectional Element Desktop <-> Threema Beta GUI relay daemon.

Element -> Threema: poll the last own message in Element (Up, Ctrl+A, Ctrl+C),
                    forward it to Threema when it is new.
Threema -> Element: poll the last incoming Threema message (context menu
                    "Copy Message" via calibrated mouse offsets) and paste it
                    into Element when it is new.

Loop protection: every forwarded text is remembered (RelayHistory). A text
that appears again on the other side is an echo and is not sent back.
"""
import argparse
import logging
import subprocess
import time
from typing import Optional
from scripts.py.func.threema.read_last_element_message import read_last_element_message
from scripts.py.func.threema.read_last_threema_message import (
    load_config,
    read_last_threema_message,
)
from scripts.py.func.threema.relay_history import RelayHistory
from scripts.py.func.threema.send_to_element_window import send_to_element_window
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


def classify_candidate(
    last_seen: Optional[str], candidate: Optional[str], history: RelayHistory
) -> str:
    """
    Pure decision (given the history): 'unchanged' | 'echo' | 'forward'.

    'echo' = new on this side but it is our own forwarded text -> remember it
    as seen, but do not send it back.
    """
    if not is_new_message(last_seen, candidate):
        return "unchanged"
    if history.knows(candidate):
        return "echo"
    return "forward"


def configure_x11_screensaver() -> None:
    """Disable X11 screensaver and DPMS standby to prevent input locks."""
    try:
        subprocess.run(["xset", "s", "off", "-dpms"], check=True)
        LOGGER.info("Disabled X11 screensaver and DPMS.")
    except (subprocess.SubprocessError, OSError) as exc:
        LOGGER.warning("Could not disable X11 screensaver via xset: %s", exc)


def run_relay(
    poll_interval_seconds: float = 2.0,
    threema_to_element: bool = True,
    element_press_enter: bool = True,
    threema_press_enter: bool = True,
) -> None:
    """Run the periodic GUI polling loop in both directions."""
    configure_x11_screensaver()
    LOGGER.info(
        "Starting relay (poll %.1fs, Threema->Element: %s)...",
        poll_interval_seconds, threema_to_element,
    )
    history = RelayHistory()
    threema_cfg = load_config()

    last_element: Optional[str] = read_last_element_message()
    if last_element:
        LOGGER.info("Initial Element baseline: %r", last_element.strip())
        history.remember(last_element)

    last_threema: Optional[str] = None
    if threema_to_element:
        last_threema = read_last_threema_message(threema_cfg)
        if last_threema:
            LOGGER.info("Initial Threema baseline: %r", last_threema)
            history.remember(last_threema)

    while True:
        try:
            time.sleep(poll_interval_seconds)

            # --- Element -> Threema -------------------------------------
            candidate = read_last_element_message()
            verdict = classify_candidate(last_element, candidate, history)
            if verdict == "echo":
                LOGGER.info("Element shows our own relayed text - not sending back.")
                last_element = candidate
            elif verdict == "forward":
                text = candidate.strip() if candidate else ""
                LOGGER.info("New Element message -> Threema: %r", text)
                history.remember(text)  # remember BEFORE sending (loop guard)
                if send_to_threema_window(text=text, press_enter=threema_press_enter):
                    last_element = candidate
                else:
                    LOGGER.error("Failed to forward message to Threema Beta window.")

            # --- Threema -> Element -------------------------------------
            if not threema_to_element:
                continue
            candidate = read_last_threema_message(threema_cfg)
            verdict = classify_candidate(last_threema, candidate, history)
            if verdict == "echo":
                LOGGER.info("Threema shows our own relayed text - not sending back.")
                last_threema = candidate
            elif verdict == "forward":
                text = candidate.strip() if candidate else ""
                LOGGER.info("New Threema message -> Element: %r", text)
                history.remember(text)  # remember BEFORE pasting (loop guard)
                if send_to_element_window(text=text, press_enter=element_press_enter):
                    last_threema = candidate
                    # What we just sent is now Element's last own message.
                    last_element = text
                else:
                    LOGGER.error("Failed to forward message to Element window.")
        except KeyboardInterrupt:
            LOGGER.info("Relay stopped by user.")
            break


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--poll", type=float, default=2.0, help="poll interval in seconds")
    parser.add_argument("--no-threema-to-element", action="store_true",
                        help="only relay Element -> Threema (old behaviour)")
    parser.add_argument("--no-element-enter", action="store_true",
                        help="paste Threema text into Element but do not press Return")
    args = parser.parse_args()
    run_relay(
        poll_interval_seconds=args.poll,
        threema_to_element=not args.no_threema_to_element,
        element_press_enter=not args.no_element_enter,
    )


if __name__ == "__main__":
    main()

