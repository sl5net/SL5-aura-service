
#!/usr/bin/env python3
from pathlib import Path
import shutil
import argparse
import sys



readme = """
Erklärung / Hinweise

    Suche: Path.rglob(name) findet rekursiv alle Pfade mit genau diesem Namen. Wir filtern mit p.is_dir() und has_hidden_component() um versteckte Pfade auszuschließen.
    Löschen: shutil.rmtree() entfernt rekursiv ein Verzeichnis. Für symbolische Links prüfen wir is_symlink() und verwenden unlink() statt rmtree, damit der Link selbst entfernt wird, nicht das Ziel.
    Sicherheit: Standardmäßig fragt das Skript vor dem Löschen nach Bestätigung. Verwende --dry-run, um zuerst nur die Liste der Kandidaten zu sehen.
    Fehlerbehandlung: Ausnahmen beim Löschen werden gefangen und auf stderr ausgegeben, so dass ein fehlerhafter Pfad den Rest nicht abbricht.

"""



lunuxcmds = """





Empfohlenes, sicheres Vorgehen (macOS / Linux)

    Trockenlauf — nur anzeigen, welche Ordner gelöscht würden (unbedingt zuerst ausführen):

find config/maps/plugins -type d -name 'self_test_zip_tmp' -print | grep -v '/\.'

find config/maps/plugins -type d -name 'self_test_zip_tmp' -print0 | while IFS= read -r -d '' d; do
  case "$d" in
    */.*) continue ;;   # skip any path containing a hidden component
  esac
  rm -rf -- "$d"
done


"""


ROOT = Path("config/maps/plugins")
TARGET_NAME = "self_test_zip_tmp"

def has_hidden_component(p: Path) -> bool:
    # Prüft, ob irgendein Teil des Pfades mit '.' beginnt
    return any(part.startswith('.') for part in p.parts)

def find_targets(root: Path, name: str):
    """Yield directories named `name` under `root`, skipping paths that contain hidden components."""
    if not root.exists():
        return
    # Verwende rglob für rekursives Finden nur von Ordnernamen
    for p in root.rglob(name):
        if p.is_dir() and not has_hidden_component(p):
            yield p

def remove_dir(path: Path, dry_run: bool):
    """Remove directory tree, special-case symlinks."""
    if dry_run:
        print("[DRY-RUN] Would remove:", path)
        return
    try:
        # Wenn es ein symbolischer Link ist, unlink statt rmtree
        if path.is_symlink():
            print("Removing symlink:", path)
            path.unlink()
        else:
            print("Removing directory tree:", path)
            shutil.rmtree(path)
    except Exception as exc:
        print(f"Error removing {path}: {exc}", file=sys.stderr)

def main(dry_run: bool):
    targets = list(find_targets(ROOT, TARGET_NAME))
    if not targets:
        print("No matching directories found.")
        return

    print(f"Found {len(targets)} directories to remove:")
    for t in targets:
        print(" -", t)

    if dry_run:
        print("\nDry run complete. No directories were deleted.")
        return

    # Bestätigungsabfrage
    ans = input("\nProceed to delete these directories? [y/N]: ").strip().lower()
    if ans != "y":
        print("Aborted by user.")
        return

    for t in targets:
        remove_dir(t, dry_run=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove all 'self_test_zip_tmp' dirs under config/maps/plugins")
    parser.add_argument("--dry-run", action="store_true", help="Only list directories that would be removed")
    args = parser.parse_args()
    main(dry_run=args.dry_run)
