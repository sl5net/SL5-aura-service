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

# config/maps/koans_english/05_koan_search_example/de-DE/FUZZY_MAP_pre.py

# using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia aproximada simple.


CONFIG_DIR = Path(__file__).parent

introduction = """
For this technical demonstration, we require a complex, publicly available dataset in a standard format (SQLite). In this context, the Bible serves merely as a well-known, freely available, and multifaceted example document to illustrate database queries and research logic.

I want to emphasize that this unit is not about theological or religious content. Our focus is purely on the implementation and application of analyzing structured text data.

The key point is the availability of such data. Many historical and cultural texts are fortunately available as open-source datasets, which enables our technical work. We could just as easily analyze a legal compendium or a scientific journal here.
"""

FUZZY_MAP_pre = [
    # TODO: active la línea siguiente eliminando el símbolo de comentario '#'

    # ('buscar en Rut capítulo 1 versículo 1', fr'^.*$', 90, {'command_flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # EXAMPLE: buscar en [libro] capítulo [número] versículo [número]

    ('(bible) search', r'^buscar en (?P<libro>\w*[ ]?\w+) capítulo (?P<capítulo>\d+) [v]\w+ (?P<versos>\d+)$', 90,
    {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # TODO: ¿Puedes inventar otros patrones de búsqueda?


]
