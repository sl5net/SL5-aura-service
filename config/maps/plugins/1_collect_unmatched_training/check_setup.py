"""
Diagnostic script to check whether the current collect_unmatched_training
setup actually has the up-to-date insert_template_rule() (the one that
embeds the spoken text, not a hardcoded 'nix').

Usage:
    python3 check_setup.py /path/to/collect_unmatched_training
    (defaults to the folder this script is in, if no path is given)
"""

import importlib.util
import re
import sys
import tempfile
from pathlib import Path


def main():
    base_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    helpers_dir = base_dir / "helpers"
    itr_file = helpers_dir / "insert_template_rule.py"
    put_file = helpers_dir / "process_unmatched_text.py"

    print(f"Checking: {base_dir}\n")

    if not base_dir.exists():
        print(f"[ERROR] This path does not exist: {base_dir.resolve()}")
        sys.exit(1)

    ok = True
    ok &= _check_file_exists(itr_file)
    ok &= _check_file_exists(put_file)
    if not ok:
        print(f"\nExpected files not found at: {helpers_dir.resolve()}")
        print("Searching the whole tree under the given path instead...\n")
        found_itr = _find_all(base_dir, "insert_template_rule.py")
        found_put = _find_all(base_dir, "process_unmatched_text.py")
        _report_found("insert_template_rule.py", found_itr)
        _report_found("process_unmatched_text.py", found_put)

        if found_itr:
            print(f"\nUsing the first found copy for the checks below: {found_itr[0]}")
            itr_file = found_itr[0]
        else:
            print("\n-> insert_template_rule.py not found anywhere under this path, aborting.")
            sys.exit(1)

    print()
    _check_source_text(itr_file)
    print()
    _check_pycache(itr_file.parent)
    print()
    _run_live_functional_test(itr_file)


def _find_all(base_dir: Path, filename: str):
    return sorted(base_dir.rglob(filename))


def _report_found(filename: str, found: list):
    if not found:
        print(f"  {filename}: NOT FOUND anywhere under {base_dir_display()}")
        return
    print(f"  {filename}: found {len(found)} copy/copies:")
    for p in found:
        print(f"    - {p}")


def base_dir_display():
    return sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent)


def _check_file_exists(path: Path) -> bool:
    exists = path.exists()
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {path}")
    return exists


def _check_source_text(itr_file: Path):
    content = itr_file.read_text(encoding="utf-8")

    has_text_param = 'text: str = "nix"' in content
    has_old_hardcoded_line = bool(
        re.search(r"""template_line\s*=\s*f["']\{indent\}\('nix', r\^\(nix\)\$'\)""", content)
    ) or "template_line = f\"{indent}('nix', r'^(nix)$'),\\n\"" in content
    has_repr_based_pattern = "repr(f'^({re.escape(text)})$')" in content or "repr(f\"^({re.escape(text)})$\")" in content

    print("Source checks on insert_template_rule.py:")
    print(f"  - has 'text' parameter (text: str = \"nix\"):  {'YES' if has_text_param else 'NO'}")
    print(f"  - still has OLD hardcoded 'nix' template line: {'YES (BAD, old version!)' if has_old_hardcoded_line else 'no'}")
    print(f"  - has NEW repr()-based pattern building:       {'YES' if has_repr_based_pattern else 'NO'}")

    if has_text_param and has_repr_based_pattern and not has_old_hardcoded_line:
        print("  => Source text looks like the current version.")
    else:
        print("  => Source text does NOT look like the current version!")


def _check_pycache(helpers_dir: Path):
    pycache = helpers_dir / "__pycache__"
    if not pycache.exists():
        print("No __pycache__ folder present (nothing to worry about).")
        return

    print(f"__pycache__ found at {pycache}:")
    stale_found = False
    for pyc in pycache.glob("*.pyc"):
        # e.g. insert_template_rule.cpython-312.pyc -> insert_template_rule.py
        base_name = pyc.stem.split(".")[0]
        source = helpers_dir / f"{base_name}.py"
        if not source.exists():
            continue
        if pyc.stat().st_mtime < source.stat().st_mtime:
            stale_found = True
            print(f"  - STALE: {pyc.name} is older than {source.name}")
        else:
            print(f"  - ok: {pyc.name}")

    if stale_found:
        print("  => Stale .pyc files found. Delete the __pycache__ folder to be safe:")
        print(f"     rm -rf {pycache}")
    else:
        print("  => No stale .pyc files detected (Python checks source mtime automatically anyway,")
        print("     so a __pycache__ folder alone is normally not a problem).")


def _run_live_functional_test(itr_file: Path):
    """
    The definitive test: actually import the real insert_template_rule.py
    file (by path, bypassing any other 'insert_template_rule' that might
    already be cached elsewhere under sys.modules) and run it for real
    against a temp fixture file with text='Federball'.
    """
    print("Live functional test (actually calling the loaded function):")

    spec = importlib.util.spec_from_file_location("insert_template_rule_live_check", itr_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "FUZZY_MAP_pre.py"
        fixture.write_text(
            "import re # noqa: F401\n"
            "FUZZY_MAP_pre = [\n"
            "\n"
            "]\n",
            encoding="utf-8",
        )
        content = fixture.read_text(encoding="utf-8")
        # Position right where a rule would be inserted (arbitrary, end of list is fine for this isolated test)
        catch_all_start = content.rfind("]")

        try:
            module.insert_template_rule(fixture, content, catch_all_start, "Federball")
        except TypeError as e:
            print(f"  => FAILURE: calling insert_template_rule(..., text='Federball') raised:")
            print(f"     {e}")
            print("     This means the loaded function does not accept a 'text' argument at all")
            print("     -> an OLD version of insert_template_rule.py is being executed.")
            return
        result = fixture.read_text(encoding="utf-8")

    print("  Resulting file content:")
    for line in result.splitlines():
        print(f"    {line}")

    if "Federball" in result and "'nix'" not in result:
        print("\n  => SUCCESS: 'Federball' was embedded correctly, no hardcoded 'nix'.")
    elif "'nix'" in result and "Federball" not in result:
        print("\n  => FAILURE: this loaded module still hardcodes 'nix' -> an OLD version of")
        print("     insert_template_rule.py is being executed. Check for:")
        print("     - a duplicate copy of the file elsewhere in the project (e.g. an older")
        print("       collect_unmatched_training folder still referenced by on_match_exec paths)")
        print("     - the FUZZY_MAP_pre.py's on_match_exec path pointing at a different")
        print("       collect_unmatched.py than the one you edited")
    else:
        print("\n  => UNEXPECTED result, please inspect manually.")


if __name__ == "__main__":
    main()
