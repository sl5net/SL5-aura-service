import math, tkinter as tk


def render_idle_pentagon(canvas: tk.Canvas, size: int) -> None:
    p = max(2, size // 7)
    c, r = size / 2.0, (size / 2.0) - p
    pts = []
    for i in range(5):
        a = i * 0.4 * math.pi - 0.5 * math.pi
        pts += [c + r * math.cos(a), c + r * math.sin(a)]
    canvas.create_polygon(pts, fill="#444444", outline="#aaaaaa")
