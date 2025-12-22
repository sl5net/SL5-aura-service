# config/maps/plugins/standard_actions/de-DE/shopping_list.py
from pathlib import Path

# Die Liste wird in einer einfachen Textdatei im selben Ordner gespeichert
LIST_FILE = Path(__file__).parent / "einkaufsliste.txt"

def execute(match_data):
    """ Verwaltet eine einfache Einkaufsliste in einer Textdatei. """
    original_text = match_data['original_text'].lower()
    text_after_replacement = match_data['text_after_replacement'].lower()
    match_obj = match_data['regex_match_obj']

    print(f"text_after_replacement")

    # Befehl: Etwas hinzufügen
    if "add to einkaufsliste" in text_after_replacement:
        item = match_obj.group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(item + "\n")
        return f"Okay, '{item}' wurde zur Einkaufsliste hinzugefügt."

    # Befehl: Liste anzeigen
    elif "zeige" in original_text:
        if not LIST_FILE.exists():
            return "Die Einkaufsliste ist noch leer."

        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.readlines()

        if not items:
            return "Die Einkaufsliste ist leer."

        response = "Hier ist deine Einkaufsliste: "
        for i, item in enumerate(items, 1):
            response += f"{i}. {item.strip()}, "
        return response.rstrip(', ') # Entfernt das letzte Komma und Leerzeichen

# Schuhe in EinkaufslisteAutos sind Einkaufsliste
