"""Parse a FUZZY_MAP_pre.py file's source and locate its top-level rule entries."""

import ast


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
        end = to_offset(el.end_lineno, el.end_col_offset)
        entries.append((start, end))
    return entries
