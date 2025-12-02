# utils.py
import sys
import time
import inspect
import os
#import sys
import logging
import sqlite3
from pathlib import Path

from nltk.stem.snowball import GermanStemmer


PLUGIN_DIR = Path(__file__).parent
MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
DB_FILE = PLUGIN_DIR / "llm_cache.db"


CURRENT_DIR = Path(__file__).resolve().parent
# DB_FILE = CURRENT_DIR / "llm_cache.db"


GLOBAL_STEMMER = GermanStemmer()

CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
for _ in range(5):
    PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.parent
sys.path.append(str(PROJECT_ROOT_DIR))

from scripts.py.func.audio_manager import create_bent_sine_wave_sound

# utils.py
PLUGIN_DIR = Path(__file__).parent
MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")

DEFAULT_RATING = 5

# utils.py
global SESSION_CACHE_HITS
global SUM_PER_CACHE
global SESSION_SEC_SUM
global SESSION_COUNT

try:
    _ = SESSION_CACHE_HITS
except NameError:
    SESSION_CACHE_HITS = 0
try:
    _ = SUM_PER_CACHE
except NameError:
    SUM_PER_CACHE = 0
try:
    _ = SESSION_SEC_SUM
except NameError:
    SESSION_SEC_SUM = 0
try:
    _ = SESSION_COUNT
except NameError:
    SESSION_COUNT = 0




MAX_HISTORY_ENTRIES = 2
CACHE_TTL_DAYS = 7
MAX_VARIANTS = 5




STOP_WORDS_DE_EXTREME = {'mein','aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'andere',
                         'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern'}

STOP_WORDS_DE_EXTREME.update({'aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'andere','anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern','der', 'die', 'das', 'ein', 'eine', 'einer', 'und', 'oder', 'mit', 'von', 'in', 'im',
    'zu', 'zur', 'auf', 'für', 'ist', 'sind', 'war', 'wäre', 'kannst', 'du', 'mir', 'uns',
    'ich', 'hallo', 'hey', 'bitte', 'danke', 'mal', 'eben', 'schnell', 'kurz',
    'computer', 'pc', 'system', 'aura'})

STOP_WORDS_DE_EXTREME.update({'aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'andere',
                         'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern'})


STOP_WORDS_DE_EXTREME.update({  'std',
    'der', 'die', 'das', 'ein', 'eine', 'einer', 'und', 'oder', 'mit', 'von', 'in', 'im',
    'zu', 'zur', 'auf', 'für', 'ist', 'sind', 'war', 'wäre', 'kannst', 'du', 'mir', 'uns',
    'ich', 'hallo', 'hey', 'bitte', 'danke', 'mal', 'eben', 'schnell', 'kurz',
    'computer', 'pc', 'system', 'aura',
'wie', 'kann', 'zum', 'als', 'ich', 'mir', 'etc.'
})


STOP_WORDS_DE_EXTREME.update({
    # Häufige Fragewörter und Füllwörter, die den Hash unnötig verändern
    'was', 'wann', 'warum', 'wohin', 'wessen', 'welche', 'welches', 'welcher', 'wieviel',

    # Weitere Hilfsverben und Präpositionen
    'vom', 'zum', 'zur', 'beim', 'mit', 'durch', 'gegen', 'ohne', 'über', 'unter',
    'ab', 'an', 'bis', 'seit', 'trotz', 'während', 'wegen', 'zum',

    # Pronomen, Adverbien & Konjunktionen
    'dich', 'dir', 'ihm', 'ihr', 'sich', 'uns', 'euch', 'euch',
    'auch', 'mal', 'noch', 'schon', 'denn', 'doch', 'halt', 'eben', 'vielleicht',
    'etwas', 'nichts', 'alles', 'man'
})


LOG_FILE = CURRENT_DIR / "ask_ollama.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Clear any pre-existing handlers to prevent duplicates.
if len(logger.handlers) > 0:
    logger.handlers.clear()

# Create a shared formatter with the custom formatTime function.
def formatTime(record, datefmt=None):
    time_str = time.strftime("%H:%M:%S")
    milliseconds = int((record.created - int(record.created)) * 1000)
    ms_str = f",{milliseconds:03d}"
    return time_str + ms_str

log_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
log_formatter.formatTime = formatTime

# Create, configure, and add the File Handler.
file_handler = logging.FileHandler(f'{LOG_FILE}', mode='w')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Create, configure, and add the Console Handler.
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)



