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

# config/maps/plugins/game/0ad/build/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']

_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
    'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
    'execute_only': True
}




baue = r'(\s*(\w+Ay\w+|auto|\Guau|agricultor\w|edificio|construir|en|bicicleta|cultivo\w*|pero|ayuda de oficina|pablo|Pablo|Por qué|warhols|fuerza|nuestro|I|construir|\w+imagen|blanco)\s*)'
farm = r'f\w*a\w*m|fa\w*es|fa|alquería|conducir|conductor|bandera|mujer|mujer|preguntas|tener|grifo|brazo|en|diente'
bauernhof = r'(\s*(b\w+\s*(patio|una casa)|barriga|rosenhof|Constructor|marrón)\s*)'

feld = r'(\w*campo|granos\w*|pablo|roca|cae|cuenta|pelo|firmemente|películas|sostiene|son|quiere|ayuda|powershell|Grobenzell)'
bauefeld_nonsens = '(vfl|aushält|ruhe sie sind|graues hält|ausfällt|warum es will|warum filmt|alles rund|oh accounts|auch im kornfeld|eure kornfeld)'

pflanze = r'(papa\w*|trigo\w*|grano\w*|lechuga\w*|flor\w*|flores\w*|jardín|confinar|grano\w*|campo\w*)'

acker_nonsens = r'(dolor de cabeza|barack obama|impresora planta|acab)'

kaserne = r'(cuartel|\que[\s\w]*[äei]rn?e|Gato|clase|\que\werne|\w*aracque|cuartel\w?|Alojamiento de tropas)'

tempel = r'(templo|Temperatura\w*|Consejo|acampar|\w[oae]diputado\wl|Jampil|Timo)'


# kas erne

# ¿Qué sería+sería?

# \era[\s\w]*[äe]rn?e


ignore_this_fill_words = r'(\b\w{1,3}\b\s*)?'

festung = r'(\s*(fortaleza|f\w+\s*\w*|conducir tú|\w+\s*alrededor|es alrededor|silenciar|se convierte silenciar|final|fortaleza|fortaleza|fortaleza)\s*)'

arsenal = r'(arsenal|grabación|Cosas\s*una casa|Armas\s*existencias|armas|armas\s*carga|armas\s*la\w+|dejar laboratorio|entonces llamadas|personal|\w+rsonell|a nombrar|n / A tiene|dos caos|a de íntimamente)'

# recorrido


turm = r'(\s*(torre|hacer|meta|recorrido|torre)\s*)'
turmtype = r'(\s*(defensivo|piedra|piedra|defensa|defensa)\s*)'

FUZZY_MAP_pre = [
    # EXAMPLE: construir casa

    # ('h', fr'^{construir}?(\w?from|Casa|\wau[^\se]*|have|Hopp|Conejo|Rust|Rau|Año de construcción|Habitación)$',

    ('h', fr'^(?!agricultores?){baue}?(\w?fuera de|Casa|\Guau[^\sí]*|tener|salto|liebre|Óxido|Bruto|Año de construcción|habitación)$',
     99, _common_meta),

    # fr'^({build}\s*)?(patata\w*|(trigo\s*)*trigo\w*|\blanco\w+en[\s\w]*will|(grano\s*)+\w*|campo\w*|(ensalada\s*)+\w*|flor e\w*|\wumen|garden|conf|grain{field}\w*|{field}\w*)\s*{ignore_this_fill_words}(cultivo\w*|{build}|recomendar|planta\w*)?\s*$',


    # EXAMPLE: grano vegetal

    ('f',
     fr'^\s*({baue}\s*)?({pflanze}(\s+{feld})?|{feld})\s*{ignore_this_fill_words}(cultivo\w*|{baue}|recomendar|planta\w*)?\s*$',
     99, _common_meta),

    # tener



    # EXAMPLE: construir campo

    # ('f', r'^\s*(build|build|power|our|build|\w+ild)\s*(missing|field|field)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construir almacén

    ('s', fr'^{baue}?(([^wz]\w*)?existencias([\shr]*fuera de)?|Tienda|\w+g[\shr]*fuera de)\w*$', 99, _common_meta),

    # EXAMPLE: construir cuarteles

    # ('construir cuarteles', r'^\s*(build|build|Build)\s+(Ba\w+)$', 99, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construir cuarteles

    # ('build barrack', r'^\s*(\w+au\w+|Build)\s+(Ba\w+e)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construir cuarteles

    # ('construir barraca', r'^\s*(\w+au\w+|build|wild|image)\s+([pb]a[rc]\w+)$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construir casa

    # ('construir casa', r'^\s*(build\s*h?aus|build\s*h?aus|h?aus\s*build|build\s*h?ouse|casa)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),




    # EXAMPLE: construir mercado

    ('m', fr'^{baue}?(mamá|mar[ck]t?|edificio\s*mercado|mercado\s*construir|construir\s*mercado|mercado)\s*$', 99, _common_meta),

    # EXAMPLE: construir puerto

    ('j', fr'^{baue}?(puerto)$', 99, _common_meta),

    # EXAMPLE: diplomacia

    ('<', r'^diplomático\w*$'),

    # forjado


    # EXAMPLE: forjado

    # EXAMPLE: construir forja

    # EXAMPLE: construir forja

    ('n', fr'^{baue}?(s(ch)?m\w*|fragua)\s*$', 99, _common_meta),

    # EXAMPLE: construir campo

    # ('f', r'^\s*(build\s*farm|build\s*farm|granja\s*build|build\s*farm|granja|frahm|f\w*a\w*m)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),

    # ('f', fr'^\s*({buildfield_nonsense}|{build}\s*{field}|build\s*{field}|{field}\s*build|build\s*{field}|{field})\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),


    # EXAMPLE: campos de plantas

    # ('f', fr'^\s*({acre_nonsense}|acre\s*build|acre|plant\w*|plant\s*field)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': Verdadero}),



    # EXAMPLE: construir arsenal

    ('a', fr'^({baue}?{arsenal}|{arsenal}\s*{baue}?)$', 99, _common_meta),

    # construir granja (dos granjas)


    # EXAMPLE: construir granja

    # EXAMPLE: construir granja

    ('ff', fr'^({baue}\s*)?{ignore_this_fill_words}?({bauernhof}|{farm})\s*$', 99, _common_meta),
    # construir fortaleza (tres granjas)


    # EXAMPLE: construir fortaleza

    # ('fff', r'^\s*(build\s*fortress|build\s*fortress|fortress\s*build|build\s*fortress|fortress|tres\s*granjas)\s*$', 99, {'command_flags': re.IGNORECASE,'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d']}),


    # EXAMPLE: construir fortaleza

    ('fff', fr'^({baue}{festung}|{festung}\s*{baue})$', 99, _common_meta ),


    # EXAMPLE: cuartel

    ('b', fr'^({baue}?{kaserne}|{kaserne}{baue}?)$', 20, _common_meta),

    # EXAMPLE: templo

    ('ttt', fr'^({baue}?{tempel}|{tempel}{baue}?)$', 20, _common_meta),

    # EXAMPLE: construir torre

    ('t', fr'^\s*({baue}{turmtype}?{turm}|{turm}|{turmtype}{turm}{baue}|{turmtype}?{turm})$', 99, _common_meta),

]
