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

# infranchissable

# tourner devant

# dans\s*fr\w*nt\w+

# infanterie


# dans le boeuf

# dans[\w\s]r\w+


infanterie = r'(dans[\w\s]r\w+|fam\w*\s*(rie|essayer|Ken)|infra\w*|infanterie|dans\s*fr\w*tn\w+|infanterie|infra essayer|le infanterie|infanterie|troupes à pied|dans\s*fr\w+t\s*\w|lui\s*fr\w+|\s*i\w*[nm]\s*fr\w+|\w*\s*infra)'

# config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py

# squelette chez les étrangers

# découvert chez des inconnus

# infanterie squelette


# sélectionner des travailleurs


# moi le morceau de hérisson


waehl = r'(E-mail|\w*choisir\w*|choix\w*|prendre\w*|goûts|marque|moi le)'

select1 = r'(sélectionner|s\w*élé\w*t+|\w*coins|Benoît|a|\nous\w+[ck]\w+t|\w*pose|se|bat|s\w+el\w*e|source)'

# lèche le bœuf


select = fr'(\s*({select1}|{waehl})\s*)'

iddle = r'(\s*(inactif|inactif|noble|i[gdts]|\wi\w+le\w+|sous[aa]tig\w*|travail\w*|sans emploi\w*|donc|recevoir)\s*)'
FUZZY_MAP_pre = [
    # EXAMPLE: choisir le milieu

    ('select iddle', fr'^{select}?({iddle}|{iddle}|{select}?)$', 20, _common_meta),

    # EXAMPLE: choisir les travailleurs

    ('select_women', fr'^{select}?(fr\w+|Travaux de construction\w*|Citoyens\w*|travail\w*|mais|Soutien\w*|vieux\s*w|vieux\s*où|vieux\s*fr|ald\s*femmes)$', 20, _common_meta),

    # EXAMPLE: femme sexy

    ('select_women', r'^\s*sel\w+$', 20, _common_meta_NO_on_match_exec),

    # ctrl+h = sélectionner la maison

    # EXAMPLE: sélectionner une maison

    ('ctrl+h', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*h(maison)?\s*$', 20, _common_meta_NO_on_match_exec),

    # ctrl+ m = sélectionner le marché

    # EXAMPLE: sélectionner un marché

    ('ctrl+m', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*m(arche|marché)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+b = sélectionner la caserne


    # EXAMPLE: caserne de contrôle

    ('ctrl+b', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*b(aracké|caserne)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ctrl+f = sélectionner la ferme


    # EXAMPLE: ferme

    ('ctrl+f', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*f(bras)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Ctrl s = sélectionner Storehouse Ship Stable Elephant table Dock... (en comprend plusieurs)


    # EXAMPLE: Entrepôt de contrôle

    ('ctrl+s', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*s(torehouse|bateau|écurie|éléphant\s*écurie|quai|bâtiment)?\s*$', 20,
     _common_meta_NO_on_match_exec),
    # Ctrl X = sélectionnez Barracks + Elephant Stable + Stable (presque tout)


    # EXAMPLE: tout contrôler

    ('ctrl+x', r'^\s*(Ctrl|contrôle|contrôle|impôt)\s*\+?\s*x(tout|bâtiment)?\s*$', 20, _common_meta_NO_on_match_exec),
    # ... plus de commandes de sélection de bâtiment



    # EXAMPLE: vieille

    ('alt+w', r'^\s*(vieux|ald)\s*\+?\s*w(Oman|femme)?\s*$', 20, _common_meta_NO_on_match_exec),

    # alt+ I = sélectionner l'infrastructure







    # EXAMPLE: vieux lancier

    ('alt+p', r'^\s*(vieux|ald)\s*\+?\s*p(Ikeman|lancier|fanatique|lancier)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+C = Cavalerie


    # EXAMPLE: vieille cavalerie

    ('alt+c', r'^\s*(vieux|ald)\s*\+?\s*c(avalerie|cavalerie)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+ A = Archer, Elephant Archer, Slinger Javelineer, ... (groupe de champions)


    # EXAMPLE: vieux frondeur

    ('alt+a', r'^\s*(vieux|ald)\s*\+?\s*a(rcher|frondeur|javelot|archer|combattant à distance)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+S = Épéiste, ..


    # EXAMPLE: vieux épéiste

    ('alt+s', r'^\s*(vieux|ald)\s*\+?\s*s(homme de mots|épéiste)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+E = Éléphant pour le support


    # EXAMPLE: vieil éléphant

    ('alt+e', r'^\s*(vieux|ald)\s*\+?\s*e(éléphant|éléphant|soutien)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+K = Catapulte (exceptions en raison de conflits)


    # EXAMPLE: vieille catapulte

    ('alt+k', r'^\s*(vieux|ald)\s*\+?\s*k(catapulte|catapulte)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+H = Guérisseur


    # EXAMPLE: vieux guérisseur

    ('alt+h', r'^\s*(vieux|ald)\s*\+?\s*h(distributeur|guérisseur)?\s*$', 20, _common_meta_NO_on_match_exec),
    # J = blessé (exceptions car proche Guérisseur)


    # EXAMPLE: blessés

    ('j', r'^\s*j(blessés|blessés)?\s*$', 20, _common_meta_NO_on_match_exec), # J for 'injured' or 'jawunded'
    # k = sélectionne uniquement maintenant blessé uniquement à l'aide de la souris


    # EXAMPLE: maintenant blessé seulement

    ('k', r'^\s*k(maintenant blessé seulement|pas\s*blessés)?\s*$', 20, _common_meta_NO_on_match_exec), # K for 'kept' or 'klar'
    # ... plus de commandes de sélection d'unité



    # Alt+ D = Éléphants dangereux (D. archer-,war-,héros-Elephant,... pas Support&Elephant)


    # EXAMPLE: alt d éléphants dangereux

    ('alt+d', r'^\s*(vieux|ald)\s*\+?\s*d(en colère\s*les éléphants|dangereux\s*les éléphants)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+V = Siège et Ministres (Siège : béliers, pas héros, Catapulte, Bolt Shooter, Siege Tower...)


    # EXAMPLE: anciennes victoires contre

    ('alt+v', r'^\s*(vieux|ald)\s*\+?\s*v(victoires|ministre|siège|ministre)?\s*$', 20, _common_meta_NO_on_match_exec),
    # Alt+M, Alt+X = sélectionner tous les militaires (maintenant blessés uniquement)

    # Ici, vous pouvez faire deux entrées, selon la transcription la plus probable


    # (construire|construire|puissance|notre|construire|\w+ild)


    # EXAMPLE: vieux militaire

    ('alt+x', r'^(vieux|ald)\s*\+?\s*m(ilit|ilit|m|x)\w+$', 20, _common_meta_NO_on_match_exec),

    # militaire


    # EXAMPLE: vieux militaire

    ('alt+x', r'^{select}?(\w*ilit\w*)$', 20, _common_meta_NO_on_match_exec),

    # EXAMPLE: vieux militaire

    ('alt+x', r'^\s*(vieux|ald)\s*\+?\s*x(militaire|militaire|tous\s*militaire)?\s*$', 20, _common_meta_NO_on_match_exec), # Alternative für X, falls es sich auf Militär bezieht
    # Alt+N = sélectionner tous les non militaires


    # EXAMPLE: vieux et pas militaire


    # EXAMPLE: vieux et non militaire

    # ('alt+n', r'^\s*(alt|ald)\s*\+?\s*n(on\s*militaire|pas\s*militaire|civils) ?\s*$', 20, _common_meta),


    # EXAMPLE: marque tout

    ('ctrl+alt', r'^(tous\w* maman\w+).*$', 85, _common_meta),

    # EXAMPLE: vieille infanterie

    # ('alt+i', r'^\s*(alt|ald)\s*\+?\s*i(nfanterie|infantry)?\s*$', 20, _common_meta_NO_on_match_exec),

    # Alt+P = sélectionnez Pikeman, Spearman, Fanatic (groupe de lanciers/combattants de mêlée)


    # EXAMPLE: infanterie

    ('select_infantry', fr'^{select}?{infanterie}$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: porteur de lance

    ('select_pikemen', r'^{select}?(lance tr[aa]ger|pikentr[aa]ger|phalange|piquiers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: cavalerie

    ('select_cavalry', r'^{select}?(cavalerie|équestre|cavalerie|cavalerie)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: archers

    ('select_archers', r'^{select}?(tir à larc[Aie]tzen|merde[Aie]tzen|svp[aa]nkler|archers)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: épéiste

    ('select_swordsmen', r'^{select}?(épée[aaae]+mpfer|épées|épéistes)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: les éléphants

    ('select_elephants', r'^{select}?(les éléphants|éléphant|les éléphants)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: catapultes

    ('select_catapults', r'^{select}?(catapultes|catapulte|siège|catapultes)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    # EXAMPLE: guérisseur

    ('select_healers', r'^{select}?(guérisseur|prêtre|guérisseurs)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': zad_title, 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]


