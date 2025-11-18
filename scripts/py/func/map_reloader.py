# scripts/py/func/map_reloader.py
import importlib
import sys
from pathlib import Path
import os

from config.dynamic_settings import settings

LAST_MODIFIED_TIMES = {}  # noqa: F824

def auto_reload_modified_maps(logger):
    # scripts/py/func/map_reloader.py:12
    global LAST_MODIFIED_TIMES # noqa: F824

    """
    Scans the map directories, detects changed files based on their
    modification time, and reloads only the necessary modules.
    """

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"def start", logger)

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
                    if settings.DEV_MODE:
                        logger.info(f"🔄 Detected change in '{map_file_path}'. Reloading...")

                relative_path = map_file_path.relative_to(project_root)
                # module_path = str(relative_path.with_suffix('')).replace(os.path.sep, '.')
                module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                log_all_map_reloaded = settings.DEV_MODE and False






                if module_name in sys.modules:
                    if last_mtime != 0:
                        if settings.DEV_MODE:
                            logger.info(f"🔄 Detected change in '{map_file_path.name}'. Reloading module...")

                    try:
                        # --- START OF MEMORY LEAK FIX ---
                        # CRITICAL STEP 1: Get the old module reference
                        # gi told_module = sys.modules[module_name]

                        # CRITICAL STEP 2: Explicitly remove the old module from sys.modules
                        # This breaks the global reference, allowing the GC to potentially clean it up.
                        del sys.modules[module_name]

                        # CRITICAL STEP 3: Manually force garbage collection BEFORE re-import
                        # This is a defensive step to clean up temporary objects from the old module.

                        # the gc.collect() for now) is technically the most aggressive and complete memory fix.
                        import gc
                        gc.collect()
                        # --- END OF MEMORY LEAK FIX ---

                        # Get the module object directly from sys.modules
                        # module_to_reload = sys.modules[module_name]
                        module_to_reload = importlib.import_module(module_name)  # 4. Correct Fresh Import
                        importlib.reload(module_to_reload)

                        LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                        if log_all_map_reloaded:
                            logger.info(f"✅ Successfully reloaded '{module_name}'.")

                        # CRITICAL STEP 4: Import the module fresh (instead of using importlib.reload)
                        # Re-importing from scratch is cleaner than reload for memory management.
                        module_to_reload = importlib.import_module(module_name)

                        # Note: If your system uses a central registry/list of map functions,
                        # you MUST clear the old functions from that registry NOW,
                        # then re-add the new functions from module_to_reload.

                        LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                        if log_all_map_reloaded:
                            logger.info(f"✅ Successfully reloaded '{module_name}'.")
                    except Exception as e:
                        logger.error(f"❌ Failed to reload module '{module_name}': {e}")








            else:
                # If no change detected, just ensure its mtime is recorded if it's a new entry
                if map_file_key not in LAST_MODIFIED_TIMES:
                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime

    except Exception as e:
        logger.error(f"Error during map reload check: {e}")

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"def end", logger)
