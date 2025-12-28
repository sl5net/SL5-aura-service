# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP.py
# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - means first is most importend, lower rules maybe not get read.


    # EXAMPLE: Timo Stösser
    ('Timo Stösser', r'\b(thiem\w|timo|thema|ti\w+r)\s+(stäfa|steffen|Stefan|stripper|stefan|stürze\w*|stütze\w*|Sturz|stösse|Schlösser|stöße|stößt|Stöße|stöpsel|stärker|Störche)\b', 70, {'flags': re.IGNORECASE}) ,

    # EXAMPLE: Fach Bereichsleitung
    ('Fachbereichsleitung', r'\bFach\w*\s+Bereichsleitung\b', 70, {'flags': re.IGNORECASE}) ,

    # EXAMPLE: PBW textix tx ex Buch
    ('Python-Buch', r'\b([PBW]\w+i\w*t\w*e\w* Buch)\b', 60, {'flags': re.IGNORECASE}),


    # EXAMPLE: Kursleiter Schulung
    ('Kursleiterschulung', r'\b(Kursleiter\s*schu\w*)\b', 60, {'flags': re.IGNORECASE})



]

