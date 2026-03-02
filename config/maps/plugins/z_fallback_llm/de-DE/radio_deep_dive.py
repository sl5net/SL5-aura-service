import os
import random
import re
import sqlite3
import hashlib
import json
import datetime
import sys
import urllib.request
from pathlib import Path
import subprocess  # Added for espeak support

# --- METADATA ---
VERSION = "1.1.0"
# AUTHOR: AI Assistant for sl5net

# --- CONFIGURATION ---
MODEL_NAME = "llama3.2:latest"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

SPEECH_ENABLED = True
BLOCKING_SPEECH = False # Set to True to wait for speech to finish before next step

# Path setup
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "llm_cache.db"
# Go up to the repository root
REPO_ROOT = SCRIPT_DIR.parents[4]


def init_db():
    """
    Version 1.1.0: Ensures tracking table exists to prevent crashes.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS radio_processed_files (
            file_path TEXT PRIMARY KEY,
            last_mtime REAL,
            last_generated TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_allowed_language(file_path):
    filename = os.path.basename(file_path).lower()

    pattern = r'[-_]([a-z]{2})(?:[-_]|lang|\.md$)'
    matches = re.findall(pattern, filename)

    if not matches:
        return True  # Kein Kürzel → verwenden

    # Nur ausschließen wenn eindeutig NICHT de/en
    if any(lang in ('de', 'en') for lang in matches):
        return True

    return False

def get_files_needing_update(root_dir):
    """
    Version 1.1.0: Filters files that are new or have been modified.
    """
    all_md_files = []
    for root, dirs, files in os.walk(root_dir):
        # Filter: exclude hidden, underscore, and noise folders
        dirs[:] = [d for d in dirs if
                   not (d.startswith('.') or d.startswith('_') or d in ['node_modules', 'venv', '__pycache__'])]
        for file in files:
            if file.endswith(".md"):
                all_md_files.append(os.path.join(root, file))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    needs_processing = []
    for f_path in all_md_files:
        try:
            current_mtime = os.path.getmtime(f_path)
            cursor.execute("SELECT last_mtime FROM radio_processed_files WHERE file_path = ?", (f_path,))
            row = cursor.fetchone()

            # Logic: If file is unknown or disk-mtime is newer than DB-mtime
            if row is None or current_mtime > row[0]:
                needs_processing.append(f_path)
        except OSError:
            continue

    conn.close()

    needs_processing = [f for f in needs_processing if is_allowed_language(f)]

    return needs_processing


def call_ollama(prompt, system_prompt=""):
    """
    Version 1.3.1: Added detailed error reporting.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }
    try:
        req = urllib.request.Request(
            OLLAMA_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=90) as response: # Increased timeout to 90s
            raw_res = response.read().decode('utf-8')
            if not raw_res:
                print("  !! Error: Ollama returned an empty response.")
                return None
            res_data = json.loads(raw_res)
            ans = res_data.get("response", "").strip()
            if not ans:
                print("  !! Error: 'response' field is empty in Ollama JSON.")
            return ans
    except Exception as e:
        print(f"  !! Ollama Connection Error: {e}")
        return None


