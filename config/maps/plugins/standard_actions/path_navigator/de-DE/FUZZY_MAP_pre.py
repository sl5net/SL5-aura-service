# config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py
import re # noqa: F401
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parents[5]

home_dir_str = str(Path.home())
project_root_str_full = str(PROJECT_ROOT)

PROJECT_ROOT_DISPLAY_STR = ''
# 1. Tilde Replacement (Only a String Operation!)
if project_root_str_full.startswith(home_dir_str):
    # This result will be a string like '~/projects/py/STT' (Linux) or '~\projects\py\STT' (Windows)
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full.replace(home_dir_str, '~', 1)
    print(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")
else:
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full
    print(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")

# 2. Use the SHELL-Display string, but manually join with the OS-Specific Separator (os.path.sep)
# This will be used in your f-string map actions.
PROJECT_ROOT_FOR_MAP = PROJECT_ROOT_DISPLAY_STR
print(f"PROJECT_ROOT_FOR_MAP: {PROJECT_ROOT_FOR_MAP}")

FUZZY_MAP_pre = [


    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensions 'py,sh,html' | xclip -selection cl

    # following search is best when inside a Git repository, this is the quickest and most effective way to exclude boilerplate (date that you not interested in)
    # https://junegunn.github.io/fzf/
    ("git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard",
     r'^(suche|search|find)\s+(file|datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # following works with fzf (highliy recomande to have, s.18.11.'25 09:00 Tue)
    # https://junegunn.github.io/fzf/
    ("fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl",
     r'^(suche|search|find)\s+(überall|everywhere)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl'


    (f'{PROJECT_ROOT_FOR_MAP}',
     r'^(Aura|Agora|Aurora|ora|hurra|Flora)\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # ~/projects/py/STT


    (f'{PROJECT_ROOT_FOR_MAP}',
     r'^(Raumfahrt)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # ~/projects/py/STT

    (f'{home_dir_str}',
     r'^(home|heimat|user)\s+(Pfad|Dir\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

#Navigiere zur Aura Da bin ich Rezo Aura

    # 2. Navigiere zu Aura Config (Directory)
    (f'cd {os.path.join(PROJECT_ROOT_FOR_MAP, "config")}',
    r'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+(Aura|Aurora|Root|Aurora)\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #cd ~/projects/py/STT/config cd ~/projects/py/STT/config

    # 2. Navigiere zu Aura (Directory)
    (f'cd {os.path.join(PROJECT_ROOT_FOR_MAP)}',
    r'^(Navigiere|Pfad|Path to|navi gerät)( zu\w*)?\s+(Aura|Aurora|Root|Aurora)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #cd ~/projects/py/STT

    # 2. Config (Directory)
    # konzentration is typoe sometimes so catch it:
    #Rover KunstAura KonfliktAura Konflikt/projects/py/STT/config
    # Laura Konflikt/projects/py/STT/config
    (f'{os.path.join(PROJECT_ROOT_FOR_MAP, "config", "settings.py")}',
     r'^(Aura|Laura|over|Dora|Horror)\s+(Konf\w*|konzentration)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    #Dora Konfiguration~/projects/py/STT/config
    #Aura Konfiguration ->~/projects/py/STT/config ->Horror Konfiguration->~/projects/py/STT/config/settings.py



    # , "dictation_service.log"
    (f'tail -f {os.path.join(PROJECT_ROOT_FOR_MAP,"log","dictation_service.log")}',
     r'^(Follow Main Lo[gk]\w*|Folge Lo[gk]\w*|Zeige Lo+[gk]\w*|Zeige Luft)$',
     95,
     {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),
    #Zeige Look->tail -f ~/projects/py/STT/log/dictation_service.log




]
