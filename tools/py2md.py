import ast
import os
import sys

def extract_strings_recursive(node):
    results = []

    if isinstance(node, ast.FunctionDef):
        return results

    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                val = node.value

                if isinstance(val, ast.Constant) and isinstance(val.value, str):
                    results.append((node.lineno, var_name, val.value))

                elif isinstance(val, ast.JoinedStr):
                    try:
                        raw_str = ast.unparse(val).strip()
                        if raw_str.startswith(('f"', "f'")) and raw_str.endswith(('"', "'")):
                            raw_str = raw_str[2:-1]
                        elif raw_str.startswith(('"', "'")) and raw_str.endswith(('"', "'")):
                            raw_str = raw_str[1:-1]
                        results.append((node.lineno, var_name, raw_str))
                    except Exception:
                        results.append((node.lineno, var_name, "Exception: [F-String cant be parsed]"))

    for child in ast.iter_child_nodes(node):
        results.extend(extract_strings_recursive(child))

    return results

def write_md(py_path, translations):
    md_path = f"{os.path.splitext(py_path)[0]}.md"

    # sort line numbers
    translations.sort(key=lambda x: x[0])

    with open(md_path, "w", encoding="utf-8") as f:
        for _, var_name, text in translations:
            f.write(f"# {var_name}\n{text}\n\n")

    print(f"created ({len(translations)} strings found): {md_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use: python py2md.py <pfad_zu_py_datei>")
        sys.exit(1)

    py_file = sys.argv[1]
    if not os.path.exists(py_file):
        print(f"ERROR: '{py_file}' not exists.")
        sys.exit(1)

    with open(py_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=py_file)

    data = extract_strings_recursive(tree)
    write_md(py_file, data)
