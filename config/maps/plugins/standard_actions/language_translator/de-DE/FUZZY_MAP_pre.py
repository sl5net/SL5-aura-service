# config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.
#sprache gabe stopp


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

# EXAMPLE: Denglisch
Englisch=r'\b(Denglisch|englisch\w*|english\w*|Wisch|nische|Irgendwelche|irgendwie|sprach.*gabe|ähnlich)\b'
# EXAMPLE: Switch
toggleCmd=r'(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|einchecken|abschalten|stopp\w*|stop|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)'

# englisch einschaltenGuten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).# EXAMPLE: hallo

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    # EXAMPLE: Englisch Switch
    ('en', fr'^{Englisch} {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: französisch einschalten
    ('fr', fr'^(französisch) {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Thai Switch
    ('th', fr'^(Thai|Tai|hi|Bei) {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: japanisch  Switch
    ('ja', fr'^(japanisch) {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: arabisch Switch
    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: persisch Switch
    ('fa', r'^(persisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Portuguese  Switch
    ('pt-BR', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (portugiesisch|Portugiesen|portugiese\w*)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: portugiesisch Switch
    ('pt-BR', r'^(portugiesisch) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: Spanien Switch
    ('es', r'^(Spanien|spanisch|starr dich|sparr dich) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)$', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # afghanisch toggle
    # EXAMPLE: afghanisch
    ('Dari', r'^(afghanisch|Afghanistan|Organisch) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)$', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    #Organisch aktivierenگرمایش را خاموش کنید (original:'heizung ausschalten').


    # übersetzung ein ausschalten
    # EXAMPLE: übersetzung ausschalten
    ('de', r'^(\w*besetzung|heizung|zum) (modus )? (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: übersetzung Switch
    ('de', r'^(\w*besetzung) (modus )? (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    # EXAMPLE: übersetzung toggle
    ('de', fr'^(\w*sprach\w*) (übersetzung)? {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # EXAMPLE: übersetzung toggle
    ('de', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (\w*besetzung)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # EXAMPLE: gute nacht
    ('', r'\b(gute nacht|schlaf gut|ich geh ins bett)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),


    # config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
    # ANCHOR: The following line is controlled by the toggle script.
    # best disable before run self-tester rules like: match all to nothing. like: .+ -> or .* -> ''
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),

]
