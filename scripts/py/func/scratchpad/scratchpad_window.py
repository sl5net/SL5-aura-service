# scripts/py/func/scratchpad/scratchpad_window.py
import threading
import tkinter as tk
from typing import Optional
from .apply_match_replacement import apply_match_replacement
from .get_languagetool_matches import get_languagetool_matches
from .highlight_matches import highlight_matches
from .inject_text_to_window import inject_text_to_window
from .scratchpad_layout import create_scratchpad_layout
from .scratchpad_suggestions_panel import render_suggestions_panel
from ..gui.tk_root_manager import run_on_tk_thread

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

        self.text_area, self.panel = create_scratchpad_layout(root)
        self._debounce_id: Optional[str] = None
        self._analysis_generation = 0
        if initial_text:            
            
            self.text_area.insert("end", initial_text)
            self.refresh_analysis()
        self.text_area.edit_modified(False)
        self.text_area.bind("<<Modified>>", self._on_text_modified)
        self.root.bind("<Control-Return>", lambda e: self._on_accept())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

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
            highlight_matches(self.text_area, matches)
            render_suggestions_panel(self.panel, matches, self._on_replace)
        run_on_tk_thread(_apply_updates)
        
        
    def _on_replace(self, offset: int, length: int, rep: str) -> None:
        new_text = apply_match_replacement(
            self.get_text(), offset, length, rep
        )
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", new_text)
        self.refresh_analysis()



    def _on_accept(self) -> None:
        inject_text_to_window(self.get_text(), self.target_window_id)
        self.root.destroy()
