# config/maps/plugins/standard_actions/ai/gemini/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
CONFIG_DIR = p(__file__).parent

_misc_errors = (
    r'(?:ruhrgebiet|groupware|udp\s+bitte|ready|babybay|babydoll|jubilee|privileg|'
    r'test|everyday|gebe\s+drei|gebe\s+dein|gb\s+daten)'
)
_studio_variants = r'(?:studi[ao]\w*|seminar\w*|style|stuhl|kapital|aviv|chapiteau|bremen)'
geminiUrl = 'https://aistudio.google.com/prompts/new_chat'

_google_prefix = r'(?:google|googeln?|gogol|guck|gucke[n\s]*|goris|gut|gb|kugeln|brooke|coral|cool|obwohl)'
_gemini_phonetics = (
    r'(?:gemini|gremien|cheminée|g[\s-]?mine|gehminuten|gehe\s+mit|gibt|gaming|kriminell\w*|'
    r'termin\w*|jimmy\s*(?:nein|knight|lai|neu)|germany|feminin|gewinner\w*|'
    r'gewinn\s+ein|ge[hmw]\w*|g\s+bedeuten|g\s+wie\s+neu|seminar\w*)'
)
_common_metaVERBOSE = {
    'flags': re.IGNORECASE | re.VERBOSE,
    'only_in_windows': [r'firefox', r'chrome', r'brave', r'fuzzy_map_pre', r'kate'],
    'exclude_windows': [r'element', r'mastodon', r'Mastodon', r'github', r'claude', r'google ai'],
}
_common_meta = {
    'flags': re.IGNORECASE,
    'only_in_windows': [r'firefox', r'chrome', r'brave', r'fuzzy_map_pre'],
    'exclude_windows': [r'element', r'mastodon', r'Mastodon', r'github', r'claude', r'google ai'],
}
FUZZY_MAP_pre = [

    (f'{geminiUrl}', r'^(google geht nicht|google gehminuten|google laminat|google germany|google gemini ring|kuchen gemini|google camille|google mobile|google b d|google gewinne|google ermitteln|gucke bitte|uri gemini|google kriminelle|google gemindert|google g minder|google gewinnt|rülke bibel|google baby|google pay bitte|google gb d|google gewinde|google gemini|google g miller|google image|google everyday|google gaming|google gravity|google gebe die|google webinar|google g b|google gebe|google gebe d|google bitte|google gebe it|google g bitte|google gäbe die|google gibt|gary hewitt|google gebiet|google gerbig|google geht|gucci baby|google gebieten|groupwise wir bitten|korrekt bitte|google g b d|coric ihr baby|gucky cebit|google wirbel d|koppe gravity|google geht wieder|guck weg gebe d|gucke ja bitte|kuckuck hier bitte|cosi baby|gucke mir bitte|cookies hier bitte|google jubilee|google wirklich|google gebe dies|gucke wir bitte|gucke gebe sie|gucke gebe d|cookies übergeben|kuckuck ihr baby|kuckuck www|vogelgrippe|google g b day|koryphäe bitte|google gebiete|gucken wir wieder|gucken wir bitte|cuckold wer wieder|kuckuck erwidert|koryphäe baby|gruppe geben|gucke wie bitte|kuckuck liebe d|kuckuck weg|googelt ihr baby|curry gemini|google ihr baby|gurke ihr baby|uwe gewebe|google termine|google kredit|kuckuck evi d|ulrike b durch|google every bitte|google wird|google g mine|google bibel|gucke dir wie neu|okay jimmy|oh gut ginny|uwe g d|google kiwi|geht wieder|hotel geben|kollege wieder|google gebildet|google pay day|gucci gewinnen|kugeln seminar|gucke gemini|jetzt aber|reno tippen|google gewinn|gofeminin|googles menü|cube seminar|google liebgewinnen|google stuhl|google studie|gucke gibt|google insights|wuchshöhe gehminuten|gucke geben|pro gewehr mine|guck gewinne|google termine ein)$', 70, _common_meta),



    # 2. aktiviere diese Regel (hinter die erste regen die du optimieren willst)
    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[p(PROJECT_ROOT) / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),

    (f'{geminiUrl}', rf'''(?ix)
    ^ (?:
        {_gemini_phonetics} |                     # Gemini direkt
        {_misc_errors} |                         # Sonderfehler
        {_google_prefix} \s+ (?:                 # Google + Anhang
            {_gemini_phonetics} |
            {_studio_variants} |
            {_misc_errors} |
            geben\ ihnen\ ein | recht | \w*minarett | dir\ bitte | b[\s-]?day
        )
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

    # Eintrag für AI Studio (Block 3)
    (f'{geminiUrl}', rf'''(?ix)
    ^ chat\ mit\s+ (?:
        {_gemini_phonetics} |
        chip | Kevin | Boot\ Gaming\ nein
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

    # todo:
    # 09:58:10,526 - INFO   - 📢📢📢 ### kugel gemini a ###
    # 09:58:25,797 - INFO   - 📢📢📢 ### google ###
    # 09:58:42,008 - INFO   - 📢📢📢 ### google gemini ###



]
