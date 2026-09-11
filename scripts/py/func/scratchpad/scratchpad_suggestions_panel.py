import tkinter as tk
from typing import Callable, List


def render_suggestions_panel(
    container: tk.Frame,
    matches: List[dict],
    on_replace: Callable[[int, int, str], None],
    max_badges: int = 5,
) -> None:
    """
    Renders clickable suggestion buttons inside the container frame.
    """
    for child in container.winfo_children():
        child.destroy()

    count = 0
    for m in matches:
        word = m.get("word", "")
        offset = m.get("offset", 0)
        length = m.get("length", 0)
        for rep in m.get("replacements", []):
            if count >= max_badges:
                return
            btn = tk.Button(
                container,
                text=f"{word} -> {rep}",
                bg="#2d2d2d",
                fg="#4ec9b0",
                activebackground="#3e3e42",
                activeforeground="#ffffff",
                font=("Sans", 9),
                relief="flat",
                padx=6,
                pady=2,
                command=lambda off=offset, ln=length, r=rep: on_replace(
                    off, ln, r
                ),
            )
            btn.pack(side="left", padx=3, pady=2)
            count += 1
