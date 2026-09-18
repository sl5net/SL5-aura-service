import json
from pathlib import Path
from typing import Tuple

STATE_FILE = Path(__file__).resolve().parents[4] / "data" / "_scratchpad" / "state.json"


def load_scratchpad_state() -> Tuple[str, bool]:
    try:
        if STATE_FILE.is_file():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return str(data.get("shortcut_mode", "direct")), bool(data.get("enter_submits", False))
    except Exception:
        pass
    return "direct", False


def save_scratchpad_state(shortcut_mode: str, enter_submits: bool) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"shortcut_mode": shortcut_mode, "enter_submits": enter_submits}, f, indent=2)
    except Exception:
        pass
