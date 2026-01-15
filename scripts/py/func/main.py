# File: scripts/py/func/main.py

import threading, time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config.dynamic_settings import settings
from .audio_manager import sound_program_loaded
from .log_memory_details import log_memory_details
from .press_trigger_button import press_trigger_button

from pathlib import Path



from .handle_trigger import handle_trigger
# from .check_memory_critical import check_memory_critical
# from .notify import notify

from .prioritize_model import prioritize_model

from .model_manager import manage_models

def main(logger, loaded_models, config, suspicious_events, recording_time, active_lt_url):

    global observer


    # active_threads = []


    # Unpack config dictionary
    script_dir = config["SCRIPT_DIR"]
    TMP_DIR = config["TMP_DIR"]

    trigger_file_path = config["TRIGGER_FILE"]
    heartbeat_file = config["HEARTBEAT_FILE"]
    project_root = config["PROJECT_ROOT"]

    SPEECH_PAUSE_TIMEOUT = config["SPEECH_PAUSE_TIMEOUT"]

    PRELOAD_MODELS = config["PRELOAD_MODELS"]
    CRITICAL_THRESHOLD_MB = config["CRITICAL_THRESHOLD_MB"]


    if not SPEECH_PAUSE_TIMEOUT:
        logger.error(f"SPEECH_PAUSE_TIMEOUT: '{SPEECH_PAUSE_TIMEOUT}' ")

    try:
        # --- UNIFIED LOGIC FOR ALL OS ---
        logger.info(f"Starting 👀 watchdog observer for triggers on '{trigger_file_path.name}'.")
        trigger_event = threading.Event()


        class TriggerEventHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.src_path == str(trigger_file_path.resolve()):
                    trigger_event.set()


        observer = Observer()
        observer.schedule(TriggerEventHandler(), path=str(TMP_DIR), recursive=False)
        observer.start()

        # scripts/py/func/main.py:66
        # if getattr(settings, "DEV_MODE_memory", False):

        if getattr(settings, "DEV_MODE_memory", False):
            log_memory_details("before while True", logger)

        is_first_loading = None
        while True:
            # Wait efficiently for a trigger, with a timeout for maintenance
            trigger_event.wait(timeout=5.0)


            # This block runs every 5s OR when a trigger happens
            Path(heartbeat_file).write_text(str(int(time.time())))
            # active_threads = [t for t in active_threads if t.is_alive()]


            if not loaded_models:
                is_first_loading = True

            manage_models(logger, loaded_models, PRELOAD_MODELS, CRITICAL_THRESHOLD_MB, script_dir)

            if is_first_loading:
                is_first_loading = False
                # sound_mute()
                sound_program_loaded()

                from scripts.py.func.process_text_in_background import process_text_in_background
                from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model
                # lang_code = get_system_language_code()

                found_key = list(loaded_models.keys())[0]
                lang_code = guess_lt_language_from_model(logger, found_key)

                logger.info(f"lang_code: {lang_code}")
                raw_text = 'Program loaded'
                tmp_dir = config['TMP_DIR']
                test_output_dir = tmp_dir / "sl5_aura_self_test"
                test_output_dir.mkdir(parents=True, exist_ok=True)

                test_output_dir = tmp_dir / "sl5_aura_self_test"

                process_text_in_background(logger,
                                           lang_code,
                                           raw_text,
                                           test_output_dir,
                                           time.time(),
                                           config['languagetool_process'],
                                           output_dir_override=test_output_dir)

            if trigger_event.is_set():
                trigger_event.clear()  # Reset for the next trigger

                if press_trigger_button():
                    handle_trigger(logger,
                                   loaded_models,
                                   suspicious_events,
                                   project_root,
                                   TMP_DIR,
                                   recording_time,
                                   active_lt_url)
                else:
                    logger.info("Ignoring debounced trigger press.")


    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    except Exception as e:
        logger.error(f"FATAL ERROR {e} in main loop:", exc_info=True)
    # finally:
    #    observer.stop()
    #    observer.join()

    #    logger.info("Waiting for all background threads to finish...")
    #    for t in active_threads:
    #        t.join()


def start_background_model_loader(logger, config, loaded_models):
    """Starts a new thread to load all models without blocking the main app."""
    from scripts.py.func.model_manager import load_single_model  # Import inside

    def loader_thread_target():
        # Hier deine Logik, um die zu ladenden Modelle zu finden
        # (z.B. durch Scannen des 'models'-Verzeichnisses)
        models_to_load = {
            "de": config["PROJECT_ROOT"] / "models/vosk-model-de-0.21",
            "en": config["PROJECT_ROOT"] / "models/vosk-model-en-us-0.22"
        }

        for lang_key, path in models_to_load.items():
            load_single_model(logger, path, lang_key, loaded_models)

    # --- START: ONE-TIME PRIORITIZATION ON STARTUP ---
    project_root = config["PROJECT_ROOT"]
    last_used_file = project_root / "config/model_name_lastused.txt"

    start_background_model_loader(logger, config, loaded_models)

    try:
        if last_used_file.exists():
            last_used_model_name = last_used_file.read_text().strip()
            key_to_prioritize = None

            # Find the corresponding short key (e.g., 'de') for the last used model name
            for key in loaded_models.keys():
                if f"-{key}-" in last_used_model_name:
                    key_to_prioritize = key
                    break

            if key_to_prioritize:
                logger.info("Performing initial model prioritization on startup.")
                prioritize_model(logger, loaded_models, key_to_prioritize)

    except Exception as e:
        logger.error(f"Could not perform initial model prioritization: {e}")
    # --- END: ONE-TIME PRIORITIZATION ON STARTUP ---


    loader_thread = threading.Thread(target=loader_thread_target, daemon=True)
    loader_thread.start()
    logger.info("🚀 Background model loader started.")



