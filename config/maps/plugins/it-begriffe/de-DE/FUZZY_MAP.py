# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP.py
# https://regex101.com/
import re # noqa: F401

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
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.

    ('Python', r'^(\b)(Brighton|breit schon|Fallschirm|peitschen|Zeiten|Titan|Scheitern)(\b)$', 75, {'flags': re.IGNORECASE}),
#
#Peitschen wird Timo Getreide Virtual environment zu nennenScheitern wird Timo in einem Virtual environment verwendet
#Zeiten wird hier in der Ritual Environment verwenden
#Ritual et DeibelVirtual environmentTitan notiert deine Wortwahl in Reiben verwendenZeiten wird hier in einem virtuell in Reiben verwenden
#Breit wird Timo in einem virtuell ein Weiber verwirrtTestZeiten wird hier in deinem virtuell Hinweis mit verwenden
#Peitschen wird Timo in einem virtuell reiben verwendenPeitschen wird hierTitan wird hier über den Virtual environment verwendet

    ('Virtual environment', r'\b(ritual|Virtuell|virtual|witwe\w*|witwer|wird schon|wird schwer|wirtschaft|wildschwein)\w* (in |wei |im |ein )?(Environment|Weibe|white|weima|metall|wei|warm|wei mit|wirbeln|et Deibel|in Reiben|reiben|Hinweis)\w*\b', 75, {'flags': re.IGNORECASE}),


]
