# config/maps/plugins/game/0ad2/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# Auto-generated 0 A.D. Hotkeys

place = "(baue|errichte|platziere|build|place|bau|paul)"
select = "(select|auswählen|markieren|fokus|fokussiert|focus|fokussiere)"

# place s barracks

FUZZY_MAP_pre = [
    # EXAMPLE: place k
    ('K', fr"^{place}\s*(k|nowoundedonly)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place arsenal
    ('A', fr"^{place}\s*(arsenal|a)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place barracks
    ('B', fr"^{place}\s*(barracks|b|kaserne)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place zivil_zentrum
    ('C', fr"^{place}\s*(zivil_zentrum|c|civil_centre)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place k
    ('K', fr"^{place}\s*(k|corral|korral)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place defense_tower
    ('D', fr"^{place}\s*(defense_tower|verteidigungsturm|d)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place e
    ('E', fr"^{place}\s*(e|elephant_stables)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place f
    ('F', fr"^{place}\s*(f|feld|field)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place n
    ('N', fr"^{place}\s*(n|forge|schmiede)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place textaus
    ('h', fr"^{place}\s*(\w+aus|bauhaus|h|haus|house|\w*aus)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place markt
    ('M', fr"^{place}\s*(markt|m|market)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place v
    ('V', fr"^{place}\s*(v|stable|stabil)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place s
    ('S', fr"^{place}\s*(s|lagerhaus|storehouse)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place t
    ('T', fr"^{place}\s*(t|temple|tempel)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place wallset_siege
    ('U', fr"^{place}\s*(wallset_siege|u)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place wallset_stone
    ('W', fr"^{place}\s*(wallset_stone|w)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arsenal)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|armycamp|armeelager)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|assembly|montage)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select amphitheaterpompeii
    ('Ctrl+A', fr"^{select}?\s*(amphitheaterpompeii|amphitheater pompeji|ctrl+a)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|zuschreibung|apadana)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arch|bogen)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select barracks
    ('Ctrl+X', fr"^{select}?\s*(barracks|ctrl+x|kaserne)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|elephantstable|elefantenstall)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|stable|stabil)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select festung
    ('Ctrl+X', fr"^{select}?\s*(festung|ctrl+x|fortress)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select militärkolonie
    ('Ctrl+X', fr"^{select}?\s*(militärkolonie|ctrl+x|militarycolony)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|arsenal)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl x
    ('Ctrl+X', fr"^{select}?\s*(ctrl+x|armycamp|armeelager)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select catapult
    ('Alt+K', fr"^{select}?\s*(catapult|katapult|alt+k)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select zentrum
    ('Ctrl+C', fr"^{select}?\s*(zentrum|cc|ctrl+c|zivilzentrum|dorfzentrum|civilcentre)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl c
    ('Ctrl+C', fr"^{select}?\s*(ctrl+c|corral|korral)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ritze
    ('Ctrl+C', fr"^{select}?\s*(ritze|ctrl+c|crannog)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl f
    ('Ctrl+F', fr"^{select}?\s*(ctrl+f|farmstead|bauernhof)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl f
    ('Ctrl+F', fr"^{select}?\s*(ctrl+f|forge|schmiede)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select festung
    ('Ctrl+F', fr"^{select}?\s*(festung|ctrl+f|fortress)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select library
    ('Ctrl+L', fr"^{select}?\s*(library|ctrl+l|bibliothek)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select markt
    ('Ctrl+M', fr"^{select}?\s*(markt|market|ctrl+m)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select militärkolonie
    ('Ctrl+M', fr"^{select}?\s*(militärkolonie|ctrl+m|militarycolony)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|lagerhaus|storehouse)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|ship|schiff)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|stable|stabil)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|elephantstable|elefantenstall)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|farmstead|bauernhof)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|forge|schmiede)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl s
    ('Ctrl+S', fr"^{select}?\s*(ctrl+s|dock)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select alt c
    ('Alt+C', fr"^{select}?\s*(alt+c|kavallerie|cavalry)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select healer
    ('Alt+H', fr"^{select}?\s*(healer|heiler|alt+h)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select infanterie
    ('Alt+I', fr"^{select}?\s*(infanterie|alt+i|infantry)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select alt v
    ('Alt+V', fr"^{select}?\s*(alt+v|minister)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place j
    ('J', fr"^{place}\s*(j|kavallerie|cavalry)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place infanterie
    ('J', fr"^{place}\s*(infanterie|j|infantry)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place soldat
    ('J', fr"^{place}\s*(soldat|soldier|j)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place siege
    ('J', fr"^{place}\s*(siege|belagerung|j)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place hund
    ('J', fr"^{place}\s*(hund|dog|j)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place elephant
    ('J', fr"^{place}\s*(elephant|j|elefant)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place unterstützung
    ('J', fr"^{place}\s*(unterstützung|j|support)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl a
    ('Ctrl+A', fr"^{select}?\s*(ctrl+a|arsenal)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select barracks
    ('Ctrl+B', fr"^{select}?\s*(barracks|ctrl+b|kaserne)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select zivil_zentrum
    ('Ctrl+C', fr"^{select}?\s*(zivil_zentrum|ctrl+c|civil_centre)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl k
    ('Ctrl+K', fr"^{select}?\s*(ctrl+k|corral|korral)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select defense_tower
    ('Ctrl+D', fr"^{select}?\s*(defense_tower|verteidigungsturm|ctrl+d)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl j
    ('Ctrl+J', fr"^{select}?\s*(ctrl+j|dock)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl e
    ('Ctrl+E', fr"^{select}?\s*(ctrl+e|elephant_stables)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl g
    ('Ctrl+G', fr"^{select}?\s*(ctrl+g|farmstead|bauernhof)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl shift f
    ('Ctrl+Shift+F', fr"^{select}?\s*(ctrl+shift+f|feld|field)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select forge
    ('Ctrl+N', fr"^{select}?\s*(forge|schmiede|ctrl+n)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select festung
    ('Ctrl+R', fr"^{select}?\s*(festung|ctrl+r|fortress)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl h
    ('Ctrl+H', fr"^{select}?\s*(ctrl+h|b\w+aus|bauhaus|haus|house|\w?aus)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select markt
    ('Ctrl+M', fr"^{select}?\s*(markt|market|ctrl+m)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl o
    ('Ctrl+O', fr"^{select}?\s*(ctrl+o|outpost|vorposten)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl y
    ('Ctrl+Y', fr"^{select}?\s*(ctrl+y|sentry_tower)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select ctrl z
    ('Ctrl+Z', fr"^{select}?\s*(ctrl+z|stable|stabil)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select lagerhaus
    ('Ctrl+V', fr"^{select}?\s*(lagerhaus|ctrl+v|storehouse)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select temple
    ('Ctrl+T', fr"^{select}?\s*(temple|ctrl+t|tempel)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: select wunder
    ('Ctrl+W', fr"^{select}?\s*(wunder|wonder|ctrl+w)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place ortsfundament
    ('farmstead', fr"^{place}\s*(ortsfundament|placefoundation|farmstead)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),
    # EXAMPLE: place femalecitizen
    ('FemaleCitizen', fr"^{place}\s*(femalecitizen|einheiten auswählen|selectunits)\w*$", 20, {'flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD']}),

]
#