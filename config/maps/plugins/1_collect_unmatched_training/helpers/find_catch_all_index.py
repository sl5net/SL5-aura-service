# config/maps/plugins/1_collect_unmatched_training/helpers/find_catch_all_index.py
"""Locate the catch-all rule among a FUZZY_MAP_pre list's entries."""


def find_catch_all_index(content: str, entries: list):
    """
    The catch-all rule is identified by the literal string 'collect_unmatched'
    appearing somewhere inside its source span (e.g. in the on_match_exec path).

    Returns the index of the catch-all rule within `entries`, or None if no
    catch-all rule is present.
    """
    marker_pos = content.find('collect_unmatched')
    if marker_pos == -1:
        return None
    for i, (start, end) in enumerate(entries):
        if 'collect_unmatched' in content[start:end]:
            return i
    return None
