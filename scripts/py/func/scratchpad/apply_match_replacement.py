"""
Applies a single LanguageTool match replacement to a text buffer.
"""


def apply_match_replacement(
    text: str, offset: int, length: int, replacement: str
) -> str:
    """
    Returns a new string with the substring at [offset, offset + length)
    replaced by the given replacement.
    """
    return text[:offset] + replacement + text[offset + length:]
