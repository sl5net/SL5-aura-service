# config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
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

FUZZY_MAP_pre = [


    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensions 'py,sh,html' | xclip -selection cl

    # config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py
    # following search is best when inside a Git repository, this is the quickest and most effective way to exclude boilerplate (date that you not interested in)
    # https://junegunn.github.io/fzf/


    (f"{fzf_smart_file_finder}",
     # EXAMPLE: suche file
     r'^(suche|search|find)\s+(file|datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (f"{fzf_in_gitRepo}",
     # EXAMPLE: file search
    r'^(file|datei|Details) (suche|search|find)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #

    # sometimes here (18.11.'25 10:36 Tue) stt undstand wrong this is quickfix:
    (f"{fzf_smart_file_finder}",
     # EXAMPLE: suche Datei
     r'^(falsche|somit datei|suche data|suche Datei|navigiere datei|suche Dateien|datei suche\w*|so geleitet hat|sorry datei)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # following works with fzf (highliy recomande to have, s.18.11.'25 09:00 Tue)
    # https://junegunn.github.io/fzf/
    # sorry datei
    (f"{fzf_smart_file_finder}",
     # EXAMPLE: suche alles
     r'^(suche|search|find)\s+(alles|everything|überall|everywhere|everything)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    #fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl'

    (f'{PROJECT_ROOT_POSIX}',
     # EXAMPLE: Aura Pfad
     r'^(Aura|Auer|Agora|Aurora|ora|hurra|Flora)\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    (f'{PROJECT_ROOT_POSIX}',
     # EXAMPLE: Raumfahrt
     r'^(Raumfahrt)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    (f'{HOME_DIR_POSIX}',
     # EXAMPLE: home Dir
     r'^(home|heimat|user)\s+(Pfad|Dir\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),



    # Navigiere zu Aura Config
    (f'cd "{Path(PROJECT_ROOT_POSIX, "config").as_posix()}"',
    # EXAMPLE: Navigiere Aura Konfiguration
    r'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+(Aura|Auer|Aurora|Root|Aurora)\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Navigiere zu Aura
    (f'cd "{PROJECT_ROOT_POSIX}"',
    # EXAMPLE: Navigiere
    r'^(Navigiere|Pfad|Path to|navi gerät)( zu\w*)?\s+(Aura|Aurora|Root|Aurora|Autoren)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Aura Konfig
    (f'{Path(PROJECT_ROOT_POSIX, "config", "settings.py").as_posix()}',
     # EXAMPLE: Aura
     r'^(Aura|Laura|over|Dora|Horror)\s+(Konf\w*|konzentration)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]
