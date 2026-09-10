import re
import subprocess
import tkinter as tk
from typing import Tuple


def detect_monitor_bounds(root: tk.Tk) -> Tuple[int, int, int, int]:
    try:
        out = subprocess.check_output(["xrandr", "--query"], text=True, timeout=2)
        pat = re.compile(
            r"^(\S+)\s+connected\s+(primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)",
            re.MULTILINE,
        )
        first = None
        for m in pat.finditer(out):
            rect = (int(m.group(5)), int(m.group(6)), int(m.group(3)), int(m.group(4)))
            if m.group(2):
                return rect
            if first is None:
                first = rect
        if first:
            return first
    except Exception:
        pass
    return 0, 0, root.winfo_screenwidth(), root.winfo_screenheight()
