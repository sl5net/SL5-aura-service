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




import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# importar sistema operativo

import sys
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
SL5NET_AURA_PROJECT_ROOT = CONFIG_DIR.parents[6]

home_dir_str = str(Path.home())
project_root_str_full = str(SL5NET_AURA_PROJECT_ROOT)

# 1. Reemplazo de tilde POSIX (Linux/Mac)

if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
else:
    # Utilice siempre la ruta completa en Windows

    PROJECT_ROOT_FOR_MAP = project_root_str_full

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_FOR_MAP).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()



PROJECT_ROOT_DISPLAY_STR = ''
# 1. Reemplazo de tilde (¡solo una operación de cadena!)

if project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full.replace(home_dir_str, '~', 1)
    # imprimir(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")

else:
    PROJECT_ROOT_DISPLAY_STR = project_root_str_full
    # imprimir(f"PROJECT_ROOT_DISPLAY_STR: {PROJECT_ROOT_DISPLAY_STR}")


# 2. Utilice la cadena SHELL-Display, pero únala manualmente con el separador específico del sistema operativo (os.path.sep)

# Esto se utilizará en las acciones del mapa f-string.

PROJECT_ROOT_FOR_MAP = PROJECT_ROOT_DISPLAY_STR

# fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selección portapapeles"

fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Comando de búsqueda de archivos compatible con Git de una sola línea

fzf_in_gitRepo = r"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
else
  find . -type f
fi | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""
#

FUZZY_MAP_pre = [

    (f'{Path(PROJECT_ROOT_FOR_MAP, "log", "aura_engine.log").as_posix()}',
    # EXAMPLE: Aura mintió

    r'^(aura |laura |dora |Hurra |\w?aura |prora |mago |encima a |oralmente )?(registro-archivo|L[o]+[gk]\w*|L[o]+[gk]\w*|L[o]+[gk]\w*|bajo|suerte|lujos|aire|b archivo|lleno cuidado de|Agujero)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),

    (f'tail -f {Path(PROJECT_ROOT_FOR_MAP, "log", "aura_engine.log").as_posix()}',
    # EXAMPLE: Seguir Seguir Registro principal

    r'^(Seguir Principal L[o]+[gk]\w*|Consecuencia[n]? L[o]+[gk]\w*|consecuencia aire|Espectáculo L[o]+[gk]\w*|Espectáculo Aire)$',
    95,
    {'flags': re.IGNORECASE,'skip_list': ['LanguageTool']}),


]
