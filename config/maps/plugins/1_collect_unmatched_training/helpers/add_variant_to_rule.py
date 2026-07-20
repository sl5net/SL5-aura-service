"""Append a new text variant to an existing rule's trailing regex group."""
import logging
import os
from pathlib import Path

from find_trailing_group_span import find_trailing_group_span  # noqa: E402

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


def add_variant_to_rule(fuzzy_map_file: Path, content: str, start: int, end: int, text: str):
    """
    Add `text` as a new '|'-separated alternative to the rule's trailing
    regex group (the group located by find_trailing_group_span) and write
    the updated content back to `fuzzy_map_file`.

    `start`/`end` are the offsets of the target rule within `content`.
    """
    rule_source = content[start:end]

    group_span = find_trailing_group_span(rule_source)
    if group_span is None:
        print(f'WARNING: could not locate the trailing "(...)$ " group in previous rule, skipping: {rule_source[:80]!r}')
        return
    group_start, group_end, has_parens = group_span
    group_text = rule_source[group_start:group_end]
    variants = group_text.split("|")
    if text in variants:
        return
    variants.append(text)

    abs_start = start + group_start
    abs_end = start + group_end
    joined = "|".join(variants)
    replacement = joined if has_parens else f"({joined})"
    new_content = content[:abs_start] + replacement + content[abs_end:]
    fuzzy_map_file.write_text(new_content, encoding="utf-8")
