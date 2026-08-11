import os
import re
import sys
from pathlib import Path


def transform_file_content(content: str) -> tuple[str, bool]:
    """Transforms SL5NET_AURA_PROJECT_ROOT references to SL5NET_AURA_PROJECT_ROOT safely."""
    if "SL5NET_AURA_PROJECT_ROOT" not in content and "SL5NET_AURA_PROJECT_ROOT" not in content:
        return content, False

    original = content

    content = re.sub(
        r"\bSL5NET_AURA_PROJECT_ROOT\s*=\s*(?:Path\([^\n]+\)|os\.environ\.get\([^\n]+\))",
        "SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()",
        content,
    )

    # Replace os.environ.get(...) assignments
    content = re.sub(
        r"(?:SL5NET_AURA_PROJECT_ROOT)\s*=\s*os\.environ\.get\(['\"](?:SL5NET_AURA_PROJECT_ROOT|SL5NET_AURA_PROJECT_ROOT)['\"][^\n]*\)",
        "SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()",
        content,
    )

    content = re.sub(r"\bSL5NET_AURA_PROJECT_ROOT\b", "SL5NET_AURA_PROJECT_ROOT", content)

    # Ensure import statement exists if get_aura_project_root is used
    import_stmt = (
        "from scripts.py.func.get_project_root import get_aura_project_root"
    )
    if import_stmt not in content and "get_aura_project_root" in content:
        lines = content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_idx = i
                break
        lines.insert(insert_idx, import_stmt)
        content = "\n".join(lines) + "\n"

    return content, content != original




def process_directory(target_dir: Path, target_ext: str) -> list[Path]:
    """Recursively processes all .py files in target directory."""
    modified_files = []
    if not target_dir.is_dir():
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return modified_files

    for file_path in target_dir.rglob(f"*.{target_ext}"):
        try:
            content = file_path.read_text(encoding="utf-8")
            new_content, changed = transform_file_content(content)
            if changed:
                file_path.write_text(new_content, encoding="utf-8")
                modified_files.append(file_path)
        except Exception as e:
            print(f"Failed to process '{file_path}': {e}")

    return modified_files


def main():
    target_str = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "config/maps"
    target_ext = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else "py"

    target_dir = Path(target_str).resolve()
    print(f"Starting SL5NET_AURA_PROJECT_ROOT replacement {target_ext}-files in: {target_dir}")

    modified = process_directory(target_dir,target_ext)
    print(f"\nReplacement completed. Total modified {target_ext}-files: {len(modified)}")
    for p in modified:
        print(f"  - {p}")
    print(f"\nReplacement completed. Total modified {target_ext}-files: {len(modified)}")


if __name__ == "__main__":
    main()

