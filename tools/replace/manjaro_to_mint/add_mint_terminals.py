#!/usr/bin/env python3
"""Add Linux Mint compatible terminal emulators to git plugin map configurations."""

from pathlib import Path
import re
import sys


def transform_terminal_list(content: str) -> str:
    """Pure transformation function to insert Mint terminals into only_in_windows lists."""
    pattern = re.compile(
        r"('only_in_windows':\s*\[\s*'Konsole',\s*'konsole',\s*'Terminal',\s*'Console')(?!,\s*'gnome-terminal')(\s*\])"
    )
    replacement = (
        r"\1, 'gnome-terminal', 'xterm', 'tilix', 'terminator'\2"
    )
    return pattern.sub(replacement, content)


def process_file(file_path: Path) -> bool:
    """Read, transform, and write back if modified."""
    original = file_path.read_text(encoding="utf-8")
    updated = transform_terminal_list(original)
    if original != updated:
        file_path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    base_dir = Path("config/maps/plugins/git")
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
