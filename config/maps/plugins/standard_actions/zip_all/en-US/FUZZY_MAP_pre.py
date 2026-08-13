# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/standard_actions/zip_all/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', rregex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'flags': ...} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


CONFIG_DIR = Path(__file__).parent

    # A type file of courseinternalsSearch lifts the homeinternalsChips Update databaseinternalsScript Renovate databaseinternalsUpdate Chip twitter shareinternalsAll folders SkillinternalsAll folders updatedinternalsA layout by meinternalsRead all foldersKeyboard MorphinReadinternalsZwick data ininternalsJeep data ininternals


    # Find a zip filesinternalsUpdate all filesReportUpdate a zip filesinternalsFind your zip filesTravel report


    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.

FUZZY_MAP_pre = [
    ('find all zips', r'''^(
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

# Add zip fileScan complete. Found 11 targets. Zips updated.

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
