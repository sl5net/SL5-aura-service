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

# Titres des fenêtres des applications LibreOffice

libreoffice_windows = ['soffice', 'LibreOffice', 'Writer', 'writer', 'Calc', 'calc', 'Impress']

fett = r'graisse|graisse\s*format|texte\s*graisse|côté|fritz|étape|ajuster|se produit|chef|scénario|mettre|audacieux|vieux|boulon|pôle|piscines|bulles|bols|bourrache|pain|aller chercher|dépassé|Oh'

duenn = r'mince|mince'

unterstrichen = "unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht"

FUZZY_MAP_pre = [

    # ('uuuuu', fr'^(souligner|souligner|et souligner|souligner le texte|souligner le texte souligner|souligner le texte)$', 85, {'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),



    # ('u2', fr'^\s*({souligné}|text\s*{souligné})\s*$', 85,{'command_flags' : re.IGNORECASE,'only_in_windows' : libreoffice_windows,}),



    #################################################
    # plateforme d'importation

    # 2. activez cette règle (derrière la première pluie que vous souhaitez optimiser)


    #################################################

    # ('f', r'^(gras|bold\s*format|text\s*bolt|sid|fritz|step|fit|step|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|bourrache|brot|holt|dépassé|oh)$', 85, {'command_flags' : re.IGNORECASE,}),






    # EXAMPLE: souligné

    ('lo unterstrichen', fr'^\s*({unterstrichen}|souligné|souligner|texte\s*souligné)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # EXAMPLE: graisse

    ('lo fett', fr'^({fett}|{duenn}|({fett}|{duenn})\s*format|texte\s*({fett}|{duenn}))$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Sauvegarder

    # EXAMPLE: mémoire

    ('lo speichern', r'^\s*(mémoire\w*|document\s*sauvegarder)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Défaire

    # EXAMPLE: dos

    ('lo rückgängig', r'^\s*(dos\w*|défaire\s*faire|défaire)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Italique

    # EXAMPLE: italique

    ('lo kursiv', r'^\s*(italique|italique\s*format|texte\s*italique)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),


    # Nouveau paragraphe

    # EXAMPLE: nouveau paragraphe

    ('lo neuer absatz', r'^\s*(plus récent?\s*paragraphe|nouveau\s*doubler|saut de ligne)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Sélectionnez tout

    # EXAMPLE: tout sélectionner

    ('lo alles auswählen', r'^\s*(tout\s*choisir|tout\s*marque)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Presse

    # EXAMPLE: presse

    ('lo drucken', r'^\s*(presse|document\s*presse)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Rechercher et remplacer

    # EXAMPLE: rechercher et remplacer

    ('lo suchen ersetzen', r'^\s*(chercher\s*(et)?\s*remplaçant|remplaçant)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Exporter au format PDF

    # EXAMPLE: Exportation PDF

    ('lo pdf exportieren', r'^\s*(pdf\s*exporter\w*|comme\s*pdf\s*sauvegarder|exporter?\s*pdf)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Copie

    # EXAMPLE: copie

    ('lo kopieren', r'^\s*(copie\w*|texte\s*copie)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Découper

    # EXAMPLE: découper

    ('lo ausschneiden', r'^\s*(découper\w*|texte\s*découper)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insérer

    # EXAMPLE: insérer

    ('lo einfügen', r'^\s*(insérer\w*|texte\s*insérer)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insérer un tableau

    # EXAMPLE: insérer un tableau

    ('lo tabelle einfügen', r'^\s*(tableau\s*insérer\w*|nouveau\s*tableau|vols?\s*tableau\s*un)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Titre 1

    # EXAMPLE: titre 1

    ('lo überschrift 1', r'^\s*(titre\s*1|titre\s*1|titre\s*1)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Titre 2

    # EXAMPLE: titre 2

    ('lo überschrift 2', r'^\s*(titre\s*2|titre\s*2|titre\s*2)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Titre 3

    # EXAMPLE: titre 3

    ('lo überschrift 3', r'^\s*(titre\s*3|titre\s*3|titre\s*3)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Texte normal / style standard

    # EXAMPLE: standard

    ('lo standard stil', r'^\s*(standard\w*|plus normal?\s*texte|standard\s*style)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Saut de page

    # EXAMPLE: saut de page

    ('lo seitenumbruch', r'^\s*(pages\w*bouleversement|nouveau\s*page|suivant\s*page)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Correcteur orthographique

    # EXAMPLE: orthographe

    ('lo rechtschreibung', r'^\s*(orthographe\w*|correcteur orthographique|orthographe)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insérer un commentaire

    # EXAMPLE: insérer un commentaire

    ('lo kommentar', r'^\s*(kommentar\s*einfüg\w*|neue[rn]?\s*kommentar|anmerkung)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Table des matières

    # EXAMPLE: table des matières

    ('lo inhaltsverzeichnis', r'^\s*(contenu\w*annuaire|annuaire\s*insérer\w*|toc)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Réinitialiser le zoom

    # EXAMPLE: zoomer en arrière

    ('lo zoom reset', r'^\s*(zoom\s*dos\w*|zoom\s*réinitialiser|normale\w*\s*zoom|avis\s*dos\w*)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Ouvrir le navigateur

    # EXAMPLE: navigateur

    ('lo navigator', r'^\s*(navigator\w*|dokument\s*navigator)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Exécuter une macro

    # EXAMPLE: exécuter une macro

    ('lo makro', r'^\s*(macro\s*exécuter\w*|plomb?\s*macro\s*de|macro)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # (f'kate {str(__file__).replace(home_dir_str, '~', 1)}',

    # EXAMPLE: Configurations LibreOffice


    ('kate ' + str(__file__).replace(home_dir_str, '~', 1),
     r'^(LibreOffice)\s+([Kc]éteint\w*|concentration|g\w+situation|paramètres?|guérir\w+ kr\w+tion|scénario\b\w*\s*\bsauvé|spr\w+t \w* \w*tet|ku\w+n g\w+dix)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),


]
