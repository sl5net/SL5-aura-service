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

# config/maps/plugins/wannweil/de-DE/buenas_noches.py

# buenas_noches.py

import random
from datetime import datetime


def execute(match_data):
    """
    Gibt eine nette und zur Tageszeit passende "Gute Nacht"-Antwort.
    """
    stunde = datetime.now().hour

    # Una lista de buenos deseos generales.

    wuensche = [
        "Schlaf gut!",
        "Träum was Schönes!",
        "Ich wünsche dir eine erholsame Nacht.",
        "Bis morgen früh!",
        "Ruh dich gut aus."
    ]

    # Elija un deseo aleatorio de la lista

    zufalls_wunsch = random.choice(wuensche)

    # --- Respuesta basada en el tiempo ---


    # Caso 1: A última hora de la tarde (20:00 - 22:59)

    if 20 <= stunde < 23:
        antworten = [
            f"Dir auch eine gute Nacht! {zufalls_wunsch}",
            f"Gute Nacht! Zeit, den Tag ausklingen zu lassen. {zufalls_wunsch}",
            f"Okay, dann eine gute Nacht. {zufalls_wunsch}"
        ]
        return random.choice(antworten)

    # Caso 2: Noche profunda (23:00 – 3:59)

    elif stunde >= 23 or stunde < 4:
        antworten = [
            f"Puh, schon so spät! Dann aber eine gute Nacht. {zufalls_wunsch}",
            f"Gute Nacht! Hol dir eine ordentliche Mütze voll Schlaf. {zufalls_wunsch}",
            f"Okay, es ist wirklich Zeit fürs Bett. Gute Nacht und {zufalls_wunsch.lower()}"
        ]
        return random.choice(antworten)

    # Caso 3: “Buenas noches” en un momento inusual (por ejemplo, durante el día)

    else:
        # Una respuesta algo irónica, pero aún así agradable.

        return "Oh, schon Schlafenszeit für dich? Na dann, schlaf gut, wann auch immer es so weit ist!"
