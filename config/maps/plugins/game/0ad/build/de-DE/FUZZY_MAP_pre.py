# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

FUZZY_MAP_pre = [

    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - means first is most importend, lower rules maybe not get read.

    # EXAMPLE: baue Haus
    # ('baue Haus', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(\w*aus|House)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue feld
    # ('f', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(fehlt|field|feld)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Lagerhaus
    # ('baue Lagerhaus', r'^\s*(\w+au\w+|baue|power|our|build|\w+ild)\s*(\w*lager|Storeh)\w*\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),



    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(baue|baue|Build)\s+(Ba\w+)$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(\w+au\w+|build|wild|bild)\s+([pb]a[rc]\w+)$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue hause
    # ('baue Haus', r'^\s*(baue\s*h?aus|bau\s*h?aus|h?aus\s*bauen|build\s*h?ouse|house)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: build markt
    ('m', r'^\s*(baue\s*markt|bau\s*markt|markt\s*bauen|build\s*market|market)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # build barrack
    ('b', r'^\s*(baue\s*baracke|bau\s*baracke|baracke\s*bauen|build\s*barrack|barrack|barack)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # build farm

    # EXAMPLE: baue farm
    ('f', r'^\s*(baue\s*farm|bau\s*farm|farm\s*bauen|build\s*farm|farm)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # build farmstead (zwei Farmen)

    # EXAMPLE: baue farmstead
    ('f,f', r'^\s*(baue\s*farmstead|bau\s*farmstead|farmstead\s*bauen|build\s*farmstead|farmstead|zwei\s*farmen)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # build fortress (drei Farmen)

    # EXAMPLE: baue festung
    ('f,f,f', r'^\s*(baue\s*festung|bau\s*festung|festung\s*bauen|build\s*fortress|fortress|drei\s*farmen)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ... weitere Bau-Befehle nach diesem Muster
]
