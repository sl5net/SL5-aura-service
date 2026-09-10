import math
import re
import subprocess
import tkinter as tk
from typing import Dict, Tuple


def parse_xrandr_monitors(xrandr_output: str) -> Dict[str, Dict[str, int]]:
    """
    Pure function parsing xrandr output into dynamic monitor geometries.
    """
    monitors = {}
    pattern = re.compile(
        r"^(\S+)\s+connected\s+(primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)",
        re.MULTILINE
    )
    for match in pattern.finditer(xrandr_output):
        name = match.group(1)
        monitors[name] = {
            "x": int(match.group(5)),
            "y": int(match.group(6)),
            "width": int(match.group(3)),
            "height": int(match.group(4)),
            "is_primary": bool(match.group(2))
        }
    return monitors


def detect_monitor_bounds(root: tk.Tk) -> Tuple[int, int, int, int]:
    """
    Dynamically resolves monitor boundaries with zero hardcoded resolutions.
    """
    try:
        raw_xrandr = subprocess.check_output(
            ["xrandr", "--query"], text=True, timeout=2
        )
        monitors = parse_xrandr_monitors(raw_xrandr)
        for data in monitors.values():
            if data.get("is_primary"):
                return data["x"], data["y"], data["width"], data["height"]
        if monitors:
            first = next(iter(monitors.values()))
            return first["x"], first["y"], first["width"], first["height"]
    except Exception:
        pass

    # Dynamic fallback to active Tkinter screen geometry
    return 0, 0, root.winfo_screenwidth(), root.winfo_screenheight()


def calculate_monitor_position(
    mon_x: int,
    mon_y: int,
    mon_w: int,
    mon_h: int,
    size: int,
    position_code: str = "tr",
    margin: int = 16
) -> Tuple[int, int]:
    """
    Pure function calculating window position dynamically within bounds.
    """
    code = position_code.lower()
    if code == "bl":
        x = mon_x + margin
        y = mon_y + mon_h - size - margin
    elif code == "tl":
        x = mon_x + margin
        y = mon_y + margin
    elif code == "br":
        x = mon_x + mon_w - size - margin
        y = mon_y + mon_h - size - margin
    else:  # Default to 'tr'
        x = mon_x + mon_w - size - margin
        y = mon_y + margin
    return x, y


class OverlayDemo:
    def __init__(self, root: tk.Tk, bounds: Tuple[int, int, int, int], size: int = 36):
        self.root = root
        self.size = size
        self.mon_x, self.mon_y, self.mon_w, self.mon_h = bounds

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)

        self.canvas = tk.Canvas(
            root,
            width=size,
            height=size,
            bg="#181818",
            highlightthickness=0
        )
        self.canvas.pack()

    def set_state(self, state: str, position_code: str = "tr"):
        margin = max(8, self.size // 2)
        x, y = calculate_monitor_position(
            self.mon_x, self.mon_y, self.mon_w, self.mon_h,
            self.size, position_code, margin
        )
        self.root.geometry(f"{self.size}x{self.size}+{x}+{y}")

        if state == "hidden":
            self.root.withdraw()
            return

        self.root.deiconify()
        self.canvas.delete("all")
        pad = max(2, self.size // 7)

        if state == "recording":
            outline_w = max(1, self.size // 18)
            self.canvas.create_oval(
                pad, pad, self.size - pad, self.size - pad,
                fill="#e62222", outline="#ff6666", width=outline_w
            )
        elif state == "pentagon":
            cx = self.size / 2.0
            cy = self.size / 2.0
            radius = (self.size / 2.0) - pad
            points = []
            for i in range(5):
                angle = (i * 2.0 * math.pi / 5.0) - (math.pi / 2.0)
                points.append(cx + radius * math.cos(angle))
                points.append(cy + radius * math.sin(angle))
            self.canvas.create_polygon(
                points,
                fill="#444444", outline="#aaaaaa", width=1
            )


def run_demo():
    root = tk.Tk()
    bounds = detect_monitor_bounds(root)
    print(f"Dynamically detected bounds: x={bounds[0]}, y={bounds[1]}, w={bounds[2]}, h={bounds[3]}")

    overlay = OverlayDemo(root, bounds=bounds, size=36)

    print("=== AURA Recording Overlay Demo ===")
    print("1. Showing IDLE ('pentagon') at Top-Right (tr)…")
    overlay.set_state("pentagon", "tr")

    def step_2():
        print("2. Switching to RECORDING (red dot) at Top-Right (tr)…")
        overlay.set_state("recording", "tr")

    def step_3():
        print("3. Switching to IDLE ('hidden') at Top-Right…")
        overlay.set_state("hidden", "tr")

    def step_4():
        print("4. Switching to RECORDING (red dot) at Bottom-Left (bl)…")
        overlay.set_state("recording", "bl")

    def step_finish():
        print("5. Demo finished. Closing window.")
        root.destroy()

    root.after(2500, step_2)
    root.after(5500, step_3)
    root.after(8000, step_4)
    root.after(11000, step_finish)

    root.mainloop()


if __name__ == "__main__":
    run_demo()
