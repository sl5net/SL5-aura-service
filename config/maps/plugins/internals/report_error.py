



from datetime import datetime
from pathlib import Path
import re


def between_first_last_hash_manual(s: str) -> str:
    try:
        start = s.index('#') + 1
        end = s.rindex('#')
    except ValueError:
        return ''
    return s[start:end].strip()



def execute(match_data):
    # Pfad-Logik: Von .../internals/report_error.py zum Root
    root = Path(__file__).resolve().parents[4]
    log_file = root / "log" / "aura_engine.log"
    report_file = root / "docs" / "bugfix" / "TODO" / "misrecognitions.md"

    # Begriffe, die wir ignorieren (da sie den Befehl selbst beschreiben)
    triggers = ["fehler melden", "logge fehler", "das war falsch", "fehlermeldung", "fehler mail"]

    try:
        if not log_file.exists():
            return "Log-Datei nicht gefunden."

        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 1. Wir filtern nur Zeilen mit deinem Fehler-Präfix
        # 2. Wir drehen die Liste um (reversed), um am Ende der Datei zu starten
        error_line = None
        for line in reversed(lines):
            line_clean = line.strip()

            # Suche nach deinem speziellen Log-Präfix
            if "📢📢📢 #" in line_clean:
                # Prüfen: Ist das nur der Befehl selbst?
                is_trigger = any(t.lower() in line_clean.lower() for t in triggers)

                if not is_trigger:
                    error_line = line_clean
                    break

        if not error_line:
            return "Keine passende Fehl-Erkennung im Log gefunden."

        # Zeitstempel für die Markdown-Tabelle
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sicherstellen, dass der Zielordner existiert
        report_file.parent.mkdir(parents=True, exist_ok=True)

        error_line = re.sub(r"(.)\1+", r"\1", error_line)

        error_line = between_first_last_hash_manual(error_line)

        # In die TODO-Liste schreiben
        with open(report_file, "a", encoding="utf-8") as f:
            f.write(f"📢 {timestamp}:\n{error_line}\n")

        return f" internals "

    except Exception as e:
        return f"Fehler im Reporting-Script: {str(e)}"