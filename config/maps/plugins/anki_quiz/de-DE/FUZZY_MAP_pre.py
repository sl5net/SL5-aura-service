# from .anki_logic import execute
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
FUZZY_MAP_pre = [
    ('Antwort 1',
     r'^(?:die\s+)?Antwort\s*(?:ist\s+)?(e\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    ('Antwort 2',
     r'^(?:die\s+)?Antwort\s*(?:ist\s+)?(z\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    ('Antwort 3',
     r'^(?:die\s+)?Antwort\s*(?:ist\s+)?([df]\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    ('', r'^Antwort (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),

    ('', r'^(quitt|quiz|quizz|swiss) (starten)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),
    ('', r'^(start) (quitt|quiz|quizz)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),
]
# Richtig!Quiz gestartetRichtig!Falsch, nochmal!Falsch, nochmal!Falsch, nochmal!Richtig!
# Richtig!die antwort ist zweidie antwort ist eins Richtig!Richtig!Richtig!Richtig!