# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/wannweil/de-DE/shopping_list.py

from pathlib import Path

# La lista se guarda en un archivo de texto simple en la misma carpeta.

LIST_FILE = Path(__file__).parent / "einkaufsliste.txt"

def execute(match_data):
    """ Verwaltet eine einfache Einkaufsliste in einer Textdatei. """
    original_text = match_data['original_text'].lower()
    text_after_replacement = match_data['text_after_replacement'].lower()
    match_obj = match_data['regex_match_obj']

    print("text_after_replacement")

    # Comando: agregar algo

    if "add to einkaufsliste" in text_after_replacement:
        item = match_obj.group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(item + "\n")
        return f"Okay, '{item}' wurde zur Einkaufsliste hinzugefügt."

    # Comando: Mostrar lista

    elif "zeige" in original_text:
        if not LIST_FILE.exists():
            return "Die Einkaufsliste ist noch leer."

        with open(LIST_FILE, "r", codificación="utf-8") as f:
            items = f.readlines()

        if not items:
            return "Die Einkaufsliste ist leer."

        response = "Hier ist deine Einkaufsliste: "
        for i, item in enumerate(items, 1):
            response += f"{i}. {item.strip()}, "
        return response.rstrip(', ') # Entfernt das letzte Komma und Leerzeichen

# Zapatos en la lista de compras Los autos están en la lista de compras

