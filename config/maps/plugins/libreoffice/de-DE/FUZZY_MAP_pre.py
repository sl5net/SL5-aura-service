# config/maps/plugins/libreoffice/de-DE/FUZZY_MAP_pre.py:1
import platform
import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
home_dir_str = str(Path.home())

# Window titles of LibreOffice apps
libreoffice_windows = ['soffice', 'LibreOffice', 'Writer', 'Calc', 'Impress']

fett = r'fett|fett\s*formatieren|text\s*fett|sid|fritz|schritt|fit|tritt|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|borretsch|brot|holt|überholt|oh'

unterstrichen = f"unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht"

FUZZY_MAP_pre = [

    # ('uuuuu', fr'^(unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht)$', 85, {'flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),


    #('u2', fr'^\s*({unterstrichen}|text\s*{unterstrichen})\s*$', 85,{'flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),


    #################################################
    # import platform
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################

    # ('f', r'^(fett|fett\s*formatieren|text\s*fett|sid|fritz|schritt|fit|tritt|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|borretsch|brot|holt|überholt|oh)$', 85, {'flags': re.IGNORECASE,}),





    # Unterstrichen
    ('lo unterstrichen', fr'^\s*({unterstrichen}|unterstrichen|unterstreichen|text\s*unterstrichen)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),



    # Fett
    ('lo fett', fr'^({fett}|fett\s*formatieren|text\s*fett)$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Speichern
    ('lo speichern', r'^\s*(speicher\w*|dokument\s*speichern)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Rückgängig
    ('lo rückgängig', r'^\s*(rück\w*|rückgängig\s*machen|undo)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kursiv
    ('lo kursiv', r'^\s*(kursiv|kursiv\s*formatieren|text\s*kursiv)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),


    # Neuer Absatz
    ('lo neuer absatz', r'^\s*(neuer?\s*absatz|neue\s*zeile|zeilenumbruch)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Alles auswählen
    ('lo alles auswählen', r'^\s*(alles\s*auswählen|alles\s*markieren)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Drucken
    ('lo drucken', r'^\s*(drucken|dokument\s*drucken)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Suchen und Ersetzen
    ('lo suchen ersetzen', r'^\s*(suchen\s*(und)?\s*ersetzen|ersetzen)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Als PDF exportieren
    ('lo pdf exportieren', r'^\s*(pdf\s*export\w*|als\s*pdf\s*speichern|exportiere?\s*pdf)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kopieren
    ('lo kopieren', r'^\s*(kopier\w*|text\s*kopieren)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Ausschneiden
    ('lo ausschneiden', r'^\s*(ausschneid\w*|text\s*ausschneiden)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Einfügen
    ('lo einfügen', r'^\s*(einfüg\w*|text\s*einfügen)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Tabelle einfügen
    ('lo tabelle einfügen', r'^\s*(tabelle\s*einfüg\w*|neue\s*tabelle|füge?\s*tabelle\s*ein)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 1
    ('lo überschrift 1', r'^\s*(überschrift\s*1|heading\s*1|titel\s*1)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 2
    ('lo überschrift 2', r'^\s*(überschrift\s*2|heading\s*2|titel\s*2)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 3
    ('lo überschrift 3', r'^\s*(überschrift\s*3|heading\s*3|titel\s*3)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Normaler Text / Standard-Stil
    ('lo standard stil', r'^\s*(standard\w*|normaler?\s*text|standard\s*stil)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Seitenumbruch
    ('lo seitenumbruch', r'^\s*(seiten\w*umbruch|neue\s*seite|nächste\s*seite)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Rechtschreibprüfung
    ('lo rechtschreibung', r'^\s*(rechtschreib\w*|rechtschreibprüfung|spelling)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kommentar einfügen
    ('lo kommentar', r'^\s*(kommentar\s*einfüg\w*|neue[rn]?\s*kommentar|anmerkung)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Inhaltsverzeichnis
    ('lo inhaltsverzeichnis', r'^\s*(inhalts\w*verzeichnis|verzeichnis\s*einfüg\w*|toc)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Zoom zurücksetzen
    ('lo zoom reset', r'^\s*(zoom\s*zurück\w*|zoom\s*reset|normal\w*\s*zoom|ansicht\s*zurück\w*)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Navigator öffnen
    ('lo navigator', r'^\s*(navigator\w*|dokument\s*navigator)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Makro ausführen
    ('lo makro', r'^\s*(makro\s*ausführ\w*|führe?\s*makro\s*aus|macro)\s*$', 85, {
        'flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    (f'kate {str(__file__).replace(home_dir_str, '~', 1)}',
     # EXAMPLE: LibreOffice Konfigurationen
     r'^(LibreOffice)\s+([Kc]onf\w*|konzentration|g\w+situation|settings?|kur\w+ kr\w+tion|script\b\w*\s*\bgerettet|spr\w+t \w* \w*tet|ku\w+n g\w+ten)$',
     90,
     {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),


]
