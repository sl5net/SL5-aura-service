# projects/py/STT/config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP.py
import re # noqa: F401


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

