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

from scripts.py.func.get_project_root import get_aura_project_root
import platform
import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


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


    # Seau à citrouilleSyltkorrekt aussi

    # EXAMPLE: bloc de chaos

    ('https://pad.ccc-mannheim.de/p/1', r'^(chaos)\w*\s+.*tampon.*$', 60,
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chaos x Tübingen

    ('https://pad.cttue.de/1', r'^(chaos)\w*\s+.*Tübingen.*$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    #################################################
    # 2. activez cette règle (derrière la première pluie que vous souhaitez optimiser)


    #################################################


    # EXAMPLE: chaos

    ('https://cttue.de',
     r'^(chaos|Gris|Charles|dehors) (rencontrer|coups) (Tübingen|taper)\s*\w*$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chaos

    ('https://cttue.de/doku.php?id=start#was_ansteht',
     r'^(chaos|Charles)\s+.*Quoi.*à.*$', 60, {'command_flags': re.IGNORECASE}),









    # EXAMPLE: chaos

    ('https://pad.cttue.de/cttue-meta#', r'^(chaos|Charles)\w*\s+.*Procès-verbaux de réunion.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: chaos

    ('https://cttue.de/doku.php?id=events:past', r'^(chaos|Charles)\s+.* \bComp.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Fred Vettel

    ('06.03.-08.03.2026 Uni Stuttgart selfnet.de/uplink INCO guserav Selfnet e.V. Mastodon', r'^(Stuttgart|Réseau personnel|mastodonte)(\s*\w*\s*\b)(Stuttgart|ccc)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # https://events.ccc.de/congress/2025/hub/de/wiki/event-vorstellungen



    # EXAMPLE: Fred Vettel

    ('https://ki-maker.space/', r'^(fred|graisse|vettel)(\s*\w*\s*\b)(Tübingen|taper)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: ateliers de cours fred

    ('https://ki-maker.space/angebote/kurse-und-workshops', r'^(ki|fred|graisse|vettel)(\s*\w*\s*\b)(Tübingen|taper).*(Cours|ateliers)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Livre Python

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Livre)$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: carte de rue ouverte

    (r'https://www.carte de rue ouverte.org/nœud/9879183939',
     r'^carte de rue ouverte$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE})

]

