# projects/py/STT/config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP.py
import re # noqa: F401
# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.

# PETER-AUFGABE fuer Koan: 07_koan_auto_fix_map_errors
# Keine auskommentierten Regeln gefunden.
# -> Erstelle eine sinnvolle neue Regel fuer diesen Koan.
FUZZY_MAP = [
    ('tübingen', 'tübingen'),
    ("hallo", "welt"),
]

"""
#
Profozieren Sie einen Fehler.

Schreiben Sie anstelle
    ('tübingen', 'tübingen'),
nur tübingen

Was passiert=

Lernziel:

Automatische Fehlerbehebung in Map-Plugins (z.B. NameError für nicht definierte Variablen)
Umwandlung von "bare words" in gültige Tuples
Header-Cleanup (Dubletten entfernen, Pfade aktualisieren)

"""
