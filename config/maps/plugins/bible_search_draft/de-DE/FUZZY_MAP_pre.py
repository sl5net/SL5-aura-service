# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pr.py
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

    # To-do aufgaben:
    # Es müssen die Buch Namen eingesprochen werden so lange bis sie korrekt verstanden werden (Powered by SL5.de/Aura)
    # Jetzt muss entschieden werden, ob ein alle Bibel lebt oder du will (Powered by SL5.de/Aura)
    # Und welche die beste ist (Powered by SL5.de/Aura)

    # Hier Sprachergebnisse:

    #Das Buch 'johannes' existiert nicht in der Übersetzung 'GerElb1905'.
    #Das Buch 'peter' existiert nicht in der Übersetzung 'GerElb1905'.

    #Suche in esther Kapitel 1 Vers ein 1
    #esther 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Und es geschah in den Tagen des Ahasveros (das ist der Ahasveros, der von Indien bis Äthiopien über hundertsiebenundzwanzig Landschaften regierte),

    ('bible suche', r'^suche \w+ (?P<book>.*) kapitel (?P<chapter>\d+) [vf]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),







]

