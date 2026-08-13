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

# configmaps/koans deutsch/01_koan_erste_stiege/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# aussi<-de

FUZZY_MAP_pre = [

# ============================================================
# Koan 01 : Votre première règle – Bienvenue sur Aura !

# ============================================================
#
# Condition préalable : Aura est déjà en cours d'exécution et votre raccourci clavier est configuré.

# Sinon : voir docs/GettingStarted.md

#
# TÂCHE:

# Supprimez le « # » devant la règle ci-dessous (ligne avec « hello world »).

# Enregistrez le fichier. Aura charge la règle à la prochaine pression sur une touche

# (Déclencheur de raccourci clavier) automatiquement nouveau - en mode veille, Aura dort complètement.

# Appuyez ensuite sur votre touche de raccourci et dites : "Bonjour tout le monde".

#
# RÉSULTAT ATTENDU :

# Types d'aura : "Hello World 01"

#
# POURQUOI LE PIPELINE S'ARRÊTE-T-IL APRÈS CELA ?

# Le motif r'^.*$' s'adapte à TOUT. Dès que cette règle s'applique,

# aucune autre règle n'est vérifiée. C’est le « Full Match Stop ».

# Pour en savoir plus : docs/FuzzyMapRuleGuide.md

#
# ============================================================

    # ('Bonjour tout le monde 01', r'^bonjour tout le monde$', 0, {'command_flags' : re.IGNORECASE}),

]
