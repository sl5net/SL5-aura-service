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

# config/maps/koans_2_peter_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# Rule format: ('replacement text', r'pattern', threshold, flags)

# Logic: Top-down, first hit wins. Fullmatch (^...$) stops the pipeline.



user_name = "USER_NAME"
# user_name = getattr(settings, "USER_NAME", "[name missing]")


# too<-from

# PETER TASK for Koan: 09_personal_signature

# No commented out rules found.

# -> Create a meaningful new rule for this koan.

FUZZY_MAP_pre = [
    # EXAMPLE: mfg

    (f"Mit freundlichen Grüßen, {user_name}\n", r"^(mfg|best regards|With friendly Greet|Tree)\w*$", 55, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': 'koans_2_peter_deutsch',
        },
    ),

    # === FUZZY MATCHING TEST ===
    # Word: jam -> replacement: DELICIOUS


    # Test 1: Strict rule (threshold 0 or 100 - depending on the system)

    # "Score" uses (0-100%): 100 = Exact


]
