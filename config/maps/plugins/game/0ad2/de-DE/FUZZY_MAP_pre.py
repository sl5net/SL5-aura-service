# config/maps/plugins/game/0ad2/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# Auto-generated 0 A.D. Hotkeys

place = "(baue|errichte|platziere|build|place|bau|paul)"
select = "(select|auswählen|markieren|fokus|fokussiert|focus|fokussiere)"

# place s barracks

FUZZY_MAP_pre = [
    # EXAMPLE: place k
    ('K', fr"^{place}\s*(k|nowoundedonly)\w*$"),
    # EXAMPLE: place arsenal
    ('A', fr"^{place}\s*(arsenal|a)\w*$"),
    # EXAMPLE: place barracks
    ('B', fr"^{place}\s*(barracks|b|kaserne)\w*$"),
    # EXAMPLE: place zivil_zentrum
    ('C', fr"^{place}\s*(zivil_zentrum|c|civil_centre)\w*$"),
    # EXAMPLE: place k
    ('K', fr"^{place}\s*(k|corral|korral)\w*$"),
    # EXAMPLE: place defense_tower
    ('D', fr"^{place}\s*(defense_tower|verteidigungsturm|d)\w*$"),
    # EXAMPLE: place e
    ('E', fr"^{place}\s*(e|elephant_stables)\w*$"),
    # EXAMPLE: place f
    ('F', fr"^{place}\s*(f|feld|field)\w*$"),
    # EXAMPLE: place n
    ('N', fr"^{place}\s*(n|forge|schmiede)\w*$"),
    # EXAMPLE: place textaus
    ('h', fr"^{place}\s*(\w+aus|bauhaus|h|haus|house|\w*aus)\w*$"),
    # EXAMPLE: place markt
    ('M', fr"^{place}\s*(markt|m|market)\w*$"),
    # EXAMPLE: place v
    ('V', fr"^{place}\s*(v|stable|stabil)\w*$"),
    # EXAMPLE: place s
    ('S', fr"^{place}\s*(s|lagerhaus|storehouse)\w*$"),
    # EXAMPLE: place t
    ('T', fr"^{place}\s*(t|temple|tempel)\w*$"),
    # EXAMPLE: place wallset_siege
    ('U', fr"^{place}\s*(wallset_siege|u)\w*$"),
    # EXAMPLE: place wallset_stone
    ('W', fr"^{place}\s*(wallset_stone|w)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arsenal)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|armycamp|armeelager)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|assembly|montage)\w*$"),
    # EXAMPLE: select amphitheaterpompeii
    ('Ctrl+A', fr"^{select}?\s*(amphitheaterpompeii|amphitheater pompeji|ctrl+a)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|zuschreibung|apadana)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arch|bogen)\w*$"),
    # EXAMPLE: select barracks
    ('Ctrl+X', fr"^{select}?\s*(barracks|ctrl+x|kaserne)\w*$"),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|elephantstable|elefantenstall)\w*$"),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|stable|stabil)\w*$"),
    # EXAMPLE: select festung
    ('Ctrl+X', fr"^{select}?\s*(festung|ctrl+x|fortress)\w*$"),
    # EXAMPLE: select militärkolonie
    ('Ctrl+X', fr"^{select}?\s*(militärkolonie|ctrl+x|militarycolony)\w*$"),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|arsenal)\w*$"),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|armycamp|armeelager)\w*$"),
    # EXAMPLE: select catapult
    ('Alt+K', fr"^{select}?\s*(catapult|katapult|alt+k)\w*$"),
    # EXAMPLE: select zentrum
    ('Ctrl+C', fr"^{select}?\s*(zentrum|cc|ctrl+c|zivilzentrum|dorfzentrum|civilcentre)\w*$"),
    # EXAMPLE: select ctrl c
    ('Ctrl+C', fr"^{select}?\s*(ctrl+c|corral|korral)\w*$"),
    # EXAMPLE: select ritze
    ('Ctrl+C', fr"^{select}?\s*(ritze|ctrl+c|crannog)\w*$"),
    # EXAMPLE: select ctrl f
    ('Ctrl+F', fr"^{select}?\s*(ctrl+f|farmstead|bauernhof)\w*$"),
    # EXAMPLE: select ctrl f
    ('Ctrl+F', fr"^{select}?\s*(ctrl+f|forge|schmiede)\w*$"),
    # EXAMPLE: select festung
    ('Ctrl+F', fr"^{select}?\s*(festung|ctrl+f|fortress)\w*$"),
    # EXAMPLE: select library
    ('Ctrl+L', fr"^{select}?\s*(library|ctrl+l|bibliothek)\w*$"),
    # EXAMPLE: select markt
    ('Ctrl+M', fr"^{select}?\s*(markt|market|ctrl+m)\w*$"),
    # EXAMPLE: select militärkolonie
    ('Ctrl+M', fr"^{select}?\s*(militärkolonie|ctrl+m|militarycolony)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|lagerhaus|storehouse)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|ship|schiff)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|stable|stabil)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|elephantstable|elefantenstall)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|farmstead|bauernhof)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|forge|schmiede)\w*$"),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|dock)\w*$"),
    # EXAMPLE: select alt c
    ('Alt+C', fr"^{select}?\s*(alt+c|kavallerie|cavalry)\w*$"),
    # EXAMPLE: select healer
    ('Alt+H', fr"^{select}?\s*(healer|heiler|alt+h)\w*$"),
    # EXAMPLE: select infanterie
    ('Alt+I', fr"^{select}?\s*(infanterie|alt+i|infantry)\w*$"),
    # EXAMPLE: select alt v
    ('Alt+V', fr"^{select}?\s*(alt+v|minister)\w*$"),
    # EXAMPLE: place j
    ('J', fr"^{place}\s*(j|kavallerie|cavalry)\w*$"),
    # EXAMPLE: place infanterie
    ('J', fr"^{place}\s*(infanterie|j|infantry)\w*$"),
    # EXAMPLE: place soldat
    ('J', fr"^{place}\s*(soldat|soldier|j)\w*$"),
    # EXAMPLE: place siege
    ('J', fr"^{place}\s*(siege|belagerung|j)\w*$"),
    # EXAMPLE: place hund
    ('J', fr"^{place}\s*(hund|dog|j)\w*$"),
    # EXAMPLE: place elephant
    ('J', fr"^{place}\s*(elephant|j|elefant)\w*$"),
    # EXAMPLE: place unterstützung
    ('J', fr"^{place}\s*(unterstützung|j|support)\w*$"),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arsenal)\w*$"),
    # EXAMPLE: select barracks
    ('Ctrl+B', fr"^{select}?\s*(barracks|ctrl+b|kaserne)\w*$"),
    # EXAMPLE: select zivil_zentrum
    ('Ctrl+C', fr"^{select}?\s*(zivil_zentrum|ctrl+c|civil_centre)\w*$"),
    # EXAMPLE: select ctrl k
    ('Ctrl+K', fr"^{select}?\s*(ctrl+k|corral|korral)\w*$"),
    # EXAMPLE: select defense_tower
    ('Ctrl+D', fr"^{select}?\s*(defense_tower|verteidigungsturm|ctrl+d)\w*$"),
    # EXAMPLE: select ctrl j
    ('Ctrl+J', fr"^{select}?\s*(ctrl+j|dock)\w*$"),
    # EXAMPLE: select ctrl e
    ('Ctrl+E', fr"^{select}?\s*(ctrl+e|elephant_stables)\w*$"),
    # EXAMPLE: select ctrl g
    ('Ctrl+G', fr"^{select}?\s*(ctrl+g|farmstead|bauernhof)\w*$"),
    # EXAMPLE: select ctrl shift f
    ('Ctrl+Shift+F', fr"^{select}?\s*(ctrl+shift+f|feld|field)\w*$"),
    # EXAMPLE: select forge
    ('Ctrl+N', fr"^{select}?\s*(forge|schmiede|ctrl+n)\w*$"),
    # EXAMPLE: select festung
    ('Ctrl+R', fr"^{select}?\s*(festung|ctrl+r|fortress)\w*$"),
    # EXAMPLE: select ctrl h
    ('Ctrl+H', fr"^{select}?\s*(ctrl+h|b\w+aus|bauhaus|haus|house|\w?aus)\w*$"),
    # EXAMPLE: select markt
    ('Ctrl+M', fr"^{select}?\s*(markt|market|ctrl+m)\w*$"),
    # EXAMPLE: select ctrl o
    ('Ctrl+O', fr"^{select}?\s*(ctrl+o|outpost|vorposten)\w*$"),
    # EXAMPLE: select ctrl y
    ('Ctrl+Y', fr"^{select}?\s*(ctrl+y|sentry_tower)\w*$"),
    # EXAMPLE: select ctrl z
    ('Ctrl+Z', fr"^{select}?\s*(ctrl+z|stable|stabil)\w*$"),
    # EXAMPLE: select lagerhaus
    ('Ctrl+V', fr"^{select}?\s*(lagerhaus|ctrl+v|storehouse)\w*$"),
    # EXAMPLE: select temple
    ('Ctrl+T', fr"^{select}?\s*(temple|ctrl+t|tempel)\w*$"),
    # EXAMPLE: select wunder
    ('Ctrl+W', fr"^{select}?\s*(wunder|wonder|ctrl+w)\w*$"),
    # EXAMPLE: place ortsfundament
    ('farmstead', fr"^{place}\s*(ortsfundament|placefoundation|farmstead)\w*$"),
    # EXAMPLE: place femalecitizen
    ('FemaleCitizen', fr"^{place}\s*(femalecitizen|einheiten auswählen|selectunits)\w*$"),
]
