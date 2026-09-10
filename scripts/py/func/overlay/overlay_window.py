import queue
import tkinter as tk
from .calculate_overlay_position import calculate_overlay_position
from .detect_monitor_bounds import detect_monitor_bounds
from .render_idle_pentagon import render_idle_pentagon
from .render_recording_dot import render_recording_dot


class OverlayWindow:
    def __init__(
        self,
        root: tk.Tk,
        cmd_queue: queue.Queue,
        size: int = 36,
        position: str = "tr",
        idle_mode: str = "hidden",
        topmost: bool = True,
    ):
        self.root = root
        self.cmd_queue = cmd_queue
        self.size = size
        self.idle_mode = idle_mode

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", topmost)

        b = detect_monitor_bounds(root)
        margin = max(8, size // 2)
        x, y = calculate_overlay_position(b[0], b[1], b[2], b[3], size, position, margin)
        self.root.geometry(f"{size}x{size}+{x}+{y}")

        self.canvas = tk.Canvas(
            root, width=size, height=size, bg="#181818", highlightthickness=0
        )
        self.canvas.pack()

        self._update(self.idle_mode)
        self._poll()

    def _poll(self):
        try:
            while True:
                cmd = self.cmd_queue.get_nowait()
                if cmd == "stop":
                    self.root.destroy()
                    return
                self._update(cmd)
        except queue.Empty:
            pass
        self.root.after(40, self._poll)

    def _update(self, state: str):
        actual = self.idle_mode if state == "idle" else state
        if actual == "hidden":
            self.root.withdraw()
            return
        self.root.deiconify()
        self.canvas.delete("all")
        if actual == "recording":
            render_recording_dot(self.canvas, self.size)
        elif actual == "pentagon":
            render_idle_pentagon(self.canvas, self.size)
