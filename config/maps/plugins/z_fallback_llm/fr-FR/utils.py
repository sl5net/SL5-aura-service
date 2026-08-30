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

# config/maps/plugins/z_fallback_llm/de-DE/utils.py

# utils.py

import inspect

# système d'importation
import logging
import os
import sqlite3
import sys
import time
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
# DB_FILE = RÉP_ACTUEL / "llm_cache.db"



LOG_FILE = CURRENT_DIR / "ask_ollama.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Effacez tous les gestionnaires préexistants pour éviter les doublons.

if len(logger.handlers) > 0:
    logger.handlers.clear()

# Créez un formateur partagé avec la fonction formatTime personnalisée.

def formatTime(record, datefmt=None):
    time_str = time.strftime("%H:%M:%S")
    milliseconds = int((record.created - int(record.created)) * 1000)
    ms_str = f",{milliseconds:03d}"
    return time_str + ms_str

def secDauerSeitExecFunctionStart(reset=False):
    return format_duration(secDauerSeitExecFunctionStart_REAL(reset=reset))

def secDauerSeitExecFunctionStart_REAL(reset=False):
    # Si reset=True OU la fonction s'exécute pour la toute première fois : régler l'heure

    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Calculer la différence

    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def format_duration(seconds):
    """
    Formatiert eine Dauer in Sekunden in den String 'Mm:Ss.m' (eine Stelle nach dem Komma).
    """

    # 1. Calculer les minutes

    minutes = int(seconds // 60)

    # 2. Calculez les secondes restantes

    remaining_seconds = seconds % 60

    # 3. Calculer la partie pour la sortie : secondes entières et dixièmes de seconde


    # Secondes entières (S)

    seconds_part = int(remaining_seconds)

    # Dixième de seconde (m) : le premier chiffre après la virgule

    # Multipliez la partie décimale par 10 et arrondissez au nombre entier le plus proche (ou tronquez simplement)

    # La troncature a plus de sens ici pour obtenir le dixième de seconde

    tenth_second = int((remaining_seconds - seconds_part) * 10)

    # formatage


    if minutes > 0:
        # Format : M:SS.m

        # Minutes (M), secondes (SS avec zéro non significatif), dixièmes de seconde (m)

        return f"{minutes}m:{seconds_part:02d}.{tenth_second}s"

    # Si la durée est inférieure à une minute

    else:
        # Format : S.m

        # Secondes (S), dixièmes de seconde (m)

        # Le 02d pour les secondes n'est généralement pas nécessaire pendant moins d'une minute

        return f"{seconds_part}.{tenth_second}s"


# Exemples de sorties :

# format_durée(0,1234) -> '0,1s'

# format_durée(1.007) -> '1.0s'

# format_durée (12,51) -> '12,5s'

# format_durée(65,43) -> '1m:05,4s'


log_formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(message)s')
log_formatter.formatTime = formatTime

# Créez, configurez et ajoutez le gestionnaire de fichiers.

file_handler = logging.FileHandler(f'{LOG_FILE}', mode='w', encoding="utf-8")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Créez, configurez et ajoutez le gestionnaire de console.

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)



