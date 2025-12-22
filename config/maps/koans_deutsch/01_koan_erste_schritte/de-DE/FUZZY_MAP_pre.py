# config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py
# koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [

    #TODO
    #Entfernen sie das Kommentar, und machen sie eine Spracheingabe.
    #Was passiert und haben Sie eine Idee warum?

    #('hi 01_koan_erste__schritte', r'^.*$', 80, {'flags': re.IGNORECASE}),

    #TestTestaskfjhasldfj asdljfhson
    #tschüss


]


