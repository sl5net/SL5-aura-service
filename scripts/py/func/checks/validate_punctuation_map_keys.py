# file: scripts/py/func/checks/setup_validator.py

import os
import sys
import importlib
import ast

def validate_punctuation_map_keys(project_root):
    """
    Scans all language maps and warns if any PUNCTUATION_MAP contains non-lowercase keys.
    This check only runs in DEV_MODE to help developers avoid common errors.
    """
    print("DEV_MODE: Running punctuation map key validation...")
    maps_path = os.path.join(project_root, 'config', 'languagetool_server', 'maps')
    if not os.path.isdir(maps_path):
        print(f"  -> Info: Maps directory not found at '{maps_path}', skipping check.")
        return

    # Add project root to path for dynamic imports
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    found_issues = False
    for lang_code in os.listdir(maps_path):
        if os.path.isdir(os.path.join(maps_path, lang_code)):
            try:
                module_path = f"config.languagetool_server.maps.{lang_code}.PUNCTUATION_MAP"
                punc_module = importlib.import_module(module_path)
                punctuation_map = getattr(punc_module, 'PUNCTUATION_MAP', {})

                uppercase_keys = [key for key in punctuation_map if key != key.lower()]

                if uppercase_keys:
                    found_issues = True
                    print("\n--- ----------------------------------------- ---")
                    print(f"⚠️ WARNING: Found non-lowercase keys in '{module_path}.py'")
                    print("   All keys in PUNCTUATION_MAP must be lowercase for reliable matching.")
                    print("   Please fix the following keys:")
                    for key in uppercase_keys:
                        print(f"     - '{key}'")
                    print("--- ----------------------------------------- ---\n")

            except (ModuleNotFoundError, AttributeError):
                # This is fine, a language might not have a punctuation map.
                continue

    if not found_issues:
        print("✅ OK: All found punctuation map keys are lowercase.")

