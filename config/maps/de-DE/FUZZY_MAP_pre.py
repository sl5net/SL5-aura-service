# config/languagetool_server/maps/de-DE/FUZZY_MAP_pr.py
import re

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
    # - means first is most importend, lower rules maybe not get read.

    #switch to english no English please
    # baue bauhaus




    #  Helps the Tool to switch to English
    ('english please', r'^\s*(englisch|english) (fleece|bitte)\s*$', 82, {'flags': re.IGNORECASE}),
    ('english please', r'^\s*(switch to english\s*\w*)\s*$', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (':', r'\bDoppelpunkt\b', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    ('quinquillieren', r'\b(kwink wir nieren|swing wie lire|klingt wie lire|kwink wir dir)\b', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    ('?', r'\s+(fragezeichen|fragen|fragend|frage|fragt)\s*$', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]



