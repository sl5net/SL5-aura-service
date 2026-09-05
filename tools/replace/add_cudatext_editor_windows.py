#!/usr/bin/env python3
"""Add CudaText and xed editors to window filter lists in map configuration files."""

from pathlib import Path
import re
import sys


def transform_window_list(content: str) -> str:
    """Pure transformation function to insert CudaText and xed alongside Kate."""
    pattern = re.compile(
        r"('only_in_windows':\s*\[[^\]]*r'Kate')(?!,\s*r'CudaText')([^\]]*\])"
    )
    replacement = r"\1, r'CudaText', r'xed'\2"
    return pattern.sub(replacement, content)


def process_file(file_path: Path) -> bool:
    """Read, transform, and write back if modified."""
    original = file_path.read_text(encoding="utf-8")
    updated = transform_window_list(original)
    if original != updated:
        file_path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    base_dir = Path("config/maps")
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

