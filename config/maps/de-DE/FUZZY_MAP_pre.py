# config/languagetool_server/maps/de-DE/FUZZY_MAP_pr.py
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
    # - means first is most importend, lower rules maybe not get read.

    #switch to english no English please
    # baue bauhaus




    #  Helps the Tool to switch to English
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, re.IGNORECASE),
    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, re.IGNORECASE),


    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),


    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, re.IGNORECASE),
    ('StopButton', r'\bstob\s*Button\b', 82, re.IGNORECASE),
    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    # 3? Und jetzt noch mehr? Noch mehr?  Ich glaube, er lädt die Karte nicht nutzen?


    ('???', r'\s+(fragezeichen|fragen|fragend|frage|fragt)\s*$', 80, re.IGNORECASE),


    ('AutoKey', r'\bAuto k\b', 82, re.IGNORECASE),

    ('Build Prozess', r'\bbild prozess\b', 82, re.IGNORECASE),

    ('opensource', r'\bopensource\b', 75, re.IGNORECASE),


]



