# scripts/py/func/scratchpad/scratchpad_window.py
import threading
import time
import tkinter as tk
from typing import Optional
from .apply_match_replacement import apply_match_replacement
from .get_languagetool_matches import get_languagetool_matches
from .highlight_matches import highlight_matches
from .inject_text_to_window import inject_text_to_window
from .resolve_keysym_char import resolve_keysym_char
from typing import Optional, Tuple
from .scratchpad_layout import create_scratchpad_layout
from .scratchpad_state_io import load_scratchpad_state, save_scratchpad_state
from .scratchpad_suggestions_panel import render_suggestions_panel
from ..gui.tk_root_manager import run_on_tk_thread

KP_CODE_MAP = {
    87: 1, 88: 2, 89: 3,
    83: 4, 84: 5, 85: 6,
    79: 7, 80: 8, 81: 9,
    97: 1, 98: 2, 99: 3,
    100: 4, 101: 5, 102: 6,
    103: 7, 104: 8, 105: 9,
}


def _resolve_digit_key(event: tk.Event) -> Tuple[Optional[int], bool]:
    code = getattr(event, "keycode", 0)
    if code in KP_CODE_MAP:
        return KP_CODE_MAP[code], True
    if event.keysym.startswith("KP_") and event.keysym[3:] in "123456789":
        return int(event.keysym[3:]), True
    if event.keysym in "123456789":
        return int(event.keysym), False
    return None, False
