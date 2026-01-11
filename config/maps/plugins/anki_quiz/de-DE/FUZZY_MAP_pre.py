# from .anki_logic import execute
import re # noqa: F401
from pathlib import Path


CONFIG_DIR = Path(__file__).parent
FUZZY_MAP_pre = [


    #Antwort 1Falsch, nochmal!
    # r'^(?:die\s+)?Antwort\s*(?:ist\s+)?(e\w*)$'
    #
    ('Antwort 1',
     r'^(?:die\s+)?Antwort\s*(?:ist\s+)?(e\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    #('Antwort 1', r'^Antwort (e\w*)$',
    #{'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', #'LT_SKIP_RATIO_THRESHOLD']}),

    #antwort ist 1

    ('', r'^Antwort (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),

    # ('', r'^(1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),

    ('', r'^(quitt|quiz|quizz|swiss) (starten)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),
    ('', r'^(start) (quitt|quiz|quizz)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),
    # ('', r'^(1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py']}),
]

#die antwort ist 1
#Funktioniert es immer noch quizze startenQuiz gestartetdie antwort ist 1
