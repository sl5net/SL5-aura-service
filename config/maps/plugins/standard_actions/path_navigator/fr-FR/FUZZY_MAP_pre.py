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

# projets/py/STT/config/maps/plugins/standard_actions/path_navigator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# aussi<-de

# importer le système d'exploitation

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
    # 'clip' est la commande standard pour rediriger vers le presse-papiers de Windows

    CLIPBOARD_COMMAND = 'clip'
    REQUIRED_COMMANDS.append('clip')
elif sys.platform == 'darwin':
    # 'pbcopy' est la commande standard pour le presse-papiers de macOS

    CLIPBOARD_COMMAND = 'pbcopy'
    REQUIRED_COMMANDS.append('pbcopy')
    REQUIRED_COMMANDS.append('file')
else:
    # Repli/Avertissement pour un système d'exploitation non pris en charge

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
# print(f"PROJECT_ROOT_FOR_MAP : {PROJECT_ROOT_FOR_MAP}")


# fzf_in_gitRepo1="git ls-files | fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection presse-papiers"

fzf_everything="""
fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection cl
"""

fzf_in_gitRepo="""
git ls-files | fzf --style full --preview 'cat {}' --bind 'focus:transform-header:file --brief {}' | xclip -selection clipboard
"""

# fzf_smart_file_finder Commande de recherche de fichiers sur une seule ligne, compatible Git

if sys.platform.startswith('linux'):
    # Syntaxe Linux Shell avec logique Git/Find et xclip

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files --cached --others --exclude-standard
    else
    find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND} -selection clipboard
"""
elif sys.platform == 'darwin':
    # Syntaxe macOS Shell avec logique Git/Find et pbcopy

    # pbcopy ne prend pas en charge/nécessite l'indicateur '-selection clipboard'

    fzf_smart_file_finder = rf"""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files
    else
  find . -type f
fi | fzf --style full --preview 'cat {{}}' --bind 'focus:transform-header:file --brief {{}}' | {CLIPBOARD_COMMAND}
"""
elif sys.platform == 'win32':
    # Commande FZF simple pour Windows, comme demandé

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"
else:
    # Repli pour d'autres systèmes

    # EXAMPLE: fzf

    fzf_smart_file_finder = r"fzf"

PROJECT_ROOT_POSIX = Path(PROJECT_ROOT_DISPLAY_STR).as_posix()
HOME_DIR_POSIX = Path(home_dir_str).as_posix()

suche_text = r'grep -rn "text\|string" --include="*.py" . | grep -v ".venv"  | grep -v ".git" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_" | grep -v "/docs" | grep -v "/doc_sources" | grep -v "/release-chunks" | grep -v "/data" '

"""
grep -rn "suche datei" --include="*.py" . | grep -v ".venv" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_"

