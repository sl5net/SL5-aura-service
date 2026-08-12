# file scripts/py/func/guess_lt_language_from_model.py
import re

LANG_REGION_PAIR_MAP = {
    ("en", "us"): "en-US",
    ("en", "gb"): "en-GB",
    ("pt", "br"): "pt-BR",
    ("pt", "pt"): "pt-PT",
    ("zh", "cn"): "zh-CN",
    ("zh", "tw"): "zh-TW",
}

LANG_DEFAULT_REGION_MAP = {
    "de": "de-DE",
    "en": "en-US",
    "fr": "fr-FR",
    "es": "es-ES",
    "it": "it-IT",
    "pt": "pt-PT",
    "nl": "nl-NL",
    "ru": "ru-RU",
    "pl": "pl-PL",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "hi": "hi-IN",
    "ar": "ar",
}


def guess_lt_language_from_model(logger, model_name):
    """Guesses the LanguageTool language code from a Vosk model name.

    Splits the model name into alphabetic tokens and looks for a known
    lang+region pair first (e.g. 'en'+'us' -> 'en-US'), then falls back
    to a single known language token with its default region.
    Examples: 'vosk-model-de-0.21' -> 'de-DE',
              'vosk-model-en-us-0.22' -> 'en-US'.
    """
    name = model_name.lower()
    tokens = re.findall(r"[a-z]+", name)
    language_code = "de-DE"  # Default fallback value

    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        if pair in LANG_REGION_PAIR_MAP:
            language_code = LANG_REGION_PAIR_MAP[pair]
            logger.info(f"'🎤{model_name}': Returning '{language_code}'.")
            return language_code

    for token in tokens:
        if token in LANG_DEFAULT_REGION_MAP:
            language_code = LANG_DEFAULT_REGION_MAP[token]
            break

    # The 'else' case is handled by the default value above.
    logger.info(f"'🎤{model_name}': Returning '{language_code}'.")
    return language_code

