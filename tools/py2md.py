# tools/py2md.py
import ast
import os
import sys

def is_translatable(var_name, text):
    t = text.strip()
    if " " not in t:
        return False
    if len(t) <= 2:
        return False
    # Exclude technical identifier tokens with underscores (e.g. text_detected, Scroll_Lock)
    if "_" in t and " " not in t:
        return False
    # Exclude technical mapping variable names
    var_lower = var_name.lower()
    if any(suffix in var_lower for suffix in ("_map", "_keys", "_codes", "fallback")):
        return False
    return True

def is_translatable(var_name, text):
    t = text.strip()
    if len(t) <= 2:
        return False
    if "_" in t and " " not in t:
        return False
    var_lower = var_name.lower()
    if any(suffix in var_lower for suffix in ("_map", "_keys", "_codes", "fallback")):
        return False
    return True

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
                    if is_translatable(var_name, val.value):
                        results.append((node.lineno, var_name, val.value))

                elif isinstance(val, ast.JoinedStr):
                    try:
                        raw_str = ast.unparse(val).strip()
                        if raw_str.startswith(('f"', "f'")) and raw_str.endswith(('"', "'")):
                            raw_str = raw_str[2:-1]
                        elif raw_str.startswith(('"', "'")) and raw_str.endswith(('"', "'")):
                            raw_str = raw_str[1:-1]
                        if is_translatable(var_name, raw_str):
                            results.append((node.lineno, var_name, raw_str))
                    except Exception:
                        pass

                elif isinstance(val, (ast.List, ast.Tuple)):
                    for i, elt in enumerate(val.elts):
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            if is_translatable(var_name, elt.value):
                                results.append((elt.lineno, f"{var_name}[{i}]", elt.value))

                elif isinstance(val, ast.Dict):
                    for k, v in zip(val.keys, val.values):
                        k_name = k.value if isinstance(k, ast.Constant) else "key"
                        if isinstance(v, ast.Constant) and isinstance(v.value, str):
                            if is_translatable(var_name, v.value):
                                results.append((v.lineno, f"{var_name}['{k_name}']", v.value))
                        elif isinstance(v, (ast.List, ast.Tuple)):
                            for i, elt in enumerate(v.elts):
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    if is_translatable(var_name, elt.value):
                                        results.append((elt.lineno, f"{var_name}['{k_name}'][{i}]", elt.value))
                elif isinstance(val, (ast.List, ast.Tuple)):
                    for i, elt in enumerate(val.elts):
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            results.append((elt.lineno, f"{var_name}[{i}]", elt.value))

                elif isinstance(val, ast.Dict):
                    for k, v in zip(val.keys, val.values):
                        k_name = k.value if isinstance(k, ast.Constant) else "key"
                        if isinstance(v, ast.Constant) and isinstance(v.value, str):
                            results.append((v.lineno, f"{var_name}['{k_name}']", v.value))
                        elif isinstance(v, (ast.List, ast.Tuple)):
                            for i, elt in enumerate(v.elts):
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    results.append((elt.lineno, f"{var_name}['{k_name}'][{i}]", elt.value))
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
