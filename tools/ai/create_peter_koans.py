# create_peter_koans.py
# Version: 0.1.0
# Erstellt koans_2_peter_deutsch – eine für Peter optimierte Koan-Sammlung.
#
# Was das Script macht:
#   1. Kopiert alle Koans aus koans_deutsch nach koans_2_peter_deutsch
#   2. Vereinfacht die Map-Dateien für Peter:
#      - Entfernt langen schwierigeNamen-Text (Ablenkung für LLM)
#      - Behält TODO-Kommentare und auskommentierte Regeln
#      - Fügt einen kurzen PETER-Hinweis hinzu was die Aufgabe ist
#      - Bei mehreren auskommentierten Regeln: erste wird Aufgabe, Rest bleibt als Hinweis
#
# Aufruf:
#   python create_peter_koans.py            → erstellt/aktualisiert koans_2_peter_deutsch
#   python create_peter_koans.py --dry-run  → zeigt was passieren würde

import re
import shutil
import argparse
from pathlib import Path

REPO_ROOT = Path.cwd()
SOURCE_DIR = REPO_ROOT / "config" / "maps" / "koans_deutsch"
TARGET_DIR = REPO_ROOT / "config" / "maps" / "koans_2_peter_deutsch"
LANGUAGE = "de-DE"

HEADER = '''import re # noqa: F401
# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.
'''


def strip_schwierige_namen(content):
    """Entfernt den langen schwierigeNamen String – zu viel Rauschen für Peter."""
    # Entfernt alles zwischen schwierigeNamen = """ und dem schließenden """
    content = re.sub(
        r'schwierigeNamen\s*=\s*""".*?"""',
        '',
        content,
        flags=re.DOTALL
    )
    return content


def extract_commented_rules(content):
    """Sammelt alle auskommentierten Regelzeilen."""
    pattern = re.compile(r"^\s*#\s*(\((['\"]).*?\2.*?\))\s*,?\s*$", re.MULTILINE)
    return pattern.findall(content)


def transform_map_file(content, fname, koan_name):
    """
    Transformiert eine Map-Datei für Peter:
    - Entfernt schwierigeNamen
    - Vereinfacht Header
    - Behält TODO + auskommentierte Regeln
    - Fügt klaren PETER-Hinweis hinzu
    """
    # Schritt 1: schwierigeNamen entfernen
    content = strip_schwierige_namen(content)

    # Schritt 2: Finde auskommentierte Regeln
    commented = extract_commented_rules(content)

    # Schritt 3: Finde den MAP-Variablennamen
    map_var = "FUZZY_MAP_pre"
    if "FUZZY_MAP_pre" not in content:
        map_var = "FUZZY_MAP"

    # Schritt 4: Baue neuen Inhalt
    peter_hint = f"# PETER-AUFGABE fuer Koan: {koan_name}\n"

    if len(commented) == 0:
        peter_hint += "# Keine auskommentierten Regeln gefunden.\n"
        peter_hint += "# -> Erstelle eine sinnvolle neue Regel fuer diesen Koan.\n"
    elif len(commented) == 1:
        peter_hint += "# Es gibt EINE auskommentierte Regel.\n"
        peter_hint += "# -> Entferne das '#' um sie zu aktivieren.\n"
        peter_hint += "# -> Was passiert danach in der Pipeline?\n"
    else:
        peter_hint += f"# Es gibt {len(commented)} auskommentierte Regeln.\n"
        peter_hint += "# -> Aktiviere die ERSTE Regel (entferne das '#').\n"
        peter_hint += "# -> Die anderen sind Alternativen zum Vergleich.\n"

    # Schritt 5: Alten Header durch neuen ersetzen
    # Entferne den langen englischen Kommentar-Block
    content = re.sub(
        r'# This map uses a hybrid approach:.*?# 2\. If no regex matches.*?\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Schritt 6: Füge Peter-Hint direkt vor der MAP-Variable ein
    content = re.sub(
        rf'({map_var}\s*=\s*\[)',
        peter_hint + r'\1',
        content,
        count=1
    )

    # Schritt 7: Sauberer Header
    content = re.sub(r'import re.*?\n', HEADER + '\n', content, count=1)

    # Mehrfache Leerzeilen reduzieren
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip() + '\n'


def create_peter_koans(dry_run=False):
    if not SOURCE_DIR.exists():
        print(f"!! Quellverzeichnis nicht gefunden: {SOURCE_DIR}")
        return

    print(f"Quelle:  {SOURCE_DIR}")
    print(f"Ziel:    {TARGET_DIR}")
    print(f"Modus:   {'DRY-RUN' if dry_run else 'SCHREIBEN'}\n")

    koan_dirs = sorted([d for d in SOURCE_DIR.iterdir()
                        if d.is_dir() and not d.name.startswith("_")])

    for koan_dir in koan_dirs:
        lang_dir = koan_dir / LANGUAGE
        if not lang_dir.exists():
            continue

        target_koan = TARGET_DIR / koan_dir.name
        target_lang = target_koan / LANGUAGE

        print(f"Koan: {koan_dir.name}")

        # __init__.py kopieren
        for init_file in [koan_dir / "__init__.py", lang_dir / "__init__.py"]:
            if init_file.exists():
                rel = init_file.relative_to(koan_dir)
                target = target_koan / rel
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(init_file, target)

        # Map-Dateien transformieren
        for fname in ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
            src = lang_dir / fname
            if not src.exists():
                continue

            original = src.read_text(encoding="utf-8")
            transformed = transform_map_file(original, fname, koan_dir.name)

            target = target_lang / fname

            # Zeige Diff-Zusammenfassung
            orig_lines = len(original.splitlines())
            new_lines = len(transformed.splitlines())
            print(f"  {fname}: {orig_lines} -> {new_lines} Zeilen", end="")

            commented = extract_commented_rules(original)
            if commented:
                print(f"  ({len(commented)} auskommentierte Regel(n) gefunden)", end="")
            print()

            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(transformed, encoding="utf-8")

        # MD-Dateien: nur schwierigeNamen.md vereinfachen, Rest kopieren
        for md_file in lang_dir.rglob("*.md"):
            rel = md_file.relative_to(koan_dir)
            target = target_koan / rel
            content = md_file.read_text(encoding="utf-8")

            # schwierigeNamen.md kuerzen auf ersten Absatz
            if "schwierigeNamen" in md_file.name:
                lines = content.splitlines()
                # Behalte nur die ersten 5 Zeilen als Kontext
                short = "\n".join(lines[:5]) + "\n...(gekuerzt fuer Peter)\n"
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(short, encoding="utf-8")
                print(f"  {md_file.name}: gekuerzt")
            else:
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(md_file, target)

        print()

    if not dry_run:
        print(f"Fertig! Peter-Koans erstellt unter:\n  {TARGET_DIR}")
    else:
        print("DRY-RUN abgeschlossen. Nichts wurde geschrieben.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Erstellt koans_2_peter_deutsch")
    parser.add_argument('--dry-run', action='store_true', help='Nur anzeigen, nichts schreiben')
    args = parser.parse_args()
    create_peter_koans(dry_run=args.dry_run)
