#!/usr/bin/env python3
"""
tools/find_catch_all_in_fuzzy_maps.py

Scans every FUZZY_MAP_pre.py under config/maps/ for catch-all regex rules.
A catch-all rule matches almost anything (e.g. r'^(.*)$', r'^.*$', etc.)
and will intercept text before collect_unmatched.py can ever run.

Usage:
    python3 tools/find_catch_all_in_fuzzy_maps.py
"""
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Patterns that are considered catch-all
# ---------------------------------------------------------------------------
CATCH_ALL_PATTERNS = [
    re.compile(r"r['\"]\^\(\.\*\)\$['\"]"),      # r'^(.*)$'
    re.compile(r"r['\"]\^\.\*\$['\"]"),              # r'^.*$'
    re.compile(r"r['\"]\(\.\*\)['\"]"),              # r'(.*)'
    re.compile(r"r['\"]\.\*['\"]"),                   # r'.*'
    re.compile(r"r['\"]\^\(\?\:\.\*\)\$['\"]"), # r'^(?:.*)$'
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_all_fuzzy_map_files(root: Path) -> list[Path]:
    """Recursively find every file named FUZZY_MAP_pre.py under root."""
    return list(root.rglob("FUZZY_MAP_pre.py"))


def scan_file_for_catch_all(path: Path) -> list[tuple[int, str]]:
    """Return (line_number, line_text) for every catch-all match in the file."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:
        print(f"ERROR reading {path}: {exc}")
        return []

    matches = []
    for i, line in enumerate(lines, 1):
        for pat in CATCH_ALL_PATTERNS:
            if pat.search(line):
                matches.append((i, line.strip()))
    return matches


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    # Determine project root: assume this script lives in <root>/tools/
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    maps_dir = project_root / "config" / "maps"

    if not maps_dir.exists():
        print(f"ERROR: directory not found: {maps_dir}")
        return 1

    fuzzy_files = find_all_fuzzy_map_files(maps_dir)
    if not fuzzy_files:
        print(f"No FUZZY_MAP_pre.py files found under {maps_dir}")
        return 0

    found_any = False
    print("=" * 70)
    print("SCANNING FOR CATCH-ALL RULES")
    print(f"Root: {maps_dir}")
    print("=" * 70)

    for f in sorted(fuzzy_files):
        matches = scan_file_for_catch_all(f)
        if matches:
            found_any = True
            # Show relative path from project root for readability
            rel = f.relative_to(project_root)
            print(f"\n🚨  {rel}")
            for line_no, line_text in matches:
                print(f"    Line {line_no}: {line_text}")

    print()
    if found_any:
        print("=" * 70)
        print("RESULT: Catch-all rules FOUND — they will intercept ALL text.")
        print("ACTION: Remove or deprioritize them so collect_unmatched.py can run.")
        print("=" * 70)
        return 1
    else:
        print("✅  No catch-all rules found in any FUZZY_MAP_pre.py.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
