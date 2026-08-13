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

# config/maps/plugins/standard_actions/bookmark_link_url_navigator/de-DE/FUZZY_MAP_pre.py


import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702





FUZZY_MAP_pre = [


    # EXAMPLE: CCC eventos eventos Tubinga

    ('https://events.ccc.de/search/?s=T%C3%BCbingen', r'^(CCC)\s*Eventos\s*(eventos Tubinga)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # sitio web de bitsundso bus982

    # EXAMPLE: autobús982

    ('https://www.bitsundso.de/bus982/transcript/', r'^(autobús982)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bits y así mastodonte

    # EXAMPLE: bitsundso b mastodonte s

    ('https://mastodon.social/@bitsundso', r'^bits y así sucesivamente\b\s*(mastodonte\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bits y así mastodonte

    # EXAMPLE: bitsundso b tchncsx s

    ('https://social.tchncs.de/@bitsundso@mastodon.social', r'^bits y así sucesivamente\b\s*(tchncs\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),



    # bits y así Bluesky

    # EXAMPLE: bitsundso b blueskyx s

    ('https://mastodon.social/@bitsundso', r'^bits y así sucesivamente\b\s*(cielo azul\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # huella bitsundso

    # EXAMPLE: bitsundso b impresión p

    ('https://www.bitsundso.de/impressum/', r'^bits y así sucesivamente\b\s*(imprimir)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # correo electrónico de bitsandso

    # EXAMPLE: bitsundso b Correo electrónico s

    ('info@undsoversum.de', r'^bits y así sucesivamente\b\s*(Correo electrónico)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Radio onda del desierto livex

    ('https://www.wueste-welle.de/broadcasts/livestream', r'^(radio desierto ola vivir\w*|desierto ola vivir\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Onda de radio del desierto

    ('https://www.wueste-welle.de/', r'^(radio desierto ola|desierto ola)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: LORA Munichx

    ('https://lora924.de/livestream/live-horen/', r'^(lora Munich\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Radio gratuita Stuttgart

    ('https://www.freies-radio.de/', r'^(Gratis radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Archivo Radio gratuita Stuttgart

    ('https://www.youtube.com/gbsstuttgart', r'^(Archivo Gratis radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: animado x

    ('https://regex101.com/', r'^(?:enérgico?x|registro ex|expresión regular101|expresión regular 101|registro-?ex101|registro\-?ex|registro ex|expresión|expresión regular|registro(popular)?exp.|registro(e|ä)x|reschex|resh-ex|reschex101|expresión regular\s*ensayador|expresión regular\s*ensayador|expresión regular\s*prueba|expresión regular\s*página|expresión regular\s*página|regeks|regeks|regeks101|página de expresiones regulares|regexportal|regextool|expresión regular\s*en línea|en línea\s*expresión regular|expresión regular\s*ayuda(e|es)|expresión regular\s*ayuda|expresión regular\s*sitio web|expresión regular\s*sitio web)\s*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),




    # Grupo sin captura (?:prueba)


    # EXAMPLE: Coloridos eventos en librerías

    ('https://www.bunterbuchladen.de/veranstaltungen', r'^(Vistoso|Abajo)\s*(Librería)\s*(Eventos)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),



]
