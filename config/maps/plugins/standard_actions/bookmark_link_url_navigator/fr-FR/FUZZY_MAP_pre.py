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


import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





FUZZY_MAP_pre = [


    # EXAMPLE: Événements CCC événements Tübingen

    ('https://events.ccc.de/search/?s=T%C3%BCbingen', r'^(CCC)\s*Événements\s*(événements Tübingen)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # site Web bitsundso bus982

    # EXAMPLE: bus982

    ('https://www.bitsundso.de/bus982/transcript/', r'^(bus982)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # des morceaux et donc un mastodonte

    # EXAMPLE: bitsundso b mastodonte s

    ('https://mastodon.social/@bitsundso', r'^des morceaux et ainsi de suite\b\s*(mastodonte\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # des morceaux et donc un mastodonte

    # EXAMPLE: bitsundso b tchncsx s

    ('https://social.tchncs.de/@bitsundso@mastodon.social', r'^des morceaux et ainsi de suite\b\s*(tchncs\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),



    # des morceaux et donc Bluesky

    # EXAMPLE: bitsundso b Blueskyx s

    ('https://mastodon.social/@bitsundso', r'^des morceaux et ainsi de suite\b\s*(Ciel bleu\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # empreinte bitsundso

    # EXAMPLE: bitsundso b empreinte p

    ('https://www.bitsundso.de/impressum/', r'^des morceaux et ainsi de suite\b\s*(imprimer)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # Bitsandso E-mail

    # EXAMPLE: bitsundso b E-mails

    ('info@undsoversum.de', r'^des morceaux et ainsi de suite\b\s*(E-mail)\s*$', 70, # min_accuracy
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


    # EXAMPLE: animé x

    ('https://regex101.com/', r'^(?:rapide?x|reg ex|expression régulière101|expression régulière 101|reg-?ex101|reg\-?ex|reg ex|expression|expression régulière|reg(populaire)?exp|reg(e|ä)x|reschex|resh-ex|reschex101|expression régulière\s*testeur|expression rationnelle\s*testeur|expression régulière\s*test|expression régulière\s*page|expression régulière\s*page|reckets|reeks|reeks101|page dexpression régulière|réexportation|outil dexpression régulière|expression régulière\s*en ligne|en ligne\s*expression régulière|expression régulière\s*aide(e|fr)|expression régulière\s*aide|expression régulière\s*site web|expression régulière\s*site web)\s*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),




    # Groupe non capturant (?:test)


    # EXAMPLE: Des événements colorés en librairie

    ('https://www.bunterbuchladen.de/veranstaltungen', r'^(Coloré|Vers le bas)\s*(Librairie)\s*(Événements)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),



]