def log_debug(text):
    # sec = secDurationSinceExecFunctionStart()

    caller_frame = inspect.currentframe().f_back
    filename = os.path.basename(caller_frame.f_code.co_filename)


    message = f"{filename}:{caller_frame.f_lineno} - {text}\n"
    logging.info(message)

    print(f"{LOG_FILE}")

    print(message)
    try:
        with Path(LOG_FILE).open('a', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        logger.error(f" {e}")
    # sys.exit(1)


PLUGIN_DIR = Path(__file__).parent
MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
DB_FILE = PLUGIN_DIR / "llm_cache.db"



class LazyGermanStemmer:
    def __init__(self):
        self._stemmer = None
    def stem(self, *args, **kwargs):
        if self._stemmer is None:
            from nltk.stem.snowball import GermanStemmer
            self._stemmer = GermanStemmer()
        return self._stemmer.stem(*args, **kwargs)
GLOBAL_STEMMER = LazyGermanStemmer()



CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
for _ in range(5):
    PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.parent
sys.path.append(str(PROJECT_ROOT_DIR))



try:
    # import scripts.py.func.audio_manager # ne fonctionne pas pour moi 4 décembre 25 17h20 Jeu

    from scripts.py.func.audio_manager import (
        sound_program_loaded,  # works 4.12.'25 17:20 Thu
    )
except ImportError as e:
    print(f"Fehler: Konnte 'audio_manager.py' nicht als Modul importieren: {e}")
    log_debug(f"Fehler: Konnte 'audio_manager' pas comme module importer: {e}")

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
'wie', 'kann', 'zum', 'als', 'etc.'
})


STOP_WORDS_DE_EXTREME.update({
    # Mots de question courants et mots de remplissage qui modifient inutilement le hachage

    'was', 'wann', 'warum', 'wohin', 'wessen', 'welche', 'welches', 'welcher', 'wieviel',

    # Plus de verbes auxiliaires et de prépositions

    'vom', 'zum', 'zur', 'beim', 'mit', 'durch', 'gegen', 'ohne', 'über', 'unter',
    'ab', 'an', 'bis', 'seit', 'trotz', 'während', 'wegen', 'zum',

    # Pronoms, adverbes et conjonctions

    'dich', 'dir', 'ihm', 'ihr', 'sich', 'uns', 'euch', 'auch', 'mal', 'noch', 'schon', 'denn', 'doch', 'halt', 'eben', 'vielleicht',
    'etwas', 'nichts', 'alles', 'man'
})





# à partir du chemin d'importation pathlib




# --- COUCHE BASE DE DONNÉES ---

def init_db():
    try:
        # 1. Utilisez un délai d'attente élevé et activez immédiatement le mode WAL

        conn = sqlite3.connect(DB_FILE, timeout=90)
        conn.execute("PRAGMA journal_mode=WAL;")
        c = conn.cursor()

        # 2. Tableaux de base

        c.execute('''CREATE TABLE IF NOT EXISTS prompts (
                        hash TEXT PRIMARY KEY,
                        prompt_text TEXT,
                        clean_input TEXT,
                        keywords TEXT,
                        embedding BLOB,
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

        # 3. N'exécutez des migrations/vues que si nous ne sommes pas dans une simulation à haute concurrence

        # ou enveloppez-les de manière à ne pas planter l'initialisation

        try:
            # Vérifiez si nous devons mettre à jour les notes

            c.execute(f"UPDATE responses SET rating = {DEFAULT_RATING} WHERE rating = 0 AND comment IS NULL")

            # Les vues sont lourdes sur les verrous, recréez-les uniquement si nécessaire

            c.execute("DROP VIEW IF EXISTS overview_readable")
            c.execute('''
                CREATE VIEW overview_readable AS
                SELECT r.id, r.rating, r.usage_count, p.clean_input AS User_Frage, p.keywords, r.response_text, r.comment, r.created_at
                FROM responses r LEFT JOIN prompts p ON r.prompt_hash = p.hash ORDER BY r.created_at DESC
            ''')
        except sqlite3.OperationalError as e:
            # Si la base de données est verrouillée, ignorez la recréation de la vue pour cette session

            logging.warning(f"Skipping view recreation due to lock: {e}")

        conn.commit()
        conn.close()
    except Exception as e:
        # C'est ici que votre erreur de ligne 302 a été détectée

        log_debug(f"DB Init Error: {e}")


def play_cache_hit_sound():
    sound_program_loaded()
    # si create_bent_sine_wave_sound :

    # try:

    # son = create_bent_sine_wave_sound(880, 1200, 80, 0,15)

    # son.play()

    # sauf exception comme error_msg :

    # log_debug(f"Erreur : {error_msg}")

    # passeport



