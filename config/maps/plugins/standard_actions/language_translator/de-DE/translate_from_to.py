# config/maps/plugins/standard_actions/language_translator/de-DE/translate_from_to.py
# CONFIG_DIR / 'translate_from_to.py'
import re
import sys
import time
from pathlib import Path
import subprocess
import logging

# config/maps/plugins/standard_actions/language_translator/de-DE/translate_from_to.py:9

from scripts.py.func.global_state import SIGNATURE_TIMES, SEQUENCE_LOCK
from config import settings
from scripts.py.func.get_active_window_title import get_active_window_title_safe


from config.settings import LANGUAGE_PREFIXES, SIGNATURE_MAPPING # signatur_ar,signatur_en,signatur_pt_br,signatur_ja
from scripts.py.func.handle_trigger import text_detected

from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result


#Hello, how are you (original:'hallo wie geht's').

STATE_FILE = Path(__file__).parent / 'translation_state.py'

project_dir = Path(__file__).parent.parent.parent.parent.parent.parent.parent

TRANSLATE_SCRIPT = project_dir / 'tools' / 'simple_translate.py'
PYTHON_EXECUTABLE = project_dir / '.venv' / 'bin' / 'python3'

# config/maps/plugins/standard_actions/language_translator/de-DE/translate_from_to.py

import time
import re
from scripts.py.func.global_state import SIGNATURE_TIMES, SEQUENCE_LOCK


def get_current_signature(lang_target, window_title):
    # 1. Hol den sprachspezifischen Präfix (z.B. "Voice Translation")
    # Wir nutzen deine alten Varianten als Basis
    # prefixes = {
    #     'pt-br': 'Tradução de Voz',
    #     'en': 'Voice Translation',
    #     'ar': 'تحدثت الترجمة',
    #     'ja': '話し言葉の翻訳'
    # }
    prefixes = LANGUAGE_PREFIXES


    prefix = prefixes.get(lang_target.lower(), "")

    # 2. Prüfe App-Mapping & Cooldown
    current_time = time.time()
    brand_text = ""
    cooldown = 3600  # Default

    if hasattr(settings, 'SIGNATURE_MAPPING'):
        for pattern, config in settings.SIGNATURE_MAPPING.items():
            if re.search(pattern, str(window_title), re.IGNORECASE):
                brand_text, cooldown = config
                break

    # 3. DER ENTSCHEIDENDE COOLDOWN-CHECK
    if brand_text:
        with SEQUENCE_LOCK:
            last_time = SIGNATURE_TIMES.get(window_title, 0)
            if (current_time - last_time > cooldown):
                # Zeitstempel aktualisieren!
                SIGNATURE_TIMES[window_title] = current_time
                # Rückgabe: "Präfix + Branding"
                return f" {prefix} {brand_text}".strip()

    return ""  # Cooldown aktiv -> Keine Signatur

















def get_smart_signature(lang_target, window_title):
    # 1. Sprach-Präfix holen
    prefix = LANGUAGE_PREFIXES.get(lang_target.lower(), LANGUAGE_PREFIXES["DEFAULT"])

    # 2. App-Branding & Cooldown bestimmen
    active_sig_text = ""
    active_cooldown = 3600
    for pattern, config in SIGNATURE_MAPPING.items():
        if re.search(pattern, str(window_title), re.IGNORECASE):
            active_sig_text, active_cooldown = config
            break

    # 3. Cooldown-Check
    with SEQUENCE_LOCK:
        current_time = time.time()
        last_time = SIGNATURE_TIMES.get(window_title, 0)

        if (current_time - last_time > active_cooldown):
            # Update Zeitstempel
            SIGNATURE_TIMES[window_title] = current_time
            # Kombiniere Präfix und Branding
            # Falls Präfix vorhanden, füge ein Leerzeichen dazwischen ein
            full_sig = f"{prefix} {active_sig_text}".strip()
            return full_sig

    return ""  # Cooldown aktiv oder keine Signatur konfiguriert




def execute(match_data):
    """
    Prüft den Übersetzungsmodus. Wenn aktiv, wird der Text mit dem sauberen
    simple_translate.py Skript übersetzt und das Ergebnis zurückgegeben.
    """
    # 1. Prüfen, ob der Übersetzungsmodus aktiv ist
    original_text = match_data.get('original_text')

    # match_obj = match_data['regex_match_obj']

    # ('', r'^(Switch|Aktiviere|aktivieren|aktiviert|aktiv|einschalten|deaktivieren|deaktiviere|ausschalten|ausschau|toggle) (Englisch|ennglish\w*)\b', 95, {

    # = int(match_obj.group(1))
    # operator = match_obj.group(2).lower()
    # lang_target = int(match_obj.group(3))



    #Übersetzung anschaltenenglisch einschaltenokay (original:'okay').englisch ausschalten

    if not STATE_FILE.exists():
        # return '2025-1222-0606'
        return original_text  # Modus aus, nichts tun

