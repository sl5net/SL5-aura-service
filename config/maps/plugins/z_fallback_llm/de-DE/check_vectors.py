# check_vectors.py
import sqlite3
import pickle
from pathlib import Path

try:
    from .utils import init_db, DB_FILE
except ImportError:
    from utils import init_db, DB_FILE

# Ensure the database and its tables exist before querying
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
