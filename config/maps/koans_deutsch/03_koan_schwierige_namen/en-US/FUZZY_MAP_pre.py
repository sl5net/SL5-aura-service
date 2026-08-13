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

# config/maps/koans_deutsch/03_koan_schwierige_namen/de-DE/FUZZY_MAP_pre.py

# ============================================================
# Koan 03: Difficult names – fuzzy matching in practice

# ============================================================
#
# LEARNING GOAL:

# Vosk often misrecognizes difficult names. With regex you can

# You can still match reliably - even if there are typos.

#
# TASK:

# Try saying this title:

# “Your Most Reverend Arch-Officer Councilor of Silesia”

#
# Then look in the log to see what Vosk really heard:

# grep "📢📢📢" log/aura_engine.log | tail -5

#
# Then activate the rule that fits best (remove #).

#
# QUESTION FOR THINKING:

# Which rule is more robust – the exact one or the one with .*?

# What are the advantages and disadvantages of r'^Your Highness.*$'?

#
# NEXT STEP: Koan 04

# ============================================================

FUZZY_MAP_pre = [


    # EXAMPLE: aunt

    ('Tante Emmelie', r'^(aunt|tandy|And|to the|and in|and How) (Emmelie|emil\w*|Onélie|vivien)*$'),


    # Exact Match (precise but fragile):

    # ('Great :) Congratulations', r'^Your Highest Honor.*Silesia.*$'),


    # Robust Match (flexible but non-specific):

    # ('Great :) Congratulations', r'^Your High Honor.*$'),


    # Fuzzy Match for the name:

    # ('Countess recognized!', r'^.*gr[äa]fin.*$', 0, {'command_flags': re.IGNORECASE}),

]
