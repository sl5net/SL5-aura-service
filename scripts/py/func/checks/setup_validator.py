# scripts/py/func/checks/setup_validator.py
#
# This script contains functions to validate the application's environment
# and perform static code analysis for quality checks.

import os
import sys
import ast
from pathlib import Path
from collections import Counter # <-- FIX: Import Counter

# ==============================================================================
# 1. CORE VALIDATION
# ==============================================================================

def validate_setup(project_root, logger):
    """Verifies that essential directories exist."""
    logger.info("INFO: Running setup validation...")
    log_dir = os.path.join(project_root, 'log')
    if not os.path.isdir(log_dir):
        logger.info("\nFATAL: Setup validation failed. The 'log' directory is missing.", file=sys.stderr)
        logger.info("       Please run the appropriate setup script.", file=sys.stderr)
        sys.exit(1)
    logger.info("INFO: [OK] Setup validation successful.")

# ==============================================================================
# 2. STATIC ANALYSIS HELPERS (AST Visitors)
# ==============================================================================

class DefinitionVisitor(ast.NodeVisitor):
    """Collects all function definitions."""
    def __init__(self):
        self.defined_functions = set()

    def visit_FunctionDef(self, node):
        if not node.name.startswith('_'):
            self.defined_functions.add(node.name)
        self.generic_visit(node)

class CallVisitor(ast.NodeVisitor):
    """Counts all function calls."""
    def __init__(self):
        self.called_functions = Counter() # Uses the imported Counter

    def visit_Call(self, node):
        def _add_call(name):
            if not name.startswith('_'):
                self.called_functions[name] += 1

        if isinstance(node.func, ast.Name):
            _add_call(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            _add_call(node.func.attr)

        for arg in node.args + [kw.value for kw in node.keywords]:
             if isinstance(arg, ast.Name):
                _add_call(arg.id)
        self.generic_visit(node)

# ==============================================================================
# 3. STATIC ANALYSIS CORE FUNCTIONS
# ==============================================================================

def parse_all_files(project_root, logger):
    """
    Parses all relevant Python files ONCE and returns a dictionary of ASTs.
    This is efficient as we don't re-read files for each check.
    """
    logger.info("\n--- Parsing project files for analysis (dev-mode) ---")
    files_to_check = [project_root / 'dictation_service.py']
    files_to_check.extend(project_root.glob('scripts/**/*.py'))

    parsed_trees = {}
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(file_path))
                parsed_trees[file_path] = tree
        except Exception as e:
            logger.warning(f"WARNING: Could not parse file: {file_path} ({e})")
    return parsed_trees

def check_for_unused_functions(parsed_trees, project_root, logger):
    """Finds unused functions using the pre-parsed ASTs."""
    logger.info("\n--- Checking for unused functions (dev-mode) ---")
    EXTERNALLY_CALLED_FUNCTIONS = {
        'on_created', 'audio_callback', 'visit_FunctionDef', 'visit_Call',
        'visit_Assign', 'visit_Dict', 'on_any_event', 'setUp', 'on_modified', 'filter',
        'test_transcription_with_long_pause_yields_multiple_chunks',
        'test_transcription_with_short_pause_yields_one_chunk'
    }

    all_definitions = {}
    all_calls = set()

    # Pass 1: Collect definitions
    for file_path, tree in parsed_trees.items():
        visitor = DefinitionVisitor()
        visitor.visit(tree)
        for func_name in visitor.defined_functions:
            all_definitions[func_name] = file_path

    # Pass 2: Collect calls
    call_visitor = CallVisitor()
    for tree in parsed_trees.values():
        call_visitor.visit(tree)
    all_calls.update(call_visitor.called_functions.keys())

    # Analysis
    unused = set(all_definitions.keys()) - all_calls - EXTERNALLY_CALLED_FUNCTIONS
    if not unused:
        logger.info("INFO: No unused functions found. Clean!")
    else:
        logger.error("\nFATAL: The following functions appear to be unused (dead code):")
        for name in sorted(list(unused)):
            file = all_definitions[name]
            logger.error(f"  - {name:<30} | Defined in: {file.relative_to(project_root)}")
        logger.error("\n  -> Please remove or use these functions.")
        sys.exit(1)

def check_for_frequent_calls(parsed_trees, logger, threshold=1):
    """Finds functions called more often than the threshold."""
    logger.info(f"\n--- Checking for functions called more than {threshold} time(s) ---")
    ALLOWED_FREQUENT_FUNCTIONS = {
        'info', 'debug', 'warning', 'error', 'critical', 'exception', 'print', 'join',
        'format', 'open', 'close', 'read', 'write', 'add', 'update', 'append', 'extend',
        'get', 'set', 'pop', 'startswith', 'endswith', 'strip', 'replace', 'split',
        'lower', 'upper', 'is_dir', 'is_file', 'exists', 'mkdir', 'relative_to', 'glob'
    }

    visitor = CallVisitor()
    for tree in parsed_trees.values():
        visitor.visit(tree)

    frequently_called = []
    for name, count in visitor.called_functions.items():
        if count > threshold and name not in ALLOWED_FREQUENT_FUNCTIONS:
            frequently_called.append((name, count))

    if not frequently_called:
        logger.info("INFO: No excessively frequent function calls found. Clean!")
    else:
        logger.warning("\nWARNING: The following functions are called frequently. Review for performance/redundancy:")
        for name, count in sorted(frequently_called, key=lambda item: item[1], reverse=True):
            logger.warning(f"  - {name:<30} | Called: {count} times")

# ==============================================================================
# 4. SCRIPT EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # This block runs only when you execute the script directly
    # e.g., python scripts/py/func/checks/setup_validator.py

    # Setup a simple logger for direct execution
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()

    # Define project root relative to this script's location
    # scripts/py/func/checks/setup_validator.py -> Navigate up 4 levels
    project_root = Path(__file__).resolve().parents[4]

    # --- Execute all checks ---
    parsed_trees = parse_all_files(project_root, logger)
    check_for_unused_functions(parsed_trees, project_root, logger)
    check_for_frequent_calls(parsed_trees, logger, threshold=1)

    logger.info("\n\n✅ All static analysis checks passed successfully.")

