import queue
import shutil
import subprocess
import sys
import threading
from typing import Optional
import tkinter as tk
from .scratchpad_window import ScratchpadWindow
from .window_focus_manager import get_active_window_id
from ..gui.tk_root_manager import ensure_tk_root_running, run_on_tk_thread
_cmd_queue: queue.Queue = queue.Queue()
_window_ref: Optional[ScratchpadWindow] = None
_is_open = False
_lock = threading.Lock()
def _poll_scratchpad_queue(top: tk.Toplevel) -> None:
    global _window_ref
    try:
        while True:
            action, data = _cmd_queue.get_nowait()
            if action == "append" and _window_ref:
                _window_ref.append_text(data)
                _window_ref.refresh_analysis()
    except queue.Empty:
        pass
    if top.winfo_exists():
        top.after(50, lambda: _poll_scratchpad_queue(top))

def _create_scratchpad(
    server_url: str,
    language: str,
    initial_text: str,
    target_win_id: Optional[str],
) -> None:
    global _window_ref, _is_open
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write("_create_scratchpad called\n")
        f.flush()
    root = ensure_tk_root_running()
    top = tk.Toplevel(root)
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"scratchpad top created, mapped={top.winfo_ismapped()}\n")
        f.flush()    
    
    _window_ref = ScratchpadWindow(
        top, target_win_id, server_url, language, initial_text
    )
    def _on_destroy(event: tk.Event) -> None:
        global _window_ref, _is_open
        if event.widget is top:
            _window_ref = None
            _is_open = False
    top.bind("<Destroy>", _on_destroy)
    _poll_scratchpad_queue(top)

def open_scratchpad(
    server_url: str, language: str, initial_text: str = ""
) -> None:
    global _is_open
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"open_scratchpad called, _is_open={_is_open}\n")
        f.flush()
    with _lock:
        if _is_open:
            return
        _is_open = True
    target_win = get_active_window_id()
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"open_scratchpad: target_win={target_win}, scheduling _create_scratchpad\n")
        f.flush()
    run_on_tk_thread(
        lambda: _create_scratchpad(server_url, language, initial_text, target_win)
    )

def append_scratchpad(text_chunk: str) -> None:
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"append_scratchpad called with: {text_chunk!r}\n")
        f.flush()
    if is_scratchpad_open():
        _cmd_queue.put(("append", text_chunk))
        

def is_scratchpad_open() -> bool:
    return _is_open

def restore_window_focus(window_id: Optional[str]) -> bool:
    """
    Restores keyboard and input focus to the previously active window.
    """
    if not window_id:
        return False
    try:
        if sys.platform.startswith("linux"):
            if shutil.which("xdotool"):
                subprocess.run(
                    ["xdotool", "windowactivate", "--sync", str(window_id)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1.0,
                    check=True,
                )
                return True
        elif sys.platform == "win32":
            import ctypes
            hwnd = int(window_id)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
    except Exception:
        pass
    return False
