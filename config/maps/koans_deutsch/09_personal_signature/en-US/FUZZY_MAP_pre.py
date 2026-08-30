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

# configmaps/koans deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# from config import settings



# ============================================================
# Koan 09: Personal Signature – Dynamic Rule Contents

# ============================================================
#
# LEARNING GOAL:

# Rules can contain Python variables - e.g. your name

# from config/settings_local.py

#
# TASK:

# 1. Set USER_NAME in config/settings_local.py

# 2. Say: “best regards” or “best regards”

#
# EXPECTED RESULT:

# "Sincerely, [your name]"

#
# NEXT STEP: Koan 10

# ============================================================

# user_name = getattr(settings, "USER_NAME", "[name missing]")

user_name = "Sebastian"
FUZZY_MAP_pre = [
    # EXAMPLE: Best regards

    # (f"With kind regards, {user_name}\n", r"^(best regards|with kind regards)\w*$"),


    # Best regards

    # (f"Best regards {user_name}\n", r"^(many size|every size)$",

    # 81, {'command_flags': re.IGNORECASE}),

]
