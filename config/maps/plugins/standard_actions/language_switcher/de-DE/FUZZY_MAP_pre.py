# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pr.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

Englisch=r'(Denglisch|englisch\w*|english\w*|Wisch|nische|Irgendwelche)'
toggleCmd='(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|einchecken|abschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)'

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


    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
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

