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

# config/maps/plugins/ai/gemini/de-DE/FUZZY_MAP_pre.py

import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
CONFIG_DIR = p(__file__).parent

_misc_errors = (
    r'(?:ruhr area|groupware|udp\s+please|ready|babybay|babydoll|jubilee|privilege|'
    r'test|every day|give\s+three|give\s+your|gb\s+data)'
)
_studio_variants = r'(?:study[ao]\w*|seminar\w*|style|chair|capital|aviv|chapiteau|Bremen)'
geminiUrl = 'https://aistudio.google.com/prompts/new_chat'

_google_prefix = r'(?:google|google it?|gogol|look|look[n\s]*|goris|good|gb|balls|brooke|coral|cool|although)'
_gemini_phonetics = (
    r'(?:gemini|Emily|committees|cheminée|g[\s-]?mine|minutes walk|go\s+with|gives|gaming|criminal\w*|'
    r'appointment\w*|Jimmy\s*(?:no|knight|lay|new)|germany|feminine|winner\w*|'
    r'profit\s+a|ge[mw]\w*|g\s+mean|g\s+How\s+new|seminar\w*)'
)
_common_metaVERBOSE = {
    'command_flags': re.IGNORECASE | re.VERBOSE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Chrome', r'Brave', r'FUZZY_MAP_pre', r'Kate', r'CudaText', r'xed'],
    'exclude_windows': [r'element', r'mastodon', r'GitHub', r'Claude', r'Google AI'],
}
_common_meta = {
    'command_flags': re.IGNORECASE,
    'window_ignore_case': False,
    'only_in_windows': [r'Mozilla Firefox', r'Chrome', r'Brave', r'FUZZY_MAP_pre', r'Kate', r'CudaText', r'xed'],
    'exclude_windows': [r'element', r'mastodon', r'GitHub', r'Claude', r'Google AI'],
}
FUZZY_MAP_pre = [

    # EXAMPLE: AI notebook notebook arm

    ('https://notebooklm.google', r'^notebook (lm|ai|arm)( google)?$', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: AI deepseek

    ('https://chat.deepseek.com/', r'^deepseek?$', 75, {'command_flags': re.IGNORECASE}),



    # kimi Chinese AI company Particularly good at: processing long texts




    # EXAMPLE: AI kimi chat

    ('https://www.kimi.com/en/', r'^(ai\s*)?Kimi( chat)?$', 75, {'command_flags': re.IGNORECASE}),



    # EXAMPLE: google gemini

    (f'{geminiUrl}', r'^(google gemini|google goes not|google minutes walk|google laminate|google germany|google gemini ring|cake gemini|google camille|google mobile|google b d|google win|google determine|look please|uri gemini|google criminal|google reduced|google g less|google wins|Rülke Bible|google baby|google pay please|google gb d|google thread|google gemini|google g miller|google image|google every day|google gaming|google gravity|google give the|google webinar|google g b|google give|google give d|google please|google give it|google g please|google would exist the|google gives|Gary Hewitt|google area|google tangy|google goes|gucci baby|google command|groupwise we ask|correctly please|google g b d|coric her baby|peep cebit|google vortex d|koppe gravity|google goes again|look away give d|look Yes please|cuckoo here please|cosi baby|look me please|cookies here please|google jubilee|google really|google give this|look we please|look give she|look give d|cookies hand over|cuckoo her baby|cuckoo www|bird flu|google g b day|luminary please|google areas|look we again|look we please|cuckold who again|cuckoo replied|luminary baby|group give|look How please|cuckoo love d|cuckoo away|googled her baby|curry gemini|google her baby|cucumber her baby|uwe tissue|google appointments|google credit|cuckoo Evi d|Ulrike b through|google everyone please|google becomes|google g mine|google Bible|look you How new|OK Jimmy|Oh good Ginny|uwe g d|google kiwi|goes again|hotel give|colleague again|google formed|google pay day|gucci win|balls seminar|look gemini|now but|reno tap|google profit|gofeminine|googles menu|cube seminar|google to grow fond of|google chair|google study|look gives|google insights|growth height minutes walk|look give|per gun mine|look win|google appointments a)$', 70, _common_meta),



    # 2. activate this rule (behind the first rain you want to optimize)


    # EXAMPLE: geminiUrl

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

    # EXAMPLE: AI Studio

    (f'{geminiUrl}', rf'''(?ix)
    ^ chat\ mit\s+ (?:
        {_gemini_phonetics} |
        chip | Kevin | Boot\ Gaming\ nein
    ) \b.*$
    ''', 70, _common_metaVERBOSE),

]
