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

# config/maps/plugins/wannweil/de-DE/get_current_time.py

from datetime import datetime
import locale
import random

def execute(current_text):
    """
    Gibt eine persönliche Antwort basierend auf der aktuellen Uhrzeit zurück.
    Der Parameter 'current_text' wird hier nicht verwendet, ist aber Teil der
    konsistenten Schnittstelle für alle Skripte.
    """

    # S'assure que les jours du mois et de la semaine sont en allemand (au cas où vous en auriez besoin)

    try:
        locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    except locale.Error:
        # Solution de secours pour les systèmes sur lesquels de_DE n'est pas installé

        locale.setlocale(locale.LC_TIME, "")

    jetzt = datetime.now()
    stunde = jetzt.hour
    zeit_str = jetzt.strftime('%H:%M')

    antwort = ""

    # 1. Nuit profonde (00h00 - 4h59)

    if 0 <= stunde < 5:
        antworten = [
            f"Puh, es ist schon {zeit_str} Uhr. Die Eulen sind noch wach!",
            f"Wir haben {zeit_str} Uhr. Eine gute Zeit für kreative Ideen oder tiefen Schlaf.",
            f"Es ist {zeit_str} Uhr. Ich hoffe, du musst nicht allzu früh raus."
        ]
        antwort = random.choice(antworten)

    # 2. Tôt le matin (5h00 - 9h59)

    elif 5 <= stunde < 10:
        antworten = [
            f"Guten Morgen! Es ist {zeit_str} Uhr. Zeit für einen Kaffee, um in den Tag zu starten!",
            f"Wir haben {zeit_str} Uhr. Ein super Start in den Tag wünsche ich dir!",
            f"Es ist {zeit_str} Uhr. Der frühe Vogel und so, du weißt schon."
        ]
        antwort = random.choice(antworten)

    # 3. Matin et déjeuner (10h00 - 13h59)

    elif 10 <= stunde < 14:
        antworten = [
            f"Es ist {zeit_str} Uhr. Bald Zeit für eine Mittagspause, oder? Mahlzeit!",
            f"Wir haben {zeit_str} Uhr. Die produktivste Zeit des Tages, sagt man.",
            f"Es ist {zeit_str} Uhr. Ich hoffe, dein Vormittag war bisher erfolgreich."
        ]
        antwort = random.choice(antworten)

    # 4ème après-midi (14h00 - 17h59)

    elif 14 <= stunde < 18:
        antworten = [
            f"Es ist {zeit_str} Uhr. Der Endspurt für heute! Das schaffst du.",
            f"Wir haben {zeit_str} Uhr. Zeit für ein kleines Nachmittagstief? Vielleicht ein Kaffee?",
            f"Es ist {zeit_str} Uhr. Der Feierabend rückt langsam näher."
        ]
        antwort = random.choice(antworten)

    # 5ème soirée (18h00 - 21h59)

    elif 18 <= stunde < 22:
        antworten = [
            f"Es ist {zeit_str} Uhr. Zeit, die Füße hochzulegen. Ich wünsche dir einen schönen Feierabend!",
            f"Wir haben {zeit_str} Uhr. Ich hoffe, du hattest einen guten Tag und kannst den Abend jetzt genießen.",
            f"Es ist {zeit_str} Uhr. Was Leckeres zum Abendessen geplant?"
        ]
        antwort = random.choice(antworten)

    # 6. Fin de soirée/nuit (22h00 - 23h59)

    else: # stunde >= 22
        antworten = [
            f"Es ist schon {zeit_str} Uhr. Ziemlich spät! Zeit, langsam den Tag ausklingen zu lassen.",
            f"Wir haben {zeit_str} Uhr. Nicht mehr lange bis Mitternacht. Ich hoffe, dein Bett ruft schon.",
            f"Es ist {zeit_str} Uhr. Ein guter Zeitpunkt für ein Buch oder einen Film, finde ich."
        ]
        antwort = random.choice(antworten)

    return antwort

# Ouf, il est déjà 2h24 du matin. Les chouettes sont encore éveillées ! Il est 2h24 du matin. Un bon moment pour des idées créatives ou un sommeil profond.

