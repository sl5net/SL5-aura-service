# config/maps/plugins/standard_actions/path_navigator/aura_log/de-DE/FUZZY_MAP_pre.py



import re # noqa: F401
# import os
import sys
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parents[6]

home_dir_str = str(Path.home())
project_root_str_full = str(PROJECT_ROOT)

# 1. Tilde Replacement POSIX (Linux/Mac)
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
else:
    # Auf Windows immer den vollen Pfad nehmen
    PROJECT_ROOT_FOR_MAP = project_root_str_full

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_FOR_MAP).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()



PROJECT_ROOT_DISPLAY_STR = ''
# 1. Tilde Replacement (Only a String Operation!)
if project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full.replace(home_dir_str, '~', 1)
    # print(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")
else:
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full
    # print(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")

# 2. Use the SHELL-Display string, but manually join with the OS-Specific Separator (os.path.sep)
# This will be used in your f-string map actions.
PROJECT_ROOT_FOR_MAP = PROJECT_ROOT_DISPLAY_STR

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

    (f'{Path(PROJECT_ROOT_FOR_MAP, "log", "dictation_service.log").as_posix()}',
    # EXAMPLE: Aura log
    r'^(Aura |laura |dora |hurra |\w?aura |prora |zauberer |over a |oral )?(log-datei|L[o]+[gk]\w*|L[o]+[gk]\w*|L[o]+[gk]\w*|low|luck|lux|luft|b datei|voll gesorgt)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),

    (f'tail -f {Path(PROJECT_ROOT_FOR_MAP, "log", "dictation_service.log").as_posix()}',
    # EXAMPLE: Follow Folge Main Log
    r'^(Follow Main L[o]+[gk]\w*|Folge[n]? L[o]+[gk]\w*|folge luft|Zeige L[o]+[gk]\w*|Zeige Luft)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),


]
