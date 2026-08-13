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

# config/maps/koans_english/03_koan_difficult_names/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée.


difficultNames = """
This is an excellent progression! To create a name that is phonetically maximum difficult to pronounce, we must overuse English consonant clusters, archaic titles, and unusual syllable combinations.

Here is the result:

Title:
Your Most Noble Excellency, Arch-Administrative-Councillor-of-Przewalskyst-Silesia-Westphalia, Royal-Electoral Deputy-Substitute and Authentic Trustee of Xenochronistic Chronology.

Name:
Phryxts-Gzwryl-Wzesch-Chrysth, Countess of and to Squelch-Quartzh-Pfrts-Blackened-Crest.

Can you pronounce the title?
Can you pronounce the name?

What interesting things can you find in
log/aura_engine.log?

If you have multiple friends who are also Countesses? How do you distinguish them in speech output?

solution is below

"""


















































FUZZY_MAP_pre = [
    # À FAIRE : Aidez à faire correspondre ces virelangues.


    # Peut-être comme ça pour le titre ?

    # ("Excellent travail !", r'^Votre Excellence la plus noble.*$', 90, {'command_flags' : re.IGNORECASE}),


    # Ou une correspondance partielle ?

    # ("Succès !", r'^.*Chronologie xénochronique.*$', 90, {'command_flags' : re.IGNORECASE}),


    # Et pour le nom ?

    # EXAMPLE: Comtesse

    ('Phonetics mastered!', r'^.*(Comtesse|lune|client des|À peine des|client des|compter Tess).*$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
]

# À peine bureau des un des

