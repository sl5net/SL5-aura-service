# config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py
# projects/py/STT/config/maps/koans_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'flags': re.IGNORECASE}),
]


"""
Bitte schreiben Sie ein Wort in die erste Zeile vor den Anführungstrichen.

Lernziel:

Automatische Fehlerbehebung in Map-Plugins (z.B. NameError für nicht definierte Variablen)
Umwandlung von "bare words" in gültige Tuples
Header-Cleanup (Dubletten entfernen, Pfade aktualisieren)

"""
