from pathlib import Path

# Fix für Pfade
CONFIG_DIR = Path(__file__).parent

PROJECT_ROOT = Path("/tmp/sl5_aura/sl5net_aura_project_root")


# 3. Jetzt sauber importieren
try:
    from aura_constants import AURA_VARIANTS
except ImportError:
    # Fallback, falls die Datei fehlt
    AURA_VARIANTS = r'(Aura|Auch|Aurora)'

FUZZY_MAP_pre = [
    # --- Sprachsteuerung für den Lernmodus ---
    ('Lernmodus...', fr'^{AURA_VARIANTS}.*lernmodus (an\w*|ein\w*|aus\w*|starten|stoppen)$', 100, {
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),

    ('zyxü', r'^(zyxü)$', 10),

    #nixLernmodus DEAKTIVIERT. Ich diktiere jetzt wieder normal.Hurra Lernmodus einschalten

    # --- Training-Plugin (wird vom Skript oben ein/ausgeschaltet) ---
#     (f'{str(__file__)}', r'^(.*|straßenbahn)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),


    #


]
