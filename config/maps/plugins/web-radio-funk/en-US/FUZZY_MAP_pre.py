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
# from pathlib import Path as p;import os as o # noqa: E702

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702




# from tornado.gen import sleep



# --- NEW: Lifecycle Hook ---

# def on_reload():

# """Runs automatically when Aura reloads this script."""

# print("hi from on_reload() in web-radio-funk")

# for i in range(9):

# sleep(1)

# print(f"{i} loop in web-radio-funk")




# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


    # you heard one fall asleep

    # Germany before your Germany


    # threema web

    # EXAMPLE: web threema web

    ('https://web.threema.com/', r'^(web\s*)?(threema)\s*(web)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: deutschlandfunk

    # One is sometimes noise of nothing

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(A\s*)?(deutschlandfunk|Germany radio|German\w* radio|German\w* before|Germany frank|Germany)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # your Germany

    # EXAMPLE: your Deutschlandfunk

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(your\s*)?(deutschlandfunk|Germany radio|German\w* radio|German\w* before)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: press club

    ('https://www1.wdr.de/daserste/presseclub/index.html', r'^(press club|pressing)\w*\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),



    # EXAMPLE: Radio desert wave livex

    ('https://www.wueste-welle.de/broadcasts/livestream', r'^(radio desert wave live\w*|desert wave live\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Radio desert wave

    ('https://www.wueste-welle.de/', r'^(radio desert wave|desert wave)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: LORA Munichx

    ('https://lora924.de/livestream/live-horen/', r'^(LORA Munich\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Free Radio Stuttgart

    ('https://www.freies-radio.de/', r'^(Free radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Archive Free Radio Stuttgart

    ('https://www.youtube.com/gbsstuttgart', r'^(Archive Free radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: twitch

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(twitch|Switch)\.*(search|Search on Twitter)\s*$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: twitch

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(search|Search on)\s*(twitch|Switch)\s*$', 70, {'command_flags': re.IGNORECASE}),

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

