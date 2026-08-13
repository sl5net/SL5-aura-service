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

# à partir de .anki_logic import exécuter

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path
CONFIG_DIR = Path(__file__).parent

readme = r"""
 Antwort 2
 Erklärung für Lernende:
  'Antwort 2',                                       # Index 0 (Ergebnis)
  r'^(?:le\s+)?Répondre(e)\s*(?:est\s+)?(z\w*)$',    # Index 1 (Regex Pattern)
  100,                                               # Index 2 (Threshold/Score)
  {'command_flags': re.IGNORECASE, ...}                      # Index 3 (Options Dict)
"""


FUZZY_MAP_pre = [
    # EXAMPLE: la réponse e est e

    ('Antwort 1',
     r'^(?:le\s+)?Répondre(e)\s*(?:est\s+)?(e\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocole de quiz\.Maryland']}),

    # EXAMPLE: la réponse e est z

    ('Antwort 2',
     r'^(?:le\s+)?Répondre(e)\s*(?:est\s+)?(z\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocole de quiz\.Maryland'] }),






    # EXAMPLE: la réponse e est df

    ('Antwort 3',
     r'^(?:le\s+)?Répondre(e)\s*(?:est\s+)?([df]\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocole de quiz\.Maryland']
     }),



    # Réponse 1

    # Trouve : "1", "un", "un", "un", "premier", "premier"

    # Permet des phrases telles que : "Correct est 1", "Je vais prendre celle-là", "Solution 1la"

    # (« Réponse 1 »,

    # r'.*(?:(?<!\d)1(?!\d)|eins?|eine|one|ers(?:te|dizaines)?).*', 100,

    # {'command_flags' : re.IGNORECASE, 'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Réponse 2

    # Recherche : "2", "deux", "deux", "deux", "seconde", "seconde"

    # Trouve également un exemple : "correct est 2, la solution est 2"

    # ("Réponse 2",

    # r'.*(?:(?<!\d)2(?!\d)|zwei|zwo|two|zweit(?:e|ens)?).*', 100,

    # {'command_flags' : re.IGNORECASE, 'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Réponse 3

    # Trouve : "3", "trois", "trois", "troisième", "troisième"

    # (« Réponse 3 »,

    # r'.*(?:(?<!\d)3(?!\d)|drei|trois|dritt(?:e|ens)?).*', 100,

    # {'command_flags' : re.IGNORECASE, 'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Nous définissons une liste de mots d'avertissement qui doivent précéder le numéro.

    # (?i) le rend insensible à la casse (défini par les indicateurs de toute façon, mais par mesure de sécurité).

    # \b...\b recherche des mots entiers pour le déclencheur.

    # (?:est-ce que|serait|le|le|le) ? permet des mots de remplissage entre les deux.

    # (?<!\d)1(?!\d) garantit qu'il s'agit bien de "1" et non de "10" ou "21".


    # Réponse 1

    # Correspondances : "La bonne réponse est 1", "Réponse 1", "J'en prends une", "La solution est 1le..."

    # EXAMPLE: la réponse

    ('Antwort 1',
     r'^(?:le\s+)?.*\b(?:Répondre|Solution|nombre|Correct|Choisir|Prendre|est)\b\s*(?:est|étaient|le|le|le|le)?\s*(?<!\d)(1|un|un|un|dabord)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocole de quiz\.Maryland']
     }),

    # La bonne réponse est 3


    # Réponse 2

    # Correspondances : "la solution correcte est 2...", "réponse deux", "prenez 2"

    # EXAMPLE: la réponse

    ('Antwort 2',
     r'^(?:le\s+)?.*\b(?:Répondre|Solution|nombre|Correct|Choisir|Prendre|est)\b\s*(?:est|étaient|le|le|le|le)?\s*(?<!\d)(2|deux|deux|deux|deuxième)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocole de quiz\.Maryland']
      }),

    # Réponse 3

    # Correspondances : "Réponse 3", "Solution trois", "est 3"

    # EXAMPLE: la réponse

    ('Antwort 3',
     r'^(?:le\s+)?.*\b(?:Répondre|Solution|nombre|Correct|Choisir|Prendre|est)\b\s*(?:est|étaient|le|le|le|le)?\s*(?<!\d)(3|trois|pur|trois|troisième)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocole de quiz\.Maryland']
      }),


    # EXAMPLE: Réponse 1

    ('', r'^Répondre (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
     'only_in_windows': [r'protocole de quiz\.Maryland']
    }),

    # EXAMPLE: quitter

    ('', r'^(quitter|questionnaire|quiz|suisse) (commencer)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'protocole de quiz\.Maryland']
    }),

    # EXAMPLE: commencer à quitter

    ('', r'^(commencer) (quitter|questionnaire|quiz)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'protocole de quiz\.Maryland']
    }),
]
