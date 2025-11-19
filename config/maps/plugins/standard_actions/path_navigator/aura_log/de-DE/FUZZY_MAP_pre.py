# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py


import re # noqa: F401
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parents[6]

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


    # dictation_service.log
    #    log
    (f'{os.path.join(PROJECT_ROOT_FOR_MAP,"log","dictation_service.log")}',
    r'^(Aura |laura |hurra |\w?aura |zauberer )?(log-datei|L[o]+[gk]\w*|L[o]+[gk]\w*|L[o]+[gk]\w*|low|luck|luft|b datei|voll gesorgt)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),



    # , "dictation_service.log"
    (f'tail -f {os.path.join(PROJECT_ROOT_FOR_MAP,"log","dictation_service.log")}',
     r'^(Follow Main L[o]+[gk]\w*|Folge L[o]+[gk]\w*|folge luft|Zeige L[o]+[gk]\w*|Zeige Luft)$',
     95,
     {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),
    #Zeige Look->tail -f ~/projects/py/STT/log/dictation_service.log


]
