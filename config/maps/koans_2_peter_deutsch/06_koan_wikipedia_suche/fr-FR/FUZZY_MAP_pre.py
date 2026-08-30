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

# config/maps/koans_2_peter_deutsch/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# depuis pathlib import Path as p;import os as o
# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

# TÂCHE DE PETER pour Koan : 06_koan_wikipedia_suche

#
# Ce plugin recherche le terme parlé dans Wikipédia.

# Exemple : L'utilisateur dit "wiki qu'est-ce qu'une maison"

# -> Le plugin recherche « qu'est-ce qu'une maison » dans Wikipédia

#
# La règle ci-dessous active le plugin Wikipédia pour TOUTES les entrées (^.*$).

# Après le match, le plugin est exécuté et le pipeline s'arrête.

#
# TÂCHE : Supprimez le « # » devant la règle pour l'activer.

# QUESTION : Que se passe-t-il lorsque vous dites quelque chose ? Ensuite, regardez dans : log/aura_engine.log


FUZZY_MAP_pre = [
    # ('Qu'est-ce que Tübingen ?', fr'^.*$', 90, {'command_flags' : re.IGNORECASE, 'skip_list' : ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

]
