import re

def is_window_title_skippable(active_title, only_in_list=None, exclude_list=None):
    """
    Returns True if the current window title suggests the rule should be skipped.
    Follows Fail-Safe logic: if a window is required but none is found, it skips.
    """
    if not only_in_list and not exclude_list:
        return False

    title_str = str(active_title) if active_title else ""

    # 1. Check "Only In" constraint
    if only_in_list:
        # If we need a specific window but have no title -> Skip
        if not title_str:
            return True

        found_match = False
        for pattern in only_in_list:
            if re.search(pattern, title_str, re.IGNORECASE):
                found_match = True
                break
        if not found_match:
            return True

    # 2. Check "Exclude" constraint
    if exclude_list and title_str:
        for pattern in exclude_list:
            if re.search(pattern, title_str, re.IGNORECASE):
                return True

    return False
