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

# config/maps/plugins/game/0ad/gather/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

# https://regex101.com/


CONFIG_DIR = p(__file__).parent

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

baum = r'árbol|Por qué'

FUZZY_MAP_pre = [

    # EXAMPLE: madera

    ('gather wood',
     fr'^(recolectar\s*)?(madera|conseguir\w*|rollo|rhön|Guau|hoy|tranquilo|puente|puentes|{baum}|árboles|árbol|rollo|rancho|rojo|ruiz|eructar|a nosotros)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # inigualable se agrega a tu mapa (331)

    # asldfkjasödlfsa dfanother testasdfsjdflksdöfsdj

    # sdddfgd festasdsdsadfsdf asdfasödkfjashfdasdfsadfsdfskates


    # futbol coche futbol


    # EXAMPLE: fruta

    ('gather fruit',
     r'^\s*(él|b|baya\w*|Gehring|factura|cerveza|bebé|fruta|fruta|fruta[n]?|manzanas[n]?|Manzana|Pera[n]?|bayas|cantera)\s*$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'caché': Falso

     }),

    # \w+ \w*a\w+es


    # EXAMPLE: carne

    ('gather meat',
     r'^(carne|caza|caza|\w+ \w*a\w+es|\w+ \w+a\w+es|chaquetas|Sí|Sí bien|su tener|carne|clima|cual Amén|conducir|robado|\w+\s\atrevimiento|nosotros tenía)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # EXAMPLE: piedra

    ('gather stone',
     r'^(recolectar\s*)?(piedra\w*|en ello|elevar\w*|acero|ciudad|aguijón|detener|comenzar|comenzar|estable|perturba|se levanta|disputar|pena|roca|roca|cantera|piedra)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'caché': Falso

     }),

    # A partir de ahora, la carta actual, Dance is, parece digna


    # EXAMPLE: metal

    ('gather metal',
     r'^(recolectar\s*)?(conoció\w+|estera\w+|metal|oro|resentido|con|cita|metal|bachiller|matcha|Gunter|ethan|Italia|con metal|veneno)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),


]
