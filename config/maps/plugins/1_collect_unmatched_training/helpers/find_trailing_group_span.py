"""Locate the regex group that sits directly before the final '$' anchor
of a rule's pattern string literal."""

import re


def find_trailing_group_span(rule_source: str):
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
