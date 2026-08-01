# config/maps/plugins/standard_actions/weather/de-DE/FUZZY_MAP_pre.py:1
import re # noqa: F401

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: wie wetter
    ('', r'^(wie\s*(?:ist|wird)?\s*(?:das)?\s*wetter( morgen)?|wie das wetter morgen|wie ist das fett|Die erhaltenen Wetterdaten hatten ein unerwartetes Format.|wie ist das bett|wie ist das etwa|mir ist das wetter|naechstes bild|wie ist das zwitschern|nicht das wetter|naechstes|wie ist das|wie ist es|naechstes we|lies es)$'
    , 95, {
             'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / '..' /  'weather.py'] # Passe den Pfad ggf. an
    }),

    # EXAMPLE: wie ist das wetter
    ('', r'^(wie (wird|ist|nächstes)\b.*\bwetter|wetterbericht|wettervorhersage)\??$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR /  '..' /  'weather.py']
    }),
]

