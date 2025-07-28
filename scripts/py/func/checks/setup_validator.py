# scripts/setup_validator.py
#
# This script contains functions to validate the application's environment.
import os
import sys

import ast
from pathlib import Path

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

    print("INFO: ✅ Setup validation successful.")


class DefinitionVisitor(ast.NodeVisitor):
    """An AST visitor that collects only function definitions."""
    def __init__(self):
        self.defined_functions = set()

    def visit_FunctionDef(self, node):
        # Store each defined function (excluding private/magic methods)
        if not node.name.startswith('_'):
            self.defined_functions.add(node.name)
        # Important: Also visit the function body to find nested functions.
        self.generic_visit(node)

class CallVisitor(ast.NodeVisitor):
    """
    An AST visitor that collects both direct function calls and functions
    passed as arguments.
    """
    def __init__(self):
        self.called_functions = set()

    def visit_Call(self, node):
        # Case 1: A direct function call, e.g., `my_function()` or `obj.method()`
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)

        # Case 2: A function passed as a keyword argument, e.g., `target=my_function`
        for kw in node.keywords:
            if isinstance(kw.value, ast.Name):
                self.called_functions.add(kw.value.id)

        # Case 3: A function passed as a positional argument, e.g., `map(my_function, ...)`
        for arg in node.args:
            if isinstance(arg, ast.Name):
                self.called_functions.add(arg.id)

        self.generic_visit(node)



def check_for_unused_functions(project_root):
    """
    Performs a static analysis to find unused functions.
    Uses a two-pass approach for correct results.
    """
    print("\n--- Checking for unused functions (dev-mode) ---")

    # Functions in this list are ignored.
    # Useful for callbacks from external libs or dynamically dispatched methods.
    EXTERNALLY_CALLED_FUNCTIONS = {
        # Callback from the watchdog library for file system events
        'on_created',
        # Callback from the audio library
        'audio_callback',
        # Dynamically called by the ast.NodeVisitor parent class
        'visit_FunctionDef',
        'visit_Call',
        'this_function_is_on_the_allowlist',
        'visit_Assign',
        'visit_Dict',
        'on_any_event',
        'setUp',
        'test_transcription_with_long_pause_yields_multiple_chunks',
        'test_transcription_with_short_pause_yields_one_chunk',
        'on_modified'
    }
    """
    following are only for testing, means temporarily maybe delete it later:
    on_any_event 25.7.'25 23:01 Fri
    """

    files_to_check = [project_root / 'dictation_service.py']
    files_to_check.extend(project_root.glob('scripts/**/*.py'))

    all_definitions = {}  # Stores {function_name: file_path}
    all_calls = set()
    parsed_trees = {}     # Cache for parsed trees to avoid reading files twice

    # Cache the read files and ASTs
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(file_path))
                parsed_trees[file_path] = tree
        except Exception as e:
            print(f"WARNING: Could not parse file: {file_path} ({e})")

    # PASS 1: Collect all function definitions from all files
    for file_path, tree in parsed_trees.items():
        visitor = DefinitionVisitor()
        visitor.visit(tree)
        for func_name in visitor.defined_functions:
            all_definitions[func_name] = file_path

    # PASS 2: Collect all function calls from all files
    for file_path, tree in parsed_trees.items():
        visitor = CallVisitor()
        visitor.visit(tree)
        all_calls.update(visitor.called_functions)

    # ANALYSIS: Compare the two sets
    defined_names = set(all_definitions.keys())
    unused_names = defined_names - all_calls
    truly_unused_names = unused_names - EXTERNALLY_CALLED_FUNCTIONS

    if not truly_unused_names:
        print("INFO: No unused functions found. Clean!")
    else:
        print("\nFATAL \nsetup_validator.py: The following functions are defined but never appear to be called:")
        for name in sorted(list(truly_unused_names)):
            file = all_definitions[name]
            print(f"  - Function: \n{name:<30}\n | Defined in: \n{file.relative_to(project_root)}\n")
        print("\n  -> This suggests dead code. Please remove or use these functions.")
        sys.exit(1)

    print("✅ Analysis finished successfully")

# use it in .venv
# python scripts/setup_validator.py
