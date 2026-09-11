import tkinter as tk
from typing import List


def highlight_matches(text_area: tk.Text, matches: List[dict]) -> None:
    """
    Highlights LanguageTool match spans in the text widget: bold,
    underlined, red foreground.
    """
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"highlight_matches called, matches={len(matches)}\n")
        f.flush()
    text_area.tag_configure(
        "lt_error",
        font=("Sans", 11, "bold underline"),
        foreground="#ff4444",
    )
    text_area.tag_remove("lt_error", "1.0", "end")
    for m in matches:
        offset = m.get("offset", 0)
        length = m.get("length", 0)
        if length <= 0:
            continue
        start = f"1.0+{offset}c"
        end = f"1.0+{offset + length}c"
        text_area.tag_add("lt_error", start, end)
        with open("/tmp/aura_overlay_debug.log", "a") as f:
            f.write(f"  tag_add lt_error at {start}..{end}\n")
            f.flush()
    with open("/tmp/aura_overlay_debug.log", "a") as f:
        f.write(f"highlight_matches done, tag_ranges={text_area.tag_ranges('lt_error')}\n")
        f.flush()

