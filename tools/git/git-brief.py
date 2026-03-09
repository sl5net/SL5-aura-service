import subprocess
import sys


"""


 Die "Quick & Dirty" Lösung (Git-Befehl)

Dieser Befehl ist oft schon ausreichend. Er zeigt die Statistik (welche Dateien) und dann den Diff ohne den Ballast von unveränderten Zeilen:
code Bash

git diff --stat && git diff -U0 --no-color

    --stat: Zeigt erst mal die Übersicht (Dateinamen + Anzahl Änderungen).

    -U0: Entfernt alle Kontextzeilen (du siehst nur die Zeilen mit + und -).




 "LLM-Diff" (Python-Skript)

Wenn du es wirklich elegant willst, nutzt du dieses Python-Skript. Es gruppiert die Änderungen nach Dateien und zeigt nur an, was hinzugefügt (+) oder entfernt (-) wurde, wobei es lange Blöcke kürzt.
"""

def get_brief_diff():
    # Holt den Diff ohne Kontextzeilen
    cmd = ["git", "diff", "-U0"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    lines = result.stdout.splitlines()
    current_file = ""

    for line in lines:
        if line.startswith('+++ b/'):
            current_file = line[6:]
            print(f"\nFILE: {current_file}")
        elif line.startswith('@@'):
            # Extrahiert den Funktionsnamen falls vorhanden
            parts = line.split('@@', 2)
            if len(parts) > 2 and parts[2].strip():
                print(f"  In {parts[2].strip()}:")
        elif line.startswith('+') and not line.startswith('+++'):
            # Zeigt hinzugefügte Zeilen (eingerückt)
            content = line[1:].strip()
            if content: print(f"    + {content}")
        elif line.startswith('-') and not line.startswith('---'):
            # Zeigt gelöschte Zeilen (eingerückt)
            content = line[1:].strip()
            if content: print(f"    - {content}")

if __name__ == "__main__":
    get_brief_diff()

