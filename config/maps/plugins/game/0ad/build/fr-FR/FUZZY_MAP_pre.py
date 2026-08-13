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

# config/maps/plugins/game/0ad/build/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']

_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
    'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
    'execute_only': True
}




baue = r'(\s*(\w+Aie\w+|voiture|\Ouah|fermier\w|bâtiment|construire|à|vélo|cultivation\w*|mais|aide de bureau|Paul|Paul|Pourquoi|warhols|pouvoir|notre|je|construire|\w+image|blanc)\s*)'
farm = r'f\w*a\w*m|fa\w*fr|fa|ferme|conduire|conducteur|couleurs|femme|femmes|des questions|avoir|robinet|bras|sur|dent'
bauernhof = r'(\s*(b\w+\s*(cour|une maison)|ventre|rosenhof|Constructeur|brun)\s*)'

feld = r'(\w*champ|grains\w*|Paul|rocher|tombe|compte|fourrure|fermement|films|tient|sont|veut|aide|PowerShell|Grobenzell)'
bauefeld_nonsens = '(vfl|aushält|ruhe sie sind|graues hält|ausfällt|warum es will|warum filmt|alles rund|oh accounts|auch im kornfeld|eure kornfeld)'

pflanze = r'(pomme de terre\w*|blé\w*|grain\w*|laitue\w*|fleur\w*|fleurs\w*|jardin|conf|grain\w*|champ\w*)'

acker_nonsens = r'(mal de tête|Barack Obama|imprimante usine|un taxi)'

kaserne = r'(caserne|\quoi[\s\w]*[äei]rn?e|Chat|classe|\quoi\Werne|\w*aracké|caserne\w?|Hébergement des troupes)'

tempel = r'(temple|Température\w*|Conseil|camp|\w[öae]député\wl|Jampil|Tim)'


# Kas Erne

# qu'est-ce que ce serait

# \was[\s\w]*[äe]rn?e


ignore_this_fill_words = r'(\b\w{1,3}\b\s*)?'

festung = r'(\s*(forteresse|f\w+\s*\w*|conduire toi|\w+\s*autour|est autour|muet|devient muet|fin|forteresse|forteresse|forteresse)\s*)'

arsenal = r'(arsenal|enregistrement|Des choses\s*une maison|Armes\s*action|armes|armes\s*charger|armes\s*la\w+|laisser laboratoire|donc appels|personnel|\w+rsonell|à nommer|n / A a|deux chaos|a depuis plus près)'

# tournée


turm = r'(\s*(tour|faire|but|tournée|tour)\s*)'
turmtype = r'(\s*(défensive|pierre|pierre|défense|défense)\s*)'

FUZZY_MAP_pre = [
    # EXAMPLE: construire une maison

    # ('h', fr'^{build}?(\w?from|House|\wau[^\se]*|have|Hopp|Rabbit|Rust|Rau|Année de construction|Chambre)$',

    ('h', fr'^(?!agriculteurs?){baue}?(\w?de|Maison|\Ouah[^\se]*|avoir|Hopp|lièvre|Rouiller|Rugueux|Année de construction|chambre)$',
     99, _common_meta),

    # fr'^({build}\s*)?(pomme de terre\w*|(blé\s*)*blé\w*|\white\w+en[\s\w]*will|(grain\s*)+\w*|champ\w*|(salade\s*)+\w*|fleur e\w*|\wumen|garden|conf|grain{field}\w*|{field}\w*)\s*{ignore_this_fill_words}(cultivation\w*|{build}|recommend|plant\w*)?\s*$',


    # EXAMPLE: grain de plante

    ('f',
     fr'^\s*({baue}\s*)?({pflanze}(\s+{feld})?|{feld})\s*{ignore_this_fill_words}(cultivation\w*|{baue}|recommander|usine\w*)?\s*$',
     99, _common_meta),

    # avoir



    # EXAMPLE: construire un champ

    # ('f', r'^\s*(build|build|power|our|build|\w+ild)\s*(missing|field|field)\s*$', 99, {'command_flags' : re.IGNORECASE, 'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construire un entrepôt

    ('s', fr'^{baue}?(([^wz]\w*)?action([\shr]*de)?|Storeh|\w+g[\shr]*de)\w*$', 99, _common_meta),

    # EXAMPLE: construire des casernes

    # ('construire une caserne', r'^\s*(build|build|Build)\s+(Ba\w+)$', 99, {'command_flags' : re.IGNORECASE, 'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construire des casernes

    # ('construire une caserne', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construire des casernes

    # ('construire une caserne', r'^\s*(\w+au\w+|build|wild|image)\s+([pb]a[rc]\w+)$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construire une maison

    # ('construire une maison', r'^\s*(build\s*h?aus|build\s*h?aus|h?aus\s*build|build\s*h?ouse|house)\s*$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),




    # EXAMPLE: construire un marché

    ('m', fr'^{baue}?(maman|mar[ck]t?|bâtiment\s*marché|marché\s*construire|construire\s*marché|marché)\s*$', 99, _common_meta),

    # EXAMPLE: construire un port

    ('j', fr'^{baue}?(port)$', 99, _common_meta),

    # EXAMPLE: diplomatie

    ('<', r'^diplomate\w*$'),

    # forgé


    # EXAMPLE: forgé

    # EXAMPLE: construire une forge

    # EXAMPLE: construire une forge

    ('n', fr'^{baue}?(s(ch)?m\w*|forge)\s*$', 99, _common_meta),

    # EXAMPLE: construire un champ

    # ('f', r'^\s*(build\s*farm|build\s*farm|farm\s*build|build\s*farm|farm|frahm|f\w*a\w*m)\s*$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # ('f', fr'^\s*({buildfield_nonsense}|{build}\s*{field}|build\s*{field}|{field}\s*build|build\s*{field}|{field})\s*$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec' : [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only' : True}),


    # EXAMPLE: champs de plantes

    # ('f', fr'^\s*({acre_nonsense}|acre\s*build|acre|plant\w*|plant\s*field)\s*$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec' : [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only' : True}),



    # EXAMPLE: construire un arsenal

    ('a', fr'^({baue}?{arsenal}|{arsenal}\s*{baue}?)$', 99, _common_meta),

    # construire une ferme (deux fermes)


    # EXAMPLE: construire une ferme

    # EXAMPLE: construire une ferme

    ('ff', fr'^({baue}\s*)?{ignore_this_fill_words}?({bauernhof}|{farm})\s*$', 99, _common_meta),
    # construire une forteresse (trois fermes)


    # EXAMPLE: construire une forteresse

    # ('fff', r'^\s*(build\s*fortress|build\s*fortress|fortress\s*build|build\s*fortress|fortress|trois\s*fermes)\s*$', 99, {'command_flags' : re.IGNORECASE,'only_in_windows' : ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construire une forteresse

    ('fff', fr'^({baue}{festung}|{festung}\s*{baue})$', 99, _common_meta ),


    # EXAMPLE: caserne

    ('b', fr'^({baue}?{kaserne}|{kaserne}{baue}?)$', 20, _common_meta),

    # EXAMPLE: temple

    ('ttt', fr'^({baue}?{tempel}|{tempel}{baue}?)$', 20, _common_meta),

    # EXAMPLE: construire une tour

    ('t', fr'^\s*({baue}{turmtype}?{turm}|{turm}|{turmtype}{turm}{baue}|{turmtype}?{turm})$', 99, _common_meta),

]
