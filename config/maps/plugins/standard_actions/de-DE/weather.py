# config/maps/plugins/standard_actions/de-DE/weather.py

import subprocess
from pathlib import Path
import configparser
import json
import logging

from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#

# Pfad zur Konfigurationsdatei (liegt im selben Ordner wie dieses Skript)
CONFIG_FILE = Path(__file__).parent / 'weather_config.ini'

WEATHER_TTL = 900 # 15 Minuten

log_dir = PROJECT_ROOT / 'log'
log_dir.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_dir / 'weather.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

# config/maps/plugins/standard_actions/de-DE/weather.py:28
CACHE_DIR_weather = p('/') / 'tmp' / 'sl5_aura' / 'weather_cache'
CACHE_DIR_weather.mkdir(parents=True, exist_ok=True)
# BASE_DIR_FOR_CACHE = CACHE_DIR


def execute(match_data):


    # logger = logging.getLogger(__name__)
    # logger.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    """
    Ruft die aktuelle Wettervorhersage für einen vordefinierten Ort ab
    und gibt eine menschenlesbare Zusammenfassung zurück.
    """
    # 1. Konfiguration einlesen
    if not CONFIG_FILE.exists():
        return "Fehler: Die Konfigurationsdatei für das Wetter (weather_config.ini) wurde nicht gefunden."

    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        city = config.get('Settings', 'city')
        lang = config.get('Settings', 'language', fallback='de')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        logger.info(f"Fehler in der Wetter-Konfigurationsdatei: {e}")
        return f"Fehler in der Wetter-Konfigurationsdatei: {e}"


    # 0. Benötigte Basisverzeichnisse (Muss von der aufrufenden Funktion bereitgestellt werden!)
    # ANNAHME: match_data enthält ein 'base_dir' für den stabilen Cache-Pfad
    # Hier müsste base_dir korrekt übergeben werden. Für's Beispiel nehmen wir an, es ist der Plugin-Ordner.

    # --- 1. CACHE PRÜFEN (Key-Args sind die Parameter, die die Ausgabe bestimmen) ---


    cache_key_args = (city, lang)

    # Normaler Cache-Check
    try:
        cached_response = get_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, WEATHER_TTL)
        if cached_response:
            return cached_response
    except Exception as e:
        logger.error(f"Fehler beim Cache-Lesezugriff: {e}")




    cache_key_args = (city, lang)
    cached_response = get_cached_result(
        CACHE_DIR_weather,
        'get_weather',
        cache_key_args,
        WEATHER_TTL
    )
    if cached_response:
        # CACHE HIT! KEIN NETZWERK-AUFRUF
        print(f"DEBUG: CACHE HIT! => {cached_response}")
        return cached_response



    # 2. Wetterdaten von wttr.in abrufen
    try:
        # Wir fragen das "?format=j1" an, um eine einfache JSON-Antwort zu erhalten.
        # Das ist viel stabiler als Text zu parsen.
        command = [
            'curl',
            '-s', # Silent mode, keine Fortschrittsanzeige
            f'https://wttr.in/{city}?format=j1&lang={lang}'
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # Löst bei Fehlern (z.B. keine Verbindung) eine Ausnahme aus
            encoding='utf-8',
            timeout=10 # Verhindert, dass das Skript ewig wartet
        )

        weather_data = json.loads(result.stdout)

    except Exception as e:
        logger.warning(f"API Fehler: {e}. Versuche Stale-Cache.")
        return get_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, ttl_seconds=None)

    # --- 3. EXCEPTION: FAILOVER AUF ABGELAUFENEN CACHE ---
    except (subprocess.CalledProcessError, json.JSONDecodeError, subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:

        # Füge einen Log-Eintrag hinzu, der zeigt, dass die API fehlschlug
        if logger:
            logger.warning(f"API-Abruf fehlgeschlagen ({type(e).__name__}). Versuche, den abgelaufenen Cache zu laden...")

        # ZWEITER CACHE-ABRUF: Ohne TTL-Angabe (d.h., ttl_seconds=None)
        # Dies ruft den letzten gespeicherten Eintrag ab, egal wie alt er ist (ewiger Cache).
        stale_response = get_cached_result(
            CACHE_DIR_weather,
            'get_weather',
            cache_key_args,
            logger=logger # Wichtig: TTL wird hier weggelassen/ist None
        )

        if stale_response:
            # Erfolgreicher Failover: Liefere alte, aber gültige Antwort
            if logger:
                logger.warning("Liefere ABGELAUFENEN (stale) Cache als Fallback.")
            return stale_response

        # Kein Stale-Cache verfügbar: Liefere die Fehlermeldung des API-Aufrufs

        if isinstance(e, FileNotFoundError):
            return "Fehler: Das Programm 'curl' wurde nicht gefunden. Bitte installiere es."
        elif isinstance(e, subprocess.TimeoutExpired):
            return "Die Wetterabfrage hat zu lange gedauert. Bitte versuche es später erneut."
        elif isinstance(e, (subprocess.CalledProcessError, json.JSONDecodeError)):
            return f"Ich konnte die Wetterdaten für '{city}' leider nicht abrufen."
        else:
            return f"Ein unerwarteter Fehler ist aufgetreten: {e}"

    # 3. Die JSON-Antwort verarbeiten und einen Satz bauen

        # 3. Die JSON-Antwort verarbeiten und einen Satz bauen
    try:
        current_condition = weather_data['current_condition'][0]

        # Sicherer Abruf der Werte mit Standardwerten (N/A), falls ein Key fehlt
        temp_c = current_condition.get('temp_C', '?')
        feels_like_c = current_condition.get('FeelsLikeC', '?')

        # Sprachspezifische Beschreibung finden
        # Wir versuchen erst die Sprache (z.B. lang_de), dann das Standard-Feld 'weatherDesc'
        lang_key = f'lang_{lang}'
        description_list = current_condition.get(lang_key) or current_condition.get('weatherDesc')

        if description_list and len(description_list) > 0:
            description = description_list[0].get('value', 'Keine Beschreibung verfügbar')
        else:
            description = "Wetterzustand unbekannt"

        # Baue die Antwort
        response = (
            f"Aktuell in {city} sind es {temp_c} Grad, gefühlt wie {feels_like_c} Grad. "
            f"Die Vorhersage meldet: {description}."
        )

        # --- ERFOLG: ERGEBNIS SPEICHERN ---
        set_cached_result(
            CACHE_DIR_weather,
            'get_weather',
            cache_key_args,
            response
        )

        return response

    except (KeyError, IndexError) as e:
        # Logge den Fehler und das JSON für die Fehlersuche
        logger.error(f"Strukturfehler im JSON: {e}")
        # Optional: Logge das ganze JSON, um zu sehen, was schief lief:
        # logger.debug(f"JSON Inhalt: {result.stdout}")
        return f"Die erhaltenen Wetterdaten hatten ein unerwartetes Format oder der Ort '{city}' wurde nicht gefunden."


        # --- 3. ERFOLG: ERGEBNIS SPEICHERN ---


    except (KeyError, IndexError):
        return "Die erhaltenen Wetterdaten hatten ein unerwartetes Format."



