import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional
import requests


# def get_languagetool_matches(
#     server_url: str,
#     language: str,
#     text: str,
#     max_suggestions: int = 5,
#     timeout: float = 6.0,
# ) -> List[Dict[str, Any]]:
#     """
#     Queries LanguageTool API and returns normalized matches for suggestions.
#     """
#     if not text or not text.strip() or not server_url:
#         return []
#     base_url = server_url.rstrip("/")
#     if base_url.endswith("/v2"):
#         check_url = f"{base_url}/check"
#     elif not base_url.endswith("/v2/check"):
#         check_url = f"{base_url}/v2/check"
#     else:
#         check_url = base_url
#     payload = {
#         "language": language,
#         "text": text,
#         "maxSuggestions": max_suggestions,
#     }
#     try:
#         with requests.Session() as session:
#             resp = session.post(check_url, data=payload, timeout=timeout)
#             resp.raise_for_status()
#             data = resp.json()
#     except Exception:
#         return []
#     normalized = []
#     for m in data.get("matches", []):
#         offset = int(m.get("offset", 0))
#         length = int(m.get("length", 0))
#         replacements = [
#             r.get("value")
#             for r in m.get("replacements", [])
#             if isinstance(r, dict) and r.get("value")
#         ]
#         normalized.append(
#             {
#                 "offset": offset,
#                 "length": length,
#                 "word": text[offset : offset + length],
#                 "message": m.get("message", ""),
#                 "rule_id": m.get("rule", {}).get("id", ""),
#                 "replacements": replacements[:max_suggestions],
#             }
#         )
#     return normalized


def get_active_window_id() -> Optional[str]:
    """
    Captures the identifier of the currently focused window.
    """
    try:
        if sys.platform.startswith("linux"):
            if shutil.which("xdotool"):
                out = subprocess.check_output(
                    ["xdotool", "getactivewindow"],
                    stderr=subprocess.DEVNULL,
                    timeout=1.0,
                    text=True,
                )
                return out.strip()

        elif sys.platform == "win32":
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            return str(hwnd) if hwnd else None
        elif sys.platform == "darwin":
            script = (
                'tell application "System Events" to get name of '
                "first application process whose frontmost is true"
            )
            out = subprocess.check_output(
                ["osascript", "-e", script],
                stderr=subprocess.DEVNULL,
                timeout=1.0,
                text=True,
            )
            return out.strip()
    except Exception:
        pass
    return None



def restore_window_focus(window_id: Optional[str]) -> bool:
    """
    Restores keyboard and input focus to the previously active window.
    """
    if not window_id:
        return False
    try:
        if sys.platform.startswith("linux"):
            if shutil.which("xdotool"):
                subprocess.run(
                    ["xdotool", "windowactivate", "--sync", str(window_id)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1.0,
                    check=True,
                )
                return True
        elif sys.platform == "win32":
            import ctypes
            hwnd = int(window_id)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
        elif sys.platform == "darwin":
            script = f'tell application "{window_id}" to activate'
            subprocess.run(
                ["osascript", "-e", script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1.0,
                check=True,
            )
            return True
    except Exception:
        pass
    return False
