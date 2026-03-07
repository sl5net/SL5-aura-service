# config/maps/koans_2_peter_deutsch/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

# PETER-AUFGABE fuer Koan: 06_koan_wikipedia_suche
#
# Dieses Plugin sucht in Wikipedia nach dem eingesprochenen Begriff.
# Beispiel: Der Nutzer sagt "wiki was ist ein Haus"
#           -> Plugin sucht nach "was ist ein Haus" in Wikipedia
#
# Die untere Regel aktiviert das Wikipedia-Plugin fuer ALLE Eingaben (^.*$).
# Nach dem Match wird das Plugin ausgefuehrt und die Pipeline stoppt.
#
# AUFGABE: Entferne das '#' vor der Regel um sie zu aktivieren.
# FRAGE: Was passiert wenn du etwas sagst? Schau danach in: log/aura_engine.log

FUZZY_MAP_pre = [
    #('Was ist Tübingen?', fr'^.*$', 90, {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),
]
