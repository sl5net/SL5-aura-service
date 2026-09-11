"""
Manages a single shared Tk root running in exactly one dedicated
daemon thread. All Tk widget creation/mutation must be scheduled
onto this thread via run_on_tk_thread() or by using the root
returned by ensure_tk_root_running() only from within that thread.
"""
import queue
import threading
import tkinter as tk
from typing import Callable, Optional

_root: Optional[tk.Tk] = None
_ready_event = threading.Event()
_tk_thread: Optional[threading.Thread] = None
_lock = threading.Lock()
_pending_callbacks: "queue.Queue[Callable[[], None]]" = queue.Queue()
_POLL_INTERVAL_MS = 30

def _poll_pending_callbacks() -> None:
    try:
        while True:
            callback = _pending_callbacks.get_nowait()
            callback()
    except queue.Empty:
        pass
    if _root is not None:
        _root.after(_POLL_INTERVAL_MS, _poll_pending_callbacks)


def _run_tk_mainloop() -> None:
    global _root
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write("_run_tk_mainloop starting\n")
        f.flush()
    root = tk.Tk()
    root.withdraw()
    _root = root
    _ready_event.set()
    root.after(_POLL_INTERVAL_MS, _poll_pending_callbacks)
    root.mainloop()


    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write("_run_tk_mainloop exited (should not happen while running)\n")
        f.flush()

def ensure_tk_root_running() -> tk.Tk:
    """Starts the shared Tk root thread if needed, returns the root."""
    global _tk_thread
    with _lock:
        if _tk_thread is None or not _tk_thread.is_alive():
            _ready_event.clear()
            _tk_thread = threading.Thread(target=_run_tk_mainloop, daemon=True)
            _tk_thread.start()
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write("ensure_tk_root_running waiting for ready_event\n")
        f.flush()
    got = _ready_event.wait(timeout=5.0)
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"ensure_tk_root_running wait done, got={got}\n")
        f.flush()
    return _root


def run_on_tk_thread(callback: Callable[[], None]) -> None:
    """Schedules callback on the Tk thread. Safe to call from any thread."""
    ensure_tk_root_running()
    _pending_callbacks.put(callback)
