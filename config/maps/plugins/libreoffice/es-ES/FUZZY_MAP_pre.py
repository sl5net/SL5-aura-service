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

import platform
import re
from pathlib import Path

from scripts.py.func.get_project_root import get_aura_project_root

CONFIG_DIR = Path(__file__).parent
TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()
home_dir_str = str(Path.home())

# Títulos de ventana de aplicaciones de LibreOffice

libreoffice_windows = ['soffice', 'LibreOffice', 'Writer', 'writer', 'Calc', 'calc', 'Impress']

fett = r'gordo|gordo\s*formato|texto\s*gordo|sid|fritz|paso|adaptar|ocurre|jefe|guion|poner|atrevido|viejo|tornillo|polo|quinielas|burbujas|bollos|borraja|pan|buscar|anticuado|Oh'

duenn = r'delgado|delgado'

unterstrichen = "unterstreicht|unterstreichen|und streicheln|text unterstreichen|text unterstreichen unterstreichen|text unterstreicht"

FUZZY_MAP_pre = [

    # ('uuuuu', fr'^(subrayado|subrayado|y subrayado|texto subrayado|texto subrayado subrayado|texto subrayado)$', 85, {'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),



    # ('u2', fr'^\s*({subrayado}|text\s*{subrayado})\s*$', 85,{'command_flags': re.IGNORECASE,'only_in_windows': libreoffice_windows,}),



    #################################################
    # plataforma de importación

    # 2. activa esta regla (después de la primera lluvia que deseas optimizar)


    #################################################

    # ('f', r'^(negrita|negrita\s*formato|texto\s*bolt|sid|fritz|step|fit|step|chef|script|setz|bold|viejo|bolt|pol|pools|bubbels|bols|borage|brot|holt|superado|oh)$', 85, {'command_flags': re.IGNORECASE,}),






    # EXAMPLE: testado

    ('lo unterstrichen', fr'^\s*({unterstrichen}|testado|subrayar|texto\s*testado)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # EXAMPLE: gordo

    ('lo fett', fr'^({fett}|{duenn}|({fett}|{duenn})\s*formato|texto\s*({fett}|{duenn}))$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Ahorrar

    # EXAMPLE: memoria

    ('lo speichern', r'^\s*(memoria\w*|documento\s*ahorrar)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Deshacer

    # EXAMPLE: atrás

    ('lo rückgängig', r'^\s*(atrás\w*|deshacer\s*hacer|deshacer)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Itálico

    # EXAMPLE: itálico

    ('lo kursiv', r'^\s*(itálico|itálico\s*formato|texto\s*itálico)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),


    # Punto y aparte

    # EXAMPLE: punto y aparte

    ('lo neuer absatz', r'^\s*(más nuevo?\s*párrafo|nuevo\s*línea|salto de línea)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Selecciona todo

    # EXAMPLE: seleccione todo

    ('lo alles auswählen', r'^\s*(todo\s*elegir|todo\s*marca)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Prensa

    # EXAMPLE: prensa

    ('lo drucken', r'^\s*(prensa|documento\s*prensa)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Buscar y reemplazar

    # EXAMPLE: buscar y reemplazar

    ('lo suchen ersetzen', r'^\s*(buscar\s*(y)?\s*sustituto|sustituto)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Exportar como PDF

    # EXAMPLE: Exportación de PDF

    ('lo pdf exportieren', r'^\s*(pdf\s*exportar\w*|como\s*pdf\s*ahorrar|exportar?\s*pdf)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Copiar

    # EXAMPLE: Copiar

    ('lo kopieren', r'^\s*(Copiar\w*|texto\s*Copiar)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Separar

    # EXAMPLE: separar

    ('lo ausschneiden', r'^\s*(separar\w*|texto\s*separar)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insertar

    # EXAMPLE: insertar

    ('lo einfügen', r'^\s*(insertar\w*|texto\s*insertar)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insertar tabla

    # EXAMPLE: insertar tabla

    ('lo tabelle einfügen', r'^\s*(tabla\s*insertar\w*|nuevo\s*tabla|vuelos?\s*tabla\s*a)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Título 1

    # EXAMPLE: título 1

    ('lo überschrift 1', r'^\s*(titular\s*1|título\s*1|título\s*1)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Título 2

    # EXAMPLE: encabezado 2

    ('lo überschrift 2', r'^\s*(titular\s*2|título\s*2|título\s*2)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Título 3

    # EXAMPLE: encabezado 3

    ('lo überschrift 3', r'^\s*(titular\s*3|título\s*3|título\s*3)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Texto normal/estilo estándar

    # EXAMPLE: estándar

    ('lo standard stil', r'^\s*(estándar\w*|mas normal?\s*texto|estándar\s*estilo)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Salto de página

    # EXAMPLE: salto de página

    ('lo seitenumbruch', r'^\s*(paginas\w*convulsión|nuevo\s*página|próximo\s*página)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # corrector ortográfico

    # EXAMPLE: ortografía

    ('lo rechtschreibung', r'^\s*(ortografía\w*|corrector ortográfico|ortografía)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Insertar comentario

    # EXAMPLE: insertar comentario

    ('lo kommentar', r'^\s*(kommentar\s*einfüg\w*|neue[rn]?\s*kommentar|anmerkung)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Tabla de contenido

    # EXAMPLE: Tabla de contenido

    ('lo inhaltsverzeichnis', r'^\s*(contenido\w*directorio|directorio\s*insertar\w*|toc)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Restablecer zoom

    # EXAMPLE: acercar hacia atrás

    ('lo zoom reset', r'^\s*(zoom\s*atrás\w*|zoom\s*reiniciar|normal\w*\s*zoom|opinión\s*atrás\w*)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Navegador abierto

    # EXAMPLE: navegador

    ('lo navigator', r'^\s*(navigator\w*|dokument\s*navigator)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # Ejecutar macro

    # EXAMPLE: ejecutar macro

    ('lo makro', r'^\s*(macro\s*ejecutar\w*|dirigir?\s*macro\s*fuera de|macro)\s*$', 85, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': libreoffice_windows,
        'on_match_exec': [CONFIG_DIR / 'libreoffice_actions.py'],
    }),

    # (f'kate {str(__file__).replace(home_dir_str, '~', 1)}',

    # EXAMPLE: Configuraciones de LibreOffice


    ('kate ' + str(__file__).replace(home_dir_str, '~', 1),
     r'^(LibreOffice)\s+([kc]enf\w*|concentración|g\w+situación|ajustes?|curar\w+ kr\w+ción|guion\b\w*\s*\salvado|primavera\w+t \w* \w*tete|ku\w+n g\w+diez)$',
     90,
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool'],
        'only_in_windows': ['Konsole', 'konsole', 'Console',
            r'cmd\.exe', 'PowerShell', 'Terminal', 'Eingabeaufforderung',
            'double', 'Double Commander'],
    }),


]
