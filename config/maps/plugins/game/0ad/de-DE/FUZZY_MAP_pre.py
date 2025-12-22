# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401


# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.
    # power house
    #   our house
    #  Wildhaus

    # EXAMPLE: baue Haus
    ('baue Haus', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(\w*aus|House)\s*$', 15, {'flags': re.IGNORECASE}),

    # EXAMPLE: baue feld
    ('f', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(fehlt|field|feld)\s*$', 15, {'flags': re.IGNORECASE}),

    # EXAMPLE: baue Lagerhaus
    ('baue Lagerhaus', r'^\s*(\w+au\w+|baue|power|our|build|\w+ild)\s*(\w*lager|Storeh)\w*\s*$', 15, {'flags': re.IGNORECASE}),



    # EXAMPLE: baue Baracke
    ('baue Baracke', r'^\s*(baue|baue|Build)\s+(Ba\w+)$', 15, {'flags': re.IGNORECASE}),

    # EXAMPLE: baue Baracke
    ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 15, {'flags': re.IGNORECASE}),

    # EXAMPLE: baue Baracke
    ('baue Baracke', r'^\s*(\w+au\w+|build|wild|bild)\s+([pb]a[rc]\w+)$', 15, {'flags': re.IGNORECASE}),




    #  selects Verwaltung

    # EXAMPLE: controll c
    ('ctrl+c', r'^\s*\w*([kc]ontroll\w*) c.*$', 20, {'flags': re.IGNORECASE}),
    # EXAMPLE: Verwaltunghaus
    ('ctrl+c', r'^\s*\w*(kontrollzwecken|Verwaltung\w+)$', 20, {'flags': re.IGNORECASE}),

    # EXAMPLE: select  infrantrie
    ('alt+i', r'^\s*(alt\s*e|alt\s*i|ald\s*i|select in).*\s*$', 20, {'flags': re.IGNORECASE}),


    # select iddle workwer
    # select it works
    # selbst edel Burg
    # schlägt edel burg
    # select edel wort
    # selbst edel
    # select edle burke

    # EXAMPLE: select iddle
    ('select iddle', r'^\s*(select|selbst|schlägt)\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE}),

    # EXAMPLE: select iddle
    ('select iddle', r'^\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE}),

    # select women
    # select woman select wimmeln
    # selbst wo man
    # select wümme
    # select wirbeln
    # EXAMPLE: seltext woman
    ('alt+w', r'^\s*(sel\w+\s*w+|\w+\s*wo|\w+\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*$', 20, {'flags': re.IGNORECASE}),


# EXAMPLE: baue hause
('baue Haus', r'^\s*(baue\s*h?aus|bau\s*h?aus|h?aus\s*bauen|build\s*h?ouse|house)\s*$', 15, {'flags': re.IGNORECASE}),


# EXAMPLE: build markt
('m', r'^\s*(baue\s*markt|bau\s*markt|markt\s*bauen|build\s*market|market)\s*$', 15, {'flags': re.IGNORECASE}),

# build barrack
# ('b', r'^\s*(baue\s*baracke|bau\s*baracke|baracke\s*bauen|build\s*barrack|barrack|barack)\s*$', 15, {'flags': re.IGNORECASE}),
# build farm

# EXAMPLE: baue farm
('f', r'^\s*(baue\s*farm|bau\s*farm|farm\s*bauen|build\s*farm|farm)\s*$', 15, {'flags': re.IGNORECASE}),
# build farmstead (zwei Farmen)

# EXAMPLE: baue farmstead
('f,f', r'^\s*(baue\s*farmstead|bau\s*farmstead|farmstead\s*bauen|build\s*farmstead|farmstead|zwei\s*farmen)\s*$', 15, {'flags': re.IGNORECASE}),
# build fortress (drei Farmen)

# EXAMPLE: baue festung
('f,f,f', r'^\s*(baue\s*festung|bau\s*festung|festung\s*bauen|build\s*fortress|fortress|drei\s*farmen)\s*$', 15, {'flags': re.IGNORECASE}),
# ... weitere Bau-Befehle nach diesem Muster

# ctrl+ h = select house
# EXAMPLE: select house
('ctrl+h', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*h(ouse)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ m = select markt
# EXAMPLE: select markt
('ctrl+m', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*m(arkt|market)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ b = select barrack


# EXAMPLE: control barack
('ctrl+b', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*b(aracke|barrack)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ f = select farm

# EXAMPLE: farm
('ctrl+f', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*f(arm)?\s*$', 20, {'flags': re.IGNORECASE}),
# Ctrl+ s = select Storehouse Ship Stable ElephantStable Dock ... (umfasst mehrere)

# EXAMPLE: control Storehouse
('ctrl+s', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*s(torehouse|ship|stable|elephant\s*stable|dock|gebäude)?\s*$', 20, {'flags': re.IGNORECASE}),
# Ctrl+ X = select Barracks + ElephantStable + Stable (nearly everything)

# EXAMPLE: control alles
('ctrl+x', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*x(alles|gebäude)?\s*$', 20, {'flags': re.IGNORECASE}),
# ... weitere Gebäudewahl-Befehle


# alt+ W = select woman

# EXAMPLE: alt woman
('alt+w', r'^\s*(alt|ald)\s*\+?\s*w(oman|frau)?\s*$', 20, {'flags': re.IGNORECASE}),
# alt+ I = select infrantrie

# EXAMPLE: alt infantry
('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ P = select Pikeman, Spearman, Fanatic (Gruppe von Lanzenkämpfern/Nahkämpfern)

# EXAMPLE: alt Spearman
('alt+p', r'^\s*(alt|ald)\s*\+?\s*p(ikeman|spearman|fanatic|lanzenkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ C = Cavalry

# EXAMPLE: s alt Cavalry
('alt+c', r'^\s*(alt|ald)\s*\+?\s*c(avalry|kavallerie)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ A = Archer, Elephant&Archer, Slinger Javelineer, ... (Gruppe von Fernkämpfern)

# EXAMPLE: alt slinger
('alt+a', r'^\s*(alt|ald)\s*\+?\s*a(rcher|slinger|javelineer|bogenschütze|fernkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),

# Alt+ S = Swordman , ..

# EXAMPLE: alt Swordman
('alt+s', r'^\s*(alt|ald)\s*\+?\s*s(wordman|schwertkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ E = Elephant for Support

# EXAMPLE: alt elephant
('alt+e', r'^\s*(alt|ald)\s*\+?\s*e(lefant|elephant|unterstützung)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ K = Catapult (exceptions because of conflict)

# EXAMPLE: alt katapult
('alt+k', r'^\s*(alt|ald)\s*\+?\s*k(atapult|catapult)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ H = Healer

# EXAMPLE: alt heiler
('alt+h', r'^\s*(alt|ald)\s*\+?\s*h(ealer|heiler)?\s*$', 20, {'flags': re.IGNORECASE}),
# J = wounded (exceptions because near Healer)

# EXAMPLE: wounded
('j', r'^\s*j(wounded|verwundete)?\s*$', 20, {'flags': re.IGNORECASE}), # J for 'injured' or 'jawunded'
# k = selects only nowoundedonly using mouse

# EXAMPLE: nowoundedonly
('k', r'^\s*k(nowoundedonly|nicht\s*verwundete)?\s*$', 20, {'flags': re.IGNORECASE}), # K for 'kept' or 'klar'
# ... weitere Einheitenwahl-Befehle


# Alt+ D = Dangerous Elephants (D. archer-,war-,hero-Elephant,... not Support&Elephant)

# EXAMPLE: alt d dangerous elephants
('alt+d', r'^\s*(alt|ald)\s*\+?\s*d(angerous\s*elephants|gefährliche\s*elefanten)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ V = Siege and Ministers (Siege: rams, not heros, Catapult, Bolt Shooter, Siege Tower ...)

# EXAMPLE: alt v siege
('alt+v', r'^\s*(alt|ald)\s*\+?\s*v(siege|minister|belagerung|minister)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ M, Alt+X = select all military ( nowoundedonly )
# Hier könnte man zwei Einträge machen, je nachdem, welche Transkription wahrscheinlicher ist


#  Baue Markt funktioniert noch nicht so gut.
#  Datum: 3.10.'25 Fri

# (baue auf|baue|power|our|build|\w+ild)

# EXAMPLE: alt military
('alt+m', r'^\s*(alt|ald)\s*\+?\s*m(ilitär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE}),

# EXAMPLE: alt military
('alt+x_military', r'^\s*(alt|ald)\s*\+?\s*x(militär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE}), # Alternative für X, falls es sich auf Militär bezieht
# Alt+ N = select all non military

# EXAMPLE: alt n nicht militar

# EXAMPLE: alt n non military
('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*military|nicht\s*militär|zivilisten)?\s*$', 20, {'flags': re.IGNORECASE}),
# ... weitere Sonderbefehle





]
