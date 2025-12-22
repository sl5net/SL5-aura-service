# config/maps/plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

"""
Tübingen OpenLab https://ki-maker.space/angebote/open-lab
Öffnungszeiten:
Donnerstag: 11 - 22 Uhr
Freitag: 11 - 18 Uhr
Samstag: 10 - 18 Uhr
KI-Makerspace - Geschwister-Scholl-Platz - 72074 Tübingen - hallo  ki-maker.space - ki-maker.space

https://ki-maker.space/team

https://gitlab.com/kimakerspace

FabLab In Bahnhofsnähe
Wltes-Simon-Straße 4, Tübingen (Nahe Reutlinger Straße)
https://www.openstreetmap.org/node/9879183939

"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.





    ('https://cttue.de',
     # EXAMPLE: chaos
     r'^(chaos|Graues|Karls|raus) (treff|trifft) (tübingen|Typ)\s*\w*$', 60, {'flags': re.IGNORECASE}),

    ('https://cttue.de/doku.php?id=start#was_ansteht',
     # EXAMPLE: chaos
     r'^(chaos|Karls)\s+.*was.*an.*$', 60, {'flags': re.IGNORECASE}),



    # EXAMPLE: chaos x  pad 
    ('https://pad.ccc-mannheim.de/p/1', r'^(chaos)\w*\s+.*pad.*$', 60, {'flags': re.IGNORECASE}),
    # EXAMPLE: chaos x  Tübingen 
    ('https://pad.cttue.de/1', r'^(chaos)\w*\s+.*Tübingen.*$', 60, {'flags': re.IGNORECASE}),



    # EXAMPLE: chaos
    ('https://pad.cttue.de/cttue-meta#', r'^(chaos|Karls)\w*\s+.*Sitzungsprot.*$', 60, {'flags': re.IGNORECASE}),


    # EXAMPLE: chaos
    ('https://cttue.de/doku.php?id=events:past', r'^(chaos|Karls)\s+.* \bVerg.*$', 60, {'flags': re.IGNORECASE}),

    # fettleber typ
    # vettel app tübingen
    # fred leb tübingen
    # EXAMPLE: fred
    ('https://ki-maker.space/', r'^(fred|fett|vettel)(\s*\w*\s*\b)(tübingen|typ)$', 60, {'flags': re.IGNORECASE}),

    # EXAMPLE: fred
    ('https://ki-maker.space/angebote/kurse-und-workshops', r'^(fred|fett|vettel)(\s*\w*\s*\b)(tübingen|typ).*(Kurse|workshops)$', 60, {'flags': re.IGNORECASE}),


    # EXAMPLE: Python Buch
    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Buch)$', 60, {'flags': re.IGNORECASE})
]

