from typing import Optional

KEYSYM_FALLBACK_MAP = {
    "EuroSign": "€",
    "degree": "°",
    "section": "§",
    "acute": "´",
    "grave": "`",
    "ssharp": "ß",
    "adiaeresis": "ä",
    "odiaeresis": "ö",
    "udiaeresis": "ü",
    "Adiaeresis": "Ä",
    "Odiaeresis": "Ö",
    "Udiaeresis": "Ü",
    "ntilde": "ñ",
    "Ntilde": "Ñ",
    "eacute": "é",
    "egrave": "è",
    "aacute": "á",
    "agrave": "à",
    "ccedilla": "ç",
    "Ccedilla": "Ç",
}


def resolve_keysym_char(
    keysym: str,
    char: str,
    keysym_num: Optional[int] = None,
) -> Optional[str]:
    """Pure universal resolver mapping X11 keysyms to Unicode characters."""
    if char and char.isprintable():
        return None

    if keysym_num is not None:
        if 0x01000100 <= keysym_num <= 0x0110FFFF:
            return chr(keysym_num - 0x01000000)
        if 0x00A0 <= keysym_num <= 0x00FF:
            return chr(keysym_num)

    if keysym.startswith("U") and len(keysym) in (5, 6, 7):
        try:
            return chr(int(keysym[1:], 16))
        except ValueError:
            pass

    return KEYSYM_FALLBACK_MAP.get(keysym)

