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

import re

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia aproximada simple.


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
    # TODO: Ayuda a unir estos trabalenguas.


    # ¿Quizás así por el título?

    # ('¡Buen trabajo!', r'^Su Más Noble Excelencia.*$', 90, {'command_flags': re.IGNORECASE}),


    # ¿O una coincidencia parcial?

    # ('¡Éxito!', r'^.*Cronología Xenocrónica.*$', 90, {'command_flags': re.IGNORECASE}),


    # ¿Y por el nombre?

    # EXAMPLE: Condesa

    ('Phonetics mastered!', r'^.*(Condesa|luna|cliente des|Apenas des|cliente des|contar tess).*$', 90, # min_accuracy
 {'command_flags': re.IGNORECASE}),
]

# Apenas deskund deskund des

