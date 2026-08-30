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

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re
from pathlib import Path as p

CONFIG_DIR = p(__file__).parent

import os as o
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

zad_title = ['0ad', '0AD', '0 a.d.', '0 a.d']

_common_meta_NO_on_match_exec = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
}
_common_meta = {
    'command_flags': re.IGNORECASE,
    'only_in_windows': zad_title,
    'skip_list': ['LanguageTool'],
    'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
    'execute_only': True
}

# infranqueo

# girar al frente

# en\s*fr\w*nt\w+

# infantería


# en la carne

# en[\w\s]r\w+


infanterie = r'(en[\w\s]r\w+|inf\w*\s*(rie|intentar|conocido)|infra\w*|infantería|en\s*fr\w*Nuevo Testamento\w+|infantería|infra intentar|el infantería|infantería|tropas de a pie|en\s*fr\w+t\s*\w|a él\s*fr\w+|\s*i\w*[Nuevo Méjico]\s*fr\w+|\w*\s*infra)'

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py

# esqueleto en extraños

# descubierto en extraños

# infantería esqueleto


# seleccionar trabajadores


# yo el trozo de erizo


waehl = r'(Correo electrónico|\w*elegir\w*|elección\w*|llevar\w*|gustos|marca|a mí el)'

select1 = r'(seleccionar|s\w*ele\w*t+|\w*esquinas|Benedicto|a|\nosotros\w+[ck]\w+t|\w*pone|sí mismo|late|s\w+el\w*e|fuente)'

# lame la carne


select = fr'(\s*({select1}|{waehl})\s*)'

