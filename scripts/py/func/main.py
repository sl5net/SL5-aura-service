# File: scripts/py/func/main.py

import threading, time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

    SILENCE_TIMEOUT = config["SILENCE_TIMEOUT"]

    PRELOAD_MODELS = config["PRELOAD_MODELS"]
    CRITICAL_THRESHOLD_MB = config["CRITICAL_THRESHOLD_MB"]


    if not SILENCE_TIMEOUT:
        logger.error(f"SILENCE_TIMEOUT: '{SILENCE_TIMEOUT}' ")

    try:
        # --- UNIFIED LOGIC FOR ALL OS ---
        logger.info(f"Starting watchdog observer for triggers on '{trigger_file_path.name}'.")
        trigger_event = threading.Event()


        class TriggerEventHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.src_path == str(trigger_file_path.resolve()):
                    trigger_event.set()


        observer = Observer()
        observer.schedule(TriggerEventHandler(), path=str(TMP_DIR), recursive=False)
        observer.start()

        while True:
            # Wait efficiently for a trigger, with a timeout for maintenance
            trigger_event.wait(timeout=5.0)

            # This block runs every 5s OR when a trigger happens
            Path(heartbeat_file).write_text(str(int(time.time())))
            # active_threads = [t for t in active_threads if t.is_alive()]
            manage_models(logger, loaded_models, PRELOAD_MODELS, CRITICAL_THRESHOLD_MB, script_dir)

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


