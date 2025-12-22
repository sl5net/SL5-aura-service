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

    # Stellt sicher, dass Monats- und Wochentage auf Deutsch sind (falls du sie mal brauchst)
    try:
        locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    except locale.Error:
        # Fallback für Systeme, auf denen de_DE nicht installiert ist
        locale.setlocale(locale.LC_TIME, "")

    jetzt = datetime.now()
    stunde = jetzt.hour
    zeit_str = jetzt.strftime('%H:%M')

    antwort = ""

    # 1. Tiefe Nacht (0:00 - 4:59 Uhr)
    if 0 <= stunde < 5:
        antworten = [
            f"Puh, es ist schon {zeit_str} Uhr. Die Eulen sind noch wach!",
            f"Wir haben {zeit_str} Uhr. Eine gute Zeit für kreative Ideen oder tiefen Schlaf.",
            f"Es ist {zeit_str} Uhr. Ich hoffe, du musst nicht allzu früh raus."
        ]
        antwort = random.choice(antworten)

    # 2. Früher Morgen (5:00 - 9:59 Uhr)
    elif 5 <= stunde < 10:
        antworten = [
            f"Guten Morgen! Es ist {zeit_str} Uhr. Zeit für einen Kaffee, um in den Tag zu starten!",
            f"Wir haben {zeit_str} Uhr. Ein super Start in den Tag wünsche ich dir!",
            f"Es ist {zeit_str} Uhr. Der frühe Vogel und so, du weißt schon."
        ]
        antwort = random.choice(antworten)

    # 3. Vormittag & Mittag (10:00 - 13:59 Uhr)
    elif 10 <= stunde < 14:
        antworten = [
            f"Es ist {zeit_str} Uhr. Bald Zeit für eine Mittagspause, oder? Mahlzeit!",
            f"Wir haben {zeit_str} Uhr. Die produktivste Zeit des Tages, sagt man.",
            f"Es ist {zeit_str} Uhr. Ich hoffe, dein Vormittag war bisher erfolgreich."
        ]
        antwort = random.choice(antworten)

    # 4. Nachmittag (14:00 - 17:59 Uhr)
    elif 14 <= stunde < 18:
        antworten = [
            f"Es ist {zeit_str} Uhr. Der Endspurt für heute! Das schaffst du.",
            f"Wir haben {zeit_str} Uhr. Zeit für ein kleines Nachmittagstief? Vielleicht ein Kaffee?",
            f"Es ist {zeit_str} Uhr. Der Feierabend rückt langsam näher."
        ]
        antwort = random.choice(antworten)

    # 5. Abend (18:00 - 21:59 Uhr)
    elif 18 <= stunde < 22:
        antworten = [
            f"Es ist {zeit_str} Uhr. Zeit, die Füße hochzulegen. Ich wünsche dir einen schönen Feierabend!",
            f"Wir haben {zeit_str} Uhr. Ich hoffe, du hattest einen guten Tag und kannst den Abend jetzt genießen.",
            f"Es ist {zeit_str} Uhr. Was Leckeres zum Abendessen geplant?"
        ]
        antwort = random.choice(antworten)

    # 6. Später Abend / Nacht (22:00 - 23:59 Uhr)
    else: # stunde >= 22
        antworten = [
            f"Es ist schon {zeit_str} Uhr. Ziemlich spät! Zeit, langsam den Tag ausklingen zu lassen.",
            f"Wir haben {zeit_str} Uhr. Nicht mehr lange bis Mitternacht. Ich hoffe, dein Bett ruft schon.",
            f"Es ist {zeit_str} Uhr. Ein guter Zeitpunkt für ein Buch oder einen Film, finde ich."
        ]
        antwort = random.choice(antworten)

    return antwort

#Puh, es ist schon 02:24 Uhr. Die Eulen sind noch wach!Wir haben 02:24 Uhr. Eine gute Zeit für kreative Ideen oder tiefen Schlaf.
