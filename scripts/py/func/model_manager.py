# File: scripts/py/func/model_manager.py
#
import sys, vosk
from .check_memory_critical import check_memory_critical
from .notify import notify

def manage_models(logger, loaded_models, desired_names, threshold_mb, script_dir):
    """Dynamically loads/unloads models based on available memory."""
    is_critical, avail_mb = check_memory_critical(threshold_mb)

    if is_critical:
        if len(loaded_models) > 1:
            key = list(loaded_models.keys())[-1]
            logger.warning(f"Low memory ({avail_mb:.0f}MB). Unloading model: '{key}'")
            del loaded_models[key]
        else:
            logger.warning(f"Low memory ({avail_mb:.0f}MB), keeping last model.")
        return

    # Check if a desired model is missing and can be loaded
    loaded_keys = loaded_models.keys()
    for model_name in desired_names:
        lang_key = model_name.split('-')[2]
        if lang_key not in loaded_keys:
            logger.info(f"Memory stable. Attempting to load missing model: '{model_name}'")
            try:
                model_path = script_dir / "models" / model_name
                model = vosk.Model(str(model_path))
                loaded_models[lang_key] = model
                logger.info(f"Successfully loaded model for '{lang_key}'.")
                # Load one per cycle to be safe
                break
            except Exception as e:
                logger.error(f"Failed to reload '{model_name}': {e}")
                break

