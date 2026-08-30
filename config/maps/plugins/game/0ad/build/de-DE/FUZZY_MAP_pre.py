# config/maps/plugins/game/0ad/build/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re
from pathlib import Path as p

CONFIG_DIR = p(__file__).parent

import os as o
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']

_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
    'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
    'execute_only': True
}




baue = r'(\s*(\w+au\w+|auto|\waue|bauer\w|bauens|build|bei|bike|anbau\w*|aber|bürohilfe|paul|paulus|warum|warhols|power|our|ich|build|\w+ild|white)\s*)'
farm = r'f\w*a\w*m|fa\w*en|fa|farmstead|fahren|fahrer|farben|frau|frauen|fragen|haben|hahn|arm|am|zahn'
bauernhof = r'(\s*(b\w+\s*(hof|haus)|bauch|rosenhof|Bauherrn|braun)\s*)'

feld = r'(\w*feld|korns\w*|paul|felsen|fällt|zählt|fell|fest|filmt|hält|sind|will|verhilft|powershell|gröbenzell)'
bauefeld_nonsens = '(vfl|aushält|ruhe sie sind|graues hält|ausfällt|warum es will|warum filmt|alles rund|oh accounts|auch im kornfeld|eure kornfeld)'

pflanze = r'(kartoffel\w*|weizen\w*|getreide\w*|salat\w*|blume\w*|blumen\w*|garten|conf|korn\w*|acker\w*)'

acker_nonsens = r'(kopfschmerzen|barack obama|drucker pflanzen|acab)'

kaserne = r'(kaserne|\wa[\s\w]*[äei]rn?e|Katze|klasse|\wa\werne|\w*aracke|barrack\w?|Truppenunterkunft)'

tempel = r'(Tempel|Temp\w*|Tipp|campen|\w[öae]mp\wl|Jampil|Tim)'


# kas     erne
# was\s+w äre
# \was[\s\w]*[äe]rn?e

ignore_this_fill_words = r'(\b\w{1,3}\b\s*)?'

festung = r'(\s*(festung|f\w+\s*\w*|fährst du|\w+\s*um|ist um|stumm|wird stumm|schluss|fortress|festung|fortress)\s*)'

arsenal = r'(arsenal|aufnahme|Zeug\s*haus|Waffen\s*lager|waffen|waffen\s*laden|waffen\s*la\w+|lassen lab|also nennt|personell|\w+rsonell|zu nennen|na hat|zwei chaos|a von nähere)'

# tour

turm = r'(\s*(turm|tun|tor|tour|tower)\s*)'
turmtype = r'(\s*(verteidigungs|stein|stein|wehr|defense)\s*)'

FUZZY_MAP_pre = [
    # EXAMPLE: baue Haus
    #            ('h', fr'^{baue}?(\w?aus|House|\wau[^\se]*|haben|Hopp|Hase|Rust|Rau|Baujahr|Raumes)$',
    ('h', fr'^(?!bauern?){baue}?(\w?aus|House|\wau[^\se]*|haben|Hopp|Hase|Rust|Rau|Baujahr|Raumes)$',
     99, _common_meta),

    # fr'^({baue}\s*)?(kartoffel\w*|(weizen\s*)*weizen\w*|\wei\w+en[\s\w]*will|(getreide\s*)+\w*|acker\w*|(salat\s*)+\w*|blume\w*|\wumen|garten|conf|korn{feld}\w*|{feld}\w*)\s*{ignore_this_fill_words}(anbau\w*|{baue}|empfehlen|pflanz\w*)?\s*$',

    # EXAMPLE: getreide pflanzen
    ('f',
     fr'^\s*({baue}\s*)?({pflanze}(\s+{feld})?|{feld})\s*{ignore_this_fill_words}(anbau\w*|{baue}|empfehlen|pflanz\w*)?\s*$',
     99, _common_meta),

    # haben


    # EXAMPLE: baue feld
    # ('f', r'^\s*(baue|baue|power|our|build|\w+ild)\s*(fehlt|field|feld)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Lagerhaus
    ('s', fr'^{baue}?(([^wz]\w*)?lager([\shr]*aus)?|Storeh|\w+g[\shr]*aus)\w*$', 99, _common_meta),

    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(baue|baue|Build)\s+(Ba\w+)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue Baracke
    # ('baue Baracke', r'^\s*(\w+au\w+|build|wild|bild)\s+([pb]a[rc]\w+)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue hause
    # ('baue Haus', r'^\s*(baue\s*h?aus|bau\s*h?aus|h?aus\s*bauen|build\s*h?ouse|house)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),



    # EXAMPLE: build markt
    ('m', fr'^{baue}?(ma|mar[ck]t?|bau\s*markt|markt\s*bauen|build\s*market|market)\s*$', 99, _common_meta),

    # EXAMPLE: baue hafen
    ('hh', fr'^{baue}?(hafen)$', 99, _common_meta),

    # EXAMPLE: Diplomatie
    ('<', r'^Diplomat\w*$'),

    # schmiede

    # EXAMPLE: schmiede
    # EXAMPLE: baue schmiede
    # EXAMPLE: build forge
    ('n', fr'^{baue}?(s(ch)?m\w*|forge)\s*$', 99, _common_meta),

    # EXAMPLE: baue feld
    # ('f', r'^\s*(baue\s*farm|bau\s*farm|farm\s*bauen|build\s*farm|farm|frahm|f\w*a\w*m)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),
    # ('f', fr'^\s*({bauefeld_nonsens}|{baue}\s*{feld}|bau\s*{feld}|{feld}\s*bauen|build\s*{feld}|{feld})\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: acker pflanzen
    # ('f', fr'^\s*({acker_nonsens}|acker\s*bauen|acker|pflanz\w*|pflanze\s*feld)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),


    # EXAMPLE: baue arsenal
    ('a', fr'^({baue}?{arsenal}|{arsenal}\s*{baue}?)$', 99, _common_meta),

    # build farmstead (zwei Farmen)

    # EXAMPLE: baue farm
    # EXAMPLE: baue bauernhof
    ('ff', fr'^({baue}\s*)?{ignore_this_fill_words}?({bauernhof}|{farm})\s*$', 99, _common_meta),
    # build fortress (drei Farmen)

    # EXAMPLE: baue festung
    # ('fff', r'^\s*(baue\s*festung|bau\s*festung|festung\s*bauen|build\s*fortress|fortress|drei\s*farmen)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # EXAMPLE: baue festung
    ('fff', fr'^({baue}{festung}|{festung}\s*{baue})$', 99, _common_meta ),


    # EXAMPLE: Kaserne
    ('b', fr'^({baue}?{kaserne}|{kaserne}{baue}?)$', 20, _common_meta),

    # EXAMPLE: Tempel
    ('ttt', fr'^({baue}?{tempel}|{tempel}{baue}?)$', 20, _common_meta),

    # EXAMPLE: baue turm
    ('t', fr'^\s*({baue}{turmtype}?{turm}|{turm}|{turmtype}{turm}{baue}|{turmtype}?{turm})$', 99, _common_meta),

]
