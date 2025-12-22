# config/maps/plugins/wannweil/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

# Bratwurst wäre intern

    # EXAMPLE: Kirchen s teilen
    ('Kirchentellinsfurt', r'\b(Kirchen\s*teilen|Kirchentellinsfurt|klirrend hält)\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: Rathaus
    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(Rathaus|Kontakt)\b\s*\b(Kirchen\s*teilen|Kirchentellinsfurt)\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: rathaus klirrend hält
    ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(rathaus klirrend hält)\b', 82, {'flags': re.IGNORECASE}),


# zieglersche https://www.zieglersche.de/altenhilfe.html pflegheim

#Rathaus klirrend hält
#Hartholz klirren tönt

    # EXAMPLE: wen s Welpe
    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: wen s Welpe
    ('Wannweil', r'\b(wen\s*Welpe)\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: s Wannweil
    ('Wannweil', r'^\s*(Wannweil|Annweiler|wann\s*weil|Wann\s*wann\s*weil|Wann\s*war\s*Herr|Wann\s*war\s*er|An\s*weil|Wann\s*weine\w*|Wann\s*wein|Van\s*weil|wann was)\s*$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: Sebastian Läufer
    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura|lauf|lauf war)\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: Figur
    ('Sigune Lauffer', r'\b(Figur|Sekunde|zugrunde|sigourney|sheego|Sie gute|gun|Ski gute|c gute|Schick ohne|sheikh ohne|gleich ohne|shi gunilla|spione)'
                       # EXAMPLE: Läufer
                       r' (Läufer|laufer|Lauffer|lauf|laufe|laufen|Laura|lauf war|darauf warten|in haufen|aufhören|nase)\b', 82, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: diesesRegexWirdNiemalsMatchen123ABC
    ('TestFuzzyNiemalsMatchen', r'\b(diesesRegexWirdNiemalsMatchen123ABC)\b', 75, {'flags': re.IGNORECASE}),

    # ('TestFuzzyImmer', r'\b(diesesRegexWirdImmerMatchen)\b', 1, {'flags': re.IGNORECASE}),


    # EXAMPLE: Paradigma Minds
    ('pragmatic minds GmbH 2019', r'\b(Paradigma Minds)\b', 75, {'flags': re.IGNORECASE}),



]

