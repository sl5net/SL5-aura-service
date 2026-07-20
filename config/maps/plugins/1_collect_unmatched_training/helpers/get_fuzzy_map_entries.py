# config/maps/plugins/1_collect_unmatched_training/helpers/get_fuzzy_map_entries.py
"""Parse a FUZZY_MAP_pre.py file's source and locate its top-level rule entries."""

import ast
import logging
import os
from pathlib import Path

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


def get_fuzzy_map_entries(content: str):
    """
    Parse the file content and return a list of (start_offset, end_offset)
    tuples, one per top-level element of the FUZZY_MAP_pre list, in source
    order.

    Using ast instead of line-based regex so multi-line rules (e.g. rules
    with nested dicts spanning several lines) are handled correctly.

    Returns None if the content can't be parsed or no FUZZY_MAP_pre list
    assignment is found.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None

    list_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'FUZZY_MAP_pre':
                    if isinstance(node.value, ast.List):
                        list_node = node.value
                        break
        if list_node is not None:
            break

    if list_node is None:
        return None

    line_offsets = [0]
    for line in content.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(line))

    def to_offset(lineno, col):
        return line_offsets[lineno - 1] + col

    entries = []
    for el in list_node.elts:
        start = to_offset(el.lineno, el.col_offset)

        # https://stackoverflow.com/ai-assist/shared/decccb81-1cfb-4907-84d1-1dc13a1763df
        seg = ast.get_source_segment(content, el)
        if seg is not None:
            end = start + len(seg)
        else:
            # fallback: use start (zero-length) or skip
            end = start

        # end = to_offset(el.end_lineno, el.end_col_offset)
        entries.append((start, end))

    log(f'entries={entries}')
    for i, (s, e) in enumerate(entries):
        log(f'entry {i}: repr={content[s:e]!r}')

    return entries
