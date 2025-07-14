# scripts/setup_validator.py
#
# This script contains functions to validate the application's environment.
import os
import sys

import ast
from pathlib import Path

# Ein Helfer, um den AST (Abstrakten Syntaxbaum) eines Skripts zu durchlaufen


def validate_setup(project_root):
    """
    Verifies that essential setup steps have been completed.
    If a check fails, it prints an error and exits the program.

    Args:
        project_root (str): The absolute path to the project's root directory.
    """
    print("INFO: Running setup validation...")

    # --- Check 1: Existence of the 'log' directory ---
    log_dir = os.path.join(project_root, 'log')
    if not os.path.isdir(log_dir):
        # This error is printed to stderr, which is standard for errors.
        print(
            "\nFATAL: Setup validation failed. The 'log' directory is missing.",
            file=sys.stderr
        )
        print(
            "       Please run the appropriate script from the 'setup/' directory.",
            file=sys.stderr
        )
        sys.exit(1) # Exit with an error code

    # --- Add future checks here ---
    # Example: Check for a specific config file
    # config_file = os.path.join(project_root, 'config', 'model_name.txt')
    # if not os.path.isfile(config_file):
    #     print("FATAL: Config file 'model_name.txt' is missing.", file=sys.stderr)
    #     sys.exit(1)

    print("INFO: Setup validation successful.")


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined_functions = set()
        self.called_functions = set()

    def visit_FunctionDef(self, node):
        # Speichere jede definierte Funktion (außer private/magic-Methoden)
        if not node.name.startswith('_'):
            self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Speichere jeden Funktionsaufruf
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)
        self.generic_visit(node)

def check_for_unused_functions(project_root):
    print("\n--- check_for_unused_functions ---")

    files_to_check = [project_root / 'dictation_service.py']
    files_to_check.extend(project_root.glob('scripts/**/*.py'))

    all_definitions = {} # Speichert {funktionsname: dateipfad}
    all_calls = set()

    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=file_path)
                visitor = FunctionVisitor()
                visitor.visit(tree)

                for func_name in visitor.defined_functions:
                    all_definitions[func_name] = file_path
                all_calls.update(visitor.called_functions)
        except Exception as e:
            print(f"WARNUNG: not analysieren: {file_path} ({e})")

    # Finde die Differenz: Funktionen, die definiert, aber nie aufgerufen wurden
    defined_names = set(all_definitions.keys())
    unused_names = defined_names - all_calls

    if not unused_names:
        print("INFO: no problem found :)")
    else:
        print("WARNUNG: folw func not used ?")
        for name in sorted(list(unused_names)):
            file = all_definitions[name]
            print(f"  - func: {name:<30} | def in: {file.relative_to(project_root)}")
        sys.exit(1)

    print("--- Analyse finised ---")


# use it in .venv
# python scripts/setup_validator.py
