# config/maps/plugins/standard_actions/de-DE/weather.py

import subprocess
from pathlib import Path
import configparser
import json

from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result

# Pfad zur Konfigurationsdatei (liegt im selben Ordner wie dieses Skript)
CONFIG_FILE = Path(__file__).parent / 'weather_config.ini'

WEATHER_TTL = 300 # 5 Minuten

def execute(match_data):
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
        return f"Fehler in der Wetter-Konfigurationsdatei: {e}"


    # 0. Benötigte Basisverzeichnisse (Muss von der aufrufenden Funktion bereitgestellt werden!)
    # ANNAHME: match_data enthält ein 'base_dir' für den stabilen Cache-Pfad
    # Hier müsste base_dir korrekt übergeben werden. Für's Beispiel nehmen wir an, es ist der Plugin-Ordner.

    # --- 1. CACHE PRÜFEN (Key-Args sind die Parameter, die die Ausgabe bestimmen) ---
    BASE_DIR_FOR_CACHE = Path(__file__).parent.parent.parent.parent.parent # <- Korrigieren Sie dies auf Ihren stabilen TMP-Pfad!

    cache_key_args = (city, lang)
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
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

    except FileNotFoundError:
        return "Fehler: Das Programm 'curl' wurde nicht gefunden. Bitte installiere es."
    except subprocess.TimeoutExpired:
        return "Die Wetterabfrage hat zu lange gedauert. Bitte versuche es später erneut."
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return f"Ich konnte die Wetterdaten für '{city}' leider nicht abrufen."
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}"

    # 3. Die JSON-Antwort verarbeiten und einen Satz bauen
    try:
        current_condition = weather_data['current_condition'][0]
        temp_c = current_condition['temp_C']
        feels_like_c = current_condition['FeelsLikeC']
        # Die Beschreibung ist in einer Liste, wir nehmen das erste Element.
        description = current_condition[f'lang_{lang}'][0]['value']

        # Baue einen schönen, verständlichen Satz
        response = (
            f"Aktuell in {city} sind es {temp_c} Grad, gefühlt wie {feels_like_c} Grad. "
            f"Die Vorhersage meldet: {description}."
        )


       # --- 3. ERFOLG: ERGEBNIS SPEICHERN ---
        set_cached_result(
            BASE_DIR_FOR_CACHE,
            'get_weather',
            cache_key_args,
            response # Speichere nur die erfolgreiche menschenlesbare Antwort
        )

        return response

    except (KeyError, IndexError):
        return "Die erhaltenen Wetterdaten hatten ein unerwartetes Format."

