#!/usr/bin/env python3
"""
Verify matching balance of 'if' and 'fi' statements in Shell scripts.
"""
import sys
import re
from pathlib import Path


def check_file(file_path: Path) -> bool:
    if not file_path.is_file():
        print(f"[ERROR] File not found: {file_path}")
        return False

    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    stack = []
    total_ifs = 0
    total_fis = 0

    if_pattern = re.compile(r'(?<![\w-])if(?![\w-])')
    fi_pattern = re.compile(r'(?<![\w-])fi(?![\w-])')

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        content = stripped.split("#")[0].strip()
        if not content:
            continue

        if_matches = if_pattern.findall(content)
        fi_matches = fi_pattern.findall(content)

        for _ in if_matches:
            total_ifs += 1
            stack.append((idx, line.strip()))

        for _ in fi_matches:
            total_fis += 1
            if stack:
                stack.pop()
            else:
                print(f"  [ERROR] Unmatched 'fi' at Line {idx}: {line.strip()}")

    print(f"[{file_path}]")
    print(f"  Total 'if' found: {total_ifs}")
    print(f"  Total 'fi' found: {total_fis}")

    if not stack and total_ifs == total_fis:
        print(f"  [OK] Balance verified: All {total_ifs} 'if' block(s) properly closed with 'fi'.")
        return True
    else:
        print(f"  [MISMATCH] Remaining unclosed 'if' statements: {len(stack)}")
        for l_num, text in stack:
            print(f"    - Unclosed 'if' from Line {l_num}: {text}")
        return False


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "setup/helper/install_cudatext.sh"
    p = Path(target)
    if p.is_dir():
        all_ok = True
        for f in sorted(p.glob("**/*.sh")):
            if not check_file(f):
                all_ok = False
        sys.exit(0 if all_ok else 1)
    else:
        success = check_file(p)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

