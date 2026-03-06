import os
import re
import glob

# --- KONFIGURATION ---
DRY_RUN = True  # Auf False setzen, um Änderungen wirklich zu speichern!
# DRY_RUN = False  # Auf False setzen, um Änderungen wirklich zu speichern!
# ---------------------

def repair_i18n_links():
    # Suche alle .md Dateien in Unterordnern, die auf .i18n enden
    files = glob.glob("**/*.i18n/*.md", recursive=True)

    # Regex für [text](url) oder ![alt](url)
    link_pattern = re.compile(r'(\[!?.*?\])\((.*?)\)')

    mode_suffix = " (DEMO-MODUS - Keine Datei wird verändert)" if DRY_RUN else " (LIVE-MODUS - Dateien werden überschrieben!)"
    print(f"Starte Link-Reparatur{mode_suffix}")
    print(f"Gefundene Dateien: {len(files)}\n")

    total_fixes = 0

    for file_path in files:
        current_dir = os.path.dirname(file_path)
        file_fixes = 0
        new_lines = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Fehler beim Lesen von {file_path}: {e}")
            continue

        for line_num, line in enumerate(lines, 1):
            def replace_logic(match):
                nonlocal file_fixes
                prefix = match.group(1)
                url = match.group(2)

                # 1. Ignoriere alles, was nicht relativ ist oder schon korrigiert wurde
                if url.startswith(('http', '#', 'mailto:', '/')):
                    return match.group(0)

                # 2. Pfad für Prüfung vorbereiten (Anker entfernen)
                path_only = url.split('#')[0] if '#' in url else url
                if not path_only: # Falls es nur ein Anker war (bereits oben abgefangen, aber sicher ist sicher)
                    return match.group(0)

                # 3. Existenzprüfung im Elternverzeichnis
                # Wir bauen den Pfad zusammen: Unterordner/../Zieldatei
                potential_path = os.path.normpath(os.path.join(current_dir, "..", path_only))

                if os.path.exists(potential_path):
                    file_fixes += 1
                    new_url = f"../{url}"
                    print(f"  [FIX] In {file_path} (Zeile {line_num}):")
                    print(f"        {url}  -->  {new_url}")
                    return f"{prefix}({new_url})"
                else:
                    # Datei existiert oben nicht -> keine Änderung
                    return match.group(0)

            new_line = link_pattern.sub(replace_logic, line)
            new_lines.append(new_line)

        if file_fixes > 0:
            total_fixes += file_fixes
            if not DRY_RUN:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"  -> ✅ {file_fixes} Änderungen gespeichert.\n")
            else:
                print(f"  -> ℹ️ {file_fixes} Änderungen gefunden (nicht gespeichert).\n")

    print("--- ZUSAMMENFASSUNG ---")
    if DRY_RUN:
        print(f"Insgesamt {total_fixes} potenzielle Korrekturen in {len(files)} Dateien gefunden.")
        print("Um diese Änderungen anzuwenden, setze DRY_RUN = False im Skript.")
    else:
        print(f"Insgesamt {total_fixes} Korrekturen durchgeführt.")

if __name__ == "__main__":
    repair_i18n_links()
