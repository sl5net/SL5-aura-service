# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

FUZZY_MAP_pre = [

    # EXAMPLE: select iddle
    ('select iddle', r'^\s*(select|selbst|schlägt)\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: select iddle
    ('select iddle', r'^\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: seltext woman
    ('alt+w', r'^\s*(sel\w+\s*w+|\w+\s*wo|\w+\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # ctrl+ h = select house
    # EXAMPLE: select house
    ('ctrl+h', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*h(ouse)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # ctrl+ m = select markt
    # EXAMPLE: select markt
    ('ctrl+m', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*m(arkt|market)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ctrl+ b = select barrack

    # EXAMPLE: control barack
    ('ctrl+b', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*b(aracke|barrack)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ctrl+ f = select farm

    # EXAMPLE: farm
    ('ctrl+f', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*f(arm)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Ctrl+ s = select Storehouse Ship Stable ElephantStable Dock ... (umfasst mehrere)

    # EXAMPLE: control Storehouse
    ('ctrl+s', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*s(torehouse|ship|stable|elephant\s*stable|dock|gebäude)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Ctrl+ X = select Barracks + ElephantStable + Stable (nearly everything)

    # EXAMPLE: control alles
    ('ctrl+x', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*x(alles|gebäude)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ... weitere Gebäudewahl-Befehle


    # EXAMPLE: alt woman
    ('alt+w', r'^\s*(alt|ald)\s*\+?\s*w(oman|frau)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # alt+ I = select infrantrie

    # EXAMPLE: alt infantry
    ('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ P = select Pikeman, Spearman, Fanatic (Gruppe von Lanzenkämpfern/Nahkämpfern)

    # EXAMPLE: alt Spearman
    ('alt+p', r'^\s*(alt|ald)\s*\+?\s*p(ikeman|spearman|fanatic|lanzenkämpfer)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ C = Cavalry

    # EXAMPLE: alt Cavalry
    ('alt+c', r'^\s*(alt|ald)\s*\+?\s*c(avalry|kavallerie)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ A = Archer, Elephant&Archer, Slinger Javelineer, ... (Gruppe von Fernkämpfern)

    # EXAMPLE: alt slinger
    ('alt+a', r'^\s*(alt|ald)\s*\+?\s*a(rcher|slinger|javelineer|bogenschütze|fernkämpfer)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # Alt+ S = Swordman , ..

    # EXAMPLE: alt Swordman
    ('alt+s', r'^\s*(alt|ald)\s*\+?\s*s(wordman|schwertkämpfer)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ E = Elephant for Support

    # EXAMPLE: alt elephant
    ('alt+e', r'^\s*(alt|ald)\s*\+?\s*e(lefant|elephant|unterstützung)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ K = Catapult (exceptions because of conflict)

    # EXAMPLE: alt katapult
    ('alt+k', r'^\s*(alt|ald)\s*\+?\s*k(atapult|catapult)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ H = Healer

    # EXAMPLE: alt heiler
    ('alt+h', r'^\s*(alt|ald)\s*\+?\s*h(ealer|heiler)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # J = wounded (exceptions because near Healer)

    # EXAMPLE: wounded
    ('j', r'^\s*j(wounded|verwundete)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}), # J for 'injured' or 'jawunded'
    # k = selects only nowoundedonly using mouse

    # EXAMPLE: nowoundedonly
    ('k', r'^\s*k(nowoundedonly|nicht\s*verwundete)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}), # K for 'kept' or 'klar'
    # ... weitere Einheitenwahl-Befehle


    # Alt+ D = Dangerous Elephants (D. archer-,war-,hero-Elephant,... not Support&Elephant)

    # EXAMPLE: alt d dangerous elephants
    ('alt+d', r'^\s*(alt|ald)\s*\+?\s*d(angerous\s*elephants|gefährliche\s*elefanten)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ V = Siege and Ministers (Siege: rams, not heros, Catapult, Bolt Shooter, Siege Tower ...)

    # EXAMPLE: alt v siege
    ('alt+v', r'^\s*(alt|ald)\s*\+?\s*v(siege|minister|belagerung|minister)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # Alt+ M, Alt+X = select all military ( nowoundedonly )
    # Hier könnte man zwei Einträge machen, je nachdem, welche Transkription wahrscheinlicher ist

    # (baue auf|baue|power|our|build|\w+ild)

    # EXAMPLE: alt military
    ('alt+m', r'^\s*(alt|ald)\s*\+?\s*m(ilitär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: alt military
    ('alt+x_military', r'^\s*(alt|ald)\s*\+?\s*x(militär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}), # Alternative für X, falls es sich auf Militär bezieht
    # Alt+ N = select all non military

    # EXAMPLE: alt n nicht militar

    # EXAMPLE: alt n non military
    ('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*military|nicht\s*militär|zivilisten)?\s*$', 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


]
