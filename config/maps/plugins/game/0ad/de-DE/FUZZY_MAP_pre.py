# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pr.py
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

    # EXAMPLE: s baue
    ('baue Haus', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(\w*aus|House)\s*$', 15, {'flags': re.IGNORECASE}),

    # bild fehlt
    # EXAMPLE: s baue
    ('f', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(fehlt|field|feld)\s*$', 15, {'flags': re.IGNORECASE}),

    # frau
    # paul lagerer
    # baue Lagerhaus
    # EXAMPLE: s textautext
    ('baue Lagerhaus', r'^\s*(\w+au\w+|baue|power|our|build|\w+ild)\s*(\w*lager|Storeh)\w*\s*$', 15, {'flags': re.IGNORECASE}),



    # EXAMPLE: s baue
    ('baue Baracke', r'^\s*(baue|baue|Build)\s+(Ba\w+)$', 15, {'flags': re.IGNORECASE}),

    # EXAMPLE: s textautext
    ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 15, {'flags': re.IGNORECASE}),

    # wild backen
    # bild parat

    # EXAMPLE: s textautext
    ('baue Baracke', r'^\s*(\w+au\w+|build|wild|bild)\s+([pb]a[rc]\w+)$', 15, {'flags': re.IGNORECASE}),




    #  selects Verwaltung

    # EXAMPLE: s x kc ontrollx c...
    ('ctrl+c', r'^\s*\w*([kc]ontroll\w*) c.*$', 20, {'flags': re.IGNORECASE}),
    # EXAMPLE: s x kontrollzwecken
    ('ctrl+c', r'^\s*\w*(kontrollzwecken|Verwaltung\w+)$', 20, {'flags': re.IGNORECASE}),

    # select  infrantrie

    # EXAMPLE: s alt s e
    ('alt+i', r'^\s*(alt\s*e|alt\s*i|ald\s*i|select in).*\s*$', 20, {'flags': re.IGNORECASE}),


    # select iddle workwer
    # select it works
    # selbst edel Burg
    # schlägt edel burg
    # select edel wort
    # selbst edel
    # select edle burke

    # EXAMPLE: s select
    ('select iddle', r'^\s*(select|selbst|schlägt)\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE}),

    # Edel Yorkers
    # EXAMPLE: s edel
    ('select iddle', r'^\s*(edel|i[dts]).*$', 20, {'flags': re.IGNORECASE}),

    # select women
    # select woman select wimmeln
    # selbst wo man
    # select wümme
    # select wirbeln
    # EXAMPLE: s seltext s w
    ('alt+w', r'^\s*(sel\w+\s*w+|\w+\s*wo|\w+\s*fr|alt\s*w|alt\s*wo|alt\s*fr|ald\s*women).*$', 20, {'flags': re.IGNORECASE}),



# build house
# EXAMPLE: s baue s h aus
('baue Haus', r'^\s*(baue\s*h?aus|bau\s*h?aus|h?aus\s*bauen|build\s*h?ouse|house)\s*$', 15, {'flags': re.IGNORECASE}),
# build markt
# EXAMPLE: s baue s markt
('m', r'^\s*(baue\s*markt|bau\s*markt|markt\s*bauen|build\s*market|market)\s*$', 15, {'flags': re.IGNORECASE}),
# build barrack
# ('b', r'^\s*(baue\s*baracke|bau\s*baracke|baracke\s*bauen|build\s*barrack|barrack|barack)\s*$', 15, {'flags': re.IGNORECASE}),
# build farm
# EXAMPLE: s baue s farm
('f', r'^\s*(baue\s*farm|bau\s*farm|farm\s*bauen|build\s*farm|farm)\s*$', 15, {'flags': re.IGNORECASE}),
# build farmstead (zwei Farmen)
# EXAMPLE: s baue s farmstead
('f,f', r'^\s*(baue\s*farmstead|bau\s*farmstead|farmstead\s*bauen|build\s*farmstead|farmstead|zwei\s*farmen)\s*$', 15, {'flags': re.IGNORECASE}),
# build fortress (drei Farmen)
# EXAMPLE: s baue s festung
('f,f,f', r'^\s*(baue\s*festung|bau\s*festung|festung\s*bauen|build\s*fortress|fortress|drei\s*farmen)\s*$', 15, {'flags': re.IGNORECASE}),
# ... weitere Bau-Befehle nach diesem Muster

# ctrl+ h = select house
# EXAMPLE: s ctrl
('ctrl+h', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*h(ouse)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ m = select markt
# EXAMPLE: s ctrl
('ctrl+m', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*m(arkt|market)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ b = select barrack
# EXAMPLE: s ctrl
('ctrl+b', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*b(aracke|barrack)?\s*$', 20, {'flags': re.IGNORECASE}),
# ctrl+ f = select farm
# EXAMPLE: s ctrl
('ctrl+f', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*f(arm)?\s*$', 20, {'flags': re.IGNORECASE}),
# Ctrl+ s = select Storehouse Ship Stable ElephantStable Dock ... (umfasst mehrere)
# EXAMPLE: s ctrl
('ctrl+s', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*s(torehouse|ship|stable|elephant\s*stable|dock|gebäude)?\s*$', 20, {'flags': re.IGNORECASE}),
# Ctrl+ X = select Barracks + ElephantStable + Stable (nearly everything)
# EXAMPLE: s ctrl
('ctrl+x', r'^\s*(ctrl|control|kontroll|steuer)\s*\+?\s*x(alles|gebäude)?\s*$', 20, {'flags': re.IGNORECASE}),
# ... weitere Gebäudewahl-Befehle


# alt+ W = select woman
# EXAMPLE: s alt
('alt+w', r'^\s*(alt|ald)\s*\+?\s*w(oman|frau)?\s*$', 20, {'flags': re.IGNORECASE}),
# alt+ I = select infrantrie
# EXAMPLE: s alt
('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ P = select Pikeman, Spearman, Fanatic (Gruppe von Lanzenkämpfern/Nahkämpfern)
# EXAMPLE: s alt
('alt+p', r'^\s*(alt|ald)\s*\+?\s*p(ikeman|spearman|fanatic|lanzenkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ C = Cavalry
# EXAMPLE: s alt
('alt+c', r'^\s*(alt|ald)\s*\+?\s*c(avalry|kavallerie)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ A = Archer, Elephant&Archer, Slinger Javelineer, ... (Gruppe von Fernkämpfern)
# EXAMPLE: s alt
('alt+a', r'^\s*(alt|ald)\s*\+?\s*a(rcher|slinger|javelineer|bogenschütze|fernkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ S = Swordman , ..
# EXAMPLE: s alt
('alt+s', r'^\s*(alt|ald)\s*\+?\s*s(wordman|schwertkämpfer)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ E = Elephant for Support
# EXAMPLE: s alt
('alt+e', r'^\s*(alt|ald)\s*\+?\s*e(lefant|elephant|unterstützung)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ K = Catapult (exceptions because of conflict)
# EXAMPLE: s alt
('alt+k', r'^\s*(alt|ald)\s*\+?\s*k(atapult|catapult)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ H = Healer
# EXAMPLE: s alt
('alt+h', r'^\s*(alt|ald)\s*\+?\s*h(ealer|heiler)?\s*$', 20, {'flags': re.IGNORECASE}),
# J = wounded (exceptions because near Healer)
# EXAMPLE: s j wounded
('j', r'^\s*j(wounded|verwundete)?\s*$', 20, {'flags': re.IGNORECASE}), # J for 'injured' or 'jawunded'
# k = selects only nowoundedonly using mouse
# EXAMPLE: s k nowoundedonly
('k', r'^\s*k(nowoundedonly|nicht\s*verwundete)?\s*$', 20, {'flags': re.IGNORECASE}), # K for 'kept' or 'klar'
# ... weitere Einheitenwahl-Befehle


# Alt+ D = Dangerous Elephants (D. archer-,war-,hero-Elephant,... not Support&Elephant)
# EXAMPLE: s alt
('alt+d', r'^\s*(alt|ald)\s*\+?\s*d(angerous\s*elephants|gefährliche\s*elefanten)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ V = Siege and Ministers (Siege: rams, not heros, Catapult, Bolt Shooter, Siege Tower ...)
# EXAMPLE: s alt
('alt+v', r'^\s*(alt|ald)\s*\+?\s*v(siege|minister|belagerung|minister)?\s*$', 20, {'flags': re.IGNORECASE}),
# Alt+ M, Alt+X = select all military ( nowoundedonly )
# Hier könnte man zwei Einträge machen, je nachdem, welche Transkription wahrscheinlicher ist


#  Baue Markt funktioniert noch nicht so gut.
#  Datum: 3.10.'25 Fri

# (baue auf|baue|power|our|build|\w+ild)

# EXAMPLE: s alt
('alt+m', r'^\s*(alt|ald)\s*\+?\s*m(ilitär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE}),
# EXAMPLE: s alt
('alt+x_military', r'^\s*(alt|ald)\s*\+?\s*x(militär|military|alle\s*militärs)?\s*$', 20, {'flags': re.IGNORECASE}), # Alternative für X, falls es sich auf Militär bezieht
# Alt+ N = select all non military
# EXAMPLE: s alt
('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*military|nicht\s*militär|zivilisten)?\s*$', 20, {'flags': re.IGNORECASE}),
# ... weitere Sonderbefehle





]
