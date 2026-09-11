import shutil
import subprocess
import sys
import threading
from typing import Optional
import tkinter as tk
from .scratchpad_window import ScratchpadWindow
from .window_focus_manager import get_active_window_id
from ..gui.tk_root_manager import ensure_tk_root_running, run_on_tk_thread
_window_ref: Optional[ScratchpadWindow] = None
_is_open = False
_lock = threading.Lock()
def _create_scratchpad(        
    server_url: str,
    language: str,
    initial_text: str,
    target_win_id: Optional[str],
) -> None:
    global _window_ref
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
    top.lift()
    top.focus_force()
    _window_ref.text_area.focus_set()
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(
            f"after focus_force: top_viewable={top.winfo_viewable()}, "
            f"focus_widget={top.focus_get()}\n"
        )
        f.flush()
    
    
    
    def _on_destroy(event: tk.Event) -> None:
        global _window_ref, _is_open
        if event.widget is top:
            _window_ref = None
            _is_open = False
    top.bind("<Destroy>", _on_destroy)

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

def is_scratchpad_open() -> bool:
    return _is_open

