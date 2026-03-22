import re  # noqa: F401

# ============================================================
# Koan 02: Deine erste Regex-Regel – An oder Aus?
# ============================================================
#
# LERNZIEL:
#   Regex-Regeln können mehrere gesprochene Wörter auf einen
#   Befehl mappen. Hier: Buchstabengruppen steuern "an"/"aus".
#
# AUFGABE:
#   1. Entferne das '#' vor EINER der beiden Regeln unten.
#   2. Speichere – Aura lädt beim nächsten Tastendruck neu.
#   3. Sprich ein Wort das mit a-m beginnt (z.B. "hallo")
#      oder eines das mit n-z beginnt (z.B. "wasser").
#
# ERWARTETES ERGEBNIS:
#   "hallo" → "an"
#   "wasser" → "aus"
#
# FRAGE ZUM NACHDENKEN:
#   Was passiert wenn du beide Regeln gleichzeitig aktivierst?
#   Welche gewinnt – und warum?
#   Tipp: Regeln werden von oben nach unten verarbeitet.
#
# NÄCHSTER SCHRITT: Koan 03
# ============================================================

FUZZY_MAP_pre = [
    # ('an',  r'^[a-m]+.*$'),
    # ('aus', r'^[n-z]+.*$'),
]
