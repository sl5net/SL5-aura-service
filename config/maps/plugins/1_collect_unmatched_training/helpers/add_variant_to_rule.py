"""Append a new text variant to an existing rule's trailing regex group."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from find_trailing_group_span import find_trailing_group_span  # noqa: E402


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
    group_start, group_end = group_span  # offsets (within rule_source) of the group's inner content

    group_text = rule_source[group_start:group_end]
    variants = group_text.split("|")
    if text in variants:
        return
    variants.append(text)

    abs_start = start + group_start
    abs_end = start + group_end

    new_content = content[:abs_start] + "|".join(variants) + content[abs_end:]
    fuzzy_map_file.write_text(new_content, encoding="utf-8")
