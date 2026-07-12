import re
def get_leading_whitespace_of_line(line: str) -> str:
    m = re.match(r"\s*", line)
    return m.group() if m else ""

# If you want to determine the indentation from the content (e.g. last list entry line)
def get_leading_whitespace_before_pos(content: str, pos: int, fallback: str = "    ") -> str:
    """
    get last not empy line for pos get Whitespaces
    or get fallback
    """
    pos = max(0, min(len(content), pos))
    line_start = content.rfind("\n", 0, pos)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    # Go backwards until we find a non-empty line or are at the beginning
    search_pos = line_start
    while True:
        next_nl = content.find("\n", search_pos)
        if next_nl == -1 or next_nl >= pos:
            next_nl = pos
        line = content[search_pos:next_nl]
        if line.strip() != "":
            return get_leading_whitespace_of_line(line)

        prev_nl = content.rfind("\n", 0, search_pos - 1)
        if prev_nl == -1:

            if content[:search_pos].strip() == "":
                return fallback
            search_pos = 0
        else:
            search_pos = prev_nl + 1
        if search_pos == 0:
            first_line = content[:pos].splitlines()[0] if content[:pos].splitlines() else ""
            return get_leading_whitespace_of_line(first_line) if first_line else fallback
