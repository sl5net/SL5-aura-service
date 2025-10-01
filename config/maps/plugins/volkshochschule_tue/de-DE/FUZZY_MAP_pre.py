# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use re.IGNORECASE for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.
#  Kurztitel KI Helfer EDV und Beruf
#  Katharinenstraße Besuch Wie Launch Übungsleiterpauschale

# Kursleiter schule

# Kursleiterschulung bei uns dazukommen oder ich zeig Dir das Brett mal und Du kannst Dich damit warmspielen.
#  Kursleiter Schulungen Kursleiter Schulung

    ('Timo', r'\b(ti\w+r|T\w+i\w+o)\b', 70, re.IGNORECASE),


    ('Timo Stösser', r'^(thieme|thema|ti\w+r|T\w+i\w+o)\s+(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|stöße|stöpsel|Störche)$', 70, re.IGNORECASE),

    ('Fachbereichsleitung', r'^(fachbereichsleiter)$', 60, re.IGNORECASE),

    ('Python-Buch', r'^(\w+t\wn Buch)$', 60, re.IGNORECASE),

    ('Python-Buch', r'^(Python Buch)$', 60, re.IGNORECASE),
    ('Python-Buch', r'^(B\w+i\wt\w+ Buch)$', 60, re.IGNORECASE),

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Buch)$', 60, re.IGNORECASE),

    ('Kursleiterschulung', r'^(Kursleiter\s*schu\w*)$', 60, re.IGNORECASE)


]

# Python-Buch  Breitem Buch Python-Buch  Python-Buch bei im Buch
# Brighton Buch  Python Buch Peitsche Buch Breite Buch
# Zweites Buch Bei Totenbuch Python Buch Breiter Buch Weite Buch Python-Buch
#  Heitert Buch
#  Python-Buch