class ScratchpadWindow:
    def __init__(
        self,
        root: tk.Tk,
        target_window_id: Optional[str],
        server_url: str,
        language: str,
        initial_text: str = "",
    ):
        self.root = root
        self.target_window_id = target_window_id
        self.server_url = server_url
        self.language = language

        self.text_area, self.panel, self.hint = create_scratchpad_layout(root)
        
        self._debounce_id: Optional[str] = None
        self._analysis_generation = 0
        self._shortcut_mode, self._enter_submits = load_scratchpad_state()
        self._suggestion_actions: list = []
        self._current_matches: list = []
        self.hint.config(
            command=self._toggle_enter_mode,
            text="Enter: Inject & Close | Esc: Discard" if self._enter_submits else "Ctrl+Enter: Inject & Close | Esc: Discard",
        )        
        self._suggestion_actions: list = []
        self._current_matches: list = []        
        
        if initial_text:

            with open("/tmp/aura_overlay_debug.log", "a") as f:
                f.write(f"before insert, initial_text: {initial_text.encode('unicode_escape')!r}\n")
                f.flush()
            self.text_area.insert("end", initial_text)
            with open("/tmp/aura_overlay_debug.log", "a") as f:
                inserted = self.text_area.get("1.0", "end-1c")
                f.write(f"after insert, text_area content: {inserted.encode('unicode_escape')!r}\n")
                f.flush()
            self.refresh_analysis()
            
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"tcl encoding system={self.root.tk.call('encoding', 'system')}\n")
            f.flush()
            
        self.text_area.edit_modified(False)
        
        # Event-Bindings
        self.text_area.bind("<<Modified>>", self._on_text_modified)
        self.text_area.bind("<KeyPress>", self._on_key_press)
        self.text_area.bind("<Control-BackSpace>", self._delete_word)

        self.root.bind("<Control-Return>",   self._on_control_return)
        self.root.bind("<Escape>", self._on_escape)
        self.root.bind("<Destroy>", self._on_window_destroy)
        self.text_area.focus_set()

    def _delete_word(self, event: tk.Event) -> str:
        current_pos = self.text_area.index(tk.INSERT)
        text_before_cursor = self.text_area.get("1.0", current_pos)

        word_start_pos = text_before_cursor.rfind(" ", 0, len(text_before_cursor))
        if word_start_pos == -1:
            word_start_pos = 0
        else:
            word_start_pos += 1

        self.text_area.delete(f"1.0 + {word_start_pos} chars", current_pos)
        return "break"

    def _on_key_press(self, event: tk.Event) -> Optional[str]:
        if event.keysym in ("Return", "KP_Enter"):
            ctrl_pressed = bool(event.state & 4)
            if self._enter_submits:
                if not ctrl_pressed:
                    self._on_accept()
                    return "break"
                self.text_area.insert("insert", "\n")
                self.text_area.see("insert")
                return "break"
            if ctrl_pressed:
                self._on_accept()
                return "break"
        if event.keysym == "Tab" and self._current_matches:
            self._toggle_shortcut_mode()
            return "break"
        num, is_kp = _resolve_digit_key(event)
        if self._current_matches and num is not None:
            alt_pressed = bool(event.state & 0x0008 or event.state & 0x20000)
            if self._shortcut_mode == "alt":
                should_trigger = alt_pressed
            elif self._shortcut_mode == "numpad":
                should_trigger = is_kp and not alt_pressed and not (event.state & 4)
            else:
                should_trigger = not alt_pressed and not (event.state & 4)
            if should_trigger:
                if num == 9:
                    self._on_replace_all()
                    return "break"
                if 1 <= num <= len(self._suggestion_actions):
                    self._suggestion_actions[num - 1]()
                    return "break"
                
                
                if 1 <= num <= len(self._suggestion_actions):
                    self._suggestion_actions[num - 1]()
                    return "break"
        keysym_num = getattr(event, "keysym_num", None)
        char = resolve_keysym_char(event.keysym, event.char, keysym_num)
        
        if char is not None:
            try:
                self.text_area.delete("sel.first", "sel.last")
            except tk.TclError:
                pass
            self.text_area.insert("insert", char)
            self.text_area.see("insert")
            return "break"
        return None

    def append_text(self, text: str) -> None:
        prev_char = self.text_area.get("insert - 1 chars", "insert")
        prefix = " " if prev_char and not prev_char.isspace() else ""
        self.text_area.insert("insert", prefix + text)
        self.text_area.see("insert")
        # Explicit pause to stabilize GUI event queue on incoming speech chunks
        time.sleep(0.05)
        self.refresh_analysis()

    def get_text(self) -> str:
        return self.text_area.get("1.0", "end-1c")

    def _on_text_modified(self, event=None) -> None:
        self.text_area.edit_modified(False)
        if self._debounce_id is not None:
            self.root.after_cancel(self._debounce_id)
        self._debounce_id = self.root.after(1000, self._trigger_debounced_refresh)

    def _trigger_debounced_refresh(self) -> None:
        self._debounce_id = None
        self.refresh_analysis()


    def refresh_analysis(self) -> None:
        self._analysis_generation += 1
        gen = self._analysis_generation
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"refresh_analysis called, gen={gen}, text={self.get_text()!r}\n")
            f.flush()
        threading.Thread(
            target=self._run_async, args=(self.get_text(), gen), daemon=True
        ).start()

    def _run_async(self, text: str, gen: int) -> None:
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"_run_async: gen={gen} calling get_languagetool_matches\n")
            f.flush()
        matches = get_languagetool_matches(
            self.server_url, self.language, text
        )
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(
                f"_run_async: gen={gen} got {len(matches)} matches, "
                f"current_generation={self._analysis_generation}, "
                f"scheduling render={gen == self._analysis_generation}\n"
            )
            f.flush()
        if gen != self._analysis_generation:
            return

        def _apply_updates() -> None:
            self._current_matches = matches
            highlight_matches(self.text_area, matches)
            self._render_current_panel()            
            if matches:
                self.panel.pack(side="top", fill="x", padx=8, pady=2, before=self.text_area)
            else:
                self.panel.pack_forget()
                
            with open("/tmp/aura_overlay_debug.log", "a") as f:
                f.write(
                    f"panel visibility updated: matches={len(matches)}, mapped={self.panel.winfo_ismapped()}\n"
                )
                f.flush()
        run_on_tk_thread(_apply_updates)

        
    def _toggle_enter_mode(self) -> None:
        self._enter_submits = not self._enter_submits
        text = "Enter: Inject & Close | Esc: Discard" if self._enter_submits else "Ctrl+Enter: Inject & Close | Esc: Discard"
        self.hint.config(text=text)
        save_scratchpad_state(self._shortcut_mode, self._enter_submits)
    def _toggle_shortcut_mode(self) -> None:
        cycle = {"direct": "alt", "alt": "numpad", "numpad": "direct"}
        self._shortcut_mode = cycle.get(self._shortcut_mode, "direct")
        self._render_current_panel()
        save_scratchpad_state(self._shortcut_mode, self._enter_submits)

    def _render_current_panel(self) -> None:
        self._suggestion_actions, _ = render_suggestions_panel(
            self.panel,
            self._current_matches,
            self._on_replace,
            self._on_replace_all,
            self._toggle_shortcut_mode,
            self._shortcut_mode,
        )

    def _on_replace_all(self) -> None:
        text = self.get_text()
        sorted_matches = sorted(self._current_matches, key=lambda m: m.get("offset", 0), reverse=True)
        for m in sorted_matches:
            reps = m.get("replacements", [])
            if reps:
                text = apply_match_replacement(text, m.get("offset", 0), m.get("length", 0), reps[0])
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", text)
        self.refresh_analysis()

    def _on_replace(self, offset: int, length: int, rep: str) -> None:
        new_text = apply_match_replacement(
            self.get_text(), offset, length, rep
        )
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", new_text)
        # Explicit pause to prevent event race conditions during rapid button replacements
        time.sleep(0.05)
        self.refresh_analysis()

    def _on_escape(self, event=None) -> None:
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"Escape key pressed at {event}, destroying scratchpad\n")
            f.flush()
        self.root.destroy()

    def _on_control_return(self, event=None) -> None:
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"Control-Return pressed at {event}, triggering _on_accept\n")
            f.flush()
        self._on_accept()

    def _on_window_destroy(self, event=None) -> None:
        if event and event.widget == self.root:
            with open("/tmp/aura_overlay_debug.log", "a") as f:
                f.write(f"Scratchpad root window destroyed via {event}\n")
                f.flush()

    def _on_accept(self) -> None:
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"_on_accept called, target_window_id={self.target_window_id}\n")
            f.flush()
        inject_text_to_window(self.get_text(), self.target_window_id)
        self.root.destroy()
        
        
