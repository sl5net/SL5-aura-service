# config/maps/koans_deutsch/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py
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

log/aura_engine.log

Den Fehler können wir unter Windows folgendermasen reparieen:

.\.venv\Scripts\activate.bat


.\.venv\Scripts\python.exe  -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install wikipedia

Warum bekommen wir immernoch einen Fehler das wikipediaapi nicht funktioniert?

Wir veruchen

.\.venv\Scripts\python.exe -m pip install wikipediaapi

aber bekommen:

ERROR: Could not find a version that satisfies the requirement wikipediaapi

Dieses Plugin beispiel wurde unter Linux erstellt, aber wird jetzt unter Windows ausgeführt.

Versuchen Sie

.\.venv\Scripts\python.exe -m pip install wikipedia-api

funktioniert es jetzt?

Warum?

###### offline wikipedia ########################################################

Geht es auch komplett offline? Ja. Z.B.

mit Hilfe von

https://library.kiwix.org/#lang=deu&q=wikipedia



Nötige Speicherplatz zwischen 50 Gigabyte und 20 MB (Auswahl)

Gute Wahl: 3,54 GB ohne Bilder:
https://browse.library.kiwix.org/viewer#wikipedia_de_all_mini_2025-09
https://download.kiwix.org/zim/wikipedia/wikipedia_de_all_mini_2025-09.zim

Eine der möglichen Variante der Nutzung ist über Docker:

sudo systemctl start docker

Jetzt, da der Inhalt als Webseite verfügbar ist, kann Ihr Python-Skript ihn wie jede andere Webseite verarbeiten.

Ein Beispiel-Py-Script dafür findet sich hier: config/maps/plugins/standard_actions/de-DE/wikipedia_local.py


"""




