import subprocess

def execute(match_data):
    # Logik für die nächste Frage hier...
    subprocess.run(["espeak", "-v", "de", "Hervorragend! Nächste Frage."])
    # Hier rufen wir später die Funktion auf, die die nächste Karte in CopyQ anzeigt
    return "Nächste Frage wird geladen..."

