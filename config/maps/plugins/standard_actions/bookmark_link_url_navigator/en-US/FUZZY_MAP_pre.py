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

# from pathlib import Path as p;import os as o

# with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





FUZZY_MAP_pre = [


    # EXAMPLE: CCC events events Tübingen

    ('https://events.ccc.de/search/?s=T%C3%BCbingen', r'^(CCC)\s*Events\s*(events Tübingen)?$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bitsundso website bus982

    # EXAMPLE: bus982

    ('https://www.bitsundso.de/bus982/transcript/', r'^(bus982)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bits and so mastodon

    # EXAMPLE: bitsundso b mastodonx s

    ('https://mastodon.social/@bitsundso', r'^bits and so on\b\s*(mastodon\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bits and so mastodon

    # EXAMPLE: bitsundso b tchncsx s

    ('https://social.tchncs.de/@bitsundso@mastodon.social', r'^bits and so on\b\s*(tchncs\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),



    # bits and so Bluesky

    # EXAMPLE: bitsundso b Blueskyx s

    ('https://mastodon.social/@bitsundso', r'^bits and so on\b\s*(Bluesky\w*)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bitsundso imprint

    # EXAMPLE: bitsundso b imprint p

    ('https://www.bitsundso.de/impressum/', r'^bits and so on\b\s*(imprint)\s*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # bitsandso Email

    # EXAMPLE: bitsundso b Email s

    ('info@undsoversum.de', r'^bits and so on\b\s*(E-mail)\s*$', 70, # min_accuracy
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


    # EXAMPLE: lively x

    ('https://regex101.com/', r'^(?:brisk?x|reg ex|regex101|regex 101|reg-?ex101|reg\-?ex|reg ex|expression|regular expression|reg(ular)?exp|reg(e|ä)x|reschex|resh-ex|reschex101|regex\s*tester|regexp\s*tester|regex\s*test|regex\s*page|regex\s*page|regecks|regeks|regeks101|regex page|regexportal|regextool|regex\s*on-line|on-line\s*regex|regex\s*help(e|en)|regex\s*help|regex\s*website|regex\s*website)\s*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),




    # Non-capturing group (?:test)


    # EXAMPLE: Colorful bookstore events

    ('https://www.bunterbuchladen.de/veranstaltungen', r'^(Colorful|Down)\s*(Bookstore)\s*(Events)$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),



]
