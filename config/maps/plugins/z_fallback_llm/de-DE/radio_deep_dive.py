import os
import random
import sqlite3
import hashlib
import json
import datetime
import urllib.request
from pathlib import Path

# --- METADATA ---
VERSION = "1.1.0"
# AUTHOR: AI Assistant for sl5net

# --- CONFIGURATION ---
MODEL_NAME = "llama3.2:latest"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

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
    """ Simple wrapper for Ollama API. """
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
        with urllib.request.urlopen(req, timeout=60) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception as e:
        print(f"  !! Ollama Error: {e}")
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


def main():
    """
    Version 1.1.0: Main Orchestrator.
    """
    init_db()
    print(f"--- Radio Deep-Dive Generator v{VERSION} (Model: {MODEL_NAME}) ---")

    # Filter candidates
    candidates = get_files_needing_update(str(REPO_ROOT))

    if not candidates:
        print("All documents are up to date. No new content to generate.")
        return

    # Randomly select from the list of 'new or changed' files
    target = random.choice(candidates)
    print(f"Processing ({len(candidates)} files pending): {target}")

    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read(5000)
    except Exception as e:
        print(f"Error reading file {target}: {e}")
        return

    # Step 1: Moderator
    print("AI Moderator is thinking...")
    q_prompt = f"Datei: {os.path.basename(target)}\nInhalt: {content}\n\nStelle eine kurze, neugierige Radio-Frage auf Deutsch."
    question = call_ollama(q_prompt, "Du bist Moderator beim Radio Aura. Halte dich kurz.")

    if not question: return

    print(f"\nMODERATOR: {question}")

    # Step 2: Expert
    print("AI Expert is thinking...")
    a_prompt = f"Kontext: {content}\nFrage: {question}\n\nBeantworte die Frage kurz (max 3 Sätze) auf Deutsch."
    answer = call_ollama(a_prompt, "Du bist ein technischer Experte für das Aura-System.")

    if answer:
        print(f"EXPERT: {answer}\n")
        save_to_aura_db(question, answer, target)
        print("Radio segment cached and file tracked successfully.")
    else:
        print("Failed to get answer from AI.")


if __name__ == "__main__":
    main()