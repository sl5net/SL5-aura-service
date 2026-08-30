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

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


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


    # Cubo de calabazaSyltkorrekt también

    # EXAMPLE: almohadilla del caos

    ('https://pad.ccc-mannheim.de/p/1', r'^(caos)\w*\s+.*almohadilla.*$', 60,
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: caos x Tubinga

    ('https://pad.cttue.de/1', r'^(caos)\w*\s+.*Tubinga.*$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    #################################################
    # 2. activa esta regla (después de la primera lluvia que deseas optimizar)


    #################################################


    # EXAMPLE: caos

    ('https://cttue.de',
     r'^(caos|Gris|carlos|afuera) (encontrarse|golpes) (Tubinga|tipo)\s*\w*$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: caos

    ('https://cttue.de/doku.php?id=start#was_ansteht',
     r'^(caos|carlos)\s+.*Qué.*a.*$', 60, {'command_flags': re.IGNORECASE}),









    # EXAMPLE: caos

    ('https://pad.cttue.de/cttue-meta#', r'^(caos|carlos)\w*\s+.*Actas de la reunión.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: caos

    ('https://cttue.de/doku.php?id=events:past', r'^(caos|carlos)\s+.* \bComp.*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Fred Vettel

    ('06.03.-08.03.2026 Uni Stuttgart selfnet.de/uplink INCO guserav Selfnet e.V. Mastodon', r'^(Stuttgart|autonet|mastodonte)(\s*\w*\s*\b)(Stuttgart|ccc)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # https://events.ccc.de/congress/2025/hub/de/wiki/event-vorstellungen



    # EXAMPLE: Fred Vettel

    ('https://ki-maker.space/', r'^(fred|gordo|vettel)(\s*\w*\s*\b)(Tubinga|tipo)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: fred cursos talleres

    ('https://ki-maker.space/angebote/kurse-und-workshops', r'^(ki|fred|gordo|vettel)(\s*\w*\s*\b)(Tubinga|tipo).*(Cursos|talleres)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: libro de pitón

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Libro)$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: mapa abierto de calles

    (r'https://www.mapa abierto de calles.organización/nodo/9879183939',
     r'^mapa abierto de calles$', 60, # min_accuracy
    {'command_flags': re.IGNORECASE})

]

