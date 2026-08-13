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

# config/maps/plugins/libreoffice/de-DE/FUZZY_MAP_pre.py

from scripts.py.func.get_project_root import get_aura_project_root
import platform
import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()
home_dir_str = str(Path.home())

# Window titles of LibreOffice apps

libreoffice_windows = ['soffice', 'LibreOffice', 'Writer', 'writer', 'Calc', 'calc', 'Impress']

fett = r'fat|fat\s*format|text\s*fat|sid|fritz|step|fit|occurs|boss|script|put|bold|old|bolt|pole|pools|bubbles|bols|borage|bread|fetch|outdated|Oh'

duenn = r'thin|thin'

unterstrichen = "unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht"

FUZZY_MAP_pre = [

    # ('uuuuu', fr'^(underline|underline|and underline|underline text|underline text underline|underline text)$', 85, {'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),



    # ('u2', fr'^\s*({underlined}|text\s*{underlined})\s*$', 85,{'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),



    #################################################
    # import platform

    # 2. activate this rule (behind the first rain you want to optimize)


    #################################################

    # ('f', r'^(bold|bold\s*format|text\s*bolt|sid|fritz|step|fit|step|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|borage|brot|holt|overtaken|oh)$', 85, {'command_flags': re.IGNORECASE,}),






    # EXAMPLE: underlined

    ('lo unterstrichen', fr'^\s*({unterstrichen}|underlined|underline|text\s*underlined)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # EXAMPLE: fat

    ('lo fett', fr'^({fett}|{duenn}|({fett}|{duenn})\s*format|text\s*({fett}|{duenn}))$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Save

    # EXAMPLE: memory

    ('lo speichern', r'^\s*(memory\w*|document\s*save)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Undo

    # EXAMPLE: back

    ('lo rückgängig', r'^\s*(back\w*|undo\s*make|undo)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Italic

    # EXAMPLE: italic

    ('lo kursiv', r'^\s*(italic|italic\s*format|text\s*italic)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),


    # New paragraph

    # EXAMPLE: new paragraph

    ('lo neuer absatz', r'^\s*(newer?\s*paragraph|new\s*line|line break)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Select everything

    # EXAMPLE: select everything

    ('lo alles auswählen', r'^\s*(everything\s*choose|everything\s*mark)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Press

    # EXAMPLE: press

    ('lo drucken', r'^\s*(press|document\s*press)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Find and replace

    # EXAMPLE: search and replace

    ('lo suchen ersetzen', r'^\s*(seek\s*(and)?\s*substitute|substitute)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Export as PDF

    # EXAMPLE: PDF export

    ('lo pdf exportieren', r'^\s*(pdf\s*export\w*|as\s*pdf\s*save|export?\s*pdf)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Copy

    # EXAMPLE: copy

    ('lo kopieren', r'^\s*(copy\w*|text\s*copy)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Cut out

    # EXAMPLE: cut out

    ('lo ausschneiden', r'^\s*(cut out\w*|text\s*cut out)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insert

    # EXAMPLE: insert

    ('lo einfügen', r'^\s*(insert\w*|text\s*insert)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insert table

    # EXAMPLE: insert table

    ('lo tabelle einfügen', r'^\s*(tabel\s*insert\w*|new\s*tabel|flights?\s*tabel\s*a)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Heading 1

    # EXAMPLE: heading 1

    ('lo überschrift 1', r'^\s*(headline\s*1|heading\s*1|title\s*1)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Heading 2

    # EXAMPLE: heading 2

    ('lo überschrift 2', r'^\s*(headline\s*2|heading\s*2|title\s*2)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Heading 3

    # EXAMPLE: heading 3

    ('lo überschrift 3', r'^\s*(headline\s*3|heading\s*3|title\s*3)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Normal text / standard style

    # EXAMPLE: standard

    ('lo standard stil', r'^\s*(standard\w*|more normal?\s*text|standard\s*style)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Page break

    # EXAMPLE: page break

    ('lo seitenumbruch', r'^\s*(pages\w*upheaval|new\s*page|next\s*page)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Spell checker

    # EXAMPLE: spelling

    ('lo rechtschreibung', r'^\s*(spelling\w*|spell checker|spelling)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insert comment

    # EXAMPLE: insert comment

    ('lo kommentar', r'^\s*(kommentar\s*einfüg\w*|neue[rn]?\s*kommentar|anmerkung)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Table of contents

    # EXAMPLE: table of contents

    ('lo inhaltsverzeichnis', r'^\s*(content\w*directory|directory\s*insert\w*|toc)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Reset zoom

    # EXAMPLE: zoom back

    ('lo zoom reset', r'^\s*(zoom\s*back\w*|zoom\s*reset|normal\w*\s*zoom|opinion\s*back\w*)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Open navigator

    # EXAMPLE: navigator

    ('lo navigator', r'^\s*(navigator\w*|dokument\s*navigator)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Run macro

    # EXAMPLE: execute macro

    ('lo makro', r'^\s*(macro\s*execute\w*|lead?\s*macro\s*out of|macro)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # (f'kate {str(__file__).replace(home_dir_str, '~', 1)}',

    # EXAMPLE: LibreOffice configurations


    ('kate ' + str(__file__).replace(home_dir_str, '~', 1),
     r'^(LibreOffice)\s+([Kc]onf\w*|concentration|g\w+situation|settings?|cure\w+ kr\w+tion|script\b\w*\s*\bsaved|spr\w+t \w* \w*tet|ku\w+n g\w+ten)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),


]
