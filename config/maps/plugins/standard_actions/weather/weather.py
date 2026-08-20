# config/maps/plugins/standard_actions/weather/weather.py
import subprocess
from pathlib import Path
import configparser
import json
import logging

from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result

from pathlib import Path as p; import os as o  # noqa: E702
with open(('C:/tmp' if o.name == 'nt' else '/tmp') + '/sl5_aura/sl5net_aura_project_root', encoding='utf-8') as f:
    SL5NET_AURA_PROJECT_ROOT = p(f.read().strip())  # noqa: E702

# CONFIG_FILE = Path(__file__).parent / 'weather_config.ini'
import urllib.parse
import urllib.request

CONFIG_FILE = Path(__file__).parent / 'weather_config.ini'

WMO_WEATHER_CODES_DE = {
    0: "Klarer Himmel",
    1: "Hauptsächlich klar",
    2: "Teilweise bewölkt",
    3: "Bedeckt",
    45: "Nebel",
    48: "Reifnebel",
    51: "Leichter Nieselregen",
    53: "Mäßiger Nieselregen",
    55: "Dichter Nieselregen",
    61: "Leichter Regen",
    63: "Mäßiger Regen",
    65: "Starker Regen",
    71: "Leichter Schneefall",
    73: "Mäßiger Schneefall",
    75: "Starker Schneefall",
    80: "Leichte Regenschauer",
    81: "Mäßige Regenschauer",
    82: "Heftige Regenschauer",
    95: "Gewitter",
    96: "Gewitter mit leichtem Hagel",
    99: "Gewitter mit schwerem Hagel",
}


def fetch_open_meteo_weather(city: str, lang: str = "de", is_tomorrow: bool = False):
    encoded_city = urllib.parse.quote(city)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language={lang}&format=json"
    req_geo = urllib.request.Request(geo_url, headers={"User-Agent": "SL5-Aura/1.0"})
    with urllib.request.urlopen(req_geo, timeout=5) as resp_geo:
        geo_data = json.loads(resp_geo.read().decode("utf-8"))

    results = geo_data.get("results")
    if not results:
        return None

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]
    resolved_name = results[0].get("name", city)

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,apparent_temperature,weather_code"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )
    req_fc = urllib.request.Request(forecast_url, headers={"User-Agent": "SL5-Aura/1.0"})
    with urllib.request.urlopen(req_fc, timeout=5) as resp_fc:
        fc_data = json.loads(resp_fc.read().decode("utf-8"))

    if is_tomorrow:
        daily = fc_data.get("daily", {})
        min_temp = round(daily.get("temperature_2m_min", [0, 0])[1])
        max_temp = round(daily.get("temperature_2m_max", [0, 0])[1])
        code = daily.get("weather_code", [0, 0])[1]
        desc = WMO_WEATHER_CODES_DE.get(code, "Wetterzustand unbekannt")
        return (
            f"Morgen in {resolved_name} liegt die Temperatur zwischen {min_temp} und {max_temp} Grad. "
            f"Die Vorhersage meldet: {desc}."
        )

    current = fc_data.get("current", {})
    temp_c = round(current.get("temperature_2m", 0))
    feels_like_c = round(current.get("apparent_temperature", 0))
    code = current.get("weather_code", 0)
    desc = WMO_WEATHER_CODES_DE.get(code, "Wetterzustand unbekannt")
    return (
        f"Aktuell in {resolved_name} sind es {temp_c} Grad, gefuehlt wie {feels_like_c} Grad. "
        f"Die Vorhersage meldet: {desc}."
    )

WEATHER_TTL = 900  # 15 Minuten

log_dir = SL5NET_AURA_PROJECT_ROOT / 'log'
log_dir.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_dir / 'weather.log', encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

CACHE_DIR_weather = p('/') / 'tmp' / 'sl5_aura' / 'weather_cache'
CACHE_DIR_weather.mkdir(parents=True, exist_ok=True)

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

    # 3. Wetterdaten via Open-Meteo abrufen (mit wttr.in Fallback)
    response = None
    try:
        response = fetch_open_meteo_weather(city, lang, is_tomorrow)
    except Exception as e:
        logger.warning(f"Open-Meteo lookup failed ({type(e).__name__}: {e}). Trying wttr.in fallback.")
    if response:
        try:
            set_cached_result(CACHE_DIR_weather, 'get_weather', cache_key_args, response)
            logger.info("Ergebnis erfolgreich in Cache geschrieben.")
        except Exception as e:
            logger.error(f"Fehler beim Cache-Schreibzugriff: {e}")
        return response

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
