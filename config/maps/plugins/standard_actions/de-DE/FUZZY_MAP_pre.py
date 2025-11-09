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

# englische einschalten
#

Englisch=r'(Denglisch|englisch\w*|english\w*|Wisch|nische)'

toggleCmd='(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|einchecken|abschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle)'

#Switch on English (original:'english einschalten', Voice Translation SL5.de/Aura ).
#Hello, how are you (original:'hallo wie geht's', Voice Translation SL5.de/Aura ).
#englisch einenglisch einEnglische einschalten

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    # Englisch Nische einchecken
    # nische einchecken
    ('en', fr'^{Englisch} {toggleCmd}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # english abschalten

    ('en', fr'^{toggleCmd} {Englisch}$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),

    # bersetzung modus ausschalten
    #


# lkjlkjteile reparierenteile reparieren
#Teile reparierenAlternativekeine nummerieren
#Teile reparierenAlternativekeine nummerieren 2 lep nummerieren
#enzeilen operieren
# CMD_RENUMBER_CLIP
# CMD_RENUMBER_CLIP
# command
#Zeile nummeriereKonsole-Befehl: /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py


# johannes 3 16
#johannes 3 16 johannes 3 16
# johannes drei sechzehnHier hat es 3010 johannes 3 16
#ihr hört es 3 60johannes 3 16Früher hatte ich 30 SSWIhr hattet 3 schwächt sie
#John 3:16: 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.'
#An unexpected error occurred during command processing: NameError.
#

    # Rule to trigger the Bible Quote Plugin





































    ('bible suche', r'^suche in (?P<book>.*) kapitel (?P<chapter>\d+) [vf]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_scraper.py']
    }),

    # Example Trigger: "suche in Johannes kapitel drei vers sechzehn"
    # The regex capture groups will look for the book name ("Johannes") and the numbers ("3", "16").

# Suche in Johannes Kapitel 3 Vers schlechtThe external Bible service is currently unreachable (HTTP 404).

#The external Bible service is currently unreachable (HTTP 404).
#Reference John 3:16 (King James Version): For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.


# Suche im New Hadith Kapitel 3 Vers schicken
#Suche in Johannes fährt 3 Vers 16




    ('', r'^(Zeile\w* nummeriere\w*|Zeilen suggerieren|Zeile dumme geritten|zeile\w* operieren|Text neu nummerieren|Zwischenablage nummerieren|Laufende Zeilennummern einfügen|Zeilennummern aktualisieren|teile reparieren|keine nummerieren|Zeilesuggerieren)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
    }),


    #Google ein StudioGoogle my styleGoogle ist StudioGoogle StückGoogle my style
    # google g bedeuten
    ('https://aistudio.google.com/prompts/new_chat', r'^(gemini|cheminée|Google Jimmy|Gucke chapiteau|Google Tribüne|Google Termine|google ari studio|Google Aviv|google gewinnt|Google ein Studio|google it studio|google \w+ studio|google my style|Google ein Studie|Google leicht|Google ein Stuhl|Google eingestuft|google gb day|google kapital|Google kriminell|google gebiet\w*|Gucke gebiet\w*|google g b day|google geht wieder|gucke dir bitte|google g bitte|gucke gemini\s*\w*|google gemini ein|google gemini\s*\w*|google gemini recht|Gucke Gehminuten|Google Gewinde|Google Gehminuten|gut \w*minarett|brooke kriminelle|google gaming|google grimmen\s*.*|google grimmig|Google Germany|Google feminin|Google Gewinnern|Google wieder|google g bedeuten)\b.*$', 70, {
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

    # spanisch
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

    # Das Ergebnis von 5 plus 3 ist 8.

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

