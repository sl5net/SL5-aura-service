# config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py
import os
import random
import re
import sqlite3
import hashlib
import json
import datetime
import sys
import urllib.request
import threading

from pathlib import Path
import subprocess  # Added for espeak support
# config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py

# --- METADATA ---
VERSION = "1.1.0"
# AUTHOR: AI Assistant for sl5net



"""
ToDo:
us this somwhre:

        exp_thread202603111649 = speak(speech_text202603111649, blocking=False)
        print(speech_text202603111649)

                speech_text202603111649 = generate_announcement_text(content)
        # mod_thread = speak(speech_text202603111649, blocking=False,use_espeak=True)


"""



def get_markdown_context(f_path, max_headers=2):
    """
    Liest die Datei und extrahiert den Dateinamen sowie die ersten Überschriften.
    """
    headers = []
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Sucht nach Markdown-Überschriften (z.B. # Titel oder ## Untertitel)
                match = re.match(r'^#+\s+(.*)', line)
                if match:
                    # Wir säubern die Header von eventuellen Markdown-Links oder Formatierungen
                    clean_header = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', match.group(1)).strip()
                    headers.append(clean_header)
                if len(headers) >= max_headers:
                    break
    except Exception:
        pass

    return {
        "filename": os.path.basename(f_path).replace('_', ' ').replace('.md', ''),
        "headers": headers
    }

def generate_announcement_text(f_path): # f_path
    """
    Erstellt einen natürlich klingenden deutschen Einleitungssatz.
    """
    context = get_markdown_context(f_path)

    # Verschiedene Varianten für den Einstieg
    opening_phrases = [
        "Alles klar, schauen wir uns das mal an.",
        "Ah, interessant. Hier haben wir das nächste Dokument.",
        "So, als nächstes steht diese Aufgabe an.",
        "Mal sehen, was wir hier als Nächstes bearbeiten müssen.",
        "Ich öffne jetzt die Datei.",
        "Kommen wir zum nächsten Punkt auf der Liste.",
        "Oh, das sieht nach einem wichtigen Dokument aus."
    ]

    # Liste mit "Entwickler-Sprüchen" für die Abwechslung
    intros = [ # noqa: F841

        "Alright, let's see what we have here.",
        "Ah, interesting. Next document on the list.",
        "Okay, moving on to the next task.",
        "Let's check out this one.",
        "Next up is a document about...",
        "Scanning the next file now. Let's focus.",
        "Right, this looks like an important one."
    ]

    # Den Dateinamen einbauen (etwas natürlicher ausgesprochen)
    file_intro = f"Es geht um die Datei {context['filename']}."

    # Die Überschriften einbauen, falls vorhanden
    header_info = ""
    if context['headers']:
        if len(context['headers']) == 1:
            header_info = f" Das Hauptthema scheint {context['headers'][0]} zu sein."
        else:
            header_info = f" Darin geht es vor allem um {context['headers'][0]} und {context['headers'][1]}."

    # Alles kombinieren
    full_text = f"{random.choice(opening_phrases)} {file_intro}{header_info}"
    return full_text





















































































# --- CONFIGURATION ---
def _load_model_from_config():
    """Liest Modellname aus config/internal/ai_model.txt, fallback: llama3.2:latest"""
    from pathlib import Path as _Path
    # radio liegt in config/maps/plugins/z_fallback_llm/de-DE/
    # 5 Ebenen hoch = Repo-Root
    cfg = _Path(__file__).parents[4] / "config" / "internal" / "ai_model.txt"
    if cfg.exists():
        model = cfg.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if model:
            return model
    return "llama3.2:latest"

MODEL_NAME = _load_model_from_config()
OLLAMA_API_URL = "http://localhost:11434/api/generate"

OPEN_BROWSER = True  # Setze auf False für Massen-Generierung im Hintergrund

SPEECH_ENABLED = True
BLOCKING_SPEECH = False # Set to True to wait for speech to finish before next step

# Path setup
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "llm_cache.db"
# Go up to the repository root
REPO_ROOT = SCRIPT_DIR.parents[4]

_speech_lock = threading.Lock()

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
                if ".i18n" not in file or "-delang.md" in file:
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
    #rel_path = ""
    #if "STT/" in file_path:
    #    rel_path = file_path.split("STT/")[1]
    #elif "SL5-aura-service/" in file_path:
    #    rel_path = file_path.split("SL5-aura-service/")[1]
    # github_link = f"https://github.com/sl5net/SL5-aura-service/blob/master/{rel_path}" if rel_path else ""

    github_link = get_github_url(file_path)

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

PIPER_SERVER_HOST = '127.0.0.1'
PIPER_SERVER_PORT = 5002
PIPER_SERVER_URL = f"https://{PIPER_SERVER_HOST}:{PIPER_SERVER_PORT}/speak"
# PIPER_SPEAK_FILE = os.path.expanduser("~/projects/py/TTS/speak_file.py")


def open_url(url):
    import os
    import subprocess
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")
    subprocess.Popen(["xdg-open", url], start_new_session=True, env=env)


from pathlib import Path

def get_validated_github_url(stored_path):
    """
    Validiert einen Dateipfad aus der DB und findet die Datei, falls sie verschoben wurde.
    Erzeugt daraus die korrekte GitHub-URL.
    """
    # 1. Projekt-Root sicher finden (Deine /tmp/ Methode)
    try:
        tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
        root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
        project_root = Path(root_file.read_text(encoding="utf-8").strip())
    except Exception:
        # Fallback falls die Datei fehlt
        return None

    # 2. Pfad normalisieren (~ expandieren)
    full_path = Path(os.path.expanduser(stored_path))

    # 3. GENERATIVE SUCHE: Falls Datei nicht am alten Ort existiert
    if not full_path.exists():
        filename = full_path.name
        # Wir suchen rekursiv im Projekt nach dem Dateinamen
        # Wir ignorieren dabei .git und .venv Ordner für die Performance
        search_results = [
            p for p in project_root.rglob(filename)
            if ".venv" not in str(p) and ".git" not in str(p)
        ]

        if search_results:
            # Wir nehmen den ersten Treffer, der existiert
            full_path = search_results[0]
        else:
            # Datei ist wirklich unauffindbar
            return None

    # 4. GitHub URL aus dem (evtl. neuen) Pfad bauen
    try:
        # Pfad relativ zum Projekt-Root berechnen
        rel_path = full_path.relative_to(project_root)
        # GitHub Link bauen
        return f"https://github.com/sl5net/SL5-aura-service/blob/master/{rel_path}"
    except Exception:
        return None


def get_github_url(stored_path):
    try:
        tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
        root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
        project_root = Path(root_file.read_text(encoding="utf-8").strip())
    except Exception as e:
        print(f'error: {e}')
        return None

    # 1. Datei lokal finden (Self-Healing wie gehabt)
    current_path = Path(os.path.expanduser(stored_path))
    if not current_path.exists():
        filename = current_path.name
        found_files = [p for p in project_root.rglob(filename)
                       if ".venv" not in str(p) and ".git" not in str(p)]
        if found_files:
            current_path = found_files[0]
        else:
            return None

    # 2. PRÜFUNG: Kennt Git diese Datei überhaupt?
    # Wir fragen Git, ob die Datei im Index ist (also online sein könnte)
    try:
        check = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', str(current_path)],
            cwd=project_root,
            capture_output=True, text=True
        )
        if check.returncode != 0:
            # Datei ist nicht in Git (ignored oder noch nicht geadded)
            print(f"INFO: Überspringe Link für {current_path.name} (nicht in Git/ignored)")
            return None
    except Exception:
        pass # Falls Git-Befehl fehlschlägt

    # 3. Link generieren
    try:
        rel_path = current_path.relative_to(project_root)
        return f"https://github.com/sl5net/SL5-aura-service/blob/master/{rel_path}"
    except Exception:
        return None


def speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
    if not text or not globals().get('SPEECH_ENABLED', True):
        return None

    text = ' | GitHub SL5net Aura | ' + text # speak the GitHub repo address always

    def _do_speak(use_espeak2):
        with _speech_lock:  # 🔒 Nur eine Sprachausgabe gleichzeitig
            if not use_espeak2:
                try:
                    with open('/tmp/speak_server_input.txt', 'w') as f:
                        f.write(text)
                    requests.post(PIPER_SERVER_URL, verify=False, timeout=60)  # nosec B501 - localhost only
                    return
                except requests.exceptions.ConnectionError:
                    print("  !! Piper Server nicht erreichbar — Fallback zu espeak")
                except Exception as e:
                    print(f"  !! Piper Error: {e} — Fallback zu espeak-ng")

            # Fallback: espeak-ng
            try:
                subprocess.run(["espeak-ng", "-v", voice, "-s", "150", "-p", str(pitch), text])
            except Exception as e:
                print(f"  !! Speech Error (espeak-ng): {e}")

    t = threading.Thread(target=_do_speak, args=(use_espeak,))
    t.start()

    if blocking:
        t.join()

    return t  # statt Prozess jetzt Thread zurückgeben

def main():
    # config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py:242
    init_db()
    print(f"--- Radio Deep-Dive Generator v1.3.1 (Model: {MODEL_NAME}) ---")

    candidates = get_files_needing_update(str(REPO_ROOT))
    if not candidates:
        print("All documents are up to date.")
        return


    target = random.choice(candidates)
    target_pretty = target
    target_pretty = target_pretty.lstrip("/docs/")
    target_pretty = target_pretty.lstrip("/README.md")


    print(f"Processing ({len(candidates)} pending): {target_pretty}")

    with open(target, 'r', encoding='utf-8') as f:
        content = f.read(4000)  # Slightly reduced to 4k for better stability




        # URL generieren und Browser öffnen
        doc_url = get_github_url(target)
        # NUR öffnen, wenn der Schalter aktiv ist
        if OPEN_BROWSER and doc_url:
            print(f"\n📖 Öffne Dokumentation im Browser: {doc_url}")
            # webbrowser.open(doc_url)
            open_url(doc_url)

        elif doc_url:
            print(f"\n🔗 Dokumentations-Link: {doc_url}")  # Nur Text-Ausgabe im Hintergrund-Modus


        # --- PHASE 1: MODERATOR ---
        print("AI Moderator is thinking...")
        q_prompt = f"Datei: {os.path.basename(target)}\nInhalt: {content}\n\nStelle eine kurze Radio-Frage auf Deutsch. Am besten nur ein Satz."
        question = call_ollama(q_prompt, "Du bist Moderator beim Radio Aura. Deine Hobbies:  privacy-first, voice assistant, scriptable rule engines, regEx, SqlLite. Halte dich kurz.")

        if not question:
            print("  !! Technical Failure: Could not generate question.")
            return

        question = question.replace("#", " ")
        question = question.replace("*", " ")

        question = question.lstrip("/docs/")

        # ✅ ERST ausgeben, DANN vorlesen
        print(f"\n🤖 MODERATOR: {question}")
        sys.stdout.flush()
        # speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
        mod_thread = speak(question, blocking=False,use_espeak=True)

        # 3. AI Expert Round
        print("AI Expert is thinking...")





        a_prompt = f"Kontext: {content}\nFrage: {question}\n\nBeantworte die Frage kurz und prägnant auf Deutsch (max 3 Sätze)."

        answer = call_ollama(a_prompt, "Du bist ein technischer Experte für das Aura-System.")
        answer = answer.replace("#", " ")
        answer = answer.replace("*", " ")

        answer = answer.lstrip("/docs/")


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
        SELECT p.prompt_text, r.response_text, r.comment
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

    # question, answer = row


    question, answer, doc_url = row

    # 1. Dokument im Browser öffnen (falls Link vorhanden und Browser-Modus an)
    if globals().get('OPEN_BROWSER', True) and doc_url:
        print(f"\n📖 Öffne Dokumentation: {doc_url}")
        # webbrowser.open(doc_url)
        open_url(doc_url)


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
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()
    
    parser.add_argument('--no-browser', action='store_true')
    if args.no_browser:
        OPEN_BROWSER = False

    init_db()

    if args.demo:
        DEMO_MODE()
    else:
        main()


        
