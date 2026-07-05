# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py
# projects/py/STT/config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702


# too<-from
# import os
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

        #sys.exit(1)

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parents[5]

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
# print(f"PROJECT_ROOT_FOR_MAP: {PROJECT_ROOT_FOR_MAP}")

#fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard"
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

aura1=r"(Aura|Auer|Agora|Aurora|ora|hurra|Flora)"
aura2=r"(Auras?|Augen|woran|nora|orange|Andere|Ära|auch|Eurer|Laura|moral|Raue|over|obere|o a|o|samoa|Dora|eure|tore|Flora|ava|Horror|hurra|hoher|roter)"
aura3=r"(Aura|Auer|Aurora|Root|Aurora)"

# Empfehlung: Für die Suche (insbesodere für die Kartensuche) auch folgende Skript verwenden: ./scripts/search_rules/search_rules.bat

FUZZY_MAP_pre = [

    
    # Aura konföderation
    # EXAMPLE: Aura Konfig
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
    # following search is best when inside a Git repository, this is the quickest and most effective way to exclude boilerplate (date that you not interested in)
    # https://junegunn.github.io/fzf/


    # EXAMPLE: suche file
    (f"{fzf_smart_file_finder}",
     r'^(suche|search|find)\s+(file|datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']
      }),

    # EXAMPLE: suche text
    (f"{suche_text}",
     r'^(?:suche(?:n|r|st)?|search|find)\b(?:\s+(?:nach|the))?\s+\b(?:text|string)s?\b|\b(?:text|string)s?\b(?:\s+(?:nach|the))?\s+\b(?:suche(?:n|r|st)?|search|find)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']}),

    # EXAMPLE: file search
    (f"{fzf_in_gitRepo}",
    r'^(file|datei|Details) (suche|search|find)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
     'only_in_windows': ['Konsole', 'konsole', 'Console']
     }),

    # sometimes here (18.11.'25 10:36 Tue) stt undstand wrong this is quickfix:
    # EXAMPLE: suche Datei
    (f"{fzf_smart_file_finder}",
     r'^(falsche|somit datei|suche data|suche Datei|navigiere datei|suche Dateien|datei suche\w*|so geleitet hat|sorry datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),





    # following works with fzf (highliy recomande to have, s.18.11.'25 09:00 Tue)
    # https://junegunn.github.io/fzf/
    # sorry datei
    # EXAMPLE: suche alles
    (f"{fzf_smart_file_finder}",
     r'^(suche|search|find)\s+(alles|everything|überall|everywhere|everything)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    #fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl'

    # EXAMPLE: Aura Pfad
    (f'{PROJECT_ROOT_POSIX}',
     rf'^{aura1}\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }
     ),

    # EXAMPLE: Raumfahrt
    (f'{PROJECT_ROOT_POSIX}',
     r'^(Raumfahrt)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),


    # EXAMPLE: home Dir
    (f'{HOME_DIR_POSIX}',
     r'^(home|heimat|user)\s+(Pfad|Dir\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # EXAMPLE: zopfig
    # ('config/', r'^zopfig$', 90,
    #  {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
    #   'only_in_windows': ['Konsole', 'konsole', 'Console',
    #                       r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
    #     }),

    # EXAMPLE: skiplist
    ("'skip_list': ['LanguageTool','fullMatchStop','only_in_windows']",
     r'^(skip_list|skip_list|skip list|script bläst|lässt|script lässt|squibb lässt|es lässt|es gibt les|scribbles|es gibt list|es gibt bläst|script list|skype lässt|skype list|gpl list)$', 90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




    # EXAMPLE: Navigiere Aura Konfiguration
    (f'cd "{Path(PROJECT_ROOT_POSIX, "config").as_posix()}"', rf'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+{aura3}\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE,
     'skip_list': ['LanguageTool'],
     }),

    # EXAMPLE: Navigiere zu Aura
    (f'cd "{PROJECT_ROOT_POSIX}"', r'^(Navigiere|Pfad|Path to|navi gerät)( zu\w*)?\s+(Aura|Aurora|Root|Autoren)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Aura Lebenslauf
    (f'{Path(PROJECT_ROOT_POSIX, "config", "maps","_privat","job","bewerbung","Lebenlauf-Sammlung","_Lebenslauf").as_posix()}',
     rf'^{aura1}\s+(Lebenslauf)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Navigiere
    (f"{Path(PROJECT_ROOT_POSIX, 'config','maps','koans_deutsch').as_posix()}",
    r'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+(könne|co eins)\s*(deutsch)\s*\w*$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Ordner Baum
    ("tree -d -I '__pycache__|.*|*.i18n' -L 9 -N > ~/t.txt; kate ~/t.txt;",
     r'^(Ordner\s*Baum)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]
