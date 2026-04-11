# config/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pre.py
# config/languagetool_server/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

# from tornado.gen import sleep


# --- NEU: Lifecycle Hook ---
# def on_reload():
#     """Wird automatisch ausgeführt, wenn Aura dieses Skript neu lädt."""
#     print("hi from on_reload() in web-radio-funk")
#     for i in range(9):
#         sleep(1)
#         print(f"{i} loop in  web-radio-funk")



# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    # einen hörtest einschlafen
    # deutschland vor dein deutschlands

    # EXAMPLE: deutschlandfunk
    # Einen  is somtimes noise of nothing
    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(Einen\s*)?(deutschlandfunk|Deutschlandradio|deutsch\w* radio|deutsch\w* vor|deutschland frank)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # dein deutschlands
    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(dein\s*)?(deutschlandfunk|Deutschlandradio|deutsch\w* radio|deutsch\w* vor)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: presseclub
    ('https://www1.wdr.de/daserste/presseclub/index.html', r'^(presseclub|pressig)\w*\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),



    # EXAMPLE: Radio wüste welle livex
    ('https://www.wueste-welle.de/broadcasts/livestream', r'^(Radio wüste welle live\w*|wüste welle live\w*)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: Radio wüste welle
    ('https://www.wueste-welle.de/', r'^(Radio wüste welle|wüste welle)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),


    # EXAMPLE: LORA Münchenx
    ('https://lora924.de/livestream/live-horen/', r'^(LORA München\w*)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: Freies Radio  Stuttgart
    ('https://www.freies-radio.de/', r'^(Freies Radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),

    # EXAMPLE: Archiv Freies Radio  Stuttgart
    ('https://www.youtube.com/gbsstuttgart', r'^(Archiv Freies Radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'flags': re.IGNORECASE}),


    # EXAMPLE: twich
    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(twich|Switch)\.*(suche|Suche auf Twitter)\s*$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: twich
    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(suche|Suche auf)\s*(twich|Switch)\s*$', 70, {'flags': re.IGNORECASE}),

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

