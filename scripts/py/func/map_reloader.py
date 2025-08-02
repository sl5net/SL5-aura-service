import importlib
from pathlib import Path
import os

# Ein "Gedächtnis" für die letzte Änderungszeit jeder Datei.
# Dies ist ein globales Dictionary, das so lange lebt wie der Server.
LAST_MODIFIED_TIMES = {}  # noqa: F824

def auto_reload_modified_maps(logger):
    """
    Scans the map directories, detects changed files based on their
    modification time, and reloads only the necessary modules.
    """
    global LAST_MODIFIED_TIMES # noqa: F824

    try:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        maps_base_dir = project_root / "config" / "languagetool_server" / "maps"

        # Finde alle .py-Dateien in den Kartenverzeichnissen
        for map_file_path in maps_base_dir.glob("**/*.py"):
            if map_file_path.name == "__init__.py":
                continue # __init__.py-Dateien ignorieren

            map_file_key = str(map_file_path)
            current_mtime = os.path.getmtime(map_file_key)
            last_mtime = LAST_MODIFIED_TIMES.get(map_file_key, 0)

            # Prüfe, ob die Datei neuer ist als unser letzter bekannter Stand
            if current_mtime > last_mtime:
                logger.info(f"🔄 Detected change in '{map_file_path.name}'. Reloading module...")

                # Konvertiere den Dateipfad in einen Python-Modulpfad
                # z.B. /path/to/config/maps/de_DE/FUZZY_MAP.py -> config.maps.de_DE.FUZZY_MAP
                relative_path = map_file_path.relative_to(project_root)
                module_path = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                try:
                    module_to_reload = importlib.import_module(module_path)
                    importlib.reload(module_to_reload)

                    # Aktualisiere die letzte bekannte Änderungszeit
                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    logger.info(f"✅ Successfully reloaded '{module_path}'.")
                except Exception as e:
                    logger.error(f"❌ Failed to reload module '{module_path}': {e}")

    except Exception as e:
        logger.error(f"Error during map reload check: {e}")
