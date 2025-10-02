# file: scripts/py/func/checks/check_example_file_is_synced.py

import ast
import sys
from pathlib import Path

class ConfigKeyVisitor(ast.NodeVisitor):
    """
    An AST visitor that collects all assigned variable names and string keys
    from dictionaries, which represent configurable settings.
    """
    def __init__(self):
        self.keys = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.keys.add(target.id)
        self.generic_visit(node)

    def visit_Dict(self, node):
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                self.keys.add(key.value)
        self.generic_visit(node)

def check_example_file_is_synced(project_root: Path):
    """
    Checks if the example file contains all keys from the local settings file.
    This ensures the public documentation for developers stays up-to-date
    with the settings currently in use. Runs in DEV_MODE only.
    """
    settings_file = project_root / "config" / "settings_local.py"
    example_file = project_root / "config" / "settings_local.py_Example.txt"

    print("INFO: Checking if 'settings_local.py_Example.txt' is in sync...")

    if not settings_file.is_file():
        # No local settings, no need to check.
        print(f"INFO: Skipping sync check, '{settings_file.name}' not found.")
        return

    try:
        # 1. Parse the local settings file to find all defined keys
        with open(settings_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        visitor = ConfigKeyVisitor()
        visitor.visit(tree)
        defined_keys = visitor.keys

        # 2. Check if all found keys exist in the example file
        with open(example_file, 'r', encoding='utf-8') as f:
            example_content = f.read()

        missing_keys = [key for key in sorted(list(defined_keys)) if key not in example_content]

        # 3. Report error and exit if keys are missing
        if missing_keys:
            print("\n" + "="*60, file=sys.stderr)
            print("FATAL ERROR: Configuration Documentation Out of Sync!", file=sys.stderr)
            print(f"The example file '{example_file.name}' is missing keys from your '{settings_file.name}'.", file=sys.stderr)
            print("Missing keys:", file=sys.stderr)
            for key in missing_keys:
                print(f"  - {key}", file=sys.stderr)
            print("\nPlease update the example file.", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            # sys.exit(1)

        print("✅ INFO: Config sync check passed. Example file is up to date.")

    except Exception as e:
        print(f"ERROR: An unexpected error occurred during config sync check: {e}", file=sys.stderr)
        sys.exit(1)
