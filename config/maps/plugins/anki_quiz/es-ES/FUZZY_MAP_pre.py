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

# desde .anki_logic importar ejecutar

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



from pathlib import Path
CONFIG_DIR = Path(__file__).parent

readme = r"""
 Antwort 2
 Erklärung für Lernende:
  'Antwort 2',                                       # Index 0 (Ergebnis)
  r'^(?:el\s+)?Respuesta(e)\s*(?:es\s+)?(z\w*)$',    # Index 1 (Regex Pattern)
  100,                                               # Index 2 (Threshold/Score)
  {'command_flags': re.IGNORECASE, ...}                      # Index 3 (Options Dict)
"""


FUZZY_MAP_pre = [
    # EXAMPLE: la respuesta e es e

    ('Antwort 1',
     r'^(?:el\s+)?Respuesta(e)\s*(?:es\s+)?(e\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocolo de prueba\.Maryland']}),

    # EXAMPLE: la respuesta e es z

    ('Antwort 2',
     r'^(?:el\s+)?Respuesta(e)\s*(?:es\s+)?(z\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocolo de prueba\.Maryland'] }),






    # EXAMPLE: la respuesta e es df

    ('Antwort 3',
     r'^(?:el\s+)?Respuesta(e)\s*(?:es\s+)?([df]\w*)$', 100,
    {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'only_in_windows': [r'protocolo de prueba\.Maryland']
     }),



    # Respuesta 1

    # Encuentra: "1", "uno", "una", "uno", "primero", "primero"

    # Permite frases como: “Lo correcto es 1”, “Me quedo con el uno”, “Solución 1el”

    # ('Respuesta 1',

    # r'.*(?:(?<!\d)1(?!\d)|eins?|eine|one|ers(?:te|decenas)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Respuesta 2

    # Encuentra: "2", "dos", "dos", "dos", "segundo", "segundo"

    # También encuentra un ejemplo: "lo correcto es 2 la solución es 2"

    # ('Respuesta 2',

    # r'.*(?:(?<!\d)2(?!\d)|zwei|zwo|two|zweit(?:e|ens)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Respuesta 3

    # Encuentra: "3", "tres", "tres", "tercero", "tercero"

    # ('Respuesta 3',

    # r'.*(?:(?<!\d)3(?!\d)|drei|tres|dritt(?:e|ens)?).*', 100,

    # {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # Definimos una lista de palabras de señal que deben preceder al número.

    # (?i) hace que no distinga entre mayúsculas y minúsculas (establecido mediante indicadores de todos modos, pero para estar seguro).

    # \b...\b busca palabras completas para el activador.

    # (?:es|sería|el|el|el)? permite palabras de relleno en el medio.

    # (?<!\d)1(?!\d) garantiza que sea realmente "1" y no "10" o "21".


    # Respuesta 1

    # Coincidencias: "Lo correcto es 1", "Respuesta 1", "Tomo uno", "La solución es 1..."

    # EXAMPLE: la respuesta

    ('Antwort 1',
     r'^(?:el\s+)?.*\b(?:Respuesta|Solución|número|Correcto|Elegir|Llevar|es)\b\s*(?:es|eran|el|el|el|el)?\s*(?<!\d)(1|uno|a|uno|primero)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocolo de prueba\.Maryland']
     }),

    # La respuesta correcta es 3.


    # Respuesta 2

    # Coincidencias: "la solución correcta es 2...", "responde dos", "toma 2"

    # EXAMPLE: la respuesta

    ('Antwort 2',
     r'^(?:el\s+)?.*\b(?:Respuesta|Solución|número|Correcto|Elegir|Llevar|es)\b\s*(?:es|eran|el|el|el|el)?\s*(?<!\d)(2|dos|dos|dos|segundo)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocolo de prueba\.Maryland']
      }),

    # Respuesta 3

    # Coincidencias: "Respuesta 3", "Solución tres", "es 3"

    # EXAMPLE: la respuesta

    ('Antwort 3',
     r'^(?:el\s+)?.*\b(?:Respuesta|Solución|número|Correcto|Elegir|Llevar|es)\b\s*(?:es|eran|el|el|el|el)?\s*(?<!\d)(3|tres|puro|tres|tercero)(?!\d).*',
     100,
     {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
      'only_in_windows': [r'protocolo de prueba\.Maryland']
      }),


    # EXAMPLE: Respuesta 1

    ('', r'^Respuesta (1|2|3)$', 0, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
     'only_in_windows': [r'protocolo de prueba\.Maryland']
    }),

    # EXAMPLE: abandonar

    ('', r'^(abandonar|prueba|cuestionario|suizo) (comenzar)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'protocolo de prueba\.Maryland']
    }),

    # EXAMPLE: empezar a salir

    ('', r'^(comenzar) (abandonar|prueba|cuestionario)$', 100, {'on_match_exec': [CONFIG_DIR / 'anki_logic.py'],
        'only_in_windows': [r'protocolo de prueba\.Maryland']
    }),
]
