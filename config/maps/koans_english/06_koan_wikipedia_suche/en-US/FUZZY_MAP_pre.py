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

# config/maps/koans_english/06_koan_wikipedia_suche/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401
from pathlib import Path

# ============================================================
# Koan 06: Wikipedia Search by Voice

# ============================================================
#
# LEARNING GOAL:

# on_match_exec can query online APIs.

# Here: Wikipedia search by voice command.

#
# TASK:

# 1. Activate the rule below.

# 2. Say: "What is London?"

#
# ERRORS? Check the log:

# grep "wikipedia" log/aura_engine.log | tail -10

#
# OFFLINE OPTION:

# See config/maps/plugins/standard_actions/wikipedia_local/

#
# NEXT STEP: Koan 07

# ============================================================

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # ('What is London?', r'^what is (?P<topic>.+)\?$', 90, {

    # 'command_flags': re.IGNORECASE,

    # 'on_match_exec': [CONFIG_DIR / 'wiki_search.py']

    # }),

]
