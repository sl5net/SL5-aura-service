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

# projects/py/STT/config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

import re
import shutil
import sys

# from pathlib import Path as p;import os as o
# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
# too<-from
# import os
from pathlib import Path

# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py


REQUIRED_COMMANDS = ['fzf', 'find']
CLIPBOARD_COMMAND = None

if sys.platform.startswith('linux'):
    CLIPBOARD_COMMAND = 'xclip'
    REQUIRED_COMMANDS.append('xclip')
    REQUIRED_COMMANDS.append('file')
elif sys.platform == 'win32':
    # 'clip' is the standard command for piping to the Windows clipboard

    CLIPBOARD_COMMAND = 'clip'
    REQUIRED_COMMANDS.append('clip')
elif sys.platform == 'darwin':
    # 'pbcopy' is the standard command for macOS clipboard

    CLIPBOARD_COMMAND = 'pbcopy'
    REQUIRED_COMMANDS.append('pbcopy')
    REQUIRED_COMMANDS.append('file')
else:
    # Fallback/Warning for unsupported OS

    print(f"WARNING: Clipboard functionality not tested on '{sys.platform}'. Skipping clipboard command check.", file=sys.stderr)

BORDER = "=================================================================="

for cmd in REQUIRED_COMMANDS:
    if shutil.which(cmd) is None:
        error_message = f"🛑🛑🛑 ERROR: The required command '{cmd}' was not found in PATH. It needs to be installed. 🛑🛑🛑"

        print(BORDER, file=sys.stderr)
        print(error_message, file=sys.stderr)
        print("💡 TIP: Please check 'config/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md' for installation instructions.", file=sys.stderr)
        print(BORDER, file=sys.stderr)

        # sys.exit(1)


CONFIG_DIR = Path(__file__).parent
SL5NET_AURA_PROJECT_ROOT = CONFIG_DIR.parents[5]

home_dir_str = str(Path.home())
project_root_str_full = str(SL5NET_AURA_PROJECT_ROOT)

# 1. Tilde Replacement POSIX (Linux/Mac)

if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
else:
    # Always use the full path on Windows

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
# print(f"PROJECT_ROOT_FOR_MAP: {PROJECT_ROOT_FOR_MAP}")


# fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard"

fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Single-line, Git-aware file search command

if sys.platform.startswith('linux'):
    # Linux Shell Syntax with Git/Find logic and xclip

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files --cached --others --exclude-standard
    else
    find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND} -selection clipboard
"""
elif sys.platform == 'darwin':
    # macOS Shell Syntax with Git/Find logic and pbcopy

    # pbcopy does not support/require the '-selection clipboard' flag

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
    else
  find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND}
"""
elif sys.platform == 'win32':
    # Simple FZF command for Windows, as requested

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"
else:
    # Fallback for other systems

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_DISPLAY_STR).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()

suche_text = r'grep -rn "text\|string" --include="*.py" . | grep -v ".venv"  | grep -v ".git" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_" | grep -v "/docs" | grep -v "/doc_sources" | grep -v "/release-chunks" | grep -v "/data" '

"""
grep -rn "suche datei" --include="*.py" . | grep -v ".venv" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_"

"""

aura1=r"(aura|Auer|Agora|Aurora|ora|hurrah|flora)"
aura2=r"(Auras?|Eyes|what|nora|orange|Other|era|also|Yours|Laura|moral|Rough|over|upper|o a|o|Samoa|Dora|your|goals|flora|Ava|horror|hurrah|higher|redder)"
aura3=r"(aura|Auer|Aurora|Root|Aurora)"

# Recommendation: Use the following script for the search (especially for the map search): ./scripts/search_rules/search_rules.bat


