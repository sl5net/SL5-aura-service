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

# config/maps/plugins/anki_quiz/de-DE/FUZZY_MAP_pre.py

# from .anki_logic import execute

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path
CONFIG_DIR = Path(__file__).parent

readme = r"""
 Antwort 2
 Erklärung für Lernende:
  'Antwort 2',                                       # Index 0 (Ergebnis)
  r'^(?:the\s+)?Answer(e)\s*(?:is\s+)?(z\w*)$',    # Index 1 (Regex Pattern)
  100,                                               # Index 2 (Threshold/Score)
  {'command_flags': re.IGNORECASE, ...}                      # Index 3 (Options Dict)
"""


FUZZY_MAP_pre = [
    # EXAMPLE: the answer e is e

    ('Antwort 1',
     r'^(?:the\s+)?Answer(e)\s*(?:is\s+)?(e\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quiz protocol\.md']}),

    # EXAMPLE: the answer e is z

    ('Antwort 2',
     r'^(?:the\s+)?Answer(e)\s*(?:is\s+)?(z\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quiz protocol\.md'] }),






    # EXAMPLE: the answer e is df

    ('Antwort 3',
     r'^(?:the\s+)?Answer(e)\s*(?:is\s+)?([df]\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quiz protocol\.md']
     }),



    # Answer 1

    # Finds: "1", "one", "an", "one", "first", "first"

    # Allows sentences like: “Correct is 1”, “I’ll take the one”, “Solution 1the”

    # ('Answer 1',

    # r'.*(?:(?<!\d)1(?!\d)|eins?|eine|one|ers(?:te|tens)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Answer 2

    # Finds: "2", "two", "two", "two", "second", "second"

    # Also finds an example: "correct is 2 the solution is 2"

    # ('Answer 2',

    # r'.*(?:(?<!\d)2(?!\d)|zwei|zwo|two|zweit(?:e|ens)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Answer 3

    # Finds: "3", "three", "three", "third", "third"

    # ('Answer 3',

    # r'.*(?:(?<!\d)3(?!\d)|drei|three|dritt(?:e|ens)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # We define a list of signal words that must precede the number.

    # (?i) makes it case-insensitive (set by flags anyway, but to be on the safe side).

    # \b...\b searches for whole words for the trigger.

    # (?:is|would|the|the|the)? allows filler words in between.

    # (?<!\d)1(?!\d) ensures that it is really "1" and not "10" or "21".


    # Answer 1

    # Matches: "Correct is 1", "Answer 1", "I take the one", "Solution is 1the..."

    # EXAMPLE: the answer

    ('Antwort 1',
     r'^(?:the\s+)?.*\b(?:Answer|Solution|number|Correct|Choose|Take|is)\b\s*(?:is|were|the|the|the|the)?\s*(?<!\d)(1|one|a|one|first)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quiz protocol\.md']
     }),

    # The correct answer is 3


    # Answer 2

    # Matches: "correct is 2the solution...", "answer two", "take 2"

    # EXAMPLE: the answer

    ('Antwort 2',
     r'^(?:the\s+)?.*\b(?:Answer|Solution|number|Correct|Choose|Take|is)\b\s*(?:is|were|the|the|the|the)?\s*(?<!\d)(2|two|two|two|second)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quiz protocol\.md']
      }),

    # Answer 3

    # Matches: "Answer 3", "Solution three", "is 3"

    # EXAMPLE: the answer

    ('Antwort 3',
     r'^(?:the\s+)?.*\b(?:Answer|Solution|number|Correct|Choose|Take|is)\b\s*(?:is|were|the|the|the|the)?\s*(?<!\d)(3|three|pure|three|third)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quiz protocol\.md']
      }),


    # EXAMPLE: Answer 1

    ('', r'^Answer (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
     'only_in_windows': [r'quiz protocol\.md']
    }),

    # EXAMPLE: quit

    ('', r'^(quit|quiz|quizz|swiss) (start)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'quiz protocol\.md']
    }),

    # EXAMPLE: start quit

    ('', r'^(start) (quit|quiz|quizz)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'quiz protocol\.md']
    }),
]
