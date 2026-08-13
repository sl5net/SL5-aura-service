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

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']

_common_meta_NO_on_match_exec = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
}
_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
    'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
    'execute_only': True
}

# infranken

# turn in front

# in\s*fr\w*nt\w+

# infantry


# into the beef

# in[\w\s]r\w+


infanterie = r'(in[\w\s]r\w+|inf\w*\s*(rie|try|ken)|infra\w*|infantry|in\s*fr\w*nt\w+|infantry|infra try|the infantry|infantry|foot troops|in\s*fr\w+t\s*\w|him\s*fr\w+|\s*i\w*[nm]\s*fr\w+|\w*\s*infra)'

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py

# skeleton in strangers

# discovered in strangers

# skeleton infantry


# select workers


# me the hedgehog chunk


waehl = r'(Email|\w*choose\w*|choice\w*|take\w*|likes|mark|me the)'

select1 = r'(select|s\w*ele\w*t+|\w*corners|Benedict|a|\we\w+[ck]\w+t|\w*lays|himself|beats|s\w+el\w*e|source)'

# licks into the beef


select = fr'(\s*({select1}|{waehl})\s*)'

iddle = r'(\s*(iddle|iddle|noble|i[gdts]|\wi\w+le\w+|under[aa]tig\w*|work\w*|unemployed\w*|so|receive)\s*)'
FUZZY_MAP_pre = [
    # EXAMPLE: choose middle

    ('select iddle', fr'^{select}?({iddle}|{iddle}|{select}?)$', 20, _common_meta),

    # EXAMPLE: choose workers

    ('select_women', fr'^{select}?(fr\w+|Construction work\w*|Citizens\w*|work\w*|but|Support\w*|old\s*w|old\s*where|old\s*fr|ald\s*women)$', 20, _common_meta),

    # EXAMPLE: seltext woman

    ('select_women', r'^\s*sel\w+$', 20, _common_meta_NO_on_match_exec),

    # ctrl+h = select house

    # EXAMPLE: select house

    ('ctrl+h', r'^\s*(ctrl|control|control|tax)\s*\+?\s*h(ouse)?\s*$', 20, _common_meta_NO_on_match_exec),

    # ctrl+ m = select market

    # EXAMPLE: select market

    ('ctrl+m', r'^\s*(ctrl|control|control|tax)\s*\+?\s*m(ark|market)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+b = select barrack


    # EXAMPLE: control barack

    ('ctrl+b', r'^\s*(ctrl|control|control|tax)\s*\+?\s*b(aracke|barracks)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+f = select farm


    # EXAMPLE: farm

    ('ctrl+f', r'^\s*(ctrl|control|control|tax)\s*\+?\s*f(arm)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl s = select Storehouse Ship Stable Elephant table Dock ... (includes several)


    # EXAMPLE: control Storehouse

    ('ctrl+s', r'^\s*(ctrl|control|control|tax)\s*\+?\s*s(torehouse|ship|stable|elephant\s*stable|dock|building)?\s*$', 20,
     _common_meta_NO_on_match_exec),
    # Ctrl X = select Barracks + Elephant Stable + Stable (nearly everything)


    # EXAMPLE: control everything

    ('ctrl+x', r'^\s*(ctrl|control|control|tax)\s*\+?\s*x(everything|building)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ... more building selection commands



    # EXAMPLE: old woman

    ('alt+w', r'^\s*(old|ald)\s*\+?\s*w(Oman|woman)?\s*$', 20, _common_meta_NO_on_match_exec),

    # alt+ I = select infrastructure







    # EXAMPLE: old Spearman

    ('alt+p', r'^\s*(old|ald)\s*\+?\s*p(ikeman|spearman|fanatic|lancer)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+C = Cavalry


    # EXAMPLE: old cavalry

    ('alt+c', r'^\s*(old|ald)\s*\+?\s*c(avalry|cavalry)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ A = Archer, Elephant Archer, Slinger Javelineer, ... (group of champions)


    # EXAMPLE: old slinger

    ('alt+a', r'^\s*(old|ald)\s*\+?\s*a(rcher|slinger|javelineer|archer|ranged fighter)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+S = Swordman, ..


    # EXAMPLE: old Swordman

    ('alt+s', r'^\s*(old|ald)\s*\+?\s*s(wordman|swordsman)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+E = Elephant for Support


    # EXAMPLE: old elephant

    ('alt+e', r'^\s*(old|ald)\s*\+?\s*e(elephant|elephant|support)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+K = Catapult (exceptions because of conflict)


    # EXAMPLE: old catapult

    ('alt+k', r'^\s*(old|ald)\s*\+?\s*k(catapult|catapult)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+H = Healer


    # EXAMPLE: old healer

    ('alt+h', r'^\s*(old|ald)\s*\+?\s*h(ealer|healer)?\s*$', 20, _common_meta_NO_on_match_exec),
    # J = wounded (exceptions because near Healer)


    # EXAMPLE: wounded

    ('j', r'^\s*j(wounded|wounded)?\s*$', 20, _common_meta_NO_on_match_exec), # J for 'injured' or 'jawunded'
    # k = selects only nowwoundedonly using mouse


    # EXAMPLE: nowwoundedonly

    ('k', r'^\s*k(nowwoundedonly|not\s*wounded)?\s*$', 20, _common_meta_NO_on_match_exec), # K for 'kept' or 'klar'
    # ... more unit selection commands



    # Alt+ D = Dangerous Elephants (D. archer-,war-,hero-Elephant,... not Support&Elephant)


    # EXAMPLE: alt d dangerous elephants

    ('alt+d', r'^\s*(old|ald)\s*\+?\s*d(angry\s*elephants|dangerous\s*elephants)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+V = Siege and Ministers (Siege: rams, not heroes, Catapult, Bolt Shooter, Siege Tower ...)


    # EXAMPLE: old v victories

    ('alt+v', r'^\s*(old|ald)\s*\+?\s*v(victories|minister|siege|minister)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+M, Alt+X = select all military ( nowwoundedonly )

    # Here you could make two entries, depending on which transcription is more likely


    # (build up|build|power|our|build|\w+ild)


    # EXAMPLE: old military

    ('alt+x', r'^(old|ald)\s*\+?\s*m(ilit|ilit|m|x)\w+$', 20, _common_meta_NO_on_match_exec),

    # military


    # EXAMPLE: old military

    ('alt+x', r'^{select}?(\w*ilit\w*)$', 20, _common_meta_NO_on_match_exec),

    # EXAMPLE: old military

    ('alt+x', r'^\s*(old|ald)\s*\+?\s*x(military|military|all\s*military)?\s*$', 20, _common_meta_NO_on_match_exec), # Alternative für X, falls es sich auf Militär bezieht
    # Alt+N = select all non military


    # EXAMPLE: old n not military


    # EXAMPLE: old n non military

    # ('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*military|not\s*military|civilians)?\s*$', 20, _common_meta),


    # EXAMPLE: mark everything

    ('ctrl+alt', r'^(all\w* ma\w+).*$', 85, _common_meta),

    # EXAMPLE: old infantry

    # ('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+P = select Pikeman, Spearman, Fanatic (group of lancers/melee fighters)


    # EXAMPLE: infantry

    ('select_infantry', fr'^{select}?{infanterie}$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: spear carrier

    ('select_pikemen', r'^{select}?(spear tr[aa]ger|pikentr[aa]ger|phalanx|pikemen)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: cavalry

    ('select_cavalry', r'^{select}?(cavalry|equestrian|cavalry|cavalry)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: archers

    ('select_archers', r'^{select}?(archery[ouch]tzen|sh[ouch]tzen|pl[aa]nkler|archers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: swordsman

    ('select_swordsmen', r'^{select}?(swordk[aaae]+mpfer|swords|swordsmen)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: elephants

    ('select_elephants', r'^{select}?(elephants|elephant|elephants)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: catapults

    ('select_catapults', r'^{select}?(catapults|catapult|siege|catapults)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: healer

    ('select_healers', r'^{select}?(healer|priest|healers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]


