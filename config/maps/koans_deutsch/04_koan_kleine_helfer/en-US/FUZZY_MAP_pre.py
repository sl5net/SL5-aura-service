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

# config/maps/koans_deutsch/04_koan_kleine_helfer/de-DE/FUZZY_MAP_pre.py

# Koan 04: Little helpers – voice commands for numbers and codes

# ============================================================
#
# LEARNING GOAL:

# Numbers and codes that Vosk does not recognize directly

# are output via spoken phrases.

#
# TASK:

# Say: “Metzingen area code”

# Result: "07122"

#
# Then add your own area code or zip code!

#
# NEXT STEP: Koan 05

# ============================================================

FUZZY_MAP_pre = [


    # Area code numbers mainly 0707 (Tübingen) and 0712 (Reutlingen) as well as variations for smaller surrounding towns.


    # Tübingen and surrounding areas (0707x) area code regex description

    # EXAMPLE: Area code Tübingen main zone

    ('07071', r'^Phone prefix Tübingen Main zone$'),
    # EXAMPLE: Area code Dußlingen

    ('07073', r'^Phone prefix Dusslingen$'),
    # EXAMPLE: Area code Rottenburg am Neckar

    ('07074', r'^Phone prefix Rottenburg on Neckar$'),
    # EXAMPLE: Area code Ammerbuch

    ('07075', r'^Phone prefix Ammerbuch$'),
    # EXAMPLE: Gomaringen area code

    ('07076', r'^Phone prefix Gomaringen$'),
    # EXAMPLE: Area code Mössingen

    ('07078', r'^Phone prefix Mössingen$'),

    # Reutlingen and surroundings (0712x) area code regex description

    # EXAMPLE: Area code Reutlingen main zone

    ('07121', r'^Phone prefix Reutlingen Main zone$'),
    # EXAMPLE: Metzingen area code

    ('07122', r'^Phone prefix Metzingen$'),
    # EXAMPLE: Area code Reutlingen-Degerschlacht

    ('07123', r'^Phone prefix Reutlingen-Deger battle$'),
    # EXAMPLE: Area code Pliezhausen

    ('07124', r'^Phone prefix Pliezhausen$'),
    # EXAMPLE: Area code Pfullingen

    ('07125 hi all', r'^Phone prefix Pfullingen$'),
    # EXAMPLE: Area code Neckartenzlingen

    ('07127', r'^Phone prefix Neckartenzlingen$'),

    # Can you also ask other questions? Maybe have your own complete number issued?

    #

]
