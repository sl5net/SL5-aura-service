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

import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())



# Format de règle : ('texte de remplacement', r'modèle', seuil, drapeaux)

# Logique : de haut en bas, le premier coup gagne. Fullmatch (^...$) arrête le pipeline.



user_name = "USER_NAME"
# nom_utilisateur = getattr(paramètres, "USER_NAME", "[nom manquant]")


# aussi<-de

# TÂCHE PETER pour Koan : 09_personal_signature

# Aucune règle commentée trouvée.

# -> Créez une nouvelle règle significative pour ce koan.

FUZZY_MAP_pre = [
    # EXAMPLE: fabricant

    (f"Mit freundlichen Grüßen, {user_name}\n", r"^(fabricant|meilleur salutations|Avec amical Saluer|Arbre)\w*$", 55, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': 'koans_2_peter_deutsch',
        },
    ),

    # === FUZZY MATCHING TEST ===
    # Mot : confiture -> remplacement : DÉLICIEUX


    # Test 1 : Règle stricte (seuil 0 ou 100 - selon le système)

    # "Score" utilise (0-100%) : 100 = Exact


]
