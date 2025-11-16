# config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py

import re # noqa: F401
from pathlib import Path

CONFIG_DIR = Path(__file__).parent # e.g., .../path_navigator/de-DE
# Calculate Project Root: Up 4 levels (de-DE -> path_navigator -> plugins -> maps -> config -> STT)
PROJECT_ROOT = CONFIG_DIR.parents[5]

# --- Path Commands ---
# We define the commands directly here, using the calculated PROJECT_ROOT.

FUZZY_MAP_pre = [
    # 1. Navigiere zu Aura Root
    # Command: 'cd /home/user/projects/py/STT'
    (f'cd {PROJECT_ROOT}',
     r'^(Navigiere zu\w*|Pfad zu|Path to|navi gerät)\s+(Aura|Root)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # 2. Navigiere zu Aura Config (Directory)
    # Command: 'cd /home/user/projects/py/STT/config'
    (f'cd {PROJECT_ROOT / "config"}',
     r'^(Navigiere zu\w*|Pfad zu|Path to|navi gerät)\s+Aura Konf\w*$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (f'kate {PROJECT_ROOT / "config" / "settings.py"}',
     r'^(Öffne\w*|Editiere)( \w+)?\s+Aura Einstellungen$',
     95,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #kate /home/seeh/projects/py/STT/config/settings_local.py

    (f'kate {PROJECT_ROOT / "config" / "settings_local.py"}',
     r'^(Öffne\w*|Editiere)( \w+)?\s+Aura (local\w*|lokal\w*)$',
     95,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # 4. Navigiere zu Maps Plugin Ordner
    # Command: 'cd /home/user/projects/py/STT/config/maps/plugins'
    (f'cd {PROJECT_ROOT / "config" / "maps" / "plugins"}',
     r'^(Navigiere zu|Pfad zu)\s+Maps Plugin$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (f'kate {PROJECT_ROOT / "log" / "dictation_service.log"}',
     r'^(öffne\w* look|öffne\w* log|Öffne\w* Look|öffnen luft)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (f'tail -f {PROJECT_ROOT / "log" / "dictation_service.log"}', r'\b(Follow Main Lo[gk]\w*|Folge Lo[gk]\w*|Zeige Lo[gk]\w*)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),



    #öffnenÖffne logÖffnen logdie die logkate /home/seeh/projects/py/STT/log/dictation_service.log

    # ... weitere Einträge
]

"""
cd /home/seeh/projects/py/STT/config

cd /home/seeh/projects/py/STT/config

cd /home/seeh/projects/py/STT/config
"""
    #cd /home/seeh/projects/py/STT/configNavigiere zu Mac Logincd /home/seeh/projects/py/STT/config/config/maps/plugins
