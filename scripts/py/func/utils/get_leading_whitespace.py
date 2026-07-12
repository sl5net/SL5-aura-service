import re

def get_leading_whitespace_of_line(line: str) -> str:
    """
    Gibt die führenden Whitespaces (Tabs oder Spaces) der übergebenen Zeile zurück.
    Leerstring, wenn keine führenden Whitespaces vorhanden sind.
    """
    m = re.match(r"\s*", line)
    return m.group() if m else ""

# Wenn du die Einrückung aus dem Inhalt ermitteln willst (z.B. letzte Listeneintrag-Zeile)
def get_leading_whitespace_before_pos(content: str, pos: int, fallback: str = "    ") -> str:
    """
    Suche die letzte nicht-leere Zeile vor pos und gib deren führende Whitespaces zurück.
    Wenn nichts passendes gefunden wird, wird fallback zurückgegeben.
    """
    # Begrenze pos sicher innerhalb content
    pos = max(0, min(len(content), pos))
    # Finde Zeilenanfang der Zeile, die pos enthält
    line_start = content.rfind("\n", 0, pos)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    # Gehe rückwärts, bis wir eine nicht-leere Zeile finden oder am Anfang sind
    search_pos = line_start
    while True:
        # Finde Zeilenende
        next_nl = content.find("\n", search_pos)
        if next_nl == -1 or next_nl >= pos:
            next_nl = pos
        line = content[search_pos:next_nl]
        if line.strip() != "":
            return get_leading_whitespace_of_line(line)
        # gehe zur vorherigen Zeile
        prev_nl = content.rfind("\n", 0, search_pos - 1)
        if prev_nl == -1:
            # prüfe von Anfang bis search_pos
            if content[:search_pos].strip() == "":
                return fallback
            search_pos = 0
        else:
            search_pos = prev_nl + 1
        if search_pos == 0:
            # letzte Chance: erste Zeile
            first_line = content[:pos].splitlines()[0] if content[:pos].splitlines() else ""
            return get_leading_whitespace_of_line(first_line) if first_line else fallback
