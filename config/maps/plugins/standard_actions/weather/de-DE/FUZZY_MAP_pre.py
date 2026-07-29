# config/maps/plugins/standard_actions/weather/de-DE/FUZZY_MAP_pre.py:1
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

    # Aktuell in reutlingen sind es 15 Grad, gefuehlt wie 10 Grad. Die Vorhersage melllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
    # Aktuell in reutlingen sind es 15 Grad, gefuehlt wie 10 Grad. Die Vorhersage mellllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllf

    # Aktuell in reutlingen sind es 15 Grad, gefuehlt wie 10 Grad. Die Vorhersage m


    # EXAMPLE: wie wetter
    ('', r'^(wie\s*(?:ist|wird)?\s*(?:das)?\s*wetter( morgen)?|wie das wetter morgen|wie ist das fett|Die erhaltenen Wetterdaten hatten ein unerwartetes Format.|wie ist das bett|wie ist das etwa|mir ist das wetter|naechstes bild|wie ist das zwitschern|nicht das wetter|naechstes|wie ist das|wie ist es|naechstes we|lies es)$'
    , 95, {
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


]

