import threading
import tkinter as tk
from typing import Optional
from .apply_match_replacement import apply_match_replacement
from .get_languagetool_matches import get_languagetool_matches
from .inject_text_to_window import inject_text_to_window
from .scratchpad_layout import create_scratchpad_layout
from .scratchpad_suggestions_panel import render_suggestions_panel


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
        if initial_text:
            self.text_area.insert("end", initial_text)

        self.root.bind("<Control-Return>", lambda e: self._on_accept())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def append_text(self, chunk: str) -> None:
        self.text_area.insert("end", chunk)
        self.text_area.see("end")

    def get_text(self) -> str:
        return self.text_area.get("1.0", "end-1c")

    def refresh_analysis(self) -> None:
        threading.Thread(
            target=self._run_async, args=(self.get_text(),), daemon=True
        ).start()

    def _run_async(self, text: str) -> None:
        matches = get_languagetool_matches(
            self.server_url, self.language, text
        )
        self.root.after(
            0,
            lambda: render_suggestions_panel(
                self.panel, matches, self._on_replace
            ),
        )

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
