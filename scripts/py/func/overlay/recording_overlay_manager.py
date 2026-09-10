import queue
import threading
import tkinter as tk
from .overlay_window import OverlayWindow
from ..config.dynamic_settings import settings

_cmd_queue: queue.Queue = queue.Queue()
_overlay_thread = None
_lock = threading.Lock()


def _run_tk() -> None:
    root = tk.Tk()
    size = getattr(settings, "RECORDING_OVERLAY_SIZE", 36)
    position = getattr(settings, "RECORDING_OVERLAY_POSITION", "tr")
    idle_mode = getattr(settings, "RECORDING_OVERLAY_IDLE_MODE", "hidden")
    topmost = getattr(settings, "RECORDING_OVERLAY_TOPMOST", True)
    OverlayWindow(root, _cmd_queue, size, position, idle_mode, topmost)
    root.mainloop()


def start_recording_overlay() -> None:
    global _overlay_thread
    if not getattr(settings, "RECORDING_OVERLAY_ENABLED", False):
        return
    with _lock:
        if _overlay_thread is None or not _overlay_thread.is_alive():
            _overlay_thread = threading.Thread(target=_run_tk, daemon=True)
            _overlay_thread.start()


def set_overlay_state(state: str) -> None:
    if getattr(settings, "RECORDING_OVERLAY_ENABLED", False):
        start_recording_overlay()
        _cmd_queue.put(state)


def stop_recording_overlay() -> None:
    if _overlay_thread is not None and _overlay_thread.is_alive():
        _cmd_queue.put("stop")
