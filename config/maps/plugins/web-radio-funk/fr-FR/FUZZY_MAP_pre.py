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

# config/langagetool_server/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# depuis tornado.gen importer le sommeil



# --- NOUVEAU : Crochet de cycle de vie ---

# def on_reload() :

# """S'exécute automatiquement lorsque Aura recharge ce script."""

# print("salut de on_reload() dans la web-radio-funk")

# pour moi dans la plage (9):

# dormir(1)

# print(f"{i} boucle dans web-radio-funk")




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # tu en as entendu un s'endormir

    # L'Allemagne avant votre Allemagne


    # site Web de Threema

    # EXAMPLE: Web

    ('https://web.threema.com/', r'^(la toile\s*)?(troisma)\s*(la toile)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: deutschlandfunk

    # On est parfois bruit de rien

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(UN\s*)?(deutschlandfunk|Radio Allemagne|Allemand\w* radio|Allemand\w* avant|Allemagne franc|Allemagne)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # votre Allemagne

    # EXAMPLE: votre Deutschlandfunk

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(ton\s*)?(deutschlandfunk|Radio Allemagne|Allemand\w* radio|Allemand\w* avant)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: club de presse

    ('https://www1.wdr.de/daserste/presseclub/index.html', r'^(club de presse|pressage)\w*\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),



    # EXAMPLE: Livex radio vague du désert

    ('https://www.wueste-welle.de/broadcasts/livestream', r'^(radio désert vague en direct\w*|désert vague en direct\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Onde radio du désert

    ('https://www.wueste-welle.de/', r'^(radio désert vague|désert vague)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: LORA Munichx

    ('https://lora924.de/livestream/live-horen/', r'^(LORA Munich\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Radio gratuite Stuttgart

    ('https://www.freies-radio.de/', r'^(Gratuit radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Archives Radio Gratuite Stuttgart

    ('https://www.youtube.com/gbsstuttgart', r'^(Archive Gratuit radio .*Stuttgart)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: tic

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(tic|Changer)\.*(recherche|Recherche sur Gazouillement)\s*$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: tic

    ('https://twitch-tools.rootonline.de/channel_previews.php?broadcaster_languages%5B%5D=DE&viewers_max=0&uptime_min=900&sort_by=channelIdDesc', r'^(recherche|Recherche sur)\s*(tic|Changer)\s*$', 70, {'command_flags': re.IGNORECASE}),

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

