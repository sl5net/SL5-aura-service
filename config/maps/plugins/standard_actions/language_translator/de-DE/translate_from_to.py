# config/maps/plugins/standard_actions/language_translator/de-DE/translate_from_to.py
import os
import re
import sys
import time
from pathlib import Path
import subprocess
import logging

project_dir = Path(__file__).parent.parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_dir))

from scripts.py.func.global_state import SIGNATURE_TIMES, SEQUENCE_LOCK
from config import settings
from scripts.py.func.get_active_window_title import get_active_window_title_safe
from config.settings import LANGUAGE_PREFIXES, SIGNATURE_MAPPING
from scripts.py.func.simple_plugin_cache import get_cached_result, set_cached_result
from scripts.py.func.db.trino_client import get_feature_state, get_target_lang


TRANSLATE_SCRIPT = project_dir / 'tools' / 'simple_translate.py'
PYTHON_EXECUTABLE = project_dir / '.venv' / 'bin' / 'python3'


def get_current_signature(lang_target, window_title):
    prefixes = LANGUAGE_PREFIXES
    prefix = prefixes.get(lang_target.lower(), "")
    current_time = time.time()
    brand_text = ""
    cooldown = 3600

    if hasattr(settings, 'SIGNATURE_MAPPING'):
        for pattern, config in settings.SIGNATURE_MAPPING.items():
            if re.search(pattern, str(window_title), re.IGNORECASE):
                brand_text, cooldown = config
                break

    if brand_text:
        with SEQUENCE_LOCK:
            last_time = SIGNATURE_TIMES.get(window_title, 0)
            if (current_time - last_time > cooldown):
                SIGNATURE_TIMES[window_title] = current_time
                return f" {prefix} {brand_text}".strip()

    return ""


def get_smart_signature(lang_target, window_title):
    prefix = LANGUAGE_PREFIXES.get(lang_target.lower(), LANGUAGE_PREFIXES["DEFAULT"])
    active_sig_text = ""
    active_cooldown = 3600
    for pattern, config in SIGNATURE_MAPPING.items():
        if re.search(pattern, str(window_title), re.IGNORECASE):
            active_sig_text, active_cooldown = config
            break

    with SEQUENCE_LOCK:
        current_time = time.time()
        last_time = SIGNATURE_TIMES.get(window_title, 0)
        if (current_time - last_time > active_cooldown):
            SIGNATURE_TIMES[window_title] = current_time
            full_sig = f"{prefix} {active_sig_text}".strip()
            return full_sig

    return ""


def execute(match_data):
    """
    Prueft den Uebersetzungsmodus via Trino (interface-aware).
    Terminal und Web haben unabhaengige Translation-States.
    """
    original_text = match_data.get('original_text')
    logger = logging.getLogger(__name__)



    # 1. Trino: State fuer dieses Interface pruefen
    try:
        INTERFACE = os.getenv("INTERFACE", "speech")
        feature_state = get_feature_state(interface=INTERFACE, feature='translation')
        if feature_state != 'on':
            return original_text
        lang_target = get_target_lang(interface=INTERFACE)
        if lang_target is None:
            return original_text

    except Exception as e:
        # Fallback: translation_state.py falls Trino nicht erreichbar
        logger.warning(f"Trino nicht erreichbar, Fallback auf STATE_FILE: {e}")
        STATE_FILE = Path(__file__).parent / 'translation_state.py'
        if not STATE_FILE.exists():
            return original_text
        content = STATE_FILE.read_text().strip().lower()
        if "='on'" not in content:
            return original_text
        key, _ = content.split('=', 1)
        lang_target = key.strip().replace('_', '-')

    logger.info(f'Translating to {lang_target} (interface={match_data.get("interface", "terminal")})')

    # 2. Cache pruefen
    BASE_DIR_FOR_CACHE = Path(__file__).parent.parent.parent.parent.parent
    cache_key_args = (original_text, str(lang_target))
    cached_response = get_cached_result(
        BASE_DIR_FOR_CACHE,
        TRANSLATE_SCRIPT,
        cache_key_args,
        logger=logger
    )
    if cached_response:
        print(f"DEBUG: CACHE HIT! => {cached_response}")
        return cached_response

    # 3. Uebersetzen
    try:
        if not original_text:
            return None

        print(f"INFO: [Translator Plugin] translate: '{original_text}' interface={match_data.get('interface', 'terminal')}")

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
            check=True,
            encoding='utf-8'
        )

        translated_text = result.stdout.strip()

        _active_window_title = get_active_window_title_safe()
        _active_window_title = getattr(settings, 'active_window_title', 'Unknown')
        current_sig = get_current_signature(lang_target, _active_window_title)

        translated_text = f"{translated_text} (original:'{original_text}' {current_sig})."

        set_cached_result(
            BASE_DIR_FOR_CACHE,
            TRANSLATE_SCRIPT,
            cache_key_args,
            translated_text
        )

        return translated_text

    except subprocess.CalledProcessError as e:
        print(f"ERROR: [Translator Plugin] Fehler vom Uebersetzungsskript: {e.stderr.strip()}", file=sys.stderr)
        logger.info(f"ERROR: [Translator Plugin] Fehler: {e.stderr.strip()}")
        return "Bei der Uebersetzung ist ein Fehler aufgetreten."

    except Exception as e:
        import traceback
        with open("/tmp/stt_debug_error.txt", "a") as f:
            f.write("\n--- NEUER FEHLER ---\n")
            f.write(traceback.format_exc())
        m = 'may you need install ? sudo pacman -S translate-shell ?'
        print(f"ERROR: [Translator Plugin] : {e}", file=sys.stderr)
        logger.info(f"ERROR: [Translator Plugin] : {e} # {m}")
        return f"FEHLER-DETAILS: {str(e)} {m}"
