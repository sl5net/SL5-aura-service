import queue
import threading
import tkinter as tk
from .overlay_window import OverlayWindow
from ..config.dynamic_settings import settings
from ..gui.tk_root_manager import ensure_tk_root_running, run_on_tk_thread
_cmd_queue: queue.Queue = queue.Queue()
_overlay_ref = None
_is_open = False
_lock = threading.Lock()
def _create_overlay() -> None:
    global _overlay_ref, _is_open
    root = ensure_tk_root_running()
    top = tk.Toplevel(root)
    size = getattr(settings, "RECORDING_OVERLAY_SIZE", 36)
    position = getattr(settings, "RECORDING_OVERLAY_POSITION", "tr")
    idle_mode = getattr(settings, "RECORDING_OVERLAY_IDLE_MODE", "hidden")
    topmost = getattr(settings, "RECORDING_OVERLAY_TOPMOST", True)
    _overlay_ref = OverlayWindow(top, _cmd_queue, size, position, idle_mode, topmost)
    def _on_destroy(event: tk.Event) -> None:
        global _overlay_ref, _is_open
        if event.widget is top:
            _overlay_ref = None
            _is_open = False
    top.bind("<Destroy>", _on_destroy)
def start_recording_overlay() -> None:
    global _is_open
    if not getattr(settings, "RECORDING_OVERLAY_ENABLED", False):
        return
    with _lock:
        if _is_open:
            return
        _is_open = True
    run_on_tk_thread(_create_overlay)
def set_overlay_state(state: str) -> None:
    if getattr(settings, "RECORDING_OVERLAY_ENABLED", False):
        start_recording_overlay()
        _cmd_queue.put(state)


def stop_recording_overlay() -> None:
    if _is_open:
        _cmd_queue.put("stop")
