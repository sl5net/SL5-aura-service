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
#   Du musst kein Regex kennen. Schreib einfach ein einzelnes
#   Wort in diese Liste — ohne Anführungszeichen, ohne Tupel.
#   Aura erkennt es und korrigiert es automatisch zu einer
#   gültigen Regel.
#
# Wichtig: aus Sicherheitsgründen funktioniert dieser Modus nur innerhalb der ersten 1000 Zeichen.
# Deshalb haben wir auch unseren Text unter die Regel geschrieben.
#
# AUFGABE:
#   1. Füge unter dieser Zeile ein einzelnes Wort ein, z.B.:
#        raspberry
#   2. Speicheein Wortatei.
#   3. Sprich ein Wort
#
# NÄCHSTER SCHRITT:
#   Ändere das Wort zu einem Tupel mit eigener Ausgabe:
#      ('Himbeere', '^raspberry$', 0, {'flags': re.IGNORECASE})