iddle = r'(\s*(inactivo|inactivo|noble|i[gdts]|\Wisconsin\w+le\w+|bajo[Automóvil club británico]tig\w*|trabajar\w*|desempleados\w*|entonces|recibir)\s*)'
FUZZY_MAP_pre = [
    # EXAMPLE: elige el medio

    ('select iddle', fr'^{select}?({iddle}|{iddle}|{select}?)$', 20, _common_meta),

    # EXAMPLE: elegir trabajadores

    ('select_women', fr'^{select}?(fr\w+|Trabajos de construcción\w*|Ciudadanos\w*|trabajar\w*|pero|Apoyo\w*|viejo\s*w|viejo\s*dónde|viejo\s*fr|aldo\s*mujer)$', 20, _common_meta),

    # EXAMPLE: mujer seltext

    ('select_women', r'^\s*sel\w+$', 20, _common_meta_NO_on_match_exec),

    # Ctrl+h = seleccionar casa

    # EXAMPLE: seleccione casa

    ('ctrl+h', r'^\s*(control|control|control|impuesto)\s*\+?\s*h(casa)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Ctrl+ m = seleccionar mercado

    # EXAMPLE: seleccionar mercado

    ('ctrl+m', r'^\s*(control|control|control|impuesto)\s*\+?\s*m(arca|mercado)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl+b = seleccionar cuartel


    # EXAMPLE: controlar a barack

    ('ctrl+b', r'^\s*(control|control|control|impuesto)\s*\+?\s*b(aracque|cuartel)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl+f = seleccionar granja


    # EXAMPLE: granja

    ('ctrl+f', r'^\s*(control|control|control|impuesto)\s*\+?\s*f(brazo)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl s = seleccionar Almacén Barco Establo Mesa de elefante Muelle... (incluye varios)


    # EXAMPLE: almacén de control

    ('ctrl+s', r'^\s*(control|control|control|impuesto)\s*\+?\s*s(almacén|barco|estable|elefante\s*estable|muelle|edificio)?\s*$', 20,
     _common_meta_NO_on_match_exec),
    # Ctrl X = seleccionar Cuartel + Establo de Elefantes + Establo (casi todo)


    # EXAMPLE: controlar todo

    ('ctrl+x', r'^\s*(control|control|control|impuesto)\s*\+?\s*x(todo|edificio)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ... más comandos de selección de edificios



    # EXAMPLE: anciana

    ('alt+w', r'^\s*(viejo|aldo)\s*\+?\s*w(Omán|mujer)?\s*$', 20, _common_meta_NO_on_match_exec),

    # alt+ I = seleccionar infraestructura







    # EXAMPLE: viejo lancero

    ('alt+p', r'^\s*(viejo|aldo)\s*\+?\s*p(ikeman|lancero|fanático|lancero)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+C = Caballería


    # EXAMPLE: vieja caballería

    ('alt+c', r'^\s*(viejo|aldo)\s*\+?\s*c(avalería|caballería)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ A = Arquero, Arquero Elefante, Lanzador de jabalinas, ... (grupo de campeones)


    # EXAMPLE: viejo hondero

    ('alt+a', r'^\s*(viejo|aldo)\s*\+?\s*a(rcher|hondero|jabalinista|arquero|luchador a distancia)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+S = Espadachín, ..


    # EXAMPLE: viejo espadachín

    ('alt+s', r'^\s*(viejo|aldo)\s*\+?\s*s(hombre de palabra|espadachín)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+E = Elefante de apoyo


    # EXAMPLE: viejo elefante

    ('alt+e', r'^\s*(viejo|aldo)\s*\+?\s*e(elefante|elefante|apoyo)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+K = Catapulta (excepciones por conflicto)


    # EXAMPLE: vieja catapulta

    ('alt+k', r'^\s*(viejo|aldo)\s*\+?\s*k(catapulta|catapulta)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+H = Sanador


    # EXAMPLE: viejo curandero

    ('alt+h', r'^\s*(viejo|aldo)\s*\+?\s*h(anciano|curador)?\s*$', 20, _common_meta_NO_on_match_exec),
    # J = herido (excepciones porque está cerca del sanador)


    # EXAMPLE: herido

    ('j', r'^\s*j(herido|herido)?\s*$', 20, _common_meta_NO_on_match_exec), # J for 'injured' or 'jawunded'
    # k = selecciona solo ahora herido solo usando el mouse


    # EXAMPLE: ahora solo heridos

    ('k', r'^\s*k(ahora solo heridos|no\s*herido)?\s*$', 20, _common_meta_NO_on_match_exec), # K for 'kept' or 'klar'
    # ... más comandos de selección de unidades



    # Alt+ D = Elefantes peligrosos (D. archer-,war-,hero-Elephant,... no Support&Elephant)


    # EXAMPLE: alt d elefantes peligrosos

    ('alt+d', r'^\s*(viejo|aldo)\s*\+?\s*d(enojado\s*elefantes|peligroso\s*elefantes)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+V = Asedio y Ministros (Asedio: arietes, no héroes, Catapulta, Bolt Shooter, Torre de asedio...)


    # EXAMPLE: viejas victorias

    ('alt+v', r'^\s*(viejo|aldo)\s*\+?\s*v(victorias|ministro|cerco|ministro)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+M, Alt+X = seleccionar todos los militares (ahorasolo heridos)

    # Aquí podrías hacer dos entradas, dependiendo de qué transcripción sea más probable.


    # (construir|construir|poder|nuestro|construir|\w+ild)


    # EXAMPLE: viejo militar

    ('alt+x', r'^(viejo|aldo)\s*\+?\s*m(iluminado|iluminado|m|x)\w+$', 20, _common_meta_NO_on_match_exec),

    # militar


    # EXAMPLE: viejo militar

    ('alt+x', r'^{select}?(\w*iluminado\w*)$', 20, _common_meta_NO_on_match_exec),

    # EXAMPLE: viejo militar

    ('alt+x', r'^\s*(viejo|aldo)\s*\+?\s*x(militar|militar|todo\s*militar)?\s*$', 20, _common_meta_NO_on_match_exec), # Alternative für X, falls es sich auf Militär bezieht
    # Alt+N = seleccionar todos los no militares


    # EXAMPLE: viejo y no militar


    # EXAMPLE: viejo n no militar

    # ('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*militares|no\s*militares|civiles)?\s*$', 20, _common_meta),


    # EXAMPLE: marca todo

    ('ctrl+alt', r'^(todo\w* mamá\w+).*$', 85, _common_meta),

    # EXAMPLE: vieja infantería

    # ('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantería)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+P = seleccionar Pikeman, Spearman, Fanatic (grupo de lanceros/luchadores cuerpo a cuerpo)


    # EXAMPLE: infantería

    ('select_infantry', fr'^{select}?{infanterie}$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: portador de lanza

    ('select_pikemen', r'^{select}?(lanza tr[Automóvil club británico]ger|pikentr[Automóvil club británico]ger|falange|pikemen)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: caballería

    ('select_cavalry', r'^{select}?(caballería|ecuestre|caballería|caballería)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: arqueros

    ('select_archers', r'^{select}?(tiro al arco[Ay]tzen|sh[Ay]tzen|sustantivo, masculino, plural—[Automóvil club británico]nkler|arqueros)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: espadachín

    ('select_swordsmen', r'^{select}?(espada[aaa]+mfer|espadas|espadachines)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: elefantes

    ('select_elephants', r'^{select}?(elefantes|elefante|elefantes)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: catapultas

    ('select_catapults', r'^{select}?(catapultas|catapulta|cerco|catapultas)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: curador

    ('select_healers', r'^{select}?(curador|sacerdote|curanderos)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]


