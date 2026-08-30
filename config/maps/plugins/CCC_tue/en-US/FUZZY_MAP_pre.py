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

# config/maps/plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import platform
import re

from scripts.py.func.get_project_root import get_aura_project_root

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


"""
Tübingen OpenLab https://ki-maker.space/angebote/open-lab
Öffnungszeiten:
Donnerstag: 11 - 22 Uhr
Freitag: 11 - 18 Uhr
Samstag: 10 - 18 Uhr
KI-Makerspace - Geschwister-Scholl-Platz - 72074 Tübingen - hallo  ki-maker.space - ki-maker.space

https://ki-maker.space/team

https://gitlab.com/kimakerspace

FabLab In Bahnhofsnähe
Wltes-Simon-Straße 4, Tübingen (Nahe Reutlinger Straße)
https://www.openstreetmap.org/node/9879183939

"""
from pathlib import Path

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


FUZZY_MAP_pre = [


    # Pumpkin bucketSyltkorrekt as well

    # EXAMPLE: chaos pad

    ('https://pad.ccc-mannheim.de/p/1', r'^(chaos)\w*\s+.*pad.*$', 60,
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chaos x Tübingen

    ('https://pad.cttue.de/1', r'^(chaos)\w*\s+.*Tübingen.*$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    #################################################
    # 2. activate this rule (behind the first rain you want to optimize)


    #################################################


    # EXAMPLE: chaos

    ('https://cttue.de',
     r'^(chaos|Grey|Charles|out) (meet|hits) (Tübingen|type)\s*\w*$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chaos

    ('https://cttue.de/doku.php?id=start#was_ansteht',
     r'^(chaos|Charles)\s+.*What.*to.*$', 60, {'command_flags': re.IGNORECASE}),









    # EXAMPLE: chaos

    ('https://pad.cttue.de/cttue-meta#', r'^(chaos|Charles)\w*\s+.*Meeting minutes.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: chaos

    ('https://cttue.de/doku.php?id=events:past', r'^(chaos|Charles)\s+.* \bComp.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Fred Vettel

    ('06.03.-08.03.2026 Uni Stuttgart selfnet.de/uplink INCO guserav Selfnet e.V. Mastodon', r'^(Stuttgart|Selfnet|mastodon)(\s*\w*\s*\b)(Stuttgart|ccc)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # https://events.ccc.de/congress/2025/hub/de/wiki/event-vorstellungen



    # EXAMPLE: Fred Vettel

    ('https://ki-maker.space/', r'^(fred|fat|vettel)(\s*\w*\s*\b)(Tübingen|type)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: fred courses workshops

    ('https://ki-maker.space/angebote/kurse-und-workshops', r'^(ki|fred|fat|vettel)(\s*\w*\s*\b)(Tübingen|type).*(Courses|workshops)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Python book

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Book)$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: openstreetmap

    (r'https://www.openstreetmap.org/node/9879183939',
     r'^openstreetmap$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE})

]

