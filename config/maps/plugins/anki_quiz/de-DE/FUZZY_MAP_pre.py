# from .anki_logic import execute
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

# Antwort 2

FUZZY_MAP_pre = [
    ('Antwort 1',
     r'^(?:die\s+)?Antwort(e)\s*(?:ist\s+)?(e\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quizprotokoll\.md']}),

    ('Antwort 2',
     r'^(?:die\s+)?Antwort(e)\s*(?:ist\s+)?(z\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quizprotokoll\.md'] }),

    ('Antwort 3',
     r'^(?:die\s+)?Antwort(e)\s*(?:ist\s+)?([df]\w*)$', 100,
    {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'quizprotokoll\.md']
     }),



    # Antwort 1
    # Findet: "1", "eins", "eine", "one", "erste", "erstens"
    # Erlaubt Sätze wie: "Richtig ist 1", "Ich nehme die Eins", "Lösung 1die"
    # ('Antwort 1',
    #  r'.*(?:(?<!\d)1(?!\d)|eins?|eine|one|ers(?:te|tens)?).*', 100,
    # {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # Antwort 2
    # Findet: "2", "zwei", "zwo", "two", "zweite", "zweitens"
    # Findet auch dein Beispiel: "richtig ist 2die lösung ist 2"
    # ('Antwort 2',
    #  r'.*(?:(?<!\d)2(?!\d)|zwei|zwo|two|zweit(?:e|ens)?).*', 100,
    # {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # Antwort 3
    # Findet: "3", "drei", "three", "dritte", "drittens"
    # ('Antwort 3',
    #  r'.*(?:(?<!\d)3(?!\d)|drei|three|dritt(?:e|ens)?).*', 100,
    # {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # Wir definieren eine Liste von Signalwörtern, die vor der Zahl stehen müssen.
    # (?i) macht es case-insensitive (wird eh durch flags gesetzt, aber zur Sicherheit).
    # \b...\b sucht nach ganzen Wörtern für den Auslöser.
    # (?:ist|wäre|die|der|das|den)? erlaubt Füllwörter dazwischen.
    # (?<!\d)1(?!\d) stellt sicher, dass es wirklich "1" ist und nicht "10" oder "21".

    # Antwort 1
    # Matcht: "Richtig ist 1", "Antwort 1", "Ich nehme die Eins", "Lösung ist 1die..."
    ('Antwort 1',
     r'^(?:die\s+)?.*\b(?:Antwort|Lösung|Nummer|Richtig|Wähle|Nehme|ist)\b\s*(?:ist|wäre|die|der|das|den)?\s*(?<!\d)(1|eins|ein|one|erste)(?!\d).*',
     100,
     {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quizprotokoll\.md']
     }),

    # Richtig istantwort 3

    # Antwort 2
    # Matcht: "richtig ist 2die lösung...", "Antwort zwei", "nehme 2"
    ('Antwort 2',
     r'^(?:die\s+)?.*\b(?:Antwort|Lösung|Nummer|Richtig|Wähle|Nehme|ist)\b\s*(?:ist|wäre|die|der|das|den)?\s*(?<!\d)(2|zwei|zwo|two|zweite)(?!\d).*',
     100,
     {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quizprotokoll\.md']
      }),

    # Antwort 3
    # Matcht: "Antwort 3", "Lösung drei", "ist 3"
    ('Antwort 3',
     r'^(?:die\s+)?.*\b(?:Antwort|Lösung|Nummer|Richtig|Wähle|Nehme|ist)\b\s*(?:ist|wäre|die|der|das|den)?\s*(?<!\d)(3|drei|rein|three|dritte)(?!\d).*',
     100,
     {'flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'quizprotokoll\.md']
      }),


    ('', r'^Antwort (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
     'only_in_windows': [r'quizprotokoll\.md']
    }),

    ('', r'^(quitt|quiz|quizz|swiss) (starten)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'quizprotokoll\.md']
    }),

    ('', r'^(start) (quitt|quiz|quizz)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'quizprotokoll\.md']
    }),
]
