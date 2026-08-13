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

# config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

# language handing stop



readme = """
'Translate Shell .. is a versatile and powerful command-line translator that leverages the translation services of major providers like

Google Translate,
DeepL, and
Microsoft Translator.

Its design prioritizes ease of use and extensibility, making it an ideal companion for Linux and other Unix-like operating systems'
(10.11.'25 18:58 Mon, https://itsfoss.gitlab.io/post/how-to-use-google-translate-from-commandline-in-linux/ )

Arch-Users may use:
source .venv/bin/activate
pip install --upgrade pip
yay -S translate-shell


here's a list of common language codes you want use:

    en: English
    de: German
    jp: Japanese
    pr-br: Brazilian Portuguese
    fr: French
    es: Spanish
    it: Italian
    pt: European Portuguese
    ru: Russian
    nl: Dutch
    zh-CN: Chinese (Simplified)
    zh-TW: Chinese (Traditional)
    pl: Polish
    tr: Turkish
    sv: Swedish
    da: Danish
    no: Norwegian
    fi: Finnish
    cs: Czech
    hu: Hungarian
    ro: Romanian
    gr: Greek
    th: Thai
    ko: Korean
    ar: Arabic
    he: Hebrew
    hi: Hindi
    id: Indonesian
    ms: Malay

You can find a comprehensive list of language codes in the
ISO 639-1
ISO 15897
standards.

"""


CONFIG_DIR = Path(__file__).parent

nonsense_start_word = r'(?:(to|a|one|a|eat)\s*)?'

# EXAMPLE: Denglish

Englisch = fr'{nonsense_start_word}(Denglish|English\w*|english\w*|finally|Wipe|niche|Any|somehow|spoke.*gabe|similar)\b\s*'
# EXAMPLE: Switch

toggleCmd=r'\s*(Switch|Activate|activate|activated|active|turn on|check in|switch off|abolish|farewell|stop\w*|Stop|deactivate|deactivate|turn off|look out|toggle)\s*'

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.


    # EXAMPLE: Activate English

    ('en', fr'^{Englisch}{toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Turn on French

    ('fr', fr'^(französisch) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Thai switch

    ('th', fr'^(Thai|Tai|hi|At) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Japanese Switch

    ('ja', fr'^(Japanese) {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Arabic Switch

    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Persian Switch

    ('fa', r'^(Persian) (Switch|Activate|activate|activated|active|turn on|deactivate|deactivate|turn off|look out|toggle)', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Portuguese Switch

    ('pt-BR', r'^(Switch|Activate|activate|activated|active|turn on|deactivate|deactivate|turn off|look out|toggle) (Portuguese|Portuguese|Portuguese\w*)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: Portuguese Switch

    ('pt-BR', r'^(Portuguese) (activate|activated|active|a|turn on|abs\w*|deactivate|turn off|look out|toggle|Great Dane|double)\b', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Spain Switch

    ('es', r'^(Spain|Spanish|rigid you|sparr you) (activate|activated|active|a|turn on|abs\w*|deactivate|turn off|look out|toggle|Great Dane|double)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # Afghan toggle

    # EXAMPLE: Afghan

    ('Dari', r'^(Afghan|Afghanistan|Organic) (activate|activated|active|a|turn on|abs\w*|deactivate|turn off|look out|toggle|Great Dane|double)$', 95, {
         'command_flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # Activate organically گرمایش را خاموش کنید (original: 'switch off heating').



    # EXAMPLE: translation: turn off deactivate toggle

    ('de', r'^(\w*translation|heating|earnings estimates) (deactivate|deactivate|turn off|switch off|look out|toggle)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # translation on off

    # EXAMPLE: turn off translation

    ('de', r'^(\w*translation|heating|for the) (mode )? (Switch|Activate|activate|activated|active|turn on|deactivate|deactivate|turn off|switch off|look out|toggle)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: translation Switch

    ('de', r'^(\w*occupation\w*) (mode )? (Switch|Activate|activate|activated|active|turn on|deactivate|deactivate|turn off|look out|toggle)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: translation toggle

    ('de', fr'^(\w*spoke\w*) (translation\w*)? {toggleCmd}$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: translation toggle

    ('de', r'^(Switch|Activate|activate|activated|active|turn on|deactivate|deactivate|turn off|look out|toggle) (\w*translate\w*)\b.*$', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Good night

    ('', r'\b(good night|sleep good|I go into the bed)\b', 95, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),


    # config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py

    # ANCHOR: The following line is controlled by the toggle script.

    # best disable before run self-tester rules like: match all to nothing. like: .+ -> or .* -> ''

    # TRANSLATION_RULE

     # ('', r'.+', 5, {'command_flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),


]