#englisch einschaltenokay (original:'okay').englisch ausschaltenokay

    content = STATE_FILE.read_text().strip().lower()
    if "='on'" not in content:
        # return '2025-1222-0606b'
        return original_text  # Modus aus, nichts tun

    key, value = content.split('=', 1)

    # Prefix speichern (entfernt Leerzeichen)
    lang_target = key.strip()
    lang_target = lang_target.strip().replace('_', '-')

    # 'pt-BR' # Ziel: Brasilianisches Portugiesisch
    # 'ar' # Ziel: arabisch

    logger = logging.getLogger(__name__)
    logger.info(f'🌈 Translating to {lang_target}')


    # --- 1. CACHE PRÜFEN (Key-Args sind die Parameter, die die Ausgabe bestimmen) ---
    BASE_DIR_FOR_CACHE = Path(__file__).parent.parent.parent.parent.parent # <- Korrigieren Sie dies auf Ihren stabilen TMP-Pfad!

    cache_key_args = (original_text, str(lang_target))
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
        TRANSLATE_SCRIPT,
        cache_key_args,
        logger=logger
    )
    if cached_response:
        # CACHE HIT! KEIN NETZWERK-AUFRUF
        print(f"DEBUG: CACHE HIT! => {cached_response}")
        return cached_response

    #

    try:
        if not original_text:
            return None # Kein Text zum Übersetzen

        print(f"INFO: [Translator Plugin] trnslate: '{original_text}'")

        # 2. Das NEUE, saubere Übersetzungsskript aufrufen
        command = [
            str(PYTHON_EXECUTABLE),
            str(TRANSLATE_SCRIPT),
            original_text,
            str(lang_target)

        ]

        print(f"INFO: [Translator Plugin] Translation command: '{' '.join(command)}'")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # Löst einen Fehler aus, wenn simple_translate.py mit sys.exit(1) endet
            encoding='utf-8'
        )


        translated_text = result.stdout.strip()

        # 3. Das reine Ergebnis zurückgeben, damit der Service es sprechen kann
        # Sprachübersetzung - Tradução de VozTesttest (original:'test', Voice Translation SL5.de/Aura Powered by SL5.de/Aura ).

        #

        _active_window_title = get_active_window_title_safe()

        # --- Signatur-Check-Logik ---
        current_sig = ""  # Standard: Keine Signatur
        _active_window_title = getattr(settings, 'active_window_title', 'Unknown')  # Falls verfügbar

        # current_sig = get_smart_signature(lang_target, _active_window_title)
        current_sig = get_current_signature(lang_target, _active_window_title)

        translated_text = f"{translated_text} (original:'{original_text}' {current_sig})."

        # --- 3. ERFOLG: ERGEBNIS SPEICHERN ---
        set_cached_result(
            BASE_DIR_FOR_CACHE,
            TRANSLATE_SCRIPT,
            cache_key_args,
            translated_text # Speichere nur die erfolgreiche menschenlesbare Antwort
        )
        return translated_text


        # ﻿Sprach Übersetzung﻿ar okay funktionieren ﻿sprach BesetzungBei der Übersetzung ist ein unerwarteter Fehler aufgetreten.

    except subprocess.CalledProcessError as e:
        # Das simple_translate.py Skript hat einen Fehler gemeldet.
        # Die Fehlermeldung steht in e.stderr.
        print(f"ERROR: [Translator Plugin] Fehler vom Übersetzungsskript: {e.stderr.strip()}", file=sys.stderr)
        logger.info(f'🌈 Translating to {lang_target}')
        logger.info(f"🛑🛑🛑 ERROR: 🌈 [Translator Plugin] Fehler vom Übersetzungsskript: {e.stderr.strip()}")

        return "Bei der Übersetzung ist ein Fehler aufgetreten."
    except Exception as e:
        print(f"🛑🛑🛑 ERROR: 🌈 ERROR: [Translator Plugin] : {e}", file=sys.stderr)
        logger.info(f"🛑🛑🛑 ERROR: 🌈 ERROR: [Translator Plugin] : {e}")
        return "Bei der Übersetzung ist ein unerwarteter Fehler aufgetreten."
