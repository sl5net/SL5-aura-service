# config/maps/plugins/standard_actions/de-DE/greeting_generator.py
# greeting_generator.py
from datetime import datetime
import random
import locale

# LLLLLLLLLLLLLLLL
# LLLLLLLLLLLLLLLL

def execute(match_data):
    """
    Erzeugt eine passende, formelle Anrede basierend auf der aktuellen
    Tageszeit und dem Wochentag.
    """
    try:
        # Stellt sicher, dass Wochentage auf Deutsch sind (für eventuelle Erweiterungen)
        locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "")

    jetzt = datetime.now()
    stunde = jetzt.hour
    # .weekday() gibt 0 für Montag und 6 for Sonntag zurück
    wochentag_index = jetzt.weekday()

    # --- Spezielle Logik für besondere Tage (Montag & Freitag) ---

    # Fall 1: Freitagnachmittag (ab 12 Uhr)
    if wochentag_index == 4 and stunde >= 12:
        antworten = [
            "ich wünsche Ihnen einen schönen Start ins Wochenende.",
            "einen angenehmen Start ins wohlverdiente Wochenende wünsche ich.",
            "ich hoffe, Sie haben einen guten Übergang ins Wochenende."
        ]
        return random.choice(antworten)

    # Fall 2: Montagmorgen (vor 12 Uhr)
    elif wochentag_index == 0 and stunde < 12:
        antworten = [
            "ich wünsche Ihnen einen guten Start in die neue Woche.",
            "einen erfolgreichen Start in die Woche wünsche ich Ihnen.",
            "ich hoffe, Sie hatten ein erholsames Wochenende und starten gut in die Woche."
        ]
        return random.choice(antworten)

    # --- Standard-Logik für alle anderen Tage und Zeiten ---

    # Morgens (bis 11:59 Uhr)
    if stunde < 12:
        return "Guten Morgen,"

    # Mittags & Nachmittags (12:00 - 17:59 Uhr)
    elif stunde < 18:
        return "Guten Tag,"

    # Abends (ab 18:00 Uhr)
    else:
        return "Guten Abend,"

