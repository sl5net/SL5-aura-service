import json
from pathlib import Path
from typing import Tuple

STATE_FILE = Path(__file__).resolve().parents[4] / "data" / "_scratchpad" / "state.json"


def load_scratchpad_state() -> Tuple[bool, bool]:
    try:
        if STATE_FILE.is_file():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return bool(data.get("alt_mode", False)), bool(data.get("enter_submits", False))
    except Exception:
        pass
    return False, False


def save_scratchpad_state(alt_mode: bool, enter_submits: bool) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"alt_mode": alt_mode, "enter_submits": enter_submits}, f, indent=2)
    except Exception:
        pass
