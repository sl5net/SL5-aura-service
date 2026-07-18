# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# scripts/py/func/global_state.py

from types import SimpleNamespace
import threading
from typing import Any, Dict

# Thread-local storage for per-thread transient state
thread_state = threading.local()

# SEQUENCE_LOCK: shared namespace containing synchronization primitives and flags.
# - execute_only_event: an Event that is set once and never cleared (idempotent, thread-safe).
# - lock: an RLock to protect access to shared mutable structures where needed.
SEQUENCE_LOCK = SimpleNamespace(
    execute_only_event=threading.Event(),
    lock=threading.RLock()
)

# The last successfully processed chunk ID. All new output must be this ID + 1.
# Access to this variable should be protected by SEQUENCE_LOCK.lock.
LAST_PROCESSED_ID: int = 0

# Toggle logging (no lock needed if it's read-mostly; set at startup only)
LOGGING_ENABLED: bool = True

# Cache to store chunks that arrived out of order.
# Access must be synchronized by SEQUENCE_LOCK.lock.
OUT_OF_ORDER_CACHE: Dict[int, Any] = {}

# A mapping of all active session IDs to their last processed chunk ID.
# Access must be synchronized by SEQUENCE_LOCK.lock.
SESSION_LAST_PROCESSED: Dict[Any, int] = {}

# Signature times mapping (also protected by lock)
SIGNATURE_TIMES: Dict[Any, float] = {}

# Small ring keeping last recognitions (kept small; protect with lock if mutated from multiple threads)
_last_recognitions = []
_MAX_RECOGNITIONS = 2

last_recognitions = []

def add_recognition(text: str) -> None:
    """
    Adds a new recognition text to the global state.
    Keeps only the last 2 entries:
    Index 0: Previous input
    Index 1: Current input
    """
    # Protect other threads write to it
    with SEQUENCE_LOCK.lock:
        _last_recognitions.append(text)
        if len(_last_recognitions) > _MAX_RECOGNITIONS:
            _last_recognitions.pop(0)


# def get_last_recognitions() -> list:
#     """Return a shallow copy of the last recognitions (thread-safe)."""
#     with SEQUENCE_LOCK.lock:
#         return list(_last_recognitions)


# Helper for parsing string/various representations to bool
def _str_to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    s = str(val).strip().lower()
    return s in ("1", "true", "t", "yes", "y", "on")


def resolve_execute_only(options: Dict[str, Any]) -> bool:
    """
    Resolve and possibly set the global "execute only" flag.

    Semantics:
    - If the Event is already set -> return True (never unset).
    - If 'execute_only' not in options -> return current event state (do nothing).
    - If 'execute_only' present and parses to True -> set the Event and return True.
    - Otherwise -> return current event state (likely False).

    This function modifies the shared Event atomically (Event.set is thread-safe).
    """
    # Fast path: already set
    if SEQUENCE_LOCK.execute_only_event.is_set():
        return True

    # Key not present -> do nothing
    if 'execute_only' not in options:
        return SEQUENCE_LOCK.execute_only_event.is_set()

    # Only set on parsed true; Event.set() is thread-safe and idempotent
    if _str_to_bool(options.get('execute_only')):
        SEQUENCE_LOCK.execute_only_event.set()
        return True

    return SEQUENCE_LOCK.execute_only_event.is_set()


class SilentException(Exception):
    pass

# Example helpers to update/check LAST_PROCESSED_ID safely
# def get_last_processed_id() -> int:
#     with SEQUENCE_LOCK.lock:
#         return LAST_PROCESSED_ID


# def set_last_processed_id(new_id: int) -> None:
#     global LAST_PROCESSED_ID
#     with SEQUENCE_LOCK.lock:
#         LAST_PROCESSED_ID = new_id


# Helpers for OUT_OF_ORDER_CACHE and SESSION_LAST_PROCESSED (always use lock)
# def cache_out_of_order(expected_id: int, chunk_data: Any) -> None:
#     with SEQUENCE_LOCK.lock:
#         OUT_OF_ORDER_CACHE[expected_id] = chunk_data


# def pop_out_of_order(expected_id: int) -> Any:
#     with SEQUENCE_LOCK.lock:
#         return OUT_OF_ORDER_CACHE.pop(expected_id, None)


# def set_session_last_processed(session_id: Any, chunk_id: int) -> None:
#     with SEQUENCE_LOCK.lock:
#         SESSION_LAST_PROCESSED[session_id] = chunk_id


# def get_session_last_processed(session_id: Any) -> int:
#     with SEQUENCE_LOCK.lock:
#         return SESSION_LAST_PROCESSED.get(session_id, 0)
