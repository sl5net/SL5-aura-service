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

# check_vectors.py

import sqlite3
import pickle

try:
    from .utils import init_db, DB_FILE
except ImportError:
    from utils import init_db, DB_FILE

# Asegúrese de que la base de datos y sus tablas existan antes de realizar la consulta.

init_db()

conn = sqlite3.connect(DB_FILE)
row = conn.execute("SELECT clean_input, embedding FROM prompts WHERE embedding IS NOT NULL LIMIT 1").fetchone()
conn.close()

if row:
    text, blob = row
    vector = pickle.loads(blob)
    print(f"Input: {text}")
    print(f"Typ: {type(vector)} | Shape: {vector.shape}")
    print(f"Erste 5 Zahlen: {vector[:5]}") # Sollten kleine Floats sein
else:
    print("Keine Vektoren gefunden!")
