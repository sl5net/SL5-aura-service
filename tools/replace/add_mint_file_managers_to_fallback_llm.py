#!/usr/bin/env python3
"""Add Linux Mint file managers to exclude_windows in z_fallback_llm map files."""

from pathlib import Path
import re
import sys


def transform_fallback_llm_file_managers(content: str) -> str:
    """Pure transformation function to insert Nemo, Thunar, Caja into exclude_windows."""
    def replacer(match: re.Match) -> str:
        matched_str = match.group(0)
        keywords = ["double", "commander", "comandante", "cmd"]
        if any(kw in matched_str.lower() for kw in keywords):
            if "nemo" not in matched_str.lower():
                return re.sub(r"(\s*\])", r", r'nemo', r'thunar', r'caja'\1", matched_str)
        return matched_str

    pattern = re.compile(r"'exclude_windows':\s*\[[^\]]+\]")
    return pattern.sub(replacer, content)


def process_file(file_path: Path) -> bool:
    """Read, transform, and write back if modified."""
    original = file_path.read_text(encoding="utf-8")
    updated = transform_fallback_llm_file_managers(original)
    if original != updated:
        file_path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    base_dir = Path("config/maps/plugins/z_fallback_llm")
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}", file=sys.stderr)
        return 1

    modified_count = 0
    for path in sorted(base_dir.rglob("*.py")):
        if process_file(path):
            print(f"Updated: {path}")
            modified_count += 1

    print(f"Total files updated: {modified_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
