import os
import random
import sqlite3
import hashlib
import json
import datetime
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


def speak(text, voice="de-de", pitch=50, blocking=False):
    """
    Version 1.3.2: Merged speech function.
    Supports global toggle, custom pitch, and optional blocking.
    """
    # Check if speech is enabled globally (ensure SPEECH_ENABLED is defined at top)
    if not text or not globals().get('SPEECH_ENABLED', True):
        return None

    try:
        # -v: voice, -s: speed, -p: pitch
        # We use Popen to allow asynchronous execution
        process = subprocess.Popen([
            "espeak",
            "-v", voice,
            "-s", "150",
            "-p", str(pitch),
            text
        ])

        if blocking:
            process.wait()

        return process
    except Exception as e:
        print(f"  !! Speech Error: {e}")
        return None


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
    question = call_ollama(q_prompt, "Du bist Moderator beim Radio Aura. Halte dich kurz.")

    if not question:
        print("  !! Technical Failure: Could not generate question.")
        return

    print(f"\nMODERATOR (Voice: de-de): {question}")
    # Start speaking immediately (Non-blocking)
    # mod_voice_proc = speak(question, voice="de-de", pitch=50)
    mod_voice_proc = speak(question, voice="de-de", pitch=50, blocking=False)

    # --- PHASE 2: EXPERT (Ollama works while Moderator speaks) ---
    print("AI Expert is thinking (Parallel)...")
    a_prompt = f"Kontext: {content}\nFrage: {question}\n\nBeantworte die Frage kurz (max 3 Sätze) auf Deutsch."
    answer = call_ollama(a_prompt, "Du bist ein technischer Experte.")

    # Wait for moderator to finish talking before showing/speaking the answer
    if mod_voice_proc:
        mod_voice_proc.wait()

    if answer:
        print(f"EXPERT (Voice: de+f2): {answer}\n")
        # Expert speaks (Blocking, so we don't start the next file too early)
        # exp_voice_proc = speak(answer, voice="de+f2", pitch=65)  # Higher pitch for female voice

        exp_voice_proc = speak(answer, voice="de+f2", pitch=40, blocking=False)

        if exp_voice_proc:
            exp_voice_proc.wait()

        save_to_aura_db(question, answer, target)
        print("Radio segment saved and tracked.")
    else:
        print("  !! Technical Failure: Could not generate answer.")


if __name__ == "__main__":
    main()