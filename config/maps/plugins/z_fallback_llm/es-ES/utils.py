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

# sistema de importación
import logging
import os
import sqlite3
import sys
import time
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
# DB_FILE = CURRENT_DIR / "llm_cache.db"



LOG_FILE = CURRENT_DIR / "ask_ollama.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Borre los controladores preexistentes para evitar duplicados.

if len(logger.handlers) > 0:
    logger.handlers.clear()

# Cree un formateador compartido con la función formatTime personalizada.

def formatTime(record, datefmt=None):
    time_str = time.strftime("%H:%M:%S")
    milliseconds = int((record.created - int(record.created)) * 1000)
    ms_str = f",{milliseconds:03d}"
    return time_str + ms_str

def secDauerSeitExecFunctionStart(reset=False):
    return format_duration(secDauerSeitExecFunctionStart_REAL(reset=reset))

def secDauerSeitExecFunctionStart_REAL(reset=False):
    # Si reset=True O la función se ejecuta por primera vez: establezca la hora

    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Calcular diferencia

    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def format_duration(seconds):
    """
    Formatiert eine Dauer in Sekunden in den String 'Mm:Ss.m' (eine Stelle nach dem Komma).
    """

    # 1. Calcular minutos

    minutes = int(seconds // 60)

    # 2. Calcular los segundos restantes.

    remaining_seconds = seconds % 60

    # 3. Calcule la parte de la salida: segundos enteros y décimas de segundo


    # Segundos enteros (S)

    seconds_part = int(remaining_seconds)

    # Décima de segundo (m): el primer dígito después del punto decimal

    # Multiplica la parte decimal por 10 y redondea al número entero más cercano (o simplemente trunca)

    # El truncamiento tiene más sentido aquí para obtener la décima de segundo.

    tenth_second = int((remaining_seconds - seconds_part) * 10)

    # formateo


    if minutes > 0:
        # Formato: M:SS.m

        # Minutos (M), segundos (SS con cero a la izquierda), décimas de segundo (m)

        return f"{minutes}m:{seconds_part:02d}.{tenth_second}s"

    # Si la duración es inferior a un minuto

    else:
        # Formato: Sm

        # Segundos (S), décimas de segundo (m)

        # El 02d de segundos no suele ser necesario durante menos de un minuto

        return f"{seconds_part}.{tenth_second}s"


# Salidas de ejemplo:

# format_duration(0.1234) -> '0.1s'

# format_duration(1.007) -> '1.0s'

# format_duration(12.51) -> '12.5s'

# formato_duración(65.43) -> '1m:05.4s'


log_formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(message)s')
log_formatter.formatTime = formatTime

# Cree, configure y agregue el controlador de archivos.

file_handler = logging.FileHandler(f'{LOG_FILE}', mode='w', encoding="utf-8")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Cree, configure y agregue el controlador de consola.

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)



def log_debug(text):
    # seg = secDurationSinceExecFunctionStart()

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
    # salida del sistema (1)


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
    # import scripts.py.func.audio_manager # no funciona para mí 4 de diciembre de 25 5:20 p.m. Jue

    from scripts.py.func.audio_manager import (
        sound_program_loaded,  # works 4.12.'25 17:20 Thu
    )
except ImportError as e:
    print(f"Fehler: Konnte 'audio_manager.py' nicht als Modul importieren: {e}")
    log_debug(f"Fehler: Konnte 'audio_manager' no como módulo importar: {e}")

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
    # Palabras interrogativas comunes y palabras de relleno que cambian el hash innecesariamente

    'was', 'wann', 'warum', 'wohin', 'wessen', 'welche', 'welches', 'welcher', 'wieviel',

    # Más verbos auxiliares y preposiciones

    'vom', 'zum', 'zur', 'beim', 'mit', 'durch', 'gegen', 'ohne', 'über', 'unter',
    'ab', 'an', 'bis', 'seit', 'trotz', 'während', 'wegen', 'zum',

    # Pronombres, adverbios y conjunciones

    'dich', 'dir', 'ihm', 'ihr', 'sich', 'uns', 'euch', 'auch', 'mal', 'noch', 'schon', 'denn', 'doch', 'halt', 'eben', 'vielleicht',
    'etwas', 'nichts', 'alles', 'man'
})





# desde pathlib importar ruta




# --- CAPA DE BASE DE DATOS ---

def init_db():
    try:
        # 1. Utilice un tiempo de espera alto y habilite el modo WAL inmediatamente

        conn = sqlite3.connect(DB_FILE, timeout=90)
        conn.execute("PRAGMA journal_mode=WAL;")
        c = conn.cursor()

        # 2. Cuadros centrales

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

        # 3. Ejecutar migraciones/vistas solo si no estamos en una simulación de alta concurrencia

        # o envuélvalos de manera que no bloqueen el inicio

        try:
            # Comprobar si necesitamos actualizar las calificaciones

            c.execute(f"UPDATE responses SET rating = {DEFAULT_RATING} WHERE rating = 0 AND comment IS NULL")

            # Las vistas tienen muchas cerraduras, solo recréalas si es necesario

            c.execute("DROP VIEW IF EXISTS overview_readable")
            c.execute('''
                CREATE VIEW overview_readable AS
                SELECT r.id, r.rating, r.usage_count, p.clean_input AS User_Frage, p.keywords, r.response_text, r.comment, r.created_at
                FROM responses r LEFT JOIN prompts p ON r.prompt_hash = p.hash ORDER BY r.created_at DESC
            ''')
        except sqlite3.OperationalError as e:
            # Si la base de datos está bloqueada, omita la recreación de vista para esta sesión.

            logging.warning(f"Skipping view recreation due to lock: {e}")

        conn.commit()
        conn.close()
    except Exception as e:
        # Aquí es donde se detectó el error de la línea 302

        log_debug(f"DB Init Error: {e}")


def play_cache_hit_sound():
    sound_program_loaded()
    # si create_bent_sine_wave_sound:

    # try:

    # sonido = create_bent_sine_wave_sound(880, 1200, 80, 0.15)

    # sonido.reproducir()

    # excepto excepción como error_msg:

    # log_debug(f"Error: {error_msg}")

    # pasaporte



