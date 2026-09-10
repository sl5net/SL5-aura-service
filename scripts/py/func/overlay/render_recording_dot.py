import tkinter as tk


def render_recording_dot(canvas: tk.Canvas, size: int) -> None:
    pad = max(2, size // 7)
    canvas.create_oval(
        pad, pad, size - pad, size - pad,
        fill="#e62222", outline="#ff6666", width=max(1, size // 18)
    )
