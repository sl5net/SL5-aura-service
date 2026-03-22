# config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch', 1, {'flags': re.IGNORECASE}),
]

# ============================================================
# Koan 07: Auto-Fix — Aura repariert fehlerhafte Map-Dateien
# ============================================================
#
# WAS ES TUT:
#   Enthält eine Map-Datei ein "bare word" (kein Tupel-Format),
#   korrigiert Auras Auto-Fix es beim Laden automatisch.
#
# WICHTIG:
#   Auto-Fix funktioniert nur bei Dateien kleiner als ~1KB.
#   Das ist Absicht — unkontrolliertes Umschreiben großer
#   Map-Dateien wird so verhindert.
#
# AUFGABE:
#   1. Füge ein einzelnes Wort in FUZZY_MAP_pre ein (kein Tupel):
#        handuch
#   2. Speichern. Aura korrigiert es automatisch zu einer gültigen Regel.
#   3. Prüfe das Log auf "Auto-Fix".
#
# NÄCHSTER SCHRITT: Koan 08
# ============================================================

import re # noqa: F401
# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE fuer Koan: 07_koan_auto_fix_map_errors
# Keine auskommentierten Regeln gefunden.
# -> Erstelle eine sinnvolle neue Regel fuer diesen Koan.
FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'flags': re.IGNORECASE}),
]
