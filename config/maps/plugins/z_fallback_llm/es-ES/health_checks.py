# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/health_checks.py

import os
import sys
from pathlib import Path

from scripts.py.func.get_project_root import get_aura_project_root

# La misma lógica aquí para garantizar que se encuentren las utilidades cuando se llama desde simular_conversación

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()
plugin_dir = str(SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "z_fallback_llm" / "de-DE")

if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

import sqlite3

import utils


class LazyGermanStemmer:
    def __init__(self):
        self._stemmer = None
    def stem(self, *args, **kwargs):
        if self._stemmer is None:
            from nltk.stem.snowball import GermanStemmer
            self._stemmer = GermanStemmer()
        return self._stemmer.stem(*args, **kwargs)
GLOBAL_STEMMER = LazyGermanStemmer()

def check_db_statistics_and_exit_if_invalid():
    """Prüft die DB-Statistiken (Total Hits > Unique Prompts) und bricht bei Inkonsistenz ab."""
    conn = None
    try:
        absolute_db_path = str(utils.DB_FILE)
        conn = sqlite3.connect(f'file:{absolute_db_path}?mode=ro', timeout=10, uri=True)
        if not conn:
            print("!!! DATENBANK keine Verbindung !!!")
            print('sys.exit(1) 2025-1201-1802')
            sys.exit(1)

        c = conn.cursor()

        # Consultar el total de visitas correctamente

        S1 = "SELECT COUNT(*) FROM responses"
        print(f"{S1}")
        c.execute(S1)
        row = c.fetchone()
        total_hits = row[0] if row and row[0] is not None else 0

        # Consulta mensajes únicos correctamente

        S2 = "SELECT COUNT(DISTINCT prompt_hash) FROM responses"
        print(f"{S2}")
        c.execute(S2)
        row = c.fetchone()
        unique_prompts = row[0] if row and row[0] is not None else 0

        # Lógica de examen mejorada

        if unique_prompts == 0:
            diagnosis = f"{utils.DB_FILE} ist LEER. Es sind 0 eindeutige Fragen vorhanden. sqlitebrowser {utils.DB_FILE} & "
        elif unique_prompts < 2:
            diagnosis = f"Datenbank ist zu leer. Nur {unique_prompts} eindeutige Fragen."
        elif total_hits < unique_prompts:
            diagnosis = f"LOGIKFEHLER! Total Hits ({total_hits}) sind kleiner als Unique Prompts ({unique_prompts})."
        else:
            print(f"[STATISTIK OK] Cache-Hits: {total_hits}, Eindeutige Fragen: {unique_prompts}")
            if conn:
                conn.close()
            return True

        # Salida de error en caso de falla

        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! KRITISCHER FEHLER: DATENBANK INKONSISTENT/ZU LEER !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"DIAGNOSE: {diagnosis}")
        print(f"PRÜFUNG: Ist die Datenbank '{utils.DB_FILE}' die richtige Datei?")
        if conn:
            conn.close()
        print('sys.exit(1) 2025-1201-1801')
        sys.exit(1)

    except Exception as e:
        print(f"KRITISCHER FEHLER: Datenbankfehler: {e}")
        if conn:
            conn.close()
        print('sys.exit(1) 2025-1201-18022')
        sys.exit(1)

