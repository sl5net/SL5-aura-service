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




baue = r'(\s*(\w+ouch\w+|car|\wow|farmer\w|building|build|at|bike|cultivation\w*|but|office help|paul|Paul|Why|warhols|power|our|I|build|\w+image|white)\s*)'
farm = r'f\w*a\w*m|fa\w*en|fa|farmstead|drive|driver|colors|woman|women|questions|have|faucet|arm|on|tooth'
bauernhof = r'(\s*(b\w+\s*(yard|a house)|belly|rosenhof|Builder|brown)\s*)'

feld = r'(\w*field|grains\w*|paul|rock|falls|counts|fur|firmly|films|holds|are|wants|helps|powershell|Grobenzell)'
bauefeld_nonsens = '(vfl|aushält|ruhe sie sind|graues hält|ausfällt|warum es will|warum filmt|alles rund|oh accounts|auch im kornfeld|eure kornfeld)'

pflanze = r'(potato\w*|wheat\w*|grain\w*|lettuce\w*|flower\w*|flowers\w*|garden|conf|grain\w*|field\w*)'

acker_nonsens = r'(headache|Barack Obama|printer plant|acab)'

kaserne = r'(barracks|\wha[\s\w]*[äei]rn?e|Cat|class|\wha\werne|\w*aracke|barracks\w?|Troop accommodation)'

tempel = r'(temple|Temp\w*|Tip|camp|\w[öae]mp\wl|Jampil|Tim)'


# kas erne

# what\s+would be

# \was[\s\w]*[äe]rn?e


ignore_this_fill_words = r'(\b\w{1,3}\b\s*)?'

festung = r'(\s*(fortress|f\w+\s*\w*|drive you|\w+\s*around|is around|mute|becomes mute|ending|fortress|fortress|fortress)\s*)'

arsenal = r'(arsenal|recording|Things\s*a house|Weapons\s*stock|weapons|weapons\s*load|weapons\s*la\w+|let lab|so calls|personnel|\w+rsonell|to to name|n/a has|two chaos|a from closer)'

# tour


turm = r'(\s*(tower|do|goal|tour|tower)\s*)'
turmtype = r'(\s*(defensive|stone|stone|defense|defense)\s*)'

FUZZY_MAP_pre = [
    # EXAMPLE: build house

    # ('h', fr'^{build}?(\w?from|House|\wau[^\se]*|have|Hopp|Rabbit|Rust|Rau|Year built|Room)$',

    ('h', fr'^(?!farmers?){baue}?(\w?out of|House|\wow[^\se]*|have|Hopp|Hare|Rust|Rough|Year of construction|room)$',
     99, _common_meta),

    # fr'^({build}\s*)?(potato\w*|(wheat\s*)*wheat\w*|\white\w+en[\s\w]*will|(grain\s*)+\w*|field\w*|(salad\s*)+\w*|flower e\w*|\wumen|garden|conf|grain{field}\w*|{field}\w*)\s*{ignore_this_fill_words}(cultivation\w*|{build}|recommend|plant\w*)?\s*$',


    # EXAMPLE: plant grain

    ('f',
     fr'^\s*({baue}\s*)?({pflanze}(\s+{feld})?|{feld})\s*{ignore_this_fill_words}(cultivation\w*|{baue}|recommend|plant\w*)?\s*$',
     99, _common_meta),

    # have



    # EXAMPLE: build field

    # ('f', r'^\s*(build|build|power|our|build|\w+ild)\s*(missing|field|field)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build warehouse

    ('s', fr'^{baue}?(([^wz]\w*)?stock([\shr]*out of)?|Storeh|\w+g[\shr]*out of)\w*$', 99, _common_meta),

    # EXAMPLE: build barracks

    # ('build barracks', r'^\s*(build|build|Build)\s+(Ba\w+)$', 99, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build barracks

    # ('build barrack', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build barracks

    # ('build barrack', r'^\s*(\w+au\w+|build|wild|image)\s+([pb]a[rc]\w+)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build home

    # ('build house', r'^\s*(build\s*h?aus|build\s*h?aus|h?aus\s*build|build\s*h?ouse|house)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),




    # EXAMPLE: build market

    ('m', fr'^{baue}?(ma|mar[ck]t?|building\s*market|market\s*build|build\s*market|market)\s*$', 99, _common_meta),

    # EXAMPLE: build harbor

    ('j', fr'^{baue}?(harbor)$', 99, _common_meta),

    # EXAMPLE: diplomacy

    ('<', r'^diplomat\w*$'),

    # wrought


    # EXAMPLE: wrought

    # EXAMPLE: build forge

    # EXAMPLE: build forge

    ('n', fr'^{baue}?(s(ch)?m\w*|forge)\s*$', 99, _common_meta),

    # EXAMPLE: build field

    # ('f', r'^\s*(build\s*farm|build\s*farm|farm\s*build|build\s*farm|farm|frahm|f\w*a\w*m)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # ('f', fr'^\s*({buildfield_nonsense}|{build}\s*{field}|build\s*{field}|{field}\s*build|build\s*{field}|{field})\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),


    # EXAMPLE: plant fields

    # ('f', fr'^\s*({acre_nonsense}|acre\s*build|acre|plant\w*|plant\s*field)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),



    # EXAMPLE: build arsenal

    ('a', fr'^({baue}?{arsenal}|{arsenal}\s*{baue}?)$', 99, _common_meta),

    # build farmstead (two farms)


    # EXAMPLE: build farm

    # EXAMPLE: build farm

    ('ff', fr'^({baue}\s*)?{ignore_this_fill_words}?({bauernhof}|{farm})\s*$', 99, _common_meta),
    # build fortress (three farms)


    # EXAMPLE: build fortress

    # ('fff', r'^\s*(build\s*fortress|build\s*fortress|fortress\s*build|build\s*fortress|fortress|three\s*farms)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build fortress

    ('fff', fr'^({baue}{festung}|{festung}\s*{baue})$', 99, _common_meta ),


    # EXAMPLE: barracks

    ('b', fr'^({baue}?{kaserne}|{kaserne}{baue}?)$', 20, _common_meta),

    # EXAMPLE: temple

    ('ttt', fr'^({baue}?{tempel}|{tempel}{baue}?)$', 20, _common_meta),

    # EXAMPLE: build tower

    ('t', fr'^\s*({baue}{turmtype}?{turm}|{turm}|{turmtype}{turm}{baue}|{turmtype}?{turm})$', 99, _common_meta),

]
