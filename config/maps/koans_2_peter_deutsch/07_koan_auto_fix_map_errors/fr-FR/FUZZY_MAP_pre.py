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

# config/maps/koans_2_peter_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py

import re

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch', 1, {'command_flags': re.IGNORECASE}),
]

# ============================================================
# Koan 07 : Auto-Fix – Aura répare les fichiers de carte corrompus

# ============================================================
#
# CE QUE CELA FAIT :

# Si un fichier de carte contient un "mot nu" (et non un format de tuple),

# L'Auto-Fix d'Aura le corrige automatiquement lors du chargement.

#
# IMPORTANT:

# La correction automatique ne fonctionne que sur les fichiers inférieurs à ~ 1 Ko.

# C'est intentionnel – réécriture incontrôlée des grands

# Cela empêche les fichiers de carte.

#
# TÂCHE:

# 1. Insérez un seul mot dans FUZZY_MAP_pre (pas un tuple) :

# serviette à main

# 2. Enregistrez. Aura le corrige automatiquement selon une règle valide.

# 3. Vérifiez le journal pour "Auto-Fix".

#
# PROCHAINE ÉTAPE : Koan 08

# ============================================================

import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())



# Format de règle : ('texte de remplacement', r'modèle', seuil, drapeaux)

# Logique : de haut en bas, le premier coup gagne. Fullmatch (^...$) arrête le pipeline.


# TÂCHE PETER pour Koan : 07_koan_auto_fix_map_errors

# Aucune règle commentée trouvée.

# -> Créez une nouvelle règle significative pour ce koan.

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'command_flags': re.IGNORECASE}),
]
