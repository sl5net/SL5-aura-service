# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
"""
Handles unmatched user input by updating the FUZZY_MAP_pre.py file that
contains the catch-all rule which triggered this script.

Behaviour:
- If no catch-all rule (identified by the string 'collect_unmatched' inside
  its on_match_exec path) is found -> do nothing.
- If a catch-all rule is found and there is a rule before it -> add the
  unmatched text as a new alternative to that previous rule's regex group.
- If a catch-all rule is found and there is no rule before it -> insert a
  template rule ('nix', r'^(nix)$') right before the catch-all rule.
"""

import ast
import re
import sys
from pathlib import Path


def execute(match_data: dict):
    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']
    print(f'file_rule_path: {file_rule_path}')
    if not text:
        print(f'ERROR: text empty {text}')
        return None
    _collect_unmatched(file_rule_path, text)
    sys.exit(1)


def _collect_unmatched(file_rule_path: str, text: str):
    fuzzy_map_file = Path(file_rule_path)
    if not fuzzy_map_file.exists():
        return

    content = fuzzy_map_file.read_text(encoding="utf-8")

    entries = _get_fuzzy_map_entries(content)
    if entries is None or not entries:
        return

    catch_all_index = _find_catch_all_index(content, entries)
    if catch_all_index is None:
        # No catch-all rule present -> do nothing
        return

    if catch_all_index > 0:
        # There is a rule before the catch-all -> modify it
        prev_start, prev_end = entries[catch_all_index - 1]
        _add_variant_to_rule(fuzzy_map_file, content, prev_start, prev_end, text)
    else:
        # No rule before the catch-all -> insert a template rule
        catch_all_start, _ = entries[catch_all_index]
        _insert_template_rule(fuzzy_map_file, content, catch_all_start)


def _get_fuzzy_map_entries(content: str):
    """
    Parse the file and return a list of (start_offset, end_offset) tuples,
    one per top-level element of the FUZZY_MAP_pre list, in source order.
    Using ast instead of line-based regex so multi-line rules (e.g. rules
    with nested dicts spanning several lines) are handled correctly.
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
        end = to_offset(el.end_lineno, el.end_col_offset)
        entries.append((start, end))
    return entries


def _find_catch_all_index(content: str, entries):
    """
    The catch-all rule is identified by the literal string 'collect_unmatched'
    appearing somewhere inside its source span (e.g. in the on_match_exec path).
    """
    marker_pos = content.find('collect_unmatched')
    if marker_pos == -1:
        return None
    for i, (start, end) in enumerate(entries):
        if start <= marker_pos < end:
            return i
    return None


def _add_variant_to_rule(fuzzy_map_file: Path, content: str, start: int, end: int, text: str):
    rule_source = content[start:end]

    group_span = _find_trailing_group_span(rule_source)
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


def _find_trailing_group_span(rule_source: str):
    """
    Locate the last regex group, i.e. "(...)", that sits directly before the
    final '$' anchor inside the rule's pattern string literal. This is the
    group new variants get appended to.

    Works regardless of how complex the rest of the pattern is (optional
    prefix groups, f-string placeholders like {baum}, nested groups, ...),
    by scanning backwards from the closing ')' and counting paren balance
    instead of assuming the whole pattern is just "^(...)$ ".

    Returns (start, end) offsets (within rule_source) of the group's inner
    content (i.e. right after '(' and right before the matching ')'), or
    None if no such group could be found.
    """
    # Find the start of the pattern string literal: an optional string
    # prefix (r/f/fr/rf), a quote char, then the '^' anchor.
    literal_re = re.compile(r"[a-zA-Z]{0,2}(['\"])\^")
    lit_match = literal_re.search(rule_source)
    if not lit_match:
        return None
    quote_char = lit_match.group(1)
    pattern_start = lit_match.end()  # position right after '^'

    # Find the matching closing quote (naive: patterns here don't contain
    # the delimiting quote character itself).
    quote_end = rule_source.find(quote_char, pattern_start)
    if quote_end == -1:
        return None

    pattern_text = rule_source[pattern_start - 1:quote_end]  # includes leading '^'

    # Find the last unescaped '$' in the pattern text.
    dollar_pos = pattern_text.rfind('$')
    if dollar_pos == -1 or dollar_pos == 0:
        return None
    if pattern_text[dollar_pos - 1] == '\\':
        return None  # escaped '$', not the end anchor

    if pattern_text[dollar_pos - 1] != ')':
        return None  # pattern doesn't end in a group right before '$'

    close_paren_pos = dollar_pos - 1

    # Walk backwards from close_paren_pos to find the matching '(',
    # respecting nesting and skipping escaped parens (\( \)).
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

    # Convert positions (relative to pattern_text, which starts at
    # pattern_start - 1 within rule_source) back to rule_source offsets.
    base = pattern_start - 1
    group_start = base + open_paren_pos + 1
    group_end = base + close_paren_pos
    return group_start, group_end


def _insert_template_rule(fuzzy_map_file: Path, content: str, catch_all_start: int):
    line_start = content.rfind('\n', 0, catch_all_start) + 1
    indent_match = re.match(r'[ \t]*', content[line_start:catch_all_start])
    indent = indent_match.group() if indent_match else ''

    template_line = f"{indent}('nix', r'^(nix)$'),\n"
    new_content = content[:line_start] + template_line + content[line_start:]
    fuzzy_map_file.write_text(new_content, encoding="utf-8")
