"""
Non-blocking delayed microphone unmute utility.
"""
import threading
from typing import Optional
from .audio_manager import unmute_microphone

_delayed_unmute_timer: Optional[threading.Timer] = None
_timer_lock = threading.Lock()


def cancel_delayed_unmute() -> None:
    """Cancels any pending delayed unmute timer."""
    global _delayed_unmute_timer
    with _timer_lock:
        if _delayed_unmute_timer is not None and _delayed_unmute_timer.is_alive():
            _delayed_unmute_timer.cancel()
            _delayed_unmute_timer = None


def schedule_delayed_unmute(delay_seconds: float = 0.8, logger=None) -> None:
    """
    Schedules an unmute call after delay_seconds in a daemon timer.
    """
    global _delayed_unmute_timer

    def _timer_callback():
        if logger:
            logger.info(f"Delayed unmute timer fired ({delay_seconds}s). Restoring microphone.")
        unmute_microphone(logger=logger)

    with _timer_lock:
        if _delayed_unmute_timer is not None and _delayed_unmute_timer.is_alive():
            _delayed_unmute_timer.cancel()
        _delayed_unmute_timer = threading.Timer(delay_seconds, _timer_callback)
        _delayed_unmute_timer.daemon = True
        _delayed_unmute_timer.start()

