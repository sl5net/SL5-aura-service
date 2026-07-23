# config/maps/plugins/sikulix/fr-FR/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent
sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli', 'oculixide', 'OculiX']

FUZZY_MAP_pre = [
    #################################################
    # 2. activez cette règle (derrière la première règle que vous souhaitez optimiser)

    #################################################

    # EXAMPLE: double clic
    ('doubleClick("image.png")', r'^\s*(double\s*clic|double\s*cliquer?|double\s*cliquez|double\s*clics)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': ['sikulixide', 'SikuliX', 'oculixide', 'OculiX'],
    }),
    # EXAMPLE: clic droit
    ('rightClick("image.png")', r'^\s*(clic\s*droit|cliquer?\s*droit|cliquez\s*droit|droit\s*clic)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': ['sikulixide', 'SikuliX', 'oculixide', 'OculiX'],
    }),
    # EXAMPLE: clic
    ('click("image.png")', r'^\s*(clic|clique|cliquez|cliquer|clics)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': ['sikulixide', 'SikuliX', 'oculixide', 'OculiX'],
    }),
    # EXAMPLE: attend (wait)
    ('wait("image.png", 10)', r'^\s*(attend|attendre|attendez|pause|attente)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': ['sikulixide', 'SikuliX', 'oculixide', 'OculiX'],
    }),
    # EXAMPLE: tape (type)
    ('type("text")', r'^\s*(tape|taper|tapez|écris|écrire|écrivez|saisir|saisie)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': ['sikulixide', 'SikuliX', 'oculixide', 'OculiX'],
    }),


]
