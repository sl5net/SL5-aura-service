# file: scripts/py/func/model_manager.py
"""
This module provides a dynamic, stateful model manager designed to run
continuously within the main service loop.

Core Responsibilities:
1.  **Reactive Loading:** It iteratively loads models specified in the
    `PRELOAD_MODELS` list, but only if sufficient system memory is
    available. This prevents the service from crashing on low-memory
    systems.
2.  **Memory Monitoring:** On each invocation, it checks the current
    available memory against a critical threshold.
3.  **Proactive Unloading:** If memory becomes critical, it intelligently
    unloads the least-recently-used model to free up resources and ensure
    service stability.

By being called repeatedly, it ensures the service adapts to changing
system conditions, making it robust and responsive.
"""

import math

import vosk
from vosk import SetLogLevel
SetLogLevel(-1)
# SetLogLevel(WARNINGS)
# vosk.SetLogLevel(-1) # sadly it changes nothing (se, 15.12.'25 15:10 Mon )

from .check_memory_critical import check_memory_critical
from .notify import notify

from .config.dynamic_settings import settings

import threading

MODELS_LOCK = threading.Lock()


max_model_memory_footprint_mb = 0


def _format_gb(mb):
    """Helper to format MB into a readable GB string."""
    if mb < 1024:
        return f"{mb:.0f}MB"
    return f"{mb / 1024:.1f}GB"


# In model_manager.py

def load_single_model(logger, model_path, lang_key, loaded_models):
    """Loads a single Vosk model and adds it to the dictionary."""
    try:
        logger.info(f"Attempting to load model '{lang_key}' from {model_path}...")
        model = vosk.Model(str(model_path))

        with MODELS_LOCK:  # Protect access to the shared dictionary
            loaded_models[lang_key] = model

        logger.info(f"✅ MODEL READY: '{lang_key}'")
    except Exception as e:
        logger.error(f"Failed to load model '{lang_key}': {e}")







def manage_models(logger, loaded_models, desired_names, threshold_mb, script_dir):
    """Dynamically loads/unloads models based on available memory."""
    global max_model_memory_footprint_mb

    # --- Unloading Logic ---
    is_critical, avail_mb = check_memory_critical(threshold_mb)
    if is_critical:
        if not loaded_models:
            return max_model_memory_footprint_mb

        key_to_unload = list(loaded_models.keys())[-1]
        logger.warning(f"Low memory ({_format_gb(avail_mb)} available). Unloading model '{key_to_unload}'.")
        del loaded_models[key_to_unload]
        notify("Memory Manager", f"Unloaded '{key_to_unload}' model. {_format_gb(avail_mb)} RAM free.")
        return max_model_memory_footprint_mb

    desired_lang_keys = {name.split('-')[2] for name in desired_names}
    if set(loaded_models.keys()) == desired_lang_keys:
        # logger.info("All desired models are already loaded. Nothing to do.")
        return max_model_memory_footprint_mb

    # --- Loading Logic ---
    for model_name in desired_names:
        lang_key = model_name.split('-')[2]
        if lang_key in loaded_models:
            logger.info(f"model {lang_key} already loaded.")
            continue

        # File: scripts/py/func/model_manager.py
        model_path = script_dir / "models" / model_name
        if not model_path.exists():
            logger.warning(f"⚠️ WARNING: Model directory not found. Remove it from desired_names and skipping: {model_path}")
            desired_names.remove(model_name)
            return  # Go to the next model in the list
        else:
            logger.info(f"✅ Model directory found: ..{str(model_path)[-30:]} = ..{str(script_dir)[-10:]} / 'models' / {model_name}")


        # File: scripts/py/func/model_manager.py
        load_buffer_mb = math.ceil(threshold_mb * 0.10)
        required_memory_mb = threshold_mb + load_buffer_mb + max_model_memory_footprint_mb
        if avail_mb < required_memory_mb:
            if max_model_memory_footprint_mb > 0:
                # IMPROVED LOG: Explain the calculation for "Required Memory"
                log_msg = (
                    f"Postponing load: {_format_gb(avail_mb)} available is not enough. "
                    f"Need ~{_format_gb(required_memory_mb)} "
                    f"(Threshold: {_format_gb(threshold_mb)} + Model: {_format_gb(max_model_memory_footprint_mb)} + Buffer: {_format_gb(load_buffer_mb)})"
                )
                if settings.DEV_MODE:
                    logger.info(log_msg)
            return max_model_memory_footprint_mb



        # new code follows here :

        if avail_mb < required_memory_mb:
            if max_model_memory_footprint_mb > 0:
                log_msg = (
                    f"Postponing load: {_format_gb(avail_mb)} available is not enough. "
                    f"Need ~{_format_gb(required_memory_mb)} "
                    f"(Threshold: {_format_gb(threshold_mb)} + Model: {_format_gb(max_model_memory_footprint_mb)} + Buffer: {_format_gb(load_buffer_mb)})"
                )
                if settings.DEV_MODE: # Only log if DEV_MODE is enabled
                    logger.info(log_msg)
            # IMPORTANT CHANGE: Replace 'return' with 'continue'
            continue # <--- CONTINUE to the next model in desired_names
            # If the current model cannot be loaded due to memory,
            # we still want to check other desired models in this iteration.

            # read 2025-1013-1734.txt in home path
            # read 2025-1013-1734.txt in home path
            # read 2025-1013-1734.txt in home path
            # read 2025-1013-1734.txt in home path
            # read 2025-1013-1734.txt in home path

        logger.info(f"Attempting to ⏳ load missing model: '{model_name}'")
        try:

            _, avail_before = check_memory_critical(threshold_mb)
            loaded_model = vosk.Model(str(model_path))

            _, avail_after = check_memory_critical(threshold_mb)

            loaded_models[lang_key] = loaded_model

            footprint = avail_before - avail_after

            if footprint > max_model_memory_footprint_mb:
                max_model_memory_footprint_mb = footprint
                logger.info(f"Learned new max model footprint: ~{_format_gb(footprint)}")



            # Define ANSI color codes for clarity
            GREEN = '\033[92m'  # Bright Green
            BOLD = '\033[1m'
            ENDC = '\033[0m'  # End color

            # The visually distinct message
            print("\n")
            print(f"{BOLD}{GREEN}====================================================={ENDC}")
            print(f"{BOLD}{GREEN}==                                                 =={ENDC}")
            logger.info(f"==    ✅ MODEL READY: '{lang_key}'.")
            print(f"{BOLD}{GREEN}==                                                 =={ENDC}")
            print(f"{BOLD}{GREEN}====================================================={ENDC}")
            print("\n")


        except Exception as e:
            logger.error(f"❌ CRITICAL ERROR: Failed to load Vosk model '{model_name}' for language '{lang_key}': {e}", exc_info=True)

        return max_model_memory_footprint_mb


