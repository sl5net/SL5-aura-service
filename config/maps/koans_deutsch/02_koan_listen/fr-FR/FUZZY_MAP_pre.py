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

# configmaps/koans deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# ============================================================
# Koan 02 : Votre première règle regex – activée ou désactivée ?

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# Les règles Regex peuvent appliquer plusieurs mots prononcés à un seul

# Commande Carte. Ici : les groupes de lettres contrôlent "on"/"off".

#
# TÂCHE:

# 1. Supprimez le « # » devant UNE des deux règles ci-dessous.

# 2. Enregistrer - Aura se recharge la prochaine fois que vous appuyez sur le bouton.

# 3. Dites un mot qui commence par a-m (par exemple « bonjour »)

# ou celui qui commence par n-z (par exemple "eau").

#
# RÉSULTAT ATTENDU :

# "bonjour" → "à"

# "eau" → "dehors"

#
# QUESTION DE RÉFLEXION :

# Que se passe-t-il si vous activez les deux règles en même temps ?

# Lequel va gagner – et pourquoi ?

# Astuce : Les règles sont traitées de haut en bas.

#
# PROCHAINE ÉTAPE : Koan 03

# ============================================================

FUZZY_MAP_pre = [
    # ('un', r'^[a-m]+.*$'),

    # ('off', r'^[n-z]+.*$'),

]