"""

aura1=r"(aura|Auer|Agora|Aurore|ora|Hourra|flore)"
aura2=r"(Auras?|Yeux|quoi|Nora|orange|Autre|ère|aussi|Le vôtre|Laure|morale|Rugueux|sur|supérieur|o a|o|Samoa|Dora|ton|objectifs|flore|Ava|horreur|Hourra|plus haut|plus rouge)"
aura3=r"(aura|Auer|Aurore|Racine|Aurore)"

# Recommandation : Utilisez le script suivant pour la recherche (en particulier pour la recherche sur carte) : ./scripts/search_rules/search_rules.bat


FUZZY_MAP_pre = [

    
    # Confédération Aura

    # EXAMPLE: Configuration de l'aura

    (f'{Path(PROJECT_ROOT_POSIX, "config", "settings.py").as_posix()}',
     rf'^{aura2}\s+(Konf\w*|konzentration|settings?|\w*\s*dekoration)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),



    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' --extensions 'py,sh,html' | xclip -sélection cl


    # config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py

    # La recherche suivante est préférable dans un référentiel Git, c'est le moyen le plus rapide et le plus efficace d'exclure le passe-partout (date qui ne vous intéresse pas)

    # https://junegunn.github.io/fzf/



    # EXAMPLE: rechercher un fichier

    (f"{fzf_smart_file_finder}",
     r'^(recherche|recherche|trouver)\s+(déposer|déposer)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']
      }),

    # EXAMPLE: rechercher du texte

    (f"{suche_text}",
     r'^(?:recherche(?:n|r|St)?|recherche|trouver)\b(?:\s+(?:après|le))?\s+\b(?:texte|chaîne)s?\b|\b(?:texte|chaîne)s?\b(?:\s+(?:après|le))?\s+\b(?:recherche(?:n|r|St)?|recherche|trouver)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
      'only_in_windows': ['Konsole', 'konsole', 'Console']}),

    # EXAMPLE: recherche de fichiers

    (f"{fzf_in_gitRepo}",
    r'^(déposer|déposer|Détails) (recherche|recherche|trouver)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
     'only_in_windows': ['Konsole', 'konsole', 'Console']
     }),

    # parfois ici (18.11.'25 10:36 mar) je comprends mal, c'est une solution rapide :

    # EXAMPLE: rechercher un fichier

    (f"{fzf_smart_file_finder}",
     r'^(faux|ainsi déposer|recherche données|recherche déposer|naviguer déposer|recherche fichiers|déposer recherche\w*|donc dirigé a|Désolé déposer)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }),





    # travaux suivants avec fzf (fortement recommandé, s.18.11.'25 09h00 mar)

    # https://junegunn.github.io/fzf/

    # désolé fichier

    # EXAMPLE: tout chercher

    (f"{fzf_smart_file_finder}",
     r'^(recherche|recherche|trouver)\s+(tout|tout|partout|partout|tout)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # fzf --style full --preview 'fzf-preview.sh {}' --bind 'focus:transform-header:file --brief {}' | xclip -sélection cl'


    # EXAMPLE: Chemin de l'aura

    (f'{PROJECT_ROOT_POSIX}',
     rf'^{aura1}\s+(Aura|Pfad)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
        r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']
      }
     ),

    # EXAMPLE: Voyage spatial

    (f'{PROJECT_ROOT_POSIX}',
     r'^(Voyage spatial)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),


    # EXAMPLE: Accueil

    (f'{HOME_DIR_POSIX}',
     r'^(maison|ville natale|utilisateur.utilisateur)\s+(chemin|Toi\w*)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],

      'only_in_windows': ['Konsole', 'konsole', 'Console',
                          r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung']

      }),

    # EXAMPLE: tressé

    # ('config/', r'^tresse$', 90,

    # {'flags' : re.IGNORECASE, 'skip_list' : ['LanguageTool'],

    # 'only_in_windows' : ['Console', 'console', 'Console',

    # r'cmd\.exe', 'PowerShell', 'Terminal', 'Invite de commandes']

    # }),


    # EXAMPLE: liste de saut

    ("'skip_list': ['LanguageTool','fullMatchStop','only_in_windows']",
     r'^(sauter_liste|sauter_liste|sauter liste|scénario coups|permettons|scénario permettons|squibb permettons|il permettons|il donne lire|gribouillis|il donne liste|il donne coups|scénario liste|Skype permettons|Skype liste|gpl liste)$', 90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),




    # EXAMPLE: Naviguer dans la configuration d'Aura

    (f'cd "{Path(PROJECT_ROOT_POSIX, "config").as_posix()}"', rf'^(Navigiere\w*|Pfad|Path to|navi gerät)( zu\w*)?\s+{aura3}\s*Konf\w*$',
    90,
    {'flags': re.IGNORECASE,
     'skip_list': ['LanguageTool'],
     }),

    # EXAMPLE: Accédez à Aura

    (f'cd "{PROJECT_ROOT_POSIX}"', r'^(Naviguer|chemin|Chemin à|naviguer appareil)( à\w*)?\s+(aura|Aurore|Racine|Auteurs)$',
    90,
    {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: CV Aura

    (f'{Path(PROJECT_ROOT_POSIX, "config", "maps","_privat","job","bewerbung","Lebenlauf-Sammlung","_Lebenslauf").as_posix()}',
     rf'^{aura1}\s+(Lebenslauf)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: Naviguer

    (f"{Path(PROJECT_ROOT_POSIX, 'config','maps','koans_deutsch').as_posix()}",
    r'^(Naviguer\w*|chemin|Chemin à|naviguer appareil)( à\w*)?\s+(pourrait|co un)\s*(Allemand)\s*\w*$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Arborescence des dossiers

    ("tree -d -I '__pycache__|.*|*.i18n' -L 9 -N > ~/t.txt; kate ~/t.txt;",
     r'^(Dossier\s*Arbre)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),





]
