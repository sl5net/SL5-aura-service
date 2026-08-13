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

# good_night.py

import random
from datetime import datetime

def execute(match_data):
    """
    Gibt eine nette und zur Tageszeit passende "Gute Nacht"-Antwort.
    """
    stunde = datetime.now().hour

    # A list of general, nice wishes

    wuensche = [
        "Schlaf gut!",
        "Träum was Schönes!",
        "Ich wünsche dir eine erholsame Nacht.",
        "Bis morgen früh!",
        "Ruh dich gut aus."
    ]

    # Choose a random wish from the list

    zufalls_wunsch = random.choice(wuensche)

    # --- Reply based on time ---


    # Case 1: Late evening (8:00 p.m. - 10:59 p.m.)

    if 20 <= stunde < 23:
        antworten = [
            f"Dir auch eine gute Nacht! {zufalls_wunsch}",
            f"Gute Nacht! Zeit, den Tag ausklingen zu lassen. {zufalls_wunsch}",
            f"Okay, dann eine gute Nacht. {zufalls_wunsch}"
        ]
        return random.choice(antworten)

    # Case 2: Deep night (11:00 p.m. - 3:59 a.m.)

    elif stunde >= 23 or stunde < 4:
        antworten = [
            f"Puh, schon so spät! Dann aber eine gute Nacht. {zufalls_wunsch}",
            f"Gute Nacht! Hol dir eine ordentliche Mütze voll Schlaf. {zufalls_wunsch}",
            f"Okay, es ist wirklich Zeit fürs Bett. Gute Nacht und {zufalls_wunsch.lower()}"
        ]
        return random.choice(antworten)

    # Case 3: “Good night” at an unusual time (e.g. during the day)

    else:
        # A somewhat tongue-in-cheek, but still nice answer

        return "Oh, schon Schlafenszeit für dich? Na dann, schlaf gut, wann auch immer es so weit ist!"
