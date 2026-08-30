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

# from pathlib import Path as p;import os as o
# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

# PETER TASK for Koan: 06_koan_wikipedia_suche

#
# This plugin searches for the spoken term in Wikipedia.

# Example: The user says "wiki what is a house"

# -> Plugin searches for “what is a house” in Wikipedia

#
# The rule below activates the Wikipedia plugin for ALL entries (^.*$).

# After the match, the plugin is executed and the pipeline stops.

#
# TASK: Remove the '#' in front of the rule to activate it.

# QUESTION: What happens when you say something? Then look in: log/aura_engine.log


FUZZY_MAP_pre = [
    # ('What is Tübingen?', fr'^.*$', 90, {'command_flags': re.IGNORECASE, 'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

]
