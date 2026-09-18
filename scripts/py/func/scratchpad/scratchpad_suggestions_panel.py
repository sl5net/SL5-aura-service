# scripts/py/func/scratchpad/scratchpad_suggestions_panel.py
import tkinter as tk
from typing import Callable, List, Optional, Tuple


def _build_panel_button(
    container: tk.Frame,
    text: str,
    cmd: Callable[[], None],
) -> tk.Button:
    btn = tk.Button(
        container,
        text=text,
        bg="#2d2d2d",
        fg="#4ec9b0",
        activebackground="#3e3e42",
        activeforeground="#ffffff",
        font=("Sans", 9),
        relief="flat",
        padx=5,
        pady=2,
        command=cmd,
    )
    btn.pack(side="left", padx=2, pady=2)
    return btn


def _format_button_prefix(shortcut_mode: str, count: int) -> str:
    if shortcut_mode == "alt":
        return f"Alt+{count}: "
    if shortcut_mode == "numpad":
        return f"Num{count}: "
    return f"{count}: "


def render_suggestions_panel(
    container: tk.Frame,
    matches: List[dict],
    on_replace: Callable[[int, int, str], None],
    on_replace_all: Callable[[], None],
    on_toggle_mode: Callable[[], None],
    shortcut_mode: str = "direct",
    max_badges: int = 8,
) -> Tuple[List[Callable[[], None]], Optional[Callable[[], None]]]:
    for child in container.winfo_children():
        child.destroy()
    if not matches:
        return [], None
        
    actions: List[Callable[[], None]] = []
    mode_labels = {"alt": "[Tab: Alt+1-9]", "numpad": "[Tab: NumPad]", "direct": "[Tab: 1-9]"}
    mode_btn = tk.Button(
        container,
        text=mode_labels.get(shortcut_mode, "[Tab: 1-9]"),
        bg="#1e1e1e",
        fg="#9cdcfe",
        activebackground="#252526",
        activeforeground="#ffffff",
        font=("Sans", 9, "bold"),
        relief="flat",
        padx=4,
        pady=2,
        command=on_toggle_mode,
    )
    mode_btn.pack(side="left", padx=(0, 4), pady=2)

    count = 0
    for m in matches:
        word = m.get("word", "")
        offset = m.get("offset", 0)
        length = m.get("length", 0)
        for rep in m.get("replacements", []):
            if count >= max_badges:
                break
            count += 1
            prefix = _format_button_prefix(shortcut_mode, count)
            action = lambda off=offset, ln=length, r=rep: on_replace(off, ln, r) # noqa: E731
            actions.append(action)
            _build_panel_button(container, f"{prefix}{word} -> {rep}", action)

    apply_all_action = None
    if len(actions) > 1:
        all_prefix = _format_button_prefix(shortcut_mode, 9) + "All"
        apply_all_action = on_replace_all
        _build_panel_button(container, all_prefix, on_replace_all)

    return actions, apply_all_action
