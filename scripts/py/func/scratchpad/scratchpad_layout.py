import tkinter as tk
from typing import Tuple


def create_scratchpad_layout(root: tk.Tk) -> Tuple[tk.Text, tk.Frame, tk.Label]:
    """
    Configures and packs standard UI widgets for the AURA Scratchpad.
    Returns (text_area, suggestions_panel, hint_label).
    """
    root.title("AURA Review Scratchpad")
    root.geometry("680x380")
    root.configure(bg="#1e1e1e")

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
    text_area.pack(expand=True, fill="both", padx=8, pady=(8, 4))

    panel_frame = tk.Frame(root, bg="#1e1e1e")
    hint = tk.Label(
        root,
        text="Ctrl+Enter: Inject & Close | Esc: Discard",
        bg="#1e1e1e",
        fg="#777777",
        font=("Sans", 9),
    )
    hint.pack(anchor="w", padx=8, pady=(0, 6))
    return text_area, panel_frame, hint
