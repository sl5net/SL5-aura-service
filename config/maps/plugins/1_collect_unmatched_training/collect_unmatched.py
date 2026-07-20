# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
"""
Entry point invoked (via on_match_exec) when the catch-all rule matches.
Delegates the actual file-update logic to helpers/process_unmatched_text.py.
"""
import logging
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent / 'helpers'))

helpers_dir = str((Path(__file__).resolve().parent / "helpers"))
if helpers_dir not in sys.path:
    sys.path.insert(0, helpers_dir)

sys.path.insert(0, str(Path(__file__).parent / 'helpers'))
from process_unmatched_text import process_unmatched_text
# from process_unmatched_text import process_unmatched_text


_tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((_tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

log_dir = PROJECT_ROOT / "log"
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_logger.propagate = False  # don't bubble up to the root logger / aura_engine.log

if not _logger.handlers:
    _handler = logging.FileHandler(str(log_dir / f"{__name__}.log"))
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s,%(msecs)03d - %(threadName)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    _logger.addHandler(_handler)

def log(msg: str) -> None:
    logging.info(msg)


def execute(match_data: dict):

    log(f'execute called: {match_data}\n')

    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']
    log(f'file_rule_path: {file_rule_path}')

    if not text:
        print(f'ERROR: text empty {text}')
        return None
    process_unmatched_text(file_rule_path, text)

    # IMPORTANT: This raise is intentional and required!
    # It prevents the catch-all match from being processed further as a
    # "recognized command" and the spoken text from being typed out into
    # the active window. WITHOUT this raise, the normal pipeline continues
    # and types the text out!
    # DO NOT REMOVE, even though it may look like leftover debug code!
    raise Exception('no text after replacement')
