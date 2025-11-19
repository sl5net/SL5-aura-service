# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
import os
from pathlib import Path

import shutil
import sys


REQUIRED_COMMANDS = ['fzf', 'git', 'find', 'xclip', 'file']
BORDER = "=================================================================="

for cmd in REQUIRED_COMMANDS:
    if shutil.which(cmd) is None:
        error_message = f"🛑🛑🛑 ERROR: The required command '{cmd}' was not found in PATH. It needs to be installed. 🛑🛑🛑"

        print(BORDER, file=sys.stderr)
        print(error_message, file=sys.stderr)
        print("💡 TIP: Please check 'config/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md' for installation instructions.", file=sys.stderr)
        print(BORDER, file=sys.stderr)

        #sys.exit(1)





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

#fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard"
fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Single-line, Git-aware file search command
fzf_in_gitRepo = r"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
else
  find . -type f
fi | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""


FUZZY_MAP_pre = [


    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensions 'py,sh,html' | xclip -selection cl

    # config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py
    # following search is best when inside a Git repository, this is the quickest and most effective way to exclude boilerplate (date that you not interested in)
    # https://junegunn.github.io/fzf/
    (f"{fzf_in_gitRepo}",
     r'^(suche|search|find)\s+(file|datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #

    # sometimes here (18.11.'25 10:36 Tue) stt undstand wrong this is quickfix:
    (f"{fzf_in_gitRepo}",
     r'^(falsche|somit datei|suche data|suche Datei|suche Dateien|datei suche\w*|so geleitet hat)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # following works with fzf (highliy recomande to have, s.18.11.'25 09:00 Tue)
    # https://junegunn.github.io/fzf/
    (f"{fzf_everything}",
     r'^(suche|search|find)\s+(alles|everything|überall|everywhere|everything)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl'


    (f'{PROJECT_ROOT_FOR_MAP}',
     r'^(Aura|Agora|Aurora|ora|hurra|Flora)\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # ~/projects/py/STT
    #


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



]
