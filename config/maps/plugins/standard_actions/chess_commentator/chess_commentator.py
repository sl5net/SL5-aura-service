# config/maps/plugins/standard_actions/de-DE/chess_commentator.py
# FILE: chess_commentator.py

import random

# --- Knowledge Base of Responses ---
# A list of general, encouraging phrases in German.
# We can keep them all in one list since the desired reaction is always supportive.
SUPPORTIVE_RESPONSES = [
    "Kopf hoch. Fehler passieren auch den Weltmeistern.",
    "Okay, abhaken und auf den nächsten Zug konzentrieren.",
    "Das ist ärgerlich, aber das Spiel ist noch nicht vorbei.",
    "Passiert. Wichtig ist, wie du jetzt weiterspielst.",
    "Atme tief durch. Ein klarer Kopf ist jetzt deine stärkste Waffe.",
    "Bleib fokussiert! Eine einzige Chance kann das ganze Spiel drehen.",
    "Jeder macht Fehler. Bleib ruhig und suche nach deinem besten Zug.",
    "Gib nicht auf! Kämpfe weiter, die Partie ist noch lang.",
    "Lass dich davon nicht aus der Ruhe bringen. Weiter geht's.",
    "Zeig Kampfgeist! Jede Partie ist eine Lektion."
]

def execute(match_data):
    """
    Provides a random, supportive comment for a chess player who has made
    a negative remark.

    This function is triggered when a regex for negative self-talk matches.
    It does not need to inspect the match_data in detail, as its sole purpose
    is to provide encouragement.

    Args:
        match_data (dict): A dictionary from the main service, containing the
                           regex match object. It is not used in this function
                           but required by the system's architecture.

    Returns:
        str: A randomly selected supportive phrase in German.
    """
    try:
        # We simply select a random response from our list.
        # This is more effective than having a fixed response.
        return random.choice(SUPPORTIVE_RESPONSES)
    except IndexError:
        # This would only happen if the SUPPORTIVE_RESPONSES list were empty.
        return "Bleib dran."
    except Exception as e:
        # A general catch-all for any other unexpected errors.
        print(f"[ERROR] An unexpected error occurred in chess_commentator.py: {e}")
        return "Konzentrier dich einfach weiter."

