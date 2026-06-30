# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
import runpy


from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702




CONFIG_DIR = p(__file__).parent

acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]


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
# Wörter, die oft statt "Google" verstanden werden
FUZZY_MAP_pre = [


    # EXAMPLE: wie ist das wetter
    ('', r'^(wie ist das wetter|wie ist das fett|Die erhaltenen Wetterdaten hatten ein unerwartetes Format.|wie ist das bett|wie ist das etwa|mir ist das wetter|nächstes bild|wie ist das zwitschern|nicht das wetter|nächstes|wie ist das|wie ist es|nächstes we|lies es)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'weather.py'] # Passe den Pfad ggf. an
    }),


    # EXAMPLE: wie ist das wetter
    ('', r'^(wie (wird|ist|nächstes)\b.*\bwetter|wetterbericht|wettervorhersage)\??$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'weather.py']
    }),

    # EXAMPLE: Aura Admin öffnen open admin panel.
    ('', rf'^{AURA_VARIANTS} Admin\w*\b.*$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'open_admin.py']
    }),


    # (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702


    # EXAMPLE: einen
    ('', r'^einen$', 100, {'flags': re.IGNORECASE}),
    # EXAMPLE: einens
    ('', r'^einens$', 100, {'flags': re.IGNORECASE}),


    # === VOSK NOISE FIX ===
    # Das kleine Vosk-Modell halluziniert oft "einen" bei Stille/Atmen.
    # Wenn der Input EXAKT nur "einen" ist, wird er ignoriert.
    # (Wer wirklich "einen" sagen will, sagt meist "Ich will einen..." -> das bleibt erhalten)
    # ('', r'^einen$', 100, {'flags': re.IGNORECASE}),
    # ('', r'^einens$', 100, {'flags': re.IGNORECASE}),

    # EXAMPLE: einen
    ('', r'^\s*einen\s*$', 100, {'flags': re.IGNORECASE}),
    # EXAMPLE: einens
    ('', r'^\s*einens\s*$', 100, {'flags': re.IGNORECASE}),


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


    # EXAMPLE: Suche
    ("('Rückgabe', r'Suche', 70, {'flags': re.IGNORECASE}),",
     # EXAMPLE: Neue Regel
     r'^(Neue)\s+(Regel|RegEx)$',
     70, {'flags': re.IGNORECASE}),


    # EXAMPLE: reload
    ('reload', r'\b(w lot|Why not|wie lot|Velo|free slot)\b', 70, {'flags': re.IGNORECASE}),

    # EXAMPLE: reload
    ('reload', r'^(lot)$', 70, {'flags': re.IGNORECASE}),


    # EXAMPLE: Chat mit der e
    ('https://pi.ai/talk', r'^(Chat) mit (der e|AI|Terry|frei|ei|it|ari|3|a|der a)\b.*$', 70, {
        'flags': re.IGNORECASE
    }),

    # Regel für Python coding short
    # EXAMPLE: compact_python
    ('', r'^(compact_python|Kompakt fein|Kompakt Brighton|Kompakt bei)$', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'compact_python.py']
    }),



    # seltene unnötige falsch erennung abfangen
    # EXAMPLE: wie ist das wetter
    ('', r'^(wie ist das bett)|(wie ist es fett)$', 95, {
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

    # EXAMPLE:   Wer ist der Beste x Schachspieler 
    ("Sebastian Lauffer aus Wannweil (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?(Beste[\w]? Schachspieler.*)$', 90, {
    'flags': re.IGNORECASE
    }),

    # EXAMPLE:   Wer ist s der s herr schröer
    ("Herr Schröer ist ein netter, bisschen vergesslicher, Ergotherapeut. (fun-fake msg, 2025)", r'^.*(Wer ist)?\s*(der)?\s*(herr)?\s*\b(schröer)$', 90, {
    'flags': re.IGNORECASE
    }),


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

]

