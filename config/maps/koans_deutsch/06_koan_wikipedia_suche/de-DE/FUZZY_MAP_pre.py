# /home/seeh/projects/py/STT/config/maps/plugins/bible_search/FUZZY_MAP_pr.py
# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite

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


    #TODO: Untere Zeile aktivieren, duch entfernen des Kommentar Symbols
    #('Was ist Tübingen?', fr'^.*$', 90, {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

]



tips = fr"""

TODO: Was passiert jetzt?
TODO: Mehr Informationen, Fehlermeldungen usw, erhalten wir meisens, wenn wir die Log lesen:

log/dictation_service.log

Den Fehler können wir unter Windows folgendermasen reparieen:

.\.venv\Scripts\activate.bat


.\.venv\Scripts\python.exe  -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install wikipedia

Warum bekommen wir immernoch einen Fehler das wikipediaapi nicht funktioniert?

Wir veruchen

.\.venv\Scripts\python.exe -m pip install wikipediaapi

aber bekommen:

ERROR: Could not find a version that satisfies the requirement wikipediaapi (from versions: none)

Dieses Plugin beispiel wurde unter Linux erstellt, aber wird jetzt unter Windows ausgeführt.

Versuchen Sie

.\.venv\Scripts\python.exe -m pip install wikipedia-api

funktioniert es jetzt?

Warum?



"""

