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


Very usefull:
Restart sequence:
Stop Streamlit (port 8831):
    fuser -k 8831/tcp
Stop Uvicorn (port 8830):
    fuser -k 8830/tcp
    
fuser -k 8830/tcp;fuser -k 8831/tcp
...


"""


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    # The regex capture groups will look for the book name ("Johannes") and the numbers ("3", "16").

    #curl -s checkip.dyndns.org | grep -Eo '[0-9\.]+''
    #was ist meine ip
    # Wie ist meine IP Adresse
    ("curl -s checkip.dyndns.org | grep -Eo '[0-9\\.]+'  ",
     # EXAMPLE: wie
     r'^(wie|was)( ist meine).*(IP|IP-Adresse|IP Adresse)$',
     100, {
         'flags': re.IGNORECASE,
     }),

    #Start de Wikipedia
    #config/maps/plugins/standard_actions/de-DE/kiwix-docker-start-if-not-running.sh
    ("config/maps/plugins/standard_actions/de-DE/kiwix-docker-start-if-not-running.sh",
     # EXAMPLE: starte
     r'^(starte|Start de ).*(kiwix|Wikipedia)$',
     100, {
         'flags': re.IGNORECASE,
     }),

    # http://89.244.126.237:8831/
    # Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps - in only a few lines of code.
    #Öffnet Stream lädt Webseite
    #Öffne Stream Litschi
    #öffne stream litt
    #Essen ist ziemlichÖffentlich Stream lebt
    #http://89.244.126.237:8831/
    ("http://89.244.126.237:8831/",
     # EXAMPLE: öffne
     r'^(öffne|öffentlich).*(der )?(stream)(lit|life| litt| Lied| neu| net| lebt| lebt| liebt)\s*(webseite|webpage)?$',
     100, {
         'flags': re.IGNORECASE,
     }),

    #Starte Streamlit

     #streamlit run /home/seeh/projects/py/STT/scripts/py/chat/streamlit-chat.py --server.port 8831
    ("streamlit run /home/seeh/projects/py/STT/scripts/py/chat/streamlit-chat.py --server.port 8831",
     # EXAMPLE: starte
     r'^(starte|statt|state|stabiles).*(der )?(stream)(lit|life| litt| Lied| neu| net| lebt| lebt| liebt| List)$',
     100, {
         'flags': re.IGNORECASE,
     }),


    # python3 scripts/py/cli_client.py "Was ist ein Haus" --lang "de-DE"
    ('python3 scripts/py/cli_client.py "Was ist ein Haus" --lang "de-DE"',
     # EXAMPLE: frage   client
     r'^(frage)\b.*(client)$',
     100, {
         'flags': re.IGNORECASE,
     }),



    ('',
     # EXAMPLE: Clipboard
     r'^(Clipboard|Zwischenablage|Zeile\w*|Text neu) (nummeriere\w*|suggerieren|dumme geritten|operieren|nummerieren|nummerieren)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
     }),
    ('',
     # EXAMPLE: nummerierex
     r'^(nummeriere\w*|suggerieren|dumme geritten|operieren|nummerieren|nummerieren)\b\s*(?:!die)?(Clipboard|Zwischenablage|Zeile\w*|Text neu)$',
     70, {
         'flags': re.IGNORECASE,
         'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
     }),

    # EXAMPLE: Zeilex nummerierex
    ('', r'^(Zeile\w* nummeriere\w*|Zeilen suggerieren|Zeile dumme geritten|zeile\w* operieren|Text neu nummerieren|Zwischenablage nummerieren|Laufende Zeilennummern einfügen|Zeilennummern aktualisieren|teile reparieren|keine nummerieren|Zeilesuggerieren)$', 70, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'renumber_clipboard_text.py']
    }),


    #Google ein StudioGoogle my styleGoogle ist StudioGoogle StückGoogle my style
    # google g bedeuten
    # google gebe drei
    # coral gaming nein
    # EXAMPLE: gemini
    ('https://aistudio.google.com/prompts/new_chat', r'^(gemini|cheminée|Google Jimmy|Gucke chapiteau|Google Tribüne|Google Termine|google ari studio|Google Aviv|google gewinnt|Google ein Studio|google it studio|google \w+ studio|google my style|Google ein Studie|Google leicht|Google ein Stuhl|Google eingestuft|google gb day|google kapital|Google kriminell|google gebiet\w*|Gucke gebiet\w*|google g b day|google geht wieder|gucke dir bitte|google g bitte|gucke gemini\s*\w*|google gemini ein|google gemini\s*\w*|google gemini recht|Gucke Gehminuten|Google Gewinde|Google Gehminuten|gut \w*minarett|brooke kriminelle|google gaming|google grimmen\s*.*|google grimmig|Google Germany|Google feminin|Google Gewinnern|Google gewinne|Google wieder|google g bedeuten|google gebe drei|google gb daten|google gewinn ein|google gebe dein|google kriminelle|google gewitter|google b day|Google g wie neu|coral gaming nein)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),
    #

    # EXAMPLE: chat mit gemini
    ('https://aistudio.google.com/prompts/new_chat', r'^chat mit\s+(gemini|cheminée|Boot Gaming nein|chip|Kevin)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),



    # EXAMPLE: Suche
    ("('Rückgabe', r'Suche', 70, {'flags': re.IGNORECASE}),",
     # EXAMPLE: Neue Regel
     r'^(Neue)\s+(Regel|RegEx)$',
     70, {'flags': re.IGNORECASE}),

    #Neue regelNeue regelNeue regelwohnlich neuerenix', r'pattern', 70, {'flags': re.IGNORECASE}),'


#gewinne




    # EXAMPLE: Chat mit der e
    ('https://pi.ai/talk', r'^(Chat) mit (der e|AI|Terry|frei|ei|it|ari|3|a|der a)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

#https://aistudio.google.com/prompts/new_chat

    # Regel für Python coding short
    # EXAMPLE: compact_python
    ('', r'^(compact_python|Kompakt fein|Kompakt Brighton|Kompakt bei)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'compact_python.py']
    }),


    # Regel für die Wetterabfrage
    # EXAMPLE: wie wird
    ('', r'\b(wie (wird|ist)\b.*\bwetter|wetterbericht|wettervorhersage)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'weather.py'] # Passe den Pfad ggf. an
    }),


    # EXAMPLE: anrede
    ('anrede', r'^(anrede|begrüßung|neue email|Neue E-Mail|Schreibe anrede\w*|Schreibe begrüßung)$', 95, {
        'flags': re.IGNORECASE,
        # Ruft unser neues Skript auf
        'on_match_exec': [CONFIG_DIR / 'greeting_generator.py']
    }),

    # EXAMPLE: uhrtext
    ('', r'^uhr\w+', 75, {'flags': re.IGNORECASE,
                          'on_match_exec': [CONFIG_DIR / 'get_current_time.py'] }),

    # Das Ergebnis von 5 plus 3 ist 8.

    # Die Regex fängt zwei Zahlen (\d+) und einen Operator (plus|minus|mal|geteilt)
    # EXAMPLE: rechne
    ('', r'(?:rechne|was ist|was is|was)\s*(\d+)\s*([\+\-\*\/]|plus|minus|mal|geteilt durch)\s*(\d+)', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'calculator.py']
    }),


    # Die Regex fängt zwei Zahlen (\d+) und einen Operator (plus|minus|mal|geteilt)
#     ('', r'(rechne|was ist|was is|was) (\d+)\s*(plus|minus|mal|geteilt durch)\s*(\d+)', 95, {
#         'flags': re.IGNORECASE,
#         'on_match_exec': [CONFIG_DIR / 'calculator.py']
#     }),
# # Das Ergebnis von 5 plus 3 ist 8.

#


    # ('', r'OFFFFFFFFFFFFF mobed to other to --->post wannweil map (suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) (.*)', 90, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'wiki_search.py']}),




    # EXAMPLE:   Wer ist s der Beste x Schachspieler 
    ("Sebastian Lauffer aus Wannweil (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?(Beste[\w]? Schachspieler.*)$', 90, {
    'flags': re.IGNORECASE
    }),

    # EXAMPLE:   Wer ist s der s herr s schröer
    ("Herr Schröer ist ein netter, bisschen vergesslicher, Ergotherapeut. (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?\s*(herr)?\s*\b(schröer)$', 90, {
    'flags': re.IGNORECASE
    }),


    #



    # EXAMPLE: Computer
    ("was ist ein (Begriffsklärung)", r'^(?!Computer|Aura).*was ist ein ', 90,
     {
    'flags': re.IGNORECASE,
    'skip_list': ['LanguageTool','fullMatchStop'],
    }),

    # EXAMPLE:  was ist ein haus
    ("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
     {
    'flags': re.IGNORECASE,
    'skip_list': ['LanguageTool','fullMatchStop'],
    }),

    # EXAMPLE: Computer
    ('', r'^(?!Computer|Aura).*(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der| Herr)? (?P<search>.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),

    #



    # EXAMPLE:   zur
    ('add to einkaufsliste', r'\b(.+) (zur|in die) einkaufsliste\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
    }),

    # Regel zum Anzeigen
    # EXAMPLE: zeige die einkaufsliste
    ('', r'zeige die einkaufsliste', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
    }),



    # --- Rule for the Chess Commentator ---
    # This rule listens for various forms of negative self-talk during a game.
    # EXAMPLE: fehler
    ( 'schach_kommentator_negativ', r'^\b(fehler|mist|So ein Mist|verdammt|scheiße|blöd|dumm|idiot|nicht aufgepasst|ärgerlich|ach komm|das wars|verloren|ich geb\w? auf)\b$', 90, { 'flags': re.IGNORECASE, 'on_match_exec': [CONFIG_DIR / 'chess_commentator.py'] }),


    # Benötigt eigentlich keine übersetzung funktioniert auch so schon (15.11.'25 13:48 Sat)
    # EXAMPLE: Konsole
    ('konsole', r'^(Konsole)$', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),
    # EXAMPLE: Konsole
    ('konsole', r'\b(Konsole)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),
    # EXAMPLE: krieg x
    ('regex', r'\b(krieg x|rekik|mike x|rick x|Recaps)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),



    # EXAMPLE: Show IP
    ('ip a', r'\b(Show IP)\b', 95, {
        'flags': re.IGNORECASE,
        'skip_list': ['LanguageTool']
    }),



    # EXAMPLE: diesesRegexWirdNiemalsMatchen123ABC
    ('TestFuzzyNiemalsMatchen', r'\b(diesesRegexWirdNiemalsMatchen123ABC)\b', 75, {'flags': re.IGNORECASE}),


    ('', '^(?!Computer|Aura).*(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) ([a-z]+.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    }),


]

