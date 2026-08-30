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

# config/maps/plugins/bible_search/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


CONFIG_DIR = Path(__file__).parent

examples = r"""

Verwendung:

Beispiele:

Suche in Ruth Kapitel 1 Vers 1
Suche in erster Dave Kapitel 1 Vers halten
Suche in 1 Chroniken 1 Kapitel 1

Varianten um das gleiche zu Fragen:

Suche in Ruth Kapitel 1 Vers 1
# EXAMPLE: buscar itext x texto capítulo 123 vfdph texto 123

('bible suche', r'^buscar (i\w+ )?(?P<libro>\w*[ ]?\w+) capítulo (?P<capítulo>\d+) [vfdph]\w+ (?P<versos>\d+)$', 90, { ...

Suche in Ruth Kapitel 1 1 Vers
# EXAMPLE: buscar itext x texto capítulo 123 123 vfdph texto

('bible suche', r'^buscar (i\w+ )?(?P<libro>\w*\s*\w+) capítulo (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {...

Suche in Ruth 1 Kapitel 1 Vers
# EXAMPLE: buscar itext x texto 123 capítulo 123 texto vfdph

('bible suche', r'^buscar (i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) capítulo (?P<versos>\d+) [vfdph]\w+$', 90, {...

"in" kann auch weggelassen werden.


Suche in Ruth Kapitel 1 Vers 1
Ruth 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Und es geschah in den Tagen, als die Richter richteten, da entstand eine Hungersnot im Lande. Und ein Mann von Bethlehem-Juda zog hin, um sich in den Gefilden Moabs aufzuhalten, er und sein Weib und seine beiden Söhne.

Suche in erster Dave Kapitel 1 Vers halten

Suche in 1 Chroniken 1 Kapitel 1
Joel 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Das Wort Jehovas, welches zu Joel, dem Sohne Pethuels, geschah.
suche ihn 1 codec les kapitel 1 ps ein

I Chronicles 1:1 (# GerElb1905: German Darby Unrevidierte Elberfelder (1905)): Adam, Seth, Enos,

Suche in 1 t'gallo tot als 1 Kapitel 1 Vers'

"""


# EXAMPLE: buscar ãJ biblia

searchCmd=r'(buscar \w+ Biblia|buscar|Biblia)'

# EXAMPLE: la vía

Thessalonians = r"(dem a través de|t[\w ']*chal[\w ]*w[\w ]*o[\w ]*a[\w ]*s|t\w*\s*\w*s|k\w*e\w*alonia\w*\s*\w*)\b"



FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.



    # El libro 'Levítico' no existe en la traducción 'GerElb1905'.

    # EXAMPLE: Levíticio

    ('Leviticus', r'\blevitikus\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: cx leer

    ('Chronicles', r'\b(c\w*\s*leer|Códice\s*leer|hermano\w*\s*vamos)\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),





    # ('Timoteo', rf"(timoteo|tee[ \w]*io[ \w\-]*tee|t[ \w]+tes)\b", 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['Herramienta de idioma'],

    # }),



    # TODO: la búsqueda en II Timoteo tiene errores 9.11.'25

    # ('buscar en II Timoteo', rf"(buscar en segundo) ([\w ]+ee|[\w ]+sy)\b", 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['Herramienta de idioma'],

    # }),








    # EXAMPLE: buscar en 1

    ('suche in I Thessalonians', rf"suche in (1|erster) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: buscar en 2

    ('suche in II Thessalonians', rf"suche in (2|zweiter) {Thessalonians}\b", 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: Buscar en

    ('suche in II', r'^Buscar (en el|en) \wcontin\w*', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),
    # EXAMPLE: buscar en el segundo texto

    ('suche in II Samuel', r'buscar en segundo (s\w+|conoció)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: primerex

    # ('1', r'\b(primero\w*|más serio)\b', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'skip_list': ['Herramienta de idioma'],

    # }),

    # EXAMPLE: segundox

    ('2', r'\respectivamente\w*\b', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),


    # EXAMPLE: Buscar en Levx

    ('Suche in Leviticus', r'\bBuscar en (Lev\w*\b|\w.*corto\b|.*beso)', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),




    # EXAMPLE: versículo

    ('Vers 1', r'\b(versículo|conduce) (a|mencionado|lejos)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),

    # EXAMPLE: ser justo

    ('Vers 1', r'\b(justo ser)$', 90, {
        'command_flags': re.IGNORECASE,
        'skip_list': ['LanguageTool'],
    }),



    # EXAMPLE: VAR itext x texto capítulo 123 verso texto 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*[ ]?\w+) capítulo (?P<capítulo>\d+) [vfdph]\w+ (?P<versos>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: VAR itext x texto capítulo 123 texto de 123 versos

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*\s*\w+) capítulo (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: VAR itext x texto 123 capítulo 123 verso texto

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) capítulo (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),





    # EXAMPLE: VAR itext x texto 123 Verso texto 123

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*[ ]?\w+) (?P<capítulo>\d+) [vfdph]\w+ (?P<versos>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Buscar Rut 123 123 verso

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Buscar Rut 123 123 verso

    ('bible suche', fr'^{searchCmd} (i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),


    # ahora búsqueda experimental más agresiva (esto tal vez sobrescriba otros complementos) (S.11.11.'25 09:13 martes)


    # EXAMPLE: Rut capítulo 123 versículo 123

    ('bible suche', r'^(i\w+ )?(?P<libro>\w*[ ]?\w+) capítulo (?P<capítulo>\d+) [vfdph]\w+ (?P<versos>\d+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Rut texto capítulo 123 123 verso

    ('bible suche', r'^(i\w+ )?(?P<libro>\w*\s*\w+) capítulo (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # EXAMPLE: Rut 123 capítulo 123 verso

    ('bible suche', r'^(i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) capítulo (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),




    # lo siguiente está en conflicto con reglas como: cuánto es 5 más 3 (ver, 11.11.'25 13:35 martes)

    # Esto fue un poco difícil de encontrar.


    # ('búsqueda de la biblia', fr'^(i\w+ )?(?P<libro>\w*[ ]?\w+) (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'on_match_exec': [CONFIG_DIR / 'bible_search.py']

    # }),



    # EXAMPLE: Rut 123 123 verso

    ('bible suche', r'^(i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),
    # EXAMPLE: Lo que Rut 1 1 verso

    ('bible suche', r'^(i\w+ )?(?P<libro>\w*\s*\w+) (?P<capítulo>\d+) (?P<versos>\d+) [vfdph]\w+$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),



]















