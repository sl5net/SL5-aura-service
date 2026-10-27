"""Read the latest INCOMING message from Threema Beta via X11 mouse automation.

Threema Beta renders its own context menu, so keyboard navigation does not
work. We right-click at a calibrated point in the last incoming bubble and
click "Copy Message" at a calibrated offset. Calibration values are shared
with threema-relay.zsh (`threema-relay.zsh calibrate` writes the config).
"""
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

LOGGER = logging.getLogger(__name__)

# xdotool matches ONE WM_CLASS field (instance OR class), not the wmctrl "instance.class" form
THREEMA_WINDOW_CLASS = "Threema Beta"
DEFAULT_CONFIG_PATH = Path(
    os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
) / "threema-relay.conf"


@dataclass(frozen=True)
class ThreemaCopyConfig:
    """Click geometry relative to the Threema window (from calibration)."""
    fx: float = 0.30          # click x as fraction of window width (left = incoming)
    bottom: int = 110         # click y: pixels above the window bottom edge
    dx: int = 12              # offset click point -> "Copy Message"
    dy: int = 14
    delay_menu: float = 0.30
    delay_copy: float = 0.20
    input_fx: float = 0.50    # message composer x (fraction of window width)
    input_bottom: int = 40    # message composer y: pixels above the window bottom


def parse_conf_text(text: str) -> Dict[str, str]:
    """Pure function: parse simple KEY=VALUE lines (comments allowed)."""
    values: Dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.split("#", 1)[0].strip().strip('"\'')
    return values


def config_from_values(values: Dict[str, str]) -> ThreemaCopyConfig:
    """Pure function: build config; tolerates decimal commas from German locales."""
    def num(name: str, default):
        raw = values.get(name)
        if raw is None:
            return default
        try:
            return type(default)(float(raw.replace(",", ".")))
        except ValueError:
            LOGGER.warning("Ignoring invalid %s=%r in config", name, raw)
            return default

    base = ThreemaCopyConfig()
    return ThreemaCopyConfig(
        fx=num("FX", base.fx),
        bottom=num("BOTTOM", base.bottom),
        dx=num("DX", base.dx),
        dy=num("DY", base.dy),
        delay_menu=num("DELAY_MENU", base.delay_menu),
        delay_copy=num("DELAY_COPY", base.delay_copy),
        input_fx=num("INPUT_FX", base.input_fx),
        input_bottom=num("INPUT_BOTTOM", base.input_bottom),
    )


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> ThreemaCopyConfig:
    try:
        return config_from_values(parse_conf_text(path.read_text(encoding="utf-8")))
    except OSError:
        LOGGER.warning("No calibration at %s - using defaults (run threema-relay.zsh calibrate)", path)
        return ThreemaCopyConfig()


def compute_click_points(
    win_x: int, win_y: int, win_w: int, win_h: int, cfg: ThreemaCopyConfig
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Pure function: (right-click point, 'Copy Message' point) in screen coordinates."""
    cx = int(win_x + win_w * cfg.fx)
    cy = win_y + win_h - cfg.bottom
    return (cx, cy), (cx + cfg.dx, cy + cfg.dy)


def _run(args, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, capture_output=True, **kwargs)


def _shell_vars(args) -> Dict[str, int]:
    out = _run(args).stdout.decode()
    return {k: int(v) for k, _, v in (l.partition("=") for l in out.split()) if v.lstrip("-").isdigit()}


def _find_window(window_class: str) -> Optional[str]:
    """First visible window of the class that is big enough to be the main window."""
    for flag in (["--onlyvisible"], []):
        res = subprocess.run(
            ["xdotool", "search", *flag, "--class", window_class],
            capture_output=True,
        )
        for wid in res.stdout.decode().split():
            try:
                geo = _shell_vars(["xdotool", "getwindowgeometry", "--shell", wid])
            except subprocess.SubprocessError:
                continue
            if geo.get("WIDTH", 0) > 300 and geo.get("HEIGHT", 0) > 300:
                return wid
    return None


def read_last_threema_message(
    cfg: Optional[ThreemaCopyConfig] = None,
    window_class: str = THREEMA_WINDOW_CLASS,
) -> Optional[str]:
    """
    Copy the last incoming message of the open chat via the context menu.

    Returns None when nothing was copied (e.g. the last message is our own,
    so the click hit no bubble). A sentinel in the clipboard detects that.

    Side effects: overwrites the X11 clipboard, activates the Threema window,
    moves/clicks the mouse (position restored afterwards).
    """
    cfg = cfg or load_config()
    sentinel = f"__relay_sentinel_{os.getpid()}_{time.monotonic_ns()}__"
    try:
        wid = _find_window(window_class)
        if wid is None:
            LOGGER.error("Threema window (%s) not found", window_class)
            return None
        geo = _shell_vars(["xdotool", "getwindowgeometry", "--shell", wid])
        mouse = _shell_vars(["xdotool", "getmouselocation", "--shell"])
        (cx, cy), (mx, my) = compute_click_points(
            geo["X"], geo["Y"], geo["WIDTH"], geo["HEIGHT"], cfg
        )

        # No capture_output here: xclip stays alive as clipboard owner and would
        # keep the pipes open, blocking subprocess.run until the clipboard changes.
        subprocess.run(
            ["xclip", "-selection", "clipboard", "-i"],
            input=sentinel.encode(), check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        _run(["xdotool", "windowactivate", "--sync", wid])
        time.sleep(0.15)
        _run(["xdotool", "mousemove", str(cx), str(cy), "click", "3"])
        time.sleep(cfg.delay_menu)
        _run(["xdotool", "mousemove", str(mx), str(my), "click", "1"])
        time.sleep(cfg.delay_copy)

        text = _run(["xclip", "-o", "-selection", "clipboard"]).stdout.decode("utf-8", "replace")
        if text == sentinel or not text.strip():
            # No bubble hit: close a possibly open menu with a harmless click
            _run([
                "xdotool", "mousemove",
                str(int(geo["X"] + geo["WIDTH"] * 0.5)), str(int(geo["Y"] + geo["HEIGHT"] * 0.25)),
                "click", "1",
            ])
            text = None
        # The context-menu click leaves focus in the chat history. Click into the
        # composer so a following Ctrl+V (send_to_threema_window) lands there.
        ix = int(geo["X"] + geo["WIDTH"] * cfg.input_fx)
        iy = geo["Y"] + geo["HEIGHT"] - cfg.input_bottom
        _run(["xdotool", "mousemove", str(ix), str(iy), "click", "1"])
        _run(["xdotool", "mousemove", str(mouse.get("X", 0)), str(mouse.get("Y", 0))])
        return text.strip() if text else None
    except (subprocess.SubprocessError, OSError, KeyError) as exc:
        LOGGER.error("Reading from Threema failed: %s", exc)
        return None
