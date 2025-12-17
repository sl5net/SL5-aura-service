# config/maps/plugins/bible_search/FUZZY_MAP_pr.py
# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite

import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent




    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.
FUZZY_MAP_pre = [
('find all zips', fr'''^(
        (Alle\s)?(ZIP|Sip|Chip|Tipp|Zipp|Seb)[-\s]?(Dateien|Ordner|Daten|s)?\s(suchen|hinzu|scannen|aktualisieren|einlesen|finden|checken|neu laden)
        |
        (Scanne|Suche|Aktualisiere)\s(alle\s)?(Zips|Zip-Dateien|Chips|Tipps)
        |
        (Zip|Zips)\s(Registry|Datenbank)\s(aktualisieren|erneuern)
        |
        jagen aktualisieren
        )$''', 90, {
            'flags': re.IGNORECASE | re.VERBOSE,
            'on_match_exec': [CONFIG_DIR / 'zip.py']
        }
        ),
]

#Zip-Datei hinzuScan complete. Found 11 targets. Zips updated.
#

readme = '''
Was deckt das jetzt alles ab?
Dank der Kombinationen funktionieren nun hunderte Varianten. Hier ein paar Beispiele, die jetzt erkannt werden:

Der Standard:

"Zip Dateien suchen"
"Zips scannen"
"Zip Ordner aktualisieren"
"Alle Zips neu laden"

Die "Kreativen" (Verhörer):

"Chips suchen"
"Tipps scannen"
"Sip Dateien finden"
"Seb Ordner checken"
"Zipps einlesen"

Die Befehlsform:

"Scanne Zips"
"Aktualisiere alle Chips"

Technische Begriffe:

"Zip Registry aktualisieren"
"Zip Datenbank erneuern"

Hinweis: Ich habe re.VERBOSE (in den Flags) hinzugefügt, damit wir den Regex über mehrere Zeilen schreiben können (bessere Lesbarkeit). Falls deine Engine re.VERBOSE nicht unterstützt oder mag, sag Bescheid, dann schrumpfe ich es wieder in eine lange Zeile.

    '''















