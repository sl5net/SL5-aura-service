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

# Koan 04 : Petits assistants – commandes vocales pour chiffres et codes

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# Numéros et codes que Vosk ne reconnaît pas directement

# sont émis via des phrases parlées.

#
# TÂCHE:

# Dites : « indicatif régional de Metzingen »

# Résultat : "07122"

#
# Ajoutez ensuite votre propre indicatif régional ou code postal !

#
# PROCHAINE ÉTAPE : Koan 05

# ============================================================

FUZZY_MAP_pre = [


    # Numéros d'indicatif régional principalement 0707 (Tübingen) et 0712 (Reutlingen), ainsi que des variantes pour les petites villes environnantes.


    # Tübingen et ses environs (0707x) description de l'expression régulière de l'indicatif régional

    # EXAMPLE: Indicatif régional zone principale de Tübingen

    ('07071', r'^Préfixe téléphonique Tübingen Zone principale$'),
    # EXAMPLE: Indicatif régional Dusslingen

    ('07073', r'^Préfixe téléphonique Düsseldorf$'),
    # EXAMPLE: Indicatif régional Rottenburg am Neckar

    ('07074', r'^Préfixe téléphonique Rottenbourg sur Neckar$'),
    # EXAMPLE: Indicatif régional Ammerbuch

    ('07075', r'^Préfixe téléphonique Ammerbuch$'),
    # EXAMPLE: L'indicatif régional de Gomaringen

    ('07076', r'^Préfixe téléphonique Gomaringen$'),
    # EXAMPLE: L'indicatif régional de Mössingen

    ('07078', r'^Préfixe téléphonique Mössingen$'),

    # Reutlingen et environs (0712x) description de l'expression régulière de l'indicatif régional

    # EXAMPLE: Indicatif régional zone principale de Reutlingen

    ('07121', r'^Préfixe téléphonique Reutlingen Zone principale$'),
    # EXAMPLE: Indicatif régional de Metzingen

    ('07122', r'^Préfixe téléphonique Metzingen$'),
    # EXAMPLE: L'indicatif régional de Reutlingen-Degerschlacht

    ('07123', r'^Préfixe téléphonique Reutlingen-Bataille de Deger$'),
    # EXAMPLE: Indicatif régional Pliezhausen

    ('07124', r'^Préfixe téléphonique Pliezhausen$'),
    # EXAMPLE: Indicatif régional Pfullingen

    ('07125 hi all', r'^Préfixe téléphonique Pfullingen$'),
    # EXAMPLE: Indicatif régional Neckartenzlingen

    ('07127', r'^Préfixe téléphonique Neckartenzlingen$'),

    # Pouvez-vous également poser d'autres questions ? Peut-être avez-vous votre propre numéro complet?

    #

]