#from pathlib import Path
def log_debug(text):
    """
    Loggt mit Zeitstempel und KORREKTER Zeilennummer des Aufrufers.
    """
    # 1. Zeit holen
    sec = secDauerSeitExecFunctionStart()

    # 2. Den "Stack Frame" des Aufrufers holen (f_back = 1 Schritt zurück)
    caller_frame = inspect.currentframe().f_back

    # 3. Dateiname und Zeilennummer aus diesem Frame extrahieren
    filename = os.path.basename(caller_frame.f_code.co_filename)
    lineno = caller_frame.f_lineno

    # 4. Ausgabe formatieren
    # ⏱️
    logging.info(f"⏱{sec}⏱️ {filename}:{lineno}: {text}")

def secDauerSeitExecFunctionStart(reset=False):
    return format_duration(secDauerSeitExecFunctionStart_REAL(reset=reset))

def secDauerSeitExecFunctionStart_REAL(reset=False):
    # Wenn reset=True ist ODER die Funktion zum allerersten Mal läuft: Zeit setzen
    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Differenz berechnen
    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def format_duration(seconds):
    """
    Formatiert eine Dauer in Sekunden in den String 'Mm:Ss.m' (eine Stelle nach dem Komma).
    """

    # 1. Minuten berechnen
    minutes = int(seconds // 60)

    # 2. Restliche Sekunden berechnen
    remaining_seconds = seconds % 60

    # 3. Teil für die Ausgabe berechnen: Ganze Sekunden und Zehntelsekunde

    # Ganze Sekunden (S)
    seconds_part = int(remaining_seconds)

    # Zehntelsekunde (m): Die erste Ziffer nach dem Komma
    # Multipliziere den Dezimalteil mit 10 und runde auf die nächste Ganzzahl (oder einfach nur abschneiden)
    # Abschneiden ist hier sinnvoller, um die Zehntelsekunde zu erhalten
    tenth_second = int((remaining_seconds - seconds_part) * 10)

    # Formatierung

    if minutes > 0:
        # Format: M:SS.m
        # Minuten (M), Sekunden (SS mit führender Null), Zehntelsekunde (m)
        return f"{minutes}m:{seconds_part:02d}.{tenth_second}s"

    # Wenn die Dauer unter einer Minute liegt
    else:
        # Format: S.m
        # Sekunden (S), Zehntelsekunde (m)
        # Die 02d für Sekunden ist bei unter einer Minute i.d.R. nicht nötig
        return f"{seconds_part}.{tenth_second}s"


# Beispielausgaben:
# format_duration(0.1234) -> '0.1s'
# format_duration(1.007)  -> '1.0s'
# format_duration(12.51)  -> '12.5s'
# format_duration(65.43)  -> '1m:05.4s'

# --- DATABASE LAYER ---
def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS prompts (
                        hash TEXT PRIMARY KEY,
                        prompt_text TEXT,
                        clean_input TEXT,
                        keywords TEXT,
                        last_used TIMESTAMP
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt_hash TEXT,
                        response_text TEXT,
                        created_at TIMESTAMP,
                        rating INTEGER DEFAULT 5,
                        comment TEXT,
                        usage_count INTEGER DEFAULT 0,
                        FOREIGN KEY(prompt_hash) REFERENCES prompts(hash)
                    )''')
        # Migrationen (silent fails if exists)
        try: c.execute("ALTER TABLE responses ADD COLUMN rating INTEGER DEFAULT 5")
        except Exception: pass
        try: c.execute("ALTER TABLE responses ADD COLUMN comment TEXT")
        except Exception: pass
        try: c.execute("ALTER TABLE responses ADD COLUMN usage_count INTEGER DEFAULT 0")
        except Exception: pass
        try: c.execute("ALTER TABLE prompts ADD COLUMN clean_input TEXT")
        except Exception: pass
        try: c.execute("ALTER TABLE prompts ADD COLUMN keywords TEXT")
        except Exception: pass

        c.execute(f"UPDATE responses SET rating = {DEFAULT_RATING} WHERE rating = 0 AND comment IS NULL")

        c.execute("DROP VIEW IF EXISTS overview_readable")
        c.execute('''
            CREATE VIEW overview_readable AS
            SELECT r.id, r.rating, r.usage_count, p.clean_input AS User_Frage, p.keywords, r.response_text, r.comment, r.created_at
            FROM responses r LEFT JOIN prompts p ON r.prompt_hash = p.hash ORDER BY r.created_at DESC
        ''')
        c.execute("DROP VIEW IF EXISTS stats_most_asked")
        c.execute('''
            CREATE VIEW stats_most_asked AS
            SELECT clean_input, COUNT(*) as context_variations, SUM(r.usage_count) as total_answers_served
            FROM prompts p JOIN responses r ON p.hash = r.prompt_hash GROUP BY clean_input ORDER BY total_answers_served DESC
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        log_debug(f"DB Init Error: {e}")


def play_cache_hit_sound():
    if create_bent_sine_wave_sound:
        try:
            sound = create_bent_sine_wave_sound(880, 1200, 80, 0.15)
            sound.play()
        except Exception: pass


