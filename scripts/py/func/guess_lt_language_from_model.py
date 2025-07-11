def guess_lt_language_from_model(model_name):
    name = model_name.lower()
    if "-de-" in name: return "de-DE"
    elif "-en-" in name: return "en-US"
    elif "-fr-" in name: return "fr-FR"
    return "de-DE"
