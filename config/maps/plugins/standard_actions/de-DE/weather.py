# config/maps/plugins/standard_actions/de-DE/weather.py

import subprocess
from pathlib import Path
import configparser
import json
import logging

from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result

from pathlib import Path as p; import os as o  # noqa: E702
with open(('C:/tmp' if o.name == 'nt' else '/tmp') + '/sl5_aura/sl5net_aura_project_root', encoding='utf-8') as f:
    PROJECT_ROOT = p(f.read().strip())  # noqa: E702

CONFIG_FILE = Path(__file__).parent / 'weather_config.ini'

WEATHER_TTL = 900  # 15 Minuten

log_dir = PROJECT_ROOT / 'log'
log_dir.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_dir / 'weather.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

CACHE_DIR_weather = p('/') / 'tmp' / 'sl5_aura' / 'weather_cache'
CACHE_DIR_weather.mkdir(parents=True, exist_ok=True)

# Aktuell in reutlingen sind es 25 Grad, gefuehlt wie 27 Grad. Die Vorhersage meldet: Leicht Bewölkt.
# Aktuell in reutlingen sind es 25 Grad, gefuehlt wie 27 Grad. Die Vorhersage meldet: Leicht Bewölkt.

def execute(match_data):
    """
    Ruft die aktuelle Wettervorhersage für einen vordefinierten Ort ab
    und gibt eine menschenlesbare Zusammenfassung zurück.
    """

    logger.info("--- Weather Execute Call ---")
    logger.info(f"Type of match_data: {type(match_data)}")
    logger.info(f"Content of match_data: {repr(match_data)}")

    # 1. Konfiguration einlesen
    if not CONFIG_FILE.exists():
        return "Fehler: Die Konfigurationsdatei für das Wetter (weather_config.ini) wurde nicht gefunden."

    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        city = config.get('Settings', 'city')
        lang = config.get('Settings', 'language', fallback='de')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        logger.error(f"Fehler in der Wetter-Konfigurationsdatei: {e}")
        return f"Fehler in der Wetter-Konfigurationsdatei: {e}"

    cache_key_args = (city, lang)

    # 2. Match-Daten auswerten und Cache pruefen
    matched_text = ""
    if isinstance(match_data, dict) and 'regex_match_obj' in match_data:
        match_obj = match_data['regex_match_obj']
        logger.info(f"regex_match_obj type: {type(match_obj)}")
        matched_text = match_obj.group(0).lower()
    elif hasattr(match_data, 'group'):
        matched_text = match_data.group(0).lower()

    logger.info(f"Extracted matched_text: '{matched_text}'")

    is_tomorrow = "morgen" in matched_text
    logger.info(f"is_tomorrow evaluated to: {is_tomorrow}")

    cache_key_args = (city, lang, is_tomorrow)

    try:
        cached_response = get_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, WEATHER_TTL)
        if cached_response:
            logger.info("CACHE HIT - kein API-Aufruf noetig.")
            return cached_response
    except Exception as e:
        logger.error(f"Fehler beim Cache-Lesezugriff: {e}")

    # 3. Wetterdaten von wttr.in abrufen
    weather_data = None
    try:
        command = [
            'curl',
            '-s',
            f'https://wttr.in/{city}?format=j1&lang={lang}'
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            timeout=10
        )
        weather_data = json.loads(result.stdout)
    except FileNotFoundError:
        logger.error("curl nicht gefunden.")
        return "Fehler: Das Programm 'curl' wurde nicht gefunden. Bitte installiere es."
    except subprocess.TimeoutExpired:
        logger.warning("API-Timeout. Versuche Stale-Cache.")
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logger.warning(f"API-Fehler ({type(e).__name__}). Versuche Stale-Cache.")
    except Exception as e:
        logger.warning(f"Unbekannter Fehler beim API-Aufruf ({type(e).__name__}: {e}). Versuche Stale-Cache.")

    # 4. Failover auf abgelaufenen Cache, falls API-Aufruf fehlschlug
    if weather_data is None:
        try:
            stale_response = get_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, ttl_seconds=None,
                                               logger=logger)
            if stale_response:
                logger.warning(" (stale) Cache Fallback.")
                return stale_response
        except Exception as e:
            logger.error(f"Fehler beim Stale-Cache-Lesezugriff: {e}")
        return f"Ich konnte die Wetterdaten fuer '{city}' leider nicht abrufen und habe keinen Cache."

    # 5. JSON verarbeiten und Antwort bauen
    try:
        if is_tomorrow:
            tomorrow_weather = weather_data['weather'][1]
            max_temp = tomorrow_weather.get('maxtempC', '?')
            min_temp = tomorrow_weather.get('mintempC', '?')
            hourly_list = tomorrow_weather.get('hourly', [])
            description = "Wetterzustand unbekannt"

            # Mittags-Prognose (12:00 Uhr ist Index 4 im 3-Stunden-Raster)
            if len(hourly_list) > 4:
                midday = hourly_list[4]
            elif len(hourly_list) > 0:
                midday = hourly_list[len(hourly_list) // 2]
            else:
                midday = None

            if midday:
                lang_key = f'lang_{lang}'
                description_list = midday.get(lang_key) or midday.get('weatherDesc')
                if description_list and len(description_list) > 0:
                    description = description_list[0].get('value', 'Keine Beschreibung verfuegbar')

            response = (
                f"Morgen in {city} liegt die Temperatur zwischen {min_temp} und {max_temp} Grad. "
                f"Die Vorhersage meldet: {description}."
            )
        else:
            current_condition = weather_data['current_condition'][0]
            temp_c = current_condition.get('temp_C', '?')
            feels_like_c = current_condition.get('FeelsLikeC', '?')
            lang_key = f'lang_{lang}'
            description_list = current_condition.get(lang_key) or current_condition.get('weatherDesc')
            if description_list and len(description_list) > 0:
                description = description_list[0].get('value', 'Keine Beschreibung verfuegbar')
            else:
                description = "Wetterzustand unbekannt"
            response = (
                f"Aktuell in {city} sind es {temp_c} Grad, gefuehlt wie {feels_like_c} Grad. "
                f"Die Vorhersage meldet: {description}."
            )

        # 6. Ergebnis in Cache schreiben
        try:
            set_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, response)
            logger.info("Ergebnis erfolgreich in Cache geschrieben.")
        except Exception as e:
            logger.error(f"Fehler beim Cache-Schreibzugriff: {e}")
        return response
    except (KeyError, IndexError) as e:
        logger.error(f"Strukturfehler im JSON: {e}")
        return f"Die erhaltenen Wetterdaten hatten ein unerwartetes Format oder der Ort '{city}' wurde nicht gefunden."