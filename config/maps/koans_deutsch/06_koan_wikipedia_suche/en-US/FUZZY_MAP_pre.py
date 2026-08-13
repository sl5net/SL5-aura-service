# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# configmaps/koans deutsch/06 koan_wikipedia search/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path

# ============================================================
# Koan 06: Wikipedia search by voice

# ============================================================
#
# LEARNING GOAL:

# on_match_exec can also query online APIs.

# Here: Wikipedia search by voice command.

#
# TASK:

# 1. Activate the rule below.

# 2. Say: “What is Tübingen?”

#
# MISTAKE? Check the log:

# grep "wikipedia" log/aura_engine.log | tail -10

#
# OFFLINE VERSION:

# See config/maps/plugins/standard_actions/wikipedia_local/

#
# NEXT STEP: Koan 07

# ============================================================


CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.



    # TODO: Activate bottom line by removing the comment symbol

    # ('What is Tübingen?', fr'^.*$', 90, {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


]



tips = r"""

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

# offline wikipedia ########################################################


Geht es auch komplett offline? Ja. Z.B.

mit Hilfe von

https://library.kiwix.org/#lang=deu&q=wikipedia



Nötige Speicherplatz zwischen 50 Gigabyte und 20 MB (Auswahl)

Gute Wahl: 3,54 GB ohne Bilder:
https://browse.library.kiwix.org/viewer#wikipedia_de_all_mini_2025-09
https://download.kiwix.org/zim/wikipedia/wikipedia_de_all_mini.zim

Eine der möglichen Variante der Nutzung ist über Docker:

sudo systemctl enable --now docker.socket

Jetzt, da der Inhalt als Webseite verfügbar ist, kann Ihr Python-Skript ihn wie jede andere Webseite verarbeiten.

Ein Beispiel-Py-Script dafür findet sich hier: config/maps/plugins/standard_actions/de-DE/wikipedia_local.py


"""