def save_to_aura_db(question, answer, file_path):
    """
    Version 1.1.0: Saves dialogue and updates the tracking state.
    """
    prompt_hash = hashlib.md5(question.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    clean_input = question.lower().replace("?", "").strip()

    # GitHub Link logic
    rel_path = ""
    if "STT/" in file_path:
        rel_path = file_path.split("STT/")[1]
    elif "SL5-aura-service/" in file_path:
        rel_path = file_path.split("SL5-aura-service/")[1]
    github_link = f"https://github.com/sl5net/SL5-aura-service/blob/master/{rel_path}" if rel_path else ""

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Save content to aura cache
        cursor.execute("""
            INSERT OR IGNORE INTO prompts (hash, prompt_text, last_used, clean_input, keywords)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_hash, question, now, clean_input, "radio_deep_dive"))

        cursor.execute("""
            INSERT INTO responses (prompt_hash, response_text, created_at, usage_count, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_hash, answer, now, 0, github_link))

        # 2. Update tracking table
        current_mtime = os.path.getmtime(file_path)
        cursor.execute("""
            INSERT OR REPLACE INTO radio_processed_files (file_path, last_mtime, last_generated)
            VALUES (?, ?, ?)
        """, (file_path, current_mtime, now))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")



import requests
import subprocess
import os
import time

PIPER_SERVER_HOST = '127.0.0.1'
PIPER_SERVER_PORT = 5002
PIPER_SERVER_URL = f"https://{PIPER_SERVER_HOST}:{PIPER_SERVER_PORT}/speak"
PIPER_SPEAK_FILE = os.path.expanduser("~/projects/py/TTS/speak_file.py")

import threading

def speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
    if not text or not globals().get('SPEECH_ENABLED', True):
        return None

    def _do_speak(use_espeak2):
        if not use_espeak2:
            try:
                with open('/tmp/speak_server_input.txt', 'w') as f:
                    f.write(text)
                requests.post(PIPER_SERVER_URL, verify=False, timeout=60)
                return
            except requests.exceptions.ConnectionError:
                print("  !! Piper Server nicht erreichbar — Fallback zu espeak")
            except Exception as e:
                print(f"  !! Piper Error: {e} — Fallback zu espeak")

        # Fallback: espeak
        try:
            subprocess.run(["espeak", "-v", voice, "-s", "150", "-p", str(pitch), text])
        except Exception as e:
            print(f"  !! Speech Error (espeak): {e}")

    t = threading.Thread(target=_do_speak, args=(use_espeak,))
    t.start()

    if blocking:
        t.join()

    return t  # statt Prozess jetzt Thread zurückgeben

def main():
    init_db()
    print(f"--- Radio Deep-Dive Generator v1.3.1 (Model: {MODEL_NAME}) ---")

    candidates = get_files_needing_update(str(REPO_ROOT))
    if not candidates:
        print("All documents are up to date.")
        return

    target = random.choice(candidates)
    print(f"Processing ({len(candidates)} pending): {target}")

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read(4000)  # Slightly reduced to 4k for better stability

        # --- PHASE 1: MODERATOR ---
        print("AI Moderator is thinking...")
        q_prompt = f"Datei: {os.path.basename(target)}\nInhalt: {content}\n\nStelle eine kurze Radio-Frage auf Deutsch."
        question = call_ollama(q_prompt, "Du bist Moderator beim Radio Aura. Deine Hobies:  privacy-first, voice assistant, scriptable rule engines. Halte dich kurz.")

        if not question:
            print("  !! Technical Failure: Could not generate question.")
            return

        # ✅ ERST ausgeben, DANN vorlesen
        print(f"\n🤖 MODERATOR: {question}")
        sys.stdout.flush()
        # speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
        mod_thread = speak(question, blocking=False,use_espeak=True)

        # 3. AI Expert Round
        print("AI Expert is thinking...")
        a_prompt = f"Kontext: {content}\nFrage: {question}\n\nBeantworte die Frage kurz und prägnant auf Deutsch (max 3 Sätze)."

        answer = call_ollama(a_prompt, "Du bist ein technischer Experte für das Aura-System.")

        if mod_thread:
            mod_thread.join()  # Warten bis Moderator fertig

        if answer:
            print(f"\n🙋‍♀️ EXPERT: {answer}\n")
            sys.stdout.flush()
            save_to_aura_db(question, answer, target)
            exp_thread = speak(answer, blocking=False)
            if exp_thread:
                exp_thread.join()

            print("Radio segment saved and tracked.")
        else:
            print("  !! Technical Failure: Could not generate answer.")


def DEMO_MODE():
    print("🎙️ DEMO MODE — playing cached results")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.prompt_text, r.response_text
        FROM responses r
        JOIN prompts p ON r.prompt_hash = p.hash
        WHERE p.keywords = 'radio_deep_dive'
        ORDER BY RANDOM()
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("  !! Kein Cache vorhanden. Erst normal laufen lassen.")
        return

    question, answer = row
    print(f"\nMODERATOR: {question}")
    sys.stdout.flush()
    mod_thread = speak(question, blocking=False,use_espeak=True)
    if mod_thread:
        mod_thread.join()

    print(f"\nEXPERT: {answer}\n")
    sys.stdout.flush()
    exp_thread = speak(answer, blocking=False)
    if exp_thread:
        exp_thread.join()
    return

if __name__ == "__main__":
    if 0:
        DEMO_MODE()
    else:
        main()
