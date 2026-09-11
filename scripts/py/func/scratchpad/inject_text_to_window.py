import shutil
import subprocess
import sys
import time
from typing import Optional
from ..get_active_window_title import set_clipboard_text_linux
from .window_focus_manager import restore_window_focus


def send_paste_event() -> None:
    """
    Triggers paste shortcut (Ctrl+V) matching type_watcher.sh conventions.
    """
    if sys.platform.startswith("linux"):
        if shutil.which("dotool"):
            p = subprocess.Popen(
                ["dotool"],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            p.communicate(input=b"key ctrl+v\n")
            return
        if shutil.which("xdotool"):
            subprocess.run(
                ["xdotool", "key", "--clearmodifiers", "ctrl+v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    elif sys.platform == "win32":
        import ctypes
        user32 = ctypes.windll.user32
        user32.keybd_event(0x11, 0, 0, 0)
        user32.keybd_event(0x56, 0, 0, 0)
        user32.keybd_event(0x56, 0, 2, 0)
        user32.keybd_event(0x11, 0, 2, 0)


def inject_text_to_window(text: str, target_window_id: Optional[str] = None) -> bool:
    """
    Copies text to clipboard, restores target window focus, and triggers Ctrl+V.
    """
    if not text:
        return False
    if sys.platform.startswith("linux"):
        set_clipboard_text_linux(text)
    if target_window_id:
        restore_window_focus(target_window_id)
        time.sleep(0.08)
    send_paste_event()
    return True
