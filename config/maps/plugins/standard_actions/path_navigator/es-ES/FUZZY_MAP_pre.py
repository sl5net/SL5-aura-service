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

# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

# proyectos/py/STT/config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# también <-de

# importar sistema operativo

from pathlib import Path

import shutil
import sys
# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py


REQUIRED_COMMANDS = ['fzf', 'find']
CLIPBOARD_COMMAND = None

if sys.platform.startswith('linux'):
    CLIPBOARD_COMMAND = 'xclip'
    REQUIRED_COMMANDS.append('xclip')
    REQUIRED_COMMANDS.append('file')
elif sys.platform == 'win32':
    # 'clip' es el comando estándar para canalizar al portapapeles de Windows

    CLIPBOARD_COMMAND = 'clip'
    REQUIRED_COMMANDS.append('clip')
elif sys.platform == 'darwin':
    # 'pbcopy' es el comando estándar para el portapapeles de macOS

    CLIPBOARD_COMMAND = 'pbcopy'
    REQUIRED_COMMANDS.append('pbcopy')
    REQUIRED_COMMANDS.append('file')
else:
    # Reserva/Advertencia para sistemas operativos no compatibles

    print(f"WARNING: Clipboard functionality not tested on '{sys.platform}'. Skipping clipboard command check.", file=sys.stderr)

BORDER = "=================================================================="

for cmd in REQUIRED_COMMANDS:
    if shutil.which(cmd) is None:
        error_message = f"🛑🛑🛑 ERROR: The required command '{cmd}' was not found in PATH. It needs to be installed. 🛑🛑🛑"

        print(BORDER, file=sys.stderr)
        print(error_message, file=sys.stderr)
        print("💡 TIP: Please check 'config/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md' for installation instructions.", file=sys.stderr)
        print(BORDER, file=sys.stderr)

        # salida del sistema (1)


CONFIG_DIR = Path(__file__).parent
SL5NET_AURA_PROJECT_ROOT = CONFIG_DIR.parents[5]

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
# imprimir(f"PROJECT_ROOT_FOR_MAP: {PROJECT_ROOT_FOR_MAP}")


# fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selección portapapeles"

fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Comando de búsqueda de archivos compatible con Git de una sola línea

if sys.platform.startswith('linux'):
    # Sintaxis de Shell de Linux con lógica Git/Find y xclip

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files --cached --others --exclude-standard
    else
    find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND} -selection clipboard
"""
elif sys.platform == 'darwin':
    # Sintaxis de macOS Shell con lógica Git/Find y pbcopy

    # pbcopy no admite/requiere el indicador '-selección portapapeles'

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
    else
  find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND}
"""
elif sys.platform == 'win32':
    # Comando FZF simple para Windows, según lo solicitado

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"
else:
    # Respaldo para otros sistemas

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_DISPLAY_STR).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()

suche_text = r'grep -rn "text\|string" --include="*.py" . | grep -v ".venv"  | grep -v ".git" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_" | grep -v "/docs" | grep -v "/doc_sources" | grep -v "/release-chunks" | grep -v "/data" '

"""
grep -rn "suche datei" --include="*.py" . | grep -v ".venv" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_"

"""

aura1=r"(aura|auer|Ágora|Aurora|ora|Hurra|flora)"
aura2=r"(Auras?|Ojos|qué|nora|naranja|Otro|era|también|Tuyo|laura|moral|Bruto|encima|superior|o a|o|Samoa|dora|su|objetivos|flora|ava|horror|Hurra|más alto|más rojo)"
aura3=r"(aura|auer|Aurora|Raíz|Aurora)"

# Recomendación: utilice el siguiente script para la búsqueda (especialmente para la búsqueda en el mapa): ./scripts/search_rules/search_rules.bat


