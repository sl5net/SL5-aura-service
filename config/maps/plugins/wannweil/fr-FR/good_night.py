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

# config/maps/plugins/wannweil/de-DE/good_night.py

# bonne_nuit.py

import random
from datetime import datetime

def execute(match_data):
    """
    Gibt eine nette und zur Tageszeit passende "Gute Nacht"-Antwort.
    """
    stunde = datetime.now().hour

    # Une liste de vœux généraux et agréables

    wuensche = [
        "Schlaf gut!",
        "Träum was Schönes!",
        "Ich wünsche dir eine erholsame Nacht.",
        "Bis morgen früh!",
        "Ruh dich gut aus."
    ]

    # Choisissez un souhait au hasard dans la liste

    zufalls_wunsch = random.choice(wuensche)

    # --- Réponse basée sur l'heure ---


    # Cas 1 : Fin de soirée (20h00 - 22h59)

    if 20 <= stunde < 23:
        antworten = [
            f"Dir auch eine gute Nacht! {zufalls_wunsch}",
            f"Gute Nacht! Zeit, den Tag ausklingen zu lassen. {zufalls_wunsch}",
            f"Okay, dann eine gute Nacht. {zufalls_wunsch}"
        ]
        return random.choice(antworten)

    # Cas 2 : Nuit profonde (23h00 - 3h59)

    elif stunde >= 23 or stunde < 4:
        antworten = [
            f"Puh, schon so spät! Dann aber eine gute Nacht. {zufalls_wunsch}",
            f"Gute Nacht! Hol dir eine ordentliche Mütze voll Schlaf. {zufalls_wunsch}",
            f"Okay, es ist wirklich Zeit fürs Bett. Gute Nacht und {zufalls_wunsch.lower()}"
        ]
        return random.choice(antworten)

    # Cas 3 : « Bonne nuit » à un moment inhabituel (par exemple pendant la journée)

    else:
        # Une réponse un peu ironique, mais toujours agréable

        return "Oh, schon Schlafenszeit für dich? Na dann, schlaf gut, wann auch immer es so weit ist!"
