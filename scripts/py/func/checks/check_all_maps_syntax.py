# scripts/py/func/checks/check_all_maps_syntax.py
import os
import sys
import ast

def check_syntax(file_path):
    # log.info(f"Checking syntax for {file_path}") # Using print for direct feedback
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print("❌" * 50)
        print(f"❌ ERROR: Syntax error in {file_path} -> {e}")
        print("❌" * 50)
        return False

def check_folder_syntax(root_dir):
    print(f"INFO: Starting syntax check in directory: {root_dir}")
    has_errors = False
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                if not check_syntax(file_path):
                    has_errors = True

    if has_errors:
        print("\n❌ FAILURE: Found syntax errors in one or more map files.")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: All map files have valid Python syntax.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_syntax.py <directory_path>")

    check_folder_syntax(sys.argv[1])

