# file scripts/py/func/guess_lt_language_from_model.py
def guess_lt_language_from_model(logger, model_name):
    """Guesses the LanguageTool language code from a Vosk model name."""
    name = model_name.lower()
    language_code = "de-DE"  # Default fallback value

    if "-de-" in name or name == 'de':
        language_code = "de-DE"
    elif "-en-" in name or name == 'en':
        language_code = "en-US"
    elif "-fr-" in name or name == 'fr':
        language_code = "fr-FR"
    # The 'else' case is handled by the default value above.

    logger.info(f"'🎤{model_name}': Returning '{language_code}'.")

    return language_code

#  Test