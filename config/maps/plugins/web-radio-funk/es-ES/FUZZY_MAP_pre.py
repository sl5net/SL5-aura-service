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

# config/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# desde tornado.gen importar dormir



# --- NUEVO: Gancho de ciclo de vida ---

# def on_reload():

# """Se ejecuta automáticamente cuando Aura recarga este script."""

# print("hola de on_reload() en web-radio-funk")

# para i en el rango (9):

# dormir(1)

# print(f"{i} bucle en web-radio-funk")




# Este mapa utiliza un enfoque híbrido:

# 1. Las entradas de expresiones regulares se verifican primero. Son potentes y pueden no distinguir entre mayúsculas y minúsculas.

# Estructura: ('reemplazo', r'regex_pattern', umbral, banderas)

# - El umbral se ignora para las expresiones regulares.

# - banderas: use {'command_flags': re.IGNORECASE} para no distinguir entre mayúsculas y minúsculas, o 0 para distinguir entre mayúsculas y minúsculas.

# 2. Si no hay coincidencias de expresiones regulares, se realiza una coincidencia difusa simple en las reglas restantes.


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Usar límites de palabras (\b) y agrupar (|) para detectar variaciones de manera eficiente.

    # Importante saber:

    # - se detiene con el primer partido completo. Ejemplos: ^...$ = Coincidencia completa = ¡Detener criterio!

    # - Primero se lee primero y se importa, es posible que las reglas inferiores no se lean.


    # escuchaste a uno quedarse dormido

    # Alemania antes que tu Alemania


    # web de tres

    # EXAMPLE: web tresma web

    ('https://web.threema.com/', r'^(web\s*)?(tresma)\s*(web)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: funk alemán

    # Se es a veces ruido de la nada

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(A\s*)?(funk alemán|radio alemania|Alemán\w* radio|Alemán\w* antes|Alemania franco|Alemania)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # tu Alemania

    # EXAMPLE: tu funk alemán

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(su\s*)?(funk alemán|radio alemania|Alemán\w* radio|Alemán\w* antes)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: club de prensa

    ('https://www1.wdr.de/daserste/presseclub/index.html', r'^(club de prensa|prensado)\w*\s*$', 70, # min_accuracy
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


    # EXAMPLE: contracción nerviosa

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(contracción nerviosa|Cambiar)\.*(buscar|Buscar en Gorjeo)\s*$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: contracción nerviosa

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(buscar|Buscar en)\s*(contracción nerviosa|Cambiar)\s*$', 70, {'command_flags': re.IGNORECASE}),

]

"""
    Twitch-Tools von CommanderRoot: Dies ist das mächtigste Werkzeug dafür.

    Gehe auf die Seite, wähle bei

vierter Eintrag:
Language "German" aus.

siebter Eintrag:
    Setze bei Viewers (max) eine kleine Zahl ein (z. B. 1 oder 5).

    Du erhältst sofort eine Liste mit Streamern, die gerade fast niemanden im Chat haben und sich riesig über ein „Hallo“ freuen.[1]

Nobody.live: Diese Seite spezialisiert sich auf Streamer mit 0 Zuschauern. Man kann dort oben links die Sprache auf "Deutsch" filtern.[2]
"""

