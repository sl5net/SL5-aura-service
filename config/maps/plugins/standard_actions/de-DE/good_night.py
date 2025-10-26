# good_night.py
import random
from datetime import datetime

def execute(match_data):
    """
    Gibt eine nette und zur Tageszeit passende "Gute Nacht"-Antwort.
    """
    stunde = datetime.now().hour

    # Eine Liste mit allgemeinen, netten Wünschen
    wuensche = [
        "Schlaf gut!",
        "Träum was Schönes!",
        "Ich wünsche dir eine erholsame Nacht.",
        "Bis morgen früh!",
        "Ruh dich gut aus."
    ]

    # Wähle einen zufälligen Wunsch aus der Liste
    zufalls_wunsch = random.choice(wuensche)

    # --- Antworten basierend auf der Uhrzeit ---

    # Fall 1: Später Abend (20:00 - 22:59 Uhr)
    if 20 <= stunde < 23:
        antworten = [
            f"Dir auch eine gute Nacht! {zufalls_wunsch}",
            f"Gute Nacht! Zeit, den Tag ausklingen zu lassen. {zufalls_wunsch}",
            f"Okay, dann eine gute Nacht. {zufalls_wunsch}"
        ]
        return random.choice(antworten)

    # Fall 2: Tiefe Nacht (23:00 - 03:59 Uhr)
    elif stunde >= 23 or stunde < 4:
        antworten = [
            f"Puh, schon so spät! Dann aber eine gute Nacht. {zufalls_wunsch}",
            f"Gute Nacht! Hol dir eine ordentliche Mütze voll Schlaf. {zufalls_wunsch}",
            f"Okay, es ist wirklich Zeit fürs Bett. Gute Nacht und {zufalls_wunsch.lower()}"
        ]
        return random.choice(antworten)

    # Fall 3: "Gute Nacht" zu einer ungewöhnlichen Zeit (z.B. tagsüber)
    else:
        # Eine etwas augenzwinkernde, aber trotzdem nette Antwort
        return "Oh, schon Schlafenszeit für dich? Na dann, schlaf gut, wann auch immer es so weit ist!"
