"""Locate the regex group that sits directly before the final '$' anchor
of a rule's pattern string literal."""
import logging
import re
from pathlib import Path
import os


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


def find_trailing_group_span(rule_source: str):
    """
    Locate the last regex group, i.e. "(...)", that sits directly before the
    final '$' anchor inside the rule's pattern string literal. This is the
    group new variants get appended to.

    If no such group exists (e.g. r'^hans$'), fall back to treating the bare
    content between '^' and '$' as an implicit group that still needs to be
    wrapped in parentheses by the caller.

    Returns (start, end, has_parens):
        start, end   - offsets (within rule_source) of the group's inner
                        content (or the bare content if has_parens is False)
        has_parens   - True if (start, end) already sit inside an existing
                        "(...)" pair; False if the caller must add the
                        parentheses itself when substituting.
    Returns None if no usable pattern literal could be found at all.
    """
    # Find the start of the pattern string literal: an optional string
    # prefix (r/f/fr/rf), a quote char, then the '^' anchor.
    literal_re = re.compile(r"[a-zA-Z]{0,2}(['\"])\^")
    lit_match = literal_re.search(rule_source)
    if not lit_match:
        return None
    quote_char = lit_match.group(1)
    pattern_start = lit_match.end()

    # Find the matching closing quote (naive: patterns here don't contain
    # the delimiting quote character itself).
    quote_end = rule_source.find(quote_char, pattern_start)
    if quote_end == -1:
        return None

    pattern_text = rule_source[pattern_start - 1:quote_end]

    # Find the last unescaped '$' in the pattern text.
    dollar_pos = pattern_text.rfind('$')
    if dollar_pos == -1 or dollar_pos == 0:
        return None
    if pattern_text[dollar_pos - 1] == '\\':
        return None

    base = pattern_start - 1

    if pattern_text[dollar_pos - 1] != ')':
        bare_start = 1
        bare_end = dollar_pos
        if bare_end <= bare_start:
            return None
        group_start = base + bare_start
        group_end = base + bare_end
        return group_start, group_end, False

    close_paren_pos = dollar_pos - 1
    depth = 0
    open_paren_pos = None
    i = close_paren_pos
    while i >= 0:
        ch = pattern_text[i]
        escaped = i > 0 and pattern_text[i - 1] == '\\'
        if ch == ')' and not escaped:
            depth += 1
        elif ch == '(' and not escaped:
            depth -= 1
            if depth == 0:
                open_paren_pos = i
                break
        i -= 1
    if open_paren_pos is None:
        return None
    group_start = base + open_paren_pos + 1
    group_end = base + close_paren_pos
    return group_start, group_end, True