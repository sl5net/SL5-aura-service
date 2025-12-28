# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP_pre.py
# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

"""
Important: Please apply the regular expressions in the correct order.

You must use the composite (more general) regular expression first, and then apply the specialized one.

The reason is that if the shorter, specialized regex runs first, it might match a part of the string that is essential for the larger, composite regex. This would make it impossible for the composite regex to find its match afterwards.
"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match (^ ... $)!
    # - first is read first imported, lower rules maybe not get read.
    # EXAMPLE: titextr
    ('Timo Stösser', r'^(ti\w+r|T\w+i\w+o)\s+(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Stoffe|Schlösser|stöße|stöpsel|Störche)$', 7, {'flags': re.IGNORECASE}),

    # EXAMPLE: titextr
    ('Timo', r'\b(ti\w+r|T\w+i\w+o)\b', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: stäfa
    ('Stösser', r'^(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Schlösser|stöße|stöpsel|Störche)$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: fachbereichsleiter
    ('Fachbereichsleitung', r'^(fachbereichsleiter)$', 60, {'flags': re.IGNORECASE}),

    # EXAMPLE: texttxn Buch
    ('Python-Buch', r'^(\w+t\wn Buch)$', 60, {'flags': re.IGNORECASE}),

    # EXAMPLE: Python Buch
    ('Python-Buch', r'^(Python Buch)$', 60, {'flags': re.IGNORECASE}),
    # EXAMPLE: Btextixttext Buch
    ('Python-Buch', r'^(B\w+i\wt\w+ Buch)$', 60, {'flags': re.IGNORECASE}),

    # EXAMPLE: Python-Buch
    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Buch)$', 60, {'flags': re.IGNORECASE}),

    # ('Kursleiterschulung', r'^(Kursleiter\s*schu\w*| Dozenten Schulung  Dozenten Fortbildung)$', 60, {'flags': re.IGNORECASE})

    # EXAMPLE: Kursleiter
    ('Kursleiterschulung', r'^(Kursleiter|Dozenten)[\w\s]*(\s*schu\w*|Fortbildung)$', 60, {'flags': re.IGNORECASE})

]

# Timo Stösser


# Kursleiterschulung Python-BuchFachbereichsleitung
# Python-Buch  Breitem Buch Python-Buch  Python-Buch bei im Buch
# Brighton Buch  Python Buch Peitsche Buch Breite BuchTimoTchibo stürzen
# Zweites Buch Bei Totenbuch Python Buch Breiter Buch Weite Buch Python-Buch
#  Heitert Buch
#  Python-Buch
