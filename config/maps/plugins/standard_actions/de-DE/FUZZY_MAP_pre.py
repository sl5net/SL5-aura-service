# config/maps/plugins/.../de-DE/FUZZY_MAP_pr.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    # Regel für die WetterabfrageGoogle Jimmy datenGoogle ja bedeutenGoogle ja wiederGucke chapiteau a
    #Google TribüneGoogle Termine Google arm StudioTestGoogle eiche Stühlen TestGoogle Aviv du
    # Gucke gebiete
    # google gemini a chat mit cheminée

    #Google ein StudioGoogle my styleGoogle ist StudioGoogle StückGoogle my style
    ('https://aistudio.google.com/prompts/new_chat', r'^(gemini|cheminée|Google Jimmy|Gucke chapiteau|Google Tribüne|Google Termine|google ari studio|Google Aviv|google gewinnt|Google ein Studio|google it studio|google \w+ studio|google my style|Google ein Studie|Google leicht|Google ein Stuhl|Google eingestuft|google gb day|google kapital|Google kriminell|google gebiet\w*|Gucke gebiet\w*|google g b day|google geht wieder|gucke dir bitte|google g bitte|gucke gemini\s*\w*|google gemini ein|google gemini\s*\w*|google gemini recht|Gucke Gehminuten|Google Gewinde|Google Gehminuten|gut \w*minarett|brooke kriminelle|google gaming|google grimmen\s*.*|google grimmig|Google Germany|Google feminin|Google Gewinnern|Google wieder)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

    ('https://aistudio.google.com/prompts/new_chat', r'^chat mit\s+(gemini|cheminée|chip|Kevin)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

#




    ('https://pi.ai/talk', r'^(Chat) mit (der e|AI|Terry|frei|ei|it|ari|3|a|der a)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

#https://aistudio.google.com/prompts/new_chat

    # Regel für Python coding short
    ('', r'^(compact_python|Kompakt fein|Kompakt Brighton|Kompakt bei)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'compact_python.py']
    }),


    # Regel für die Wetterabfrage
    ('', r'\b(wie (wird|ist)\b.*\bwetter|wetterbericht|wettervorhersage)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'weather.py'] # Passe den Pfad ggf. an
    }),



    # arabisch
    #
    #Olá, como vai (original:'hallo wie geht's', Tradução de Voz SL5.de/Aura ).


    ('ar', r'^(arabisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),




#

    ('pt-BR', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (portugiesisch|Portugiesen|portugiese\w*)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    ('pt-BR', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|ein|einschalten|abs\w*|deaktivieren|ausschalten|ausschau|toggle|Dogge|doppelt)\b', 95, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    # Englisch
    ('en', r'^(Denglisch|englisch|english\w*|Wisch) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
    ('en', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (Denglisch|Englisch|ennglish\w*)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    ('de', r'^(\w*besetzung) (Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    ('de', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (\w*besetzung)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),


    #

    # ANCHOR: The following line is controlled by the toggle script.
    # best disable before run self-tester rules like: match all to nothing. like: .+ -> or .* -> ''
    # TRANSLATION_RULE
#    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),


    ('', r'\b(gute nacht|schlaf gut|ich geh ins bett)\b', 95, {
        'flags': re.IGNORECASE,
        # Ruft unser neues Skript auf
        'on_match_exec': [CONFIG_DIR / 'good_night.py']
    }),

    #

    ('anrede', r'^(anrede|begrüßung|neue email|Neue E-Mail|Schreibe anrede\w*|Schreibe begrüßung)$', 95, {
        'flags': re.IGNORECASE,
        # Ruft unser neues Skript auf
        'on_match_exec': [CONFIG_DIR / 'greeting_generator.py']
    }),

    ('', r'^uhr\w+', 75, {'flags': re.IGNORECASE,
                          'on_match_exec': [CONFIG_DIR / 'get_current_time.py'] }),

    # Die Regex fängt zwei Zahlen (\d+) und einen Operator (plus|minus|mal|geteilt)
    ('', r'was ist (\d+)\s*(plus|minus|mal|geteilt durch)\s*(\d+)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'calculator.py']
    }),
# Das Ergebnis von 5 plus 3 ist 8.


    ('', r'OFFFFFFFFFFFFF mobed to other to --->post wannweil map (suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) (.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    }),



    ('add to einkaufsliste', r'\b(.+) (zur|in die) einkaufsliste\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
    }),

    # Regel zum Anzeigen
    ('', r'zeige die einkaufsliste', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
    }),



    # --- Rule for the Chess Commentator ---
    # This rule listens for various forms of negative self-talk during a game.
    ( 'schach_kommentator_negativ', r'^\b(fehler|mist|So ein Mist|verdammt|scheiße|blöd|dumm|idiot|nicht aufgepasst|ärgerlich|ach komm|das wars|verloren|ich geb\w? auf)\b$', 90, { 'flags': re.IGNORECASE, 'on_match_exec': [CONFIG_DIR / 'chess_commentator.py'] }),


    ('TestFuzzyNiemalsMatchen', r'\b(diesesRegexWirdNiemalsMatchen123ABC)\b', 75, {'flags': re.IGNORECASE}),


    ('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) ([a-z]+.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    }),


]

