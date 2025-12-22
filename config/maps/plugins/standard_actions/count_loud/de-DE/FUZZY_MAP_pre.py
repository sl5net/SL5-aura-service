# config/maps/plugins/standard_actions/count_loud/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401


FUZZY_MAP_pre = [

    # bitsundso website bus982
    # EXAMPLE: bus982 s
    ('https://www.bitsundso.de/bus982/transcript/', r'^(bus982)\s*$', 70, {'flags': re.IGNORECASE}),

    # bitsundso mastodon
    # EXAMPLE: bitsundso b s mastodonx s
    ('https://mastodon.social/@bitsundso', r'^bitsundso\b\s*(mastodon\w*)\s*$', 70, {'flags': re.IGNORECASE}),

    # bitsundso mastodon
    # EXAMPLE: bitsundso b s tchncsx s
    ('https://social.tchncs.de/@bitsundso@mastodon.social', r'^bitsundso\b\s*(tchncs\w*)\s*$', 70, {'flags': re.IGNORECASE}),



    # bitsundso Bluesky
    # EXAMPLE: bitsundso b s Blueskyx s
    ('https://mastodon.social/@bitsundso', r'^bitsundso\b\s*(Bluesky\w*)\s*$', 70, {'flags': re.IGNORECASE}),

    # bitsundso impressum
    # EXAMPLE: bitsundso b s impressum s
    ('https://www.bitsundso.de/impressum/', r'^bitsundso\b\s*(impressum)\s*$', 70, {'flags': re.IGNORECASE}),

    # bitsundso Email
    # EXAMPLE: bitsundso b s Email s
    ('info@undsoversum.de', r'^bitsundso\b\s*(Email)\s*$', 70, {'flags': re.IGNORECASE}),


    # EXAMPLE: Radio wüste welle livex
    ('https://www.wueste-welle.de/broadcasts/livestream', r'^(Radio wüste welle live\w*|wüste welle live\w*)\s*$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: Radio wüste welle
    ('https://www.wueste-welle.de/', r'^(Radio wüste welle|wüste welle)\s*$', 70, {'flags': re.IGNORECASE}),


    # EXAMPLE: LORA Münchenx
    ('https://lora924.de/livestream/live-horen/', r'^(LORA München\w*)\s*$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: Freies Radio  Stuttgart
    ('https://www.freies-radio.de/', r'^(Freies Radio .*Stuttgart)\s*$', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: Archiv Freies Radio  Stuttgart
    ('https://www.youtube.com/gbsstuttgart', r'^(Archiv Freies Radio .*Stuttgart)\s*$', 70, {'flags': re.IGNORECASE}),


    # EXAMPLE: rege x
    ('https://regex101.com/', r'^(?:rege?x|reg ex|regex101|regex 101|reg-?ex101|reg\-?ex|reg ex|expression|regularexpression|reg(ular)?exp|reg(e|ä)x|reschex|resch-ex|reschex101|regex\s*tester|regexp\s*tester|regex\s*test|regex\s*seite|regex\s*seite|regecks|regeks|regeks101|regexseite|regexportal|regextool|regex\s*online|online\s*regex|regex\s*hilf(e|en)|regex\s*hilfe|regex\s*webseite|regex\s*website)\s*$', 60, {'flags': re.IGNORECASE}),

    # Non-capturing group (?:test)

    # EXAMPLE: Bunter Buchladen Veranstaltungen
    ('https://www.bunterbuchladen.de/veranstaltungen', r'^(Bunter|Runter)\s*(Buchladen)\s*(Veranstaltungen)$', 60, {'flags': re.IGNORECASE}),



]
