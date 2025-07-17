# file: scripts/py/func/prioritize_model.py
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

def prioritize_model(logger, loaded_models: dict, key_to_prioritize: str):
    """
    Moves a model to the front of the 'loaded_models' dictionary to ensure
    it's the last to be unloaded in low-memory situations.

    The dictionary is modified in-place.
    """
    if key_to_prioritize in loaded_models:
        logger.info(f"Prioritizing active model '{key_to_prioritize}'.")

        # Rebuild the dictionary to move the active model to the front
        active_model_instance = loaded_models.pop(key_to_prioritize)
        reordered_dict = {key_to_prioritize: active_model_instance, **loaded_models}

        loaded_models.clear()
        loaded_models.update(reordered_dict)

        logger.info(f"New model order for unloading priority: {list(loaded_models.keys())}")
    else:
        logger.warning(f"Could not prioritize model. Key '{key_to_prioritize}' not found in loaded models.")

