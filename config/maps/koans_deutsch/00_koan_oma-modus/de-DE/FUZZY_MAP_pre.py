# config/maps/koans_deutsch/00_koan_oma-modus/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', '^oma$'),
]

# Mehr dazu: docs/FuzzyMapRuleGuide.mdFUZZY_MAP_pre = [


# ============================================================
# Koan 00: Oma-Modus — Regeln ohne Syntax
# ============================================================

#
# IDEE:
#   Du musst keine Regeln (Regex) kennen. Schreib einfach ein einzelnes
#   Wort — ohne Anführungszeichen.

#   Aura erkennt es und korrigiert es automatisch zu einer
#   gültigen Regel.
#
# AUFGABE:
#   1. Füge unter dieser Zeile ein einzelnes Wort ein, z.B.:
#        Blume
#   2. Speiche als Wortatei.
#   3. Sprich ein Wort
#
# NÄCHSTER SCHRITT:
#   Ändere das Wort zu einem Tupel mit eigener Ausgabe:
#      ('Himbeere', '^Blume$', 0, {'flags': re.IGNORECASE})
