import re
import os
from pathlib import Path

# Fix für Pfade
CONFIG_DIR = Path(__file__).parent
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
PROJECT_ROOT = Path(root_file.read_text(encoding="utf-8").strip())


aura_reg = '(Aura|Auch|Aurora|laura|dora|Ära|hurra|prora|Orange|rohre|rohrer|doras|woran|Zauberer|ora|suche|uwe|obwohl|over|oh|bohrer|aurore|rum|ruhe|tore|rot|robe|buchen|hoch|horror|auren|samurai|roche|brauche|ohh|ore|anbraten brauche|k|raucher|aachen|aber|ohren|ohr|lorenz|hoa|tore zu|hey|ovale|burgess)'


FUZZY_MAP_pre = [
    # --- Sprachsteuerung für den Lernmodus ---
    ('Lernmodus...', fr'^{aura_reg}.*lernmodus (an\w*|ein\w*|aus\w*|starten|stoppen)$', 100, {
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),

    (f'zyxü', r'^(zyxü)$', 10),

    #nixLernmodus DEAKTIVIERT. Ich diktiere jetzt wieder normal.Hurra Lernmodus einschalten

    # --- Training-Plugin (wird vom Skript oben ein/ausgeschaltet) ---
#     (f'{str(__file__)}', r'^(.*|straßenbahn)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
