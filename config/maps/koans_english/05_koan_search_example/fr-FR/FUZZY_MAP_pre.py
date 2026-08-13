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


import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée.


CONFIG_DIR = Path(__file__).parent

introduction = """
For this technical demonstration, we require a complex, publicly available dataset in a standard format (SQLite). In this context, the Bible serves merely as a well-known, freely available, and multifaceted example document to illustrate database queries and research logic.

I want to emphasize that this unit is not about theological or religious content. Our focus is purely on the implementation and application of analyzing structured text data.

The key point is the availability of such data. Many historical and cultural texts are fortunately available as open-source datasets, which enables our technical work. We could just as easily analyze a legal compendium or a scientific journal here.
"""

FUZZY_MAP_pre = [
    # TODO : Activez la ligne ci-dessous en supprimant le symbole de commentaire '#'

    # ('recherche dans Ruth chapitre 1 verset 1', fr'^.*$', 90, {'command_flags' : re.IGNORECASE,'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),


    # EXAMPLE: rechercher dans [livre] chapitre [numéro] verset [numéro]

    ('(bible) search', r'^recherche dans (?P<livre>\w*[ ]?\w+) chapitre (?P<chapitre>\d+) [v]\w+ (?P<versets>\d+)$', 90,
    {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # À FAIRE : Pouvez-vous inventer d’autres modèles de recherche ?


]
