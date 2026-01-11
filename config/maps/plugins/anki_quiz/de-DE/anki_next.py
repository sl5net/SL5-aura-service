import subprocess

# UNICODE_NUMS = {1: "⓵", 2: "⓶", 3: "⓷"}
UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}


def execute(match_data):
    # Logik für die nächste Frage hier...
    subprocess.run(["espeak", "-v", "de", "Hervorragend! Nächste Frage."])
    # Hier rufen wir später die Funktion auf, die die nächste Karte in CopyQ anzeigt
    return "Nächste Frage wird geladen..."