FUZZY_MAP_pre = [

    
    # Confederación del Aura

    # EXAMPLE: Configuración de aura

    (f'{Path(PROJECT_ROOT_POSIX, "config", "settings.py").as_posix()}',
     rf'^{aura2}\s+(Konf\w*|konzentration|settings?|\w*\s*dekoration)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),



    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensiones 'py,sh,html' | xclip -selección cl


    # config/maps/plugins/.../es-DE/FUZZY_MAP_pr.py

    # La siguiente búsqueda es mejor cuando se encuentra dentro de un repositorio Git, esta es la forma más rápida y efectiva de excluir texto estándar (fecha que no le interesa)

    # https://junegunn.github.io/fzf/



    # EXAMPLE: buscar archivo

    (f"{fzf_smart_file_finder}",
     r'^(buscar|buscar|encontrar)\s+(archivo|archivo)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']
      }),

    # EXAMPLE: buscar texto

    (f"{suche_text}",
     r'^(?:buscar(?:n|r|calle)?|buscar|encontrar)\b(?:\s+(?:después|el))?\s+\b(?:texto|cadena)s?\b|\b(?:texto|cadena)s?\b(?:\s+(?:después|el))?\s+\b(?:buscar(?:n|r|calle)?|buscar|encontrar)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']}),

    # EXAMPLE: búsqueda de archivos

    (f"{fzf_in_gitRepo}",
    r'^(archivo|archivo|Detalles) (buscar|buscar|encontrar)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
     'only_in_windows': ['Konsole', 'konsole', 'Console']
     }),

    # a veces aquí (18.11.'25 10:36 martes) no entiendo mal, esta es una solución rápida:

    # EXAMPLE: buscar archivo

    (f"{fzf_smart_file_finder}",
     r'^(equivocado|de este modo archivo|buscar datos|buscar archivo|navegar por archivo|buscar archivos|archivo buscar\w*|entonces dirigido tiene|Lo siento archivo)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),





    # siguientes trabajos con fzf (muy recomendable tenerlo, s.18.11.'25 09:00 martes)

    # https://junegunn.github.io/fzf/

    # lo siento archivo

    # EXAMPLE: busca todo

    (f"{fzf_smart_file_finder}",
     r'^(buscar|buscar|encontrar)\s+(todo|todo|en todos lados|en todos lados|todo)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selección cl'


    # EXAMPLE: Camino del aura

    (f'{PROJECT_ROOT_POSIX}',
     rf'^{aura1}\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }
     ),

    # EXAMPLE: viajes espaciales

    (f'{PROJECT_ROOT_POSIX}',
     r'^(viajes espaciales)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),


    # EXAMPLE: directorio de inicio

    (f'{HOME_DIR_POSIX}',
     r'^(hogar|ciudad natal|usuario.usuario)\s+(camino|Tú\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # EXAMPLE: trenzado

    # ('config/', r'^trenzado$', 90,

    # {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

    # 'only_in_windows': ['Consola', 'consola', 'Consola',

    # r'cmd\.exe', 'PowerShell', 'Terminal', 'Símbolo del sistema']

    # }),


    # EXAMPLE: lista de omisión

    ("'skip_list': ['LanguageTool','fullMatchStop','only_in_windows']",
     r'^(saltar_lista|saltar_lista|saltar lista|guion golpes|vamos|guion vamos|squibb vamos|él vamos|él da leer|garabatos|él da lista|él da golpes|guion lista|Skype vamos|Skype lista|gpl lista)$', 90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




    # EXAMPLE: Navegar por la configuración del aura

    (f'cd "{Path(PROJECT_ROOT_POSIX, "config").as_posix()}"', rf'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+{aura3}\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE,
     'skip_list': ['LanguageTool'],
     }),

    # EXAMPLE: Navegar a Aura

    (f'cd "{PROJECT_ROOT_POSIX}"', r'^(Navegar por|camino|Camino a|navi dispositivo)( a\w*)?\s+(aura|Aurora|Raíz|Autores)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: CV Aura

    (f'{Path(PROJECT_ROOT_POSIX, "config", "maps","_privat","job","bewerbung","Lebenlauf-Sammlung","_Lebenslauf").as_posix()}',
     rf'^{aura1}\s+(Lebenslauf)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Navegar por

    (f"{Path(PROJECT_ROOT_POSIX, 'config','maps','koans_deutsch').as_posix()}",
    r'^(Navegar por\w*|camino|Camino a|navi dispositivo)( a\w*)?\s+(podría|co uno)\s*(Alemán)\s*\w*$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: árbol de carpetas

    ("tree -d -I '__pycache__|.*|*.i18n' -L 9 -N > ~/t.txt; kate ~/t.txt;",
     r'^(Carpeta\s*Árbol)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]
