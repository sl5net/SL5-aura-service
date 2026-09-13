# config/maps/plugins/0_aura_quickstart/open_scratchpad_action.py
# PYTHONPATH=. .venv/bin/python3 config/maps/plugins/0_aura_quickstart/open_scratchpad_action.py
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from scripts.py.func.config.dynamic_settings import settings
from scripts.py.func.get_project_root import get_aura_project_root
from scripts.py.func.global_state import SilentException
from scripts.py.func.gui.ensure_xauthority import ensure_xauthority_env
from scripts.py.func.scratchpad.scratchpad_manager import open_scratchpad, is_scratchpad_open

_tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

log_dir = SL5NET_AURA_PROJECT_ROOT / "log"
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_logger.propagate = False
if not _logger.handlers:
    _handler = logging.FileHandler(str(log_dir / f"{__name__}.log"))
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s,%(msecs)03d - %(threadName)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    _logger.addHandler(_handler)


def log(msg: str) -> None:
    _logger.info(msg)

def run_gui_window() -> None:
    ensure_xauthority_env()
    server_url = getattr(
        settings,
        "LANGUAGETOOL_BASE_URL",
        getattr(
            settings,
            "LANGUAGETOOL_CHECK_URL",
            f"http://127.0.0.1:{getattr(settings, 'LANGUAGETOOL_PORT', 8082)}/v2/check",
        ),
    )
    language = getattr(settings, "LT_LANGUAGE", "de-DE")
    open_scratchpad(server_url, language, initial_text="")
    time.sleep(0.5)
    while is_scratchpad_open():
        time.sleep(0.2)


def execute(match_data: dict) -> None:
    log("execute called: spawning detached scratchpad process")
    python_bin = sys.executable or str(SL5NET_AURA_PROJECT_ROOT / ".venv" / "bin" / "python3")
    script_path = Path(__file__).resolve()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(SL5NET_AURA_PROJECT_ROOT)

    ensure_xauthority_env()
    if "DISPLAY" in os.environ:
        env["DISPLAY"] = os.environ["DISPLAY"]
    if "XAUTHORITY" in os.environ:
        env["XAUTHORITY"] = os.environ["XAUTHORITY"]

    subprocess.Popen(
        [python_bin, str(script_path), "--run-window"],
        cwd=str(SL5NET_AURA_PROJECT_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True,
        start_new_session=True,
    )
    raise SilentException()


if __name__ == "__main__":
    run_gui_window()
