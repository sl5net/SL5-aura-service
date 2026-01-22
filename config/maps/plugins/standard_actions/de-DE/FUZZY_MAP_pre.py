# config/maps/plugins/  /de-DE/FUZZY_MAP_pre.py
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

flake8 = 'source .venv/bin/activate;flake8 ./aura_engine.py ./scripts ./config'

FUZZY_MAP_pre = [


    # === VOSK NOISE FIX ===
    # Das kleine Vosk-Modell halluziniert oft "einen" bei Stille/Atmen.
    # Wenn der Input EXAKT nur "einen" ist, wird er ignoriert.
    # (Wer wirklich "einen" sagen will, sagt meist "Ich will einen..." -> das bleibt erhalten)
    # ('', r'^einen$', 100, {'flags': re.IGNORECASE}),

    #Ich will einen Apfeleinen einen

    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion!
    # - first is read first imported, lower rules maybe not get read.

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
    #config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh
    # config/maps/plugins/standard_actions/wikipedia_local/de-DE/
    ("config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh",
     # EXAMPLE: starte
     r'^(starte|Start de ).*(kiwix|Wikipedia)$',
     100, {
         'flags': re.IGNORECASE,
     }),

    # http://___:8831/
    # Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps - in only a few lines of code.
    #Öffnet Stream lädt Webseite
    #Öffne Stream Litschi
    #öffne stream litt
    #Essen ist ziemlichÖffentlich Stream lebt
    #http://___:8831/
    ("http://___:8831/",
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


    (f'{flake8}',
     # EXAMPLE: frage   proof for syntac errors
     r'^(proof for syntac errors|proof errors|proof syntac|Regeln prüfen)$',
     100, { 'flags': re.IGNORECASE }),

    (
    f'{flake8}',
    r'''
    ^
    (?:
        (?:Prüft|prüfe|früchte|trüffel|frevel|pro[ovb]e?|check|scan|test|validate)\s+(?:for\s+)? 
        \s*
        (?:synta[xk]s?\b|rules?\b)?(?:err?ors?|rules?|issues?)?
    ) 
    $
    |
    (?:regeln?\s+pr[üu]fen|syntax\s+pr[üu]fen|fehler\s+suchen)
    $
    ''',
    100,
    {'flags': re.IGNORECASE | re.VERBOSE,
     'only_in_windows': ['Konsole', 'Terminal', 'Console', 'Code', 'VSC', 'Alacritty']
     }
    ),
    # attention! mit re.VERBOSE all normal spaces was ignored. its the same like ix (i for IGNORECASE x for VERBOSE)


    # disabled_2026-0117-1336___

    ('blocked_Terminal',
     # EXAMPLE: Terminal blocked
     r' disabled_2026-0117-1336___ ^.*$',
     70,
    {'flags': re.IGNORECASE | re.VERBOSE,
     'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console', 'Code', 'VSC', 'Alacritty']
    }
    ),

    # mal ausprobierennicht gebloggtund hier eigentlich nicht
    #

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
    # google seminare
    # gogol gemini ei
    #https://aistudio.google.com/prompts/new_chathttps://aistudio.google.com/prompts/new_chat

    # EXAMPLE: gemini
    # ('https://aistudio.google.com/prompts/new_chat', r'^(gemini|cheminée|Google Jimmy|Gucke chapiteau|Google Tribüne|Google Termine|google ari studio|Google Aviv|google gewinnt|Google ein Studio|google it studio|google \w+ studio|google my style|Google

    # google seminar
    # googeln jimmy nein
    # google g mine
    # googeln gehminuten gb dreht
    # gogol jimmy nein
    # https://aistudio.google.com/prompts/new_chat

    # EXAMPLE: gemini
    ('https://aistudio.google.com/prompts/new_chat', r'''(?ix)
    ^ (?:
        gemini | cheminée | gb dreht |
        (?:google|googeln|gogol|gucke|gut|gb|brooke|coral) \s+
        (?:
            gemini[\s\w]* |
            g\ mine |
            gehminuten |
            will\ gemini\ a |
            cheminée |
            studi[ao]\w* |
            seminar |
            ein\ Studio | ein\ Stuhl |
            it\ studio | my\ style
            ge[hmw]\w* | gemini\ recht | \w*minarett |
            gaming\ nein | gaming | 
            kriminell\w* |
            dir\ bitte |
            termin\w* |
            b[\s-]?day |
            jimmy\ nein |
            grimmen\s*.*|grimmig|Germany|feminin|Gewinnern|gewinne|wieder|g bedeuten|gebe drei|gb daten|gewinn ein|gebe dein|kriminelle|gewitter|b day|g wie neu|coral gaming nein|geben innere|seminare|gemini\ ei|
            kapital | aviv | leicht | eingestuft | chapiteau | my\s+style | seminare | feminin | gemini\ ei
        )
    )
    \b.*$
    '''
    , 70 ),



    # EXAMPLE: chat mit gemini
    ('https://aistudio.google.com/prompts/new_chat', r'^chat mit\s+(gemini|cheminée|Boot Gaming nein|chip|Kevin)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

    # Google kriminelle

    # EXAMPLE: Suche
    ("('Rückgabe', r'Suche', 70, {'flags': re.IGNORECASE}),",
     # EXAMPLE: Neue Regel
     r'^(Neue)\s+(Regel|RegEx)$',
     70, {'flags': re.IGNORECASE}),

    #Neue regelNeue regelNeue regelwohnlich neuerenix', r'pattern', 70, {'flags': re.IGNORECASE}),'





    # EXAMPLE: reload
    ('reload', r'\b(w lot|Why not|wie lot|Velo|free slot)\b', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: reload
    ('reload', r'^(lot)$', 70, {'flags': re.IGNORECASE}),

    #frei SlotPilotWhy notLot
    # ReloadWie Lot




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




    # EXAMPLE:   Wer ist der Beste x Schachspieler 
    ("Sebastian Lauffer aus Wannweil (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?(Beste[\w]? Schachspieler.*)$', 90, {
    'flags': re.IGNORECASE
    }),

    # EXAMPLE:   Wer ist s der s herr schröer
    ("Herr Schröer ist ein netter, bisschen vergesslicher, Ergotherapeut. (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?\s*(herr)?\s*\b(schröer)$', 90, {
    'flags': re.IGNORECASE
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

    # EXAMPLE: hot reload
    ('hot reload', r'\b(hat)\s+(Reload)\b', 95, {
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


    # ('', '^(?!Computer|Aura).*(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist) ([a-z]+.*)', 90, {
    # 'flags': re.IGNORECASE,
    # 'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    # }),

#

]

