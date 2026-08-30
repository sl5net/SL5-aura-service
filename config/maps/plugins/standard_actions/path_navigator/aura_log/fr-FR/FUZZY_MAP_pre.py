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

# config/maps/plugins/standard_actions/path_navigator/aura_log/de-DE/FUZZY_MAP_pre.py




import re

# depuis pathlib import Path as p;import os as o
# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
# importer le système d'exploitation
import sys
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
SL5NET_AURA_PROJECT_ROOT = CONFIG_DIR.parents[6]

home_dir_str = str(Path.home())
project_root_str_full = str(SL5NET_AURA_PROJECT_ROOT)

# 1. Remplacement de Tilde POSIX (Linux/Mac)

if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
else:
    # Utilisez toujours le chemin complet sous Windows

    PROJECT_ROOT_FOR_MAP = project_root_str_full

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_FOR_MAP).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()



PROJECT_ROOT_DISPLAY_STR = ''
# 1. Remplacement du Tilde (uniquement une opération de chaîne !)

if project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full.replace(home_dir_str, '~', 1)
    # print(f"PROJECT_ROOT_DISPLAY_STR : {PROJECT_ROOT_DISPLAY_STR}")

else:
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full
    # print(f"PROJECT_ROOT_DISPLAY_STR : {PROJECT_ROOT_DISPLAY_STR}")


# 2. Utilisez la chaîne SHELL-Display, mais joignez-la manuellement avec le séparateur spécifique au système d'exploitation (os.path.sep).

# Ceci sera utilisé dans vos actions de carte f-string.

PROJECT_ROOT_FOR_MAP = PROJECT_ROOT_DISPLAY_STR

# fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection presse-papiers"

fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Commande de recherche de fichiers sur une seule ligne, compatible Git

fzf_in_gitRepo = r"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
else
  find . -type f
fi | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

FUZZY_MAP_pre = [

    (f'{Path(PROJECT_ROOT_FOR_MAP, "log", "aura_engine.log").as_posix()}',
    # EXAMPLE: Aura a menti

    r'^(aura |laure |Dora |Hourra |\w?aura |prora |magicien |sur a |oralement )?(enregistrer-déposer|L[o]+[merci]\w*|L[o]+[merci]\w*|L[o]+[merci]\w*|faible|chance|lux|air|b déposer|complet pris en charge|Trou)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),

    (f'tail -f {Path(PROJECT_ROOT_FOR_MAP, "log", "aura_engine.log").as_posix()}',
    # EXAMPLE: Suivre Suivre le journal principal

    r'^(Suivre Principal L[o]+[merci]\w*|Conséquence[n]? L[o]+[merci]\w*|conséquence air|Montrer L[o]+[merci]\w*|Montrer Air)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),


]
