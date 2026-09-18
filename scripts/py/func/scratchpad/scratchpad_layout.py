# scripts/py/func/scratchpad/scratchpad_layout.py
import tkinter as tk
from typing import Tuple


def create_scratchpad_layout(root: tk.Tk) -> Tuple[tk.Text, tk.Frame, tk.Button]:
    """
    Configures and packs standard UI widgets for the AURA Scratchpad.
    Returns (text_area, suggestions_panel, hint_label).
    """
    root.title("AURA Review Scratchpad")
    root.geometry("700x480")
    root.configure(bg="#1e1e1e")

    hint = tk.Button(
        root,
        text="Ctrl+Enter: Inject & Close | Esc: Discard",
        bg="#1e1e1e",
        fg="#888888",
        activebackground="#252526",
        activeforeground="#ffffff",
        font=("Sans", 9),
        relief="flat",
        anchor="w",
        cursor="hand2",
        padx=2,
        pady=1,
    )
    hint.pack(side="top", anchor="w", padx=8, pady=(4, 2))
    panel_frame = tk.Frame(root, bg="#1e1e1e")

    text_area = tk.Text(
        root,
        wrap="word",
        bg="#252526",
        fg="#d4d4d4",
        insertbackground="#ffffff",
        font=("Sans", 11),
        padx=8,
        pady=8,
    )
    text_area.pack(side="top", expand=True, fill="both", padx=8, pady=(4, 8))    
    
    return text_area, panel_frame, hint
