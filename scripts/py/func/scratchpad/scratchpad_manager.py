# scripts/py/func/scratchpad/scratchpad_manager.py
import os
import threading
import time
from typing import Optional
import tkinter as tk
from .scratchpad_window import ScratchpadWindow
from .window_focus_manager import get_active_window_id
from ..gui.tk_root_manager import ensure_tk_root_running, run_on_tk_thread
from ..gui.ensure_xauthority import ensure_xauthority_env

LOG_FILE = "/tmp/aura_overlay_debug.log"


def _log(msg: str) -> None:
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
            f.flush()
    except Exception:
        pass


# ---- state --------------------------------------------------------
_window_ref: Optional[ScratchpadWindow] = None
_state_lock = threading.Lock()   # short-held: only guards _window_ref itself,
# never held across a Tk-thread round trip
_op_lock = threading.Lock()      # held by the CALLING thread for a WHOLE
# open-or-append round trip, so concurrent
# chunks queue up instead of racing to
# create duplicate pads or drop text
_generation = 0


def _pad_alive() -> bool:
    with _state_lock:
        ref = _window_ref
    if ref is None:
        return False
    try:
        return bool(ref.root.winfo_exists())
    except Exception:
        return False


def is_scratchpad_open() -> bool:
    global _window_ref
    if _pad_alive():
        return True
    with _state_lock:
        _window_ref = None
    return False


def _create_scratchpad(
    gen: int,
    ready_event: threading.Event,
    server_url: str,
    language: str,
    initial_text: str,
    target_win_id: Optional[str],
) -> None:
    global _window_ref
    os.environ['LANG'] = 'de_DE.UTF-8'
    os.environ['PYTHONUTF8'] = '1'
    ensure_xauthority_env()  # matters after e.g. a process self-restart
    _log(f"[gen={gen}] _create_scratchpad called")
    try:
        root = ensure_tk_root_running()
        top = tk.Toplevel(root)
        window = ScratchpadWindow(top, target_win_id, server_url, language, initial_text)
        top.attributes("-topmost", True)
        top.lift()
        top.focus_force()
        window.text_area.focus_set()

        def _on_destroy(event: tk.Event) -> None:
            global _window_ref
            if event.widget is not top:
                return
            with _state_lock:
                if _window_ref is window:
                    _window_ref = None
            _log(f"[gen={gen}] scratchpad destroyed")

        top.bind("<Destroy>", _on_destroy)

        with _state_lock:
            _window_ref = window
        _log(f"[gen={gen}] scratchpad ready, mapped={top.winfo_ismapped()}")
    except Exception as ex:
        _log(f"[gen={gen}] _create_scratchpad FAILED: {ex!r}")
    finally:
        ready_event.set()


def _append_locked(text: str, timeout: float) -> bool:
    """Assumes _op_lock is already held by the caller."""
    with _state_lock:
        ref = _window_ref
    if ref is None:
        return False
    try:
        if not ref.root.winfo_exists():
            return False
    except Exception:
        return False

    done = threading.Event()
    result = {"ok": False}

    def _do_append() -> None:
        try:
            if ref.root.winfo_exists():
                ref.append_text(text)
                ref.root.attributes("-topmost", True)
                ref.root.lift()
                ref.root.focus_force()
                ref.text_area.focus_set()
                result["ok"] = True
            else:
                _log("append: target window no longer exists")
        except Exception as ex:
            _log(f"append FAILED: {ex!r}")
        finally:
            done.set()

    run_on_tk_thread(_do_append)
    if not done.wait(timeout):
        _log("append: TIMED OUT waiting for Tk thread")
        return False
    return result["ok"]


def deliver_text(text: str, server_url: str, language: str, timeout: float = 2.0) -> bool:
    """
    Single entry point: appends `text` to the scratchpad if one is open,
    otherwise creates one with `text` as the initial content. The whole
    operation is serialized via _op_lock, so concurrent chunks queue up
    safely instead of racing to create duplicate pads or silently
    dropping text. Returns True only once delivery is confirmed.
    """
    global _generation
    os.environ['LANG'] = 'de_DE.UTF-8'
    os.environ['PYTHONUTF8'] = '1'
    with _op_lock:
        if _pad_alive():
            return _append_locked(text, timeout)
        _generation += 1
        gen = _generation
        ready = threading.Event()
        _log(f"[gen={gen}] deliver_text: no pad open, creating with initial text")
        target_win = get_active_window_id()
        run_on_tk_thread(lambda: _create_scratchpad(gen, ready, server_url, language, text, target_win))
        ok = ready.wait(timeout)
        success = ok and _pad_alive()
        if not success:
            _log(f"[gen={gen}] deliver_text: create TIMED OUT or FAILED (ok={ok})")
        return success


def open_scratchpad(
    server_url: str,
    language: str,
    initial_text: str = "",
    wait: bool = False,
    timeout: float = 2.0,
) -> bool:
    """Kept for the standalone subprocess entry point (open_scratchpad_action.py)."""
    global _generation
    os.environ['LANG'] = 'de_DE.UTF-8'
    os.environ['PYTHONUTF8'] = '1'
    with _op_lock:
        if _pad_alive():
            return True
        _generation += 1
        gen = _generation
        ready = threading.Event()
        _log(f"[gen={gen}] open_scratchpad called")
        target_win = get_active_window_id()
        run_on_tk_thread(lambda: _create_scratchpad(gen, ready, server_url, language, initial_text, target_win))
        if not wait:
            return True
        ok = ready.wait(timeout)
        success = ok and _pad_alive()
        if not success:
            _log(f"[gen={gen}] open_scratchpad TIMED OUT or FAILED (ok={ok})")
        return success


def append_to_scratchpad(text: str, timeout: float = 1.5) -> bool:
    """Kept for the standalone subprocess entry point."""
    with _op_lock:
        return _append_locked(text, timeout)
