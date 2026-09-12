import logging
import os
from pathlib import Path
from scripts.py.func.config.dynamic_settings import settings
from scripts.py.func.get_project_root import get_aura_project_root
from scripts.py.func.global_state import SilentException
from scripts.py.func.scratchpad.scratchpad_manager import open_scratchpad

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


def execute(match_data: dict) -> None:
    log("execute called for scratchpad action")
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
    raise SilentException()


if __name__ == "__main__":
    try:
        execute({})
    except SilentException:
        pass
