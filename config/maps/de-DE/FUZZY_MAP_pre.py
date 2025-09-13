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

    ('baue Haus', r'^\s*(baue auf|baue\s*\w*haus|Build House|Baue Haus)\s*$', 15, re.IGNORECASE),

    ('alt+i', r'^\s*(alt\s*e|alt\s*i|ald\s*i|select in).*\s*$', 20, re.IGNORECASE),

    ('alt+w', r'^\s*(select\s*wo|select\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*\s$', 20, re.IGNORECASE),



    #  Helps the Tool to switch to English
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, re.IGNORECASE),
    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, re.IGNORECASE),


    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, re.IGNORECASE),

    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, re.IGNORECASE),
    ('Wannweil', r'^\s*(Wannweil|Annweiler|wann\s*weil|Wann\s*wann\s*weil|Wann\s*war\s*Herr|Wann\s*war\s*er|An\s*weil|Wann\s*weine\w*|Wann\s*wein)\s*$', 70, re.IGNORECASE),

    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, re.IGNORECASE),
    ('StopButton', r'\bstob\s*Button\b', 82, re.IGNORECASE),
    ('lowerCase', r'\blobt\s*Case\b', 82, re.IGNORECASE),

    # 3? Und jetzt noch mehr? Noch mehr?  Ich glaube, er lädt die Karte nicht nutzen?


    ('???', r'\s+(fragezeichen|fragen|fragend|frage|fragt)\s*$', 80, re.IGNORECASE),


    ('AutoKey', r'\bAuto k\b', 82, re.IGNORECASE),

    ('Build Prozess', r'\bbild prozess\b', 82, re.IGNORECASE),

    ('opensource', r'\bopensource\b', 75, re.IGNORECASE),

    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura)\b', 82, re.IGNORECASE),
    ('Sigune Lauffer', r'\b(Figur|Sekunde) (Läufer|laufer|Laura)\b', 82, re.IGNORECASE),

    ('Lauffer', r'\b(Läufer|laufer)\b', 82, re.IGNORECASE), # Exact match, but ignore case



]



