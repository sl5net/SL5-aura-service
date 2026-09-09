"""
Non-blocking delayed microphone unmute utility with pre-recording state tracking.
"""
import threading
from typing import Optional
from .audio_manager import is_microphone_muted, unmute_microphone

import threading
from typing import Optional

_delayed_unmute_timer: Optional[threading.Timer] = None
_timer_lock = threading.Lock()
_was_muted_before_session: Optional[bool] = None


def record_pre_session_mute_state(logger=None) -> None:
    """
    Records whether the microphone was muted prior to session start.
    """
    global _was_muted_before_session
    with _timer_lock:
        try:
            _was_muted_before_session = is_microphone_muted(logger=logger)
            if logger:
                logger.info(f"Recorded pre-session mic mute state: {_was_muted_before_session}")
        except Exception as exc:
            if logger:
                logger.warning(f"Could not determine pre-session mute state: {exc}")
            _was_muted_before_session = None


def cancel_delayed_unmute() -> None:
    """Cancels any pending delayed unmute timer."""
    global _delayed_unmute_timer
    with _timer_lock:
        if _delayed_unmute_timer is not None and _delayed_unmute_timer.is_alive():
            _delayed_unmute_timer.cancel()
            _delayed_unmute_timer = None


def schedule_delayed_unmute(delay_seconds: float = 0.8, logger=None) -> None:
    """
    Schedules an automatic microphone unmute after delay_seconds if the
    microphone was unmuted (or unknown) before the session started.
    """
    global _delayed_unmute_timer

    with _timer_lock:
        if _was_muted_before_session:
            if logger:
                logger.info("Microphone was muted before session; skipping delayed unmute.")
            return

        # If a timer already exists, cancel and replace it
        if _delayed_unmute_timer is not None and _delayed_unmute_timer.is_alive():
            _delayed_unmute_timer.cancel()
            _delayed_unmute_timer = None

    def _timer_callback():
        # declare global because we assign to it here
        global _delayed_unmute_timer
        try:
            if logger:
                logger.info(f"Delayed unmute timer fired ({delay_seconds}s). Restoring microphone.")
            unmute_microphone(logger=logger)
        finally:
            # clear the reference under lock to avoid races
            with _timer_lock:
                _delayed_unmute_timer = None
    
    _delayed_unmute_timer = threading.Timer(delay_seconds, _timer_callback)
    _delayed_unmute_timer.daemon = True
    _delayed_unmute_timer.start()
