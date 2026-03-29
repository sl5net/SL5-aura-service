import subprocess
import os
from pathlib import Path

def execute(match_data):
    # Wir holen uns den Pfad zum Projekt
    PROJECT_ROOT = Path(os.environ.get("SL5NET_AURA_PROJECT_ROOT", Path(__file__).parents[4]))
    SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"
    
    # Wir starten das Terminal (Konsole für KDE/Manjaro)
    # Das Fenster bleibt offen, weil search_rules.sh interaktiv ist (fzf)
    subprocess.Popen(['konsole', '-e', 'bash', str(SEARCH_SCRIPT)])
    
    print("Suche wird im Terminal geöffnet...")
    exit(1)