FUZZY_MAP_pre = [

    
    # Aura Confederacy

    # EXAMPLE: Aura Config

    (f'{Path(PROJECT_ROOT_POSIX, "config", "settings.py").as_posix()}',
     rf'^{aura2}\s+(Konf\w*|konzentration|settings?|\w*\s*dekoration)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),



    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensions 'py,sh,html' | xclip -selection cl


    # config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py

    # following search is best when inside a Git repository, this is the quickest and most effective way to exclude boilerplate (date that you are not interested in)

    # https://junegunn.github.io/fzf/



    # EXAMPLE: search file

    (f"{fzf_smart_file_finder}",
     r'^(search|search|find)\s+(file|file)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']
      }),

    # EXAMPLE: search text

    (f"{suche_text}",
     r'^(?:search(?:n|r|st)?|search|find)\b(?:\s+(?:after|the))?\s+\b(?:text|string)s?\b|\b(?:text|string)s?\b(?:\s+(?:after|the))?\s+\b(?:search(?:n|r|st)?|search|find)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']}),

    # EXAMPLE: file search

    (f"{fzf_in_gitRepo}",
    r'^(file|file|Details) (search|search|find)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
     'only_in_windows': ['Konsole', 'konsole', 'Console']
     }),

    # sometimes here (18.11.'25 10:36 Tue) stt undstand wrong this is quickfix:

    # EXAMPLE: search file

    (f"{fzf_smart_file_finder}",
     r'^(wrong|thus file|search data|search file|navigate file|search files|file search\w*|so directed has|sorry file)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),





    # following works with fzf (highly recommended to have, s.18.11.'25 09:00 Tue)

    # https://junegunn.github.io/fzf/

    # sorry file

    # EXAMPLE: search everything

    (f"{fzf_smart_file_finder}",
     r'^(search|search|find)\s+(everything|everything|everywhere|everywhere|everything)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl'


    # EXAMPLE: Aura path

    (f'{PROJECT_ROOT_POSIX}',
     rf'^{aura1}\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }
     ),

    # EXAMPLE: Space travel

    (f'{PROJECT_ROOT_POSIX}',
     r'^(Space travel)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),


    # EXAMPLE: home Dir

    (f'{HOME_DIR_POSIX}',
     r'^(home|hometown|user.user)\s+(path|You\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # EXAMPLE: braided

    # ('config/', r'^braided$', 90,

    # {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

    # 'only_in_windows': ['Console', 'console', 'Console',

    # r'cmd\.exe', 'PowerShell', 'Terminal', 'Command Prompt']

    # }),


    # EXAMPLE: skiplist

    ("'skip_list': ['LanguageTool','fullMatchStop','only_in_windows']",
     r'^(skip_list|skip_list|skip list|script blows|lets|script lets|squibb lets|it lets|it gives read|scribbles|it gives list|it gives blows|script list|skype lets|skype list|gpl list)$', 90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




    # EXAMPLE: Navigate Aura Configuration

    (f'cd "{Path(PROJECT_ROOT_POSIX, "config").as_posix()}"', rf'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+{aura3}\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE,
     'skip_list': ['LanguageTool'],
     }),

    # EXAMPLE: Navigate to Aura

    (f'cd "{PROJECT_ROOT_POSIX}"', r'^(Navigate|path|Path to|navi device)( to\w*)?\s+(aura|Aurora|Root|Authors)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Aura CV

    (f'{Path(PROJECT_ROOT_POSIX, "config", "maps","_privat","job","bewerbung","Lebenlauf-Sammlung","_Lebenslauf").as_posix()}',
     rf'^{aura1}\s+(Lebenslauf)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Navigate

    (f"{Path(PROJECT_ROOT_POSIX, 'config','maps','koans_deutsch').as_posix()}",
    r'^(Navigate\w*|path|Path to|navi device)( to\w*)?\s+(could|co one)\s*(German)\s*\w*$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Folder tree

    ("tree -d -I '__pycache__|.*|*.i18n' -L 9 -N > ~/t.txt; kate ~/t.txt;",
     r'^(Folder\s*Tree)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]
