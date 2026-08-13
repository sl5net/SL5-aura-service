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
# Koan 03 : Noms difficiles – correspondance floue en pratique

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# Vosk reconnaît souvent mal les noms difficiles. Avec regex, vous pouvez

# Vous pouvez toujours faire une correspondance fiable, même s'il y a des fautes de frappe.

#
# TÂCHE:

# Essayez de dire ce titre :

# « Votre Très Révérend Archi-Officier Conseiller de Silésie »

#
# Ensuite, regardez dans le journal pour voir ce que Vosk a réellement entendu :

# grep "📢📢📢" log/aura_engine.log | queue -5

#
# Activez ensuite la règle qui vous convient le mieux (supprimez le #).

#
# QUESTION DE RÉFLEXION :

# Quelle règle est la plus robuste : la règle exacte ou celle avec .* ?

# Quels sont les avantages et les inconvénients de r'^Votre Altesse.*$' ?

#
# PROCHAINE ÉTAPE : Koan 04

# ============================================================

FUZZY_MAP_pre = [


    # EXAMPLE: tante

    ('Tante Emmelie', r'^(tante|tandy|Et|à le|et dans|et Comment) (Emmélie|Émile\w*|Surémensonge|vivien)*$'),


    # Correspondance exacte (précise mais fragile) :

    # ("Super :) Félicitations", r'^Votre plus grand honneur.*Silésie.*$'),


    # Robust Match (flexible mais non spécifique) :

    # ("Super :) Félicitations", r'^Votre Haute Honneur.*$'),


    # Correspondance floue pour le nom :

    # ('Comtesse reconnue !', r'^.*gr[äa]fin.*$', 0, {'command_flags': re.IGNORECASE}),

]
