# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pr.py
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

Englisch=r'\b(Denglisch|englisch\w*|english\w*|Wisch|nische|Irgendwelche|irgendwie|sprach.*gabe|ähnlich)\b'
toggleCmd=r'(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|einchecken|abschalten|stopp\w*|stop|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)'

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    ('en', fr'^{Englisch} {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    ('en', fr'^{toggleCmd} {Englisch}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    ('ja', fr'^(japanisch) {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    ('fa', r'^(persisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    ('pt-BR', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (portugiesisch|Portugiesen|portugiese\w*)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    ('pt-BR', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    ('es', r'^(Spanien|spanisch|starr dich|sparr dich) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)$', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),



    ('de', r'^(\w*besetzung) (modus )? (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    ('de', r'^(\w*besetzung) (modus )? (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    ('de', fr'^(\w*sprach\w*) (übersetzung)? {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    #


    ('de', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (\w*besetzung)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # ANCHOR: The following line is controlled by the toggle script.
    # best disable before run self-tester rules like: match all to nothing. like: .+ -> or .* -> ''
    # TRANSLATION_RULE
#    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),


    ('', r'\b(gute nacht|schlaf gut|ich geh ins bett)\b', 95, {
        'flags': re.IGNORECASE,
        # Ruft unser neues Skript auf
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),


]

