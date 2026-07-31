# config/maps/plugins/game/0ad/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

baue = r'(\waue|bauer|bauens|build|bei|anbau\w*|aber|bürohilfe|paul|paulus|warum|warhols)'
farm = r'f\w*a\w*m|fa\w*en|fa|farmstead|fahren|fahrer|farben|frau|frauen|fragen|haben|hahn|arm|am|zahn'
bauernhof = r'(b\w+\s*hof|bauch|rosenhof)\s*'



feld = r'(\w*feld|paul|felsen|fällt|fell|fest|filmt|hält|sind|will|verhilft|powershell)'
bauefeld_nonsens = '(vfl|aushält|ruhe sie sind|graues hält|ausfällt|warum es will|warum filmt|alles rund|oh accounts|auch im kornfeld|eure kornfeld)'

acker_nonsens = r'(kopfschmerzen|barack obama|drucker pflanzen|acab)'

ignore_this_fill_words = r'(\b\w{1,3}\b\s*)?'

festung = r'\s*(festung|f\w+\s*\w*|fährst du|\w+\s*um|ist um|stumm|wird stumm|schluss|fortress|festung|fortress)\s*'

turm = r'\s*(turm|tor|tower)\s*'
turmtype = r'\s*(verteidigungs|stein|stein|wehr|defense)\s*'

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

    # EXAMPLE: baue feld
    # ('f', r'^\s*(baue\s*farm|bau\s*farm|farm\s*bauen|build\s*farm|farm|frahm|f\w*a\w*m)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ('f', fr'^\s*({bauefeld_nonsens}|{baue}\s*{feld}|bau\s*{feld}|{feld}\s*bauen|build\s*{feld}|{feld})\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: acker pflanzen
    # ('f', fr'^\s*({acker_nonsens}|acker\s*bauen|acker|pflanz\w*|pflanze\s*feld)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # this is recommended: 30.7.'26 16:50 Thu works best.
    # EXAMPLE: getreide pflanzen
    ('f', fr'^({baue}\s*)?(kartoffel\w*|weizen\w*|getreide\w*|acker\w*|salat\w*|blume\w*|garten|kornfeld\w*|feld\w*)\s*{ignore_this_fill_words}(anbau\w*|{baue}|empfehlen|pflanz\w*)?\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),



    # build farmstead (zwei Farmen)

    # EXAMPLE: baue farm
    ('f,f', fr'^({baue}\s*)?{ignore_this_fill_words}?({bauernhof}|{farm})\s*$', 15, {'command_flags': re.IGNORECASE,
    'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],'execute_only': True}),
    # build fortress (drei Farmen)

    # EXAMPLE: baue festung
    # ('f,f,f', r'^\s*(baue\s*festung|bau\s*festung|festung\s*bauen|build\s*fortress|fortress|drei\s*farmen)\s*$', 15, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue festung
    ('fff', fr'^\s*({baue}\s*{festung}|{festung}\s*{baue})$', 15,
     {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
      'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: baue turm
    ('dd', fr'^\s*({baue}{turmtype}{turm}|{turm}|{turmtype}{turm}{baue}|{turmtype}{turm})$', 15, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]
