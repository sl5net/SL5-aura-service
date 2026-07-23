# config/maps/plugins/libreoffice/de-DE/FUZZY_MAP_pre.py
import platform
import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
home_dir_str = str(Path.home())

# Window titles of LibreOffice apps
libreoffice_windows = ['soffice', 'LibreOffice', 'Writer', 'writer', 'Calc', 'calc', 'Impress']

fett = r'fett|fett\s*formatieren|text\s*fett|sid|fritz|schritt|fit|tritt|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|borretsch|brot|holt|überholt|oh'

duenn = r'dünn|dünn'

unterstrichen = "unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht"

FUZZY_MAP_pre = [

    # ('uuuuu', fr'^(unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht)$', 85, {'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),


    #('u2', fr'^\s*({unterstrichen}|text\s*{unterstrichen})\s*$', 85,{'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),


    #################################################
    # import platform
    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)

    #################################################

    # ('f', r'^(fett|fett\s*formatieren|text\s*fett|sid|fritz|schritt|fit|tritt|chef|script|setz|bold|old|bolt|pol|pools|bubbels|bols|borretsch|brot|holt|überholt|oh)$', 85, {'command_flags': re.IGNORECASE,}),





    # EXAMPLE: unterstrichen
    ('lo unterstrichen', fr'^\s*({unterstrichen}|unterstrichen|unterstreichen|text\s*unterstrichen)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # EXAMPLE: fett
    ('lo fett', fr'^({fett}|{duenn}|({fett}|{duenn})\s*formatieren|text\s*({fett}|{duenn}))$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Speichern
    # EXAMPLE: speicher
    ('lo speichern', r'^\s*(speicher\w*|dokument\s*speichern)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Rückgängig
    # EXAMPLE: rück
    ('lo rückgängig', r'^\s*(rück\w*|rückgängig\s*machen|undo)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kursiv
    # EXAMPLE: kursiv
    ('lo kursiv', r'^\s*(kursiv|kursiv\s*formatieren|text\s*kursiv)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),


    # Neuer Absatz
    # EXAMPLE: neuer absatz
    ('lo neuer absatz', r'^\s*(neuer?\s*absatz|neue\s*zeile|zeilenumbruch)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Alles auswählen
    # EXAMPLE: alles auswählen
    ('lo alles auswählen', r'^\s*(alles\s*auswählen|alles\s*markieren)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Drucken
    # EXAMPLE: drucken
    ('lo drucken', r'^\s*(drucken|dokument\s*drucken)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Suchen und Ersetzen
    # EXAMPLE: suchen und ersetzen
    ('lo suchen ersetzen', r'^\s*(suchen\s*(und)?\s*ersetzen|ersetzen)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Als PDF exportieren
    # EXAMPLE: pdf export
    ('lo pdf exportieren', r'^\s*(pdf\s*export\w*|als\s*pdf\s*speichern|exportiere?\s*pdf)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kopieren
    # EXAMPLE: kopier
    ('lo kopieren', r'^\s*(kopier\w*|text\s*kopieren)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Ausschneiden
    # EXAMPLE: ausschneid
    ('lo ausschneiden', r'^\s*(ausschneid\w*|text\s*ausschneiden)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Einfügen
    # EXAMPLE: einfüg
    ('lo einfügen', r'^\s*(einfüg\w*|text\s*einfügen)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Tabelle einfügen
    # EXAMPLE: tabelle einfüg
    ('lo tabelle einfügen', r'^\s*(tabelle\s*einfüg\w*|neue\s*tabelle|füge?\s*tabelle\s*ein)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 1
    # EXAMPLE: überschrift 1
    ('lo überschrift 1', r'^\s*(überschrift\s*1|heading\s*1|titel\s*1)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 2
    # EXAMPLE: überschrift 2
    ('lo überschrift 2', r'^\s*(überschrift\s*2|heading\s*2|titel\s*2)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Überschrift 3
    # EXAMPLE: überschrift 3
    ('lo überschrift 3', r'^\s*(überschrift\s*3|heading\s*3|titel\s*3)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Normaler Text / Standard-Stil
    # EXAMPLE: standard
    ('lo standard stil', r'^\s*(standard\w*|normaler?\s*text|standard\s*stil)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Seitenumbruch
    # EXAMPLE: seitenumbruch
    ('lo seitenumbruch', r'^\s*(seiten\w*umbruch|neue\s*seite|nächste\s*seite)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Rechtschreibprüfung
    # EXAMPLE: rechtschreib
    ('lo rechtschreibung', r'^\s*(rechtschreib\w*|rechtschreibprüfung|spelling)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Kommentar einfügen
    # EXAMPLE: kommentar einfüg
    ('lo kommentar', r'^\s*(kommentar\s*einfüg\w*|neue[rn]?\s*kommentar|anmerkung)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Inhaltsverzeichnis
    # EXAMPLE: inhaltsverzeichnis
    ('lo inhaltsverzeichnis', r'^\s*(inhalts\w*verzeichnis|verzeichnis\s*einfüg\w*|toc)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Zoom zurücksetzen
    # EXAMPLE: zoom zurück
    ('lo zoom reset', r'^\s*(zoom\s*zurück\w*|zoom\s*reset|normal\w*\s*zoom|ansicht\s*zurück\w*)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Navigator öffnen
    # EXAMPLE: navigator
    ('lo navigator', r'^\s*(navigator\w*|dokument\s*navigator)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Makro ausführen
    # EXAMPLE: makro ausführ
    ('lo makro', r'^\s*(makro\s*ausführ\w*|führe?\s*makro\s*aus|macro)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # (f'kate {str(__file__).replace(home_dir_str, '~', 1)}',
    # EXAMPLE: LibreOffice Konfigurationen

    ('kate ' + str(__file__).replace(home_dir_str, '~', 1),
     r'^(LibreOffice)\s+([Kc]onf\w*|konzentration|g\w+situation|settings?|kur\w+ kr\w+tion|script\b\w*\s*\bgerettet|spr\w+t \w* \w*tet|ku\w+n g\w+ten)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),


]
