"""Orchestrate the update of a FUZZY_MAP_pre.py file for an unmatched text."""
import logging
import os
import sys

from pathlib import Path


# helpers4collect_unmatched
from get_fuzzy_map_entries import get_fuzzy_map_entries
from find_catch_all_index import find_catch_all_index
from add_variant_to_rule import add_variant_to_rule
from insert_template_rule import insert_template_rule

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


def process_unmatched_text(file_rule_path: str, text: str):
    """
    Update the FUZZY_MAP_pre.py file at `file_rule_path` so it can match
    `text` next time:

    - No catch-all rule found -> do nothing.
    - Catch-all rule found, with a rule before it -> add `text` as a new
      alternative to that previous rule's trailing regex group.
    - Catch-all rule found, with no rule before it -> insert the template
      rule ('nix', r'^(nix)$') right before the catch-all rule.
    """

    log(f'20260720_1942 called with argv={sys.argv}\n')

    fuzzy_map_file = Path(file_rule_path)
    if not fuzzy_map_file.exists():
        log('ABORT: file does not exist')
        return

    content = fuzzy_map_file.read_text(encoding="utf-8")

    entries = get_fuzzy_map_entries(content)
    log(f'entries found: {len(entries) if entries else 0}')
    if not entries:
        log('ABORT: no entries parsed')
        return

    catch_all_index = find_catch_all_index(content, entries)
    log(f'catch_all_index={catch_all_index}')
    if catch_all_index is None:
        log('ABORT: no catch-all found')
        return

    if catch_all_index > 0:
        # There is a rule before the catch-all -> modify it
        prev_start, prev_end = entries[catch_all_index - 1]
        log(f'adding variant to rule at {prev_start}:{prev_end}')
        add_variant_to_rule(fuzzy_map_file, content, prev_start, prev_end, text)
    else:
        # No rule before the catch-all -> insert a template rule
        catch_all_start, _ = entries[catch_all_index]
        log(f'inserting template rule before catch-all at {catch_all_start}')
        insert_template_rule(fuzzy_map_file, content, catch_all_start, text)
