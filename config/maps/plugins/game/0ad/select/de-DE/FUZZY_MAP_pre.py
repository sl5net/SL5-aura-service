# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

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
# in front drehen
# in\s*fr\w*nt\w+
# infanterie

# ins rind
# in[\w\s]r\w+

infanterie = r'(in[\w\s]r\w+|inf\w*\s*(rie|try|ken)|infra\w*|infanterie|in\s*fr\w*nt\w+|infantry|infra try|die infanterie|fussvolk|fusstruppen|in\s*fr\w+t\s*\w|ihn\s*fr\w+|\s*i\w*[nm]\s*fr\w+|\w*\s*infra)'

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py
# skelett in fremden
# entdeckt in fremd
# skelett infanterie

# arbeiter auswählen

# mir der igel brocke

waehl = r'(Mail|\w*wähl\w*|auslese\w*|nehme\w*|mag|markiere|mir der)'

select1 = r'(select|s\w*ele\w*t+|\w*eckt|benedikt|a|\we\w+[ck]\w+t|\w*legt|selbst|schlägt|s\w+el\w*e|quelle)'

# leckt ins rind

select = fr'(\s*({select1}|{waehl})\s*)'

iddle = r'(\s*(iddle|iddle|edel|i[gdts]|\wi\w+le\w+|unt[äa]tig\w*|arbeite\w*|arbeitslos\w*|also|erhalte)\s*)'
FUZZY_MAP_pre = [
    # EXAMPLE: wähle iddle
    ('select iddle', fr'^{select}?({iddle}|{iddle}|{select}?).*$', 20, _common_meta),

    # EXAMPLE: wähle arbeiter
    ('select_women', fr'^{select}?(fr\w+|Bauarbeite\w*|Bürger\w*|arbeite\w*|aber|Unterstüt\w*|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women)$', 20, _common_meta),

    # EXAMPLE: seltext woman
    ('select_women', r'^\s*sel\w+$', 20, _common_meta_NO_on_match_exec),

    # ctrl+ h = select house
    # EXAMPLE: select house
    ('ctrl+h', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*h(ouse)?\s*$', 20, _common_meta_NO_on_match_exec),

    # ctrl+ m = select markt
    # EXAMPLE: select markt
    ('ctrl+m', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*m(arkt|market)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+ b = select barrack

    # EXAMPLE: control barack
    ('ctrl+b', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*b(aracke|barrack)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+ f = select farm

    # EXAMPLE: farm
    ('ctrl+f', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*f(arm)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl+ s = select Storehouse Ship Stable ElephantStable Dock ... (umfasst mehrere)

    # EXAMPLE: control Storehouse
    ('ctrl+s', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*s(torehouse|ship|stable|elephant\s*stable|dock|gebäude)?\s*$', 20,
     _common_meta_NO_on_match_exec),
    # Ctrl+ X = select Barracks + ElephantStable + Stable (nearly everything)

    # EXAMPLE: control alles
    ('ctrl+x', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*x(alles|gebäude)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ... weitere Gebäudewahl-Befehle


    # EXAMPLE: alt woman
    ('alt+w', r'^\s*(alt|ald)\s*\+?\s*w(oman|frau)?\s*$', 20, _common_meta_NO_on_match_exec),

    # alt+ I = select infrantrie






    # EXAMPLE: alt Spearman
    ('alt+p', r'^\s*(alt|ald)\s*\+?\s*p(ikeman|spearman|fanatic|lanzenkämpfer)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ C = Cavalry

    # EXAMPLE: alt Cavalry
    ('alt+c', r'^\s*(alt|ald)\s*\+?\s*c(avalry|kavallerie)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ A = Archer, Elephant&Archer, Slinger Javelineer, ... (Gruppe von Fernkämpfern)

    # EXAMPLE: alt slinger
    ('alt+a', r'^\s*(alt|ald)\s*\+?\s*a(rcher|slinger|javelineer|bogenschütze|fernkämpfer)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+ S = Swordman , ..

    # EXAMPLE: alt Swordman
    ('alt+s', r'^\s*(alt|ald)\s*\+?\s*s(wordman|schwertkämpfer)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ E = Elephant for Support

    # EXAMPLE: alt elephant
    ('alt+e', r'^\s*(alt|ald)\s*\+?\s*e(lefant|elephant|unterstützung)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ K = Catapult (exceptions because of conflict)

    # EXAMPLE: alt katapult
    ('alt+k', r'^\s*(alt|ald)\s*\+?\s*k(atapult|catapult)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ H = Healer

    # EXAMPLE: alt heiler
    ('alt+h', r'^\s*(alt|ald)\s*\+?\s*h(ealer|heiler)?\s*$', 20, _common_meta_NO_on_match_exec),
    # J = wounded (exceptions because near Healer)

    # EXAMPLE: wounded
    ('j', r'^\s*j(wounded|verwundete)?\s*$', 20, _common_meta_NO_on_match_exec), # J for 'injured' or 'jawunded'
    # k = selects only nowoundedonly using mouse

    # EXAMPLE: nowoundedonly
    ('k', r'^\s*k(nowoundedonly|nicht\s*verwundete)?\s*$', 20, _common_meta_NO_on_match_exec), # K for 'kept' or 'klar'
    # ... weitere Einheitenwahl-Befehle


    # Alt+ D = Dangerous Elephants (D. archer-,war-,hero-Elephant,... not Support&Elephant)

    # EXAMPLE: alt d dangerous elephants
    ('alt+d', r'^\s*(alt|ald)\s*\+?\s*d(angerous\s*elephants|gefährliche\s*elefanten)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ V = Siege and Ministers (Siege: rams, not heros, Catapult, Bolt Shooter, Siege Tower ...)

    # EXAMPLE: alt v siege
    ('alt+v', r'^\s*(alt|ald)\s*\+?\s*v(siege|minister|belagerung|minister)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ M, Alt+X = select all military ( nowoundedonly )
    # Hier könnte man zwei Einträge machen, je nachdem, welche Transkription wahrscheinlicher ist

    # (baue auf|baue|power|our|build|\w+ild)

    # EXAMPLE: alt military
    ('alt+x', r'^(alt|ald)\s*\+?\s*m(ilit|ilit|m|x)\w+$', 20, _common_meta_NO_on_match_exec),

    # militär

    # EXAMPLE: alt military
    ('alt+x', r'^{select}?(\w*ilit\w*)$', 20, _common_meta_NO_on_match_exec),

    # EXAMPLE: alt military
    ('alt+x', r'^\s*(alt|ald)\s*\+?\s*x(militär|military|alle\s*militärs)?\s*$', 20, _common_meta_NO_on_match_exec), # Alternative für X, falls es sich auf Militär bezieht
    # Alt+ N = select all non military

    # EXAMPLE: alt n nicht militar

    # EXAMPLE: alt n non military
    # ('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*military|nicht\s*militär|zivilisten)?\s*$', 20, _common_meta),

    # EXAMPLE: alles markieren
    ('ctrl+alt', r'^(alle\w* ma\w+).*$', 85, _common_meta),

    # EXAMPLE: alt infantry
    # ('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ P = select Pikeman, Spearman, Fanatic (Gruppe von Lanzenkämpfern/Nahkämpfern)

    # EXAMPLE: Infanterie
    ('select_infantry', fr'^{select}?{infanterie}$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: speertraeger
    ('select_pikemen', r'^{select}?(speertr[äa]ger|pikentr[äa]ger|phalanx|pikemen)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: kavallerie
    ('select_cavalry', r'^{select}?(kavallerie|reiter|reiterei|cavalry)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: bogenschuetzen
    ('select_archers', r'^{select}?(bogensch[üu]tzen|sch[üu]tzen|pl[äa]nkler|archers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: schwertkaempfer
    ('select_swordsmen', r'^{select}?(schwertk[äae]+mpfer|schwerter|swordsmen)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: elefanten
    ('select_elephants', r'^{select}?(elefanten|elefant|elephants)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: katapulte
    ('select_catapults', r'^{select}?(katapulte|katapult|belagerung|catapults)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: heiler
    ('select_healers', r'^{select}?(heiler|priester|healers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]


