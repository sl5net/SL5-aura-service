import importlib
from pathlib import Path
import os

LAST_MODIFIED_TIMES = {}  # noqa: F824

def auto_reload_modified_maps(logger):
    global LAST_MODIFIED_TIMES # noqa: F824

    """
    Scans the map directories, detects changed files based on their
    modification time, and reloads only the necessary modules.
    """

    try:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        maps_base_dir = project_root / "config" / "maps"

        for map_file_path in maps_base_dir.glob("**/*.py"):
            if map_file_path.name == "__init__.py":
                continue # __init__.py-Dateien ignorieren

            map_file_key = str(map_file_path)

            current_mtime = os.path.getmtime(map_file_key)
            last_mtime = LAST_MODIFIED_TIMES.get(map_file_key, 0)

            if current_mtime > last_mtime:
                if last_mtime != 0:
                    logger.info(f"🔄 Detected change in '{map_file_path.name}'. Reloading module...")

                relative_path = map_file_path.relative_to(project_root)
                module_path = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                try:
                    module_to_reload = importlib.import_module(module_path)
                    importlib.reload(module_to_reload)

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    logger.info(f"✅ Successfully reloaded '{module_path}'.")
                except Exception as e:
                    logger.error(f"❌ Failed to reload module '{module_path}': {e}")

    except Exception as e:
        logger.error(f"Error during map reload check: {e}")
