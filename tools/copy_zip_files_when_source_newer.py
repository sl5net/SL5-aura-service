# tools/copy_zip_files_when_source_newer.py
import os
import shutil

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702


src_dir = p(PROJECT_ROOT / "config" / "maps")
dst_dir = p(PROJECT_ROOT / "data" / "_privat_zip")

# dst_dir.mkdir(parents=True, exist_ok=True)

def copy_zip_files_when_source_newer():

    for src_path in src_dir.glob("*.zip"):
        dst_path = dst_dir / src_path.name

        # If destination doesn't exist, copy. If it exists, copy only if source is newer.
        do_copy = not dst_path.exists() or src_path.stat().st_mtime > dst_path.stat().st_mtime

        if do_copy:
            shutil.copy2(src_path, dst_path)  # preserves metadata
            print(f"Copied: {src_path} -> {dst_path}")
        else:
            print(f"Skipped (up-to-date): {src_path}")
