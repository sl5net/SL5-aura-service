# config/languagetool_server/maps/plugins/CCC_tue/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    ('https://cttue.de', r'^(chaos|Karls) treff tübingen\s*\w*$', 60, {'flags': re.IGNORECASE}),

    # karl stress was steht an

    ('https://cttue.de/doku.php?id=start#was_ansteht', r'^(chaos|Karls)\s+.*was.*an.*$', 60, {'flags': re.IGNORECASE}),

    ('https://pad.cttue.de/cttue-meta#', r'^(chaos|Karls)\w*\s+.*Sitzungsprot.*$', 60, {'flags': re.IGNORECASE}),

    # ('https://pad.cttue.de/cttue-meta#', r'^(chaos|Karls)\s+.*Sitzungsprot.*$', 60, {'flags': re.IGNORECASE}),


    ('https://cttue.de/doku.php?id=events:past', r'^(chaos|Karls)\s+.* \bVerg.*$', 60, {'flags': re.IGNORECASE}),


    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Buch)$', 60, {'flags': re.IGNORECASE})
]

