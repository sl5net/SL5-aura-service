# config/maps/koans_2_peter_deutsch/10_koan_mathematiker/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE: Benutze AutoFixModule - schreibe nur einfache Woerter ohne Syntax
#
# Berühmte Mathematiker werden von Spracherkennungssystemen oft falsch geschrieben.
# Beispiele:
#   "gaus"   -> sollte sein: "Gauß"
#   "oiler"  -> sollte sein: "Euler"
#   "leibniz" -> korrekt, aber Großschreibung fehlt oft
#   "riemann" -> korrekt, aber Großschreibung fehlt oft
#
# Aufgabe: Schlage Regeln vor die häufige STT-Fehler bei Mathematiker-Namen korrigieren.
# Es gibt keine auskommentierte Regel – sei kreativ!

FUZZY_MAP_pre = [
]
