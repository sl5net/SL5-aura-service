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

readme = """
source .venv/bin/activate
pip install --upgrade pip
python3 -m pip install --break-system-packages wikipedia-api --upgrade

Arch-Users:
yay -S translate-shell
Sync Explicit (1): translate-shell-0.9.7.1-2
warning: translate-shell-0.9.7.1-2 is up to date -- reinstalling
Packages (1) translate-shell-0.9.7.1-2
Total Installed Size:  0.24 MiB


"""


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    # The regex capture groups will look for the book name ("Johannes") and the numbers ("3", "16").

# Suche in Johannes Kapitel 3 Vers schlechtThe external Bible service is currently unreachable (HTTP 404).

#The external Bible service is currently unreachable (HTTP 404).
#Reference John 3:16 (King James Version): For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.
#

# Suche im New Hadith Kapitel 3 Vers schicken
#Suche in Johannes fährt 3 Vers 16



    #home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py
    ('',
     r'^(Clipboard|Zwischenablage|Zeile\w*|Text neu) (nummeriere\w*|suggerieren|dumme geritten|operieren|nummerieren|nummerieren)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
     }),

    ('', r'^(Zeile\w* nummeriere\w*|Zeilen suggerieren|Zeile dumme geritten|zeile\w* operieren|Text neu nummerieren|Zwischenablage nummerieren|Laufende Zeilennummern einfügen|Zeilennummern aktualisieren|teile reparieren|keine nummerieren|Zeilesuggerieren)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
    }),


    #Google ein StudioGoogle my styleGoogle ist StudioGoogle StückGoogle my style
    # google g bedeuten
    # google gebe drei
    ('https://aistudio.google.com/prompts/new_chat', r'^(gemini|cheminée|Google Jimmy|Gucke chapiteau|Google Tribüne|Google Termine|google ari studio|Google Aviv|google gewinnt|Google ein Studio|google it studio|google \w+ studio|google my style|Google ein Studie|Google leicht|Google ein Stuhl|Google eingestuft|google gb day|google kapital|Google kriminell|google gebiet\w*|Gucke gebiet\w*|google g b day|google geht wieder|gucke dir bitte|google g bitte|gucke gemini\s*\w*|google gemini ein|google gemini\s*\w*|google gemini recht|Gucke Gehminuten|Google Gewinde|Google Gehminuten|gut \w*minarett|brooke kriminelle|google gaming|google grimmen\s*.*|google grimmig|Google Germany|Google feminin|Google Gewinnern|Google gewinne|Google wieder|google g bedeuten|google gebe drei|google gb daten|google gewinn ein|google gebe dein|google kriminelle|google gewitter|google b day|Google g wie neu)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),


    ('https://aistudio.google.com/prompts/new_chat', r'^chat mit\s+(gemini|cheminée|chip|Kevin)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),



    ("('Rückgabe', r'Suche', 70, {'flags': re.IGNORECASE}),",
     r'^(Neue)\s+(Regel|RegEx)$',
     70, {'flags': re.IGNORECASE}),

    #Neue regelNeue regelNeue regelwohnlich neuerenix', r'pattern', 70, {'flags': re.IGNORECASE}),'


#gewinne




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

#

    # ('', r'OFFFFFFFFFFFFF mobed to other to --->post wannweil map (suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) (.*)', 90, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'wiki_search.py']}),


# (?P<book>\w*[ ]?\w+) kapitel (?P<chapter>\d+) [vfdph]\w+ (?P<verse>\d+)$', 90, {

    ('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),


    #Hallo wie geht's'

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


    # Benötigt eigentlich keine übersetzung funktioniert auch so schon (15.11.'25 13:48 Sat)
    ('konsole', r'^(Konsole)$', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),
    ('konsole', r'\b(Konsole)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),
    ('regex', r'\b(krieg x|rekik|mike x|rick x|Recaps)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),



    ('ip a', r'\b(Show IP)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),



    ('TestFuzzyNiemalsMatchen', r'\b(diesesRegexWirdNiemalsMatchen123ABC)\b', 75, {'flags': re.IGNORECASE}),


    # ('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) ([a-z]+.*)', 90, {
    # 'flags': re.IGNORECASE,
    # 'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    # }),


]

