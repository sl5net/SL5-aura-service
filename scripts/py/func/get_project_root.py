# scripts/py/func/get_project_root.py
import os
import platform
import sys
from pathlib import Path


def get_aura_project_root() -> Path:
    """Resolves project root using environment variable, cache file, or relative paths."""
    resolved_root = None

    # Stage 1: Environment variable
    env_val = os.environ.get("SL5NET_AURA_PROJECT_ROOT", "").strip()
    if env_val:
        p = Path(env_val)
        if p.is_dir():
            resolved_root = p

    # Stage 2: Cached project root file in temp directory
    if not resolved_root:
        tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
        root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
        if root_file.is_file():
            try:
                cached_val = root_file.read_text(encoding="utf-8").strip()
                if cached_val:
                    p = Path(cached_val)
                    if p.is_dir():
                        resolved_root = p
            except Exception as e_20260810_1002:
                print(f"Failed to read sl5net_aura_project_root from temp. 20260810_1002:{e_20260810_1002}")

    # Stage 3: Relative path calculation (assumes file is in scripts/py/func/)
    if not resolved_root:
        current_file = Path(__file__).resolve()
        if len(current_file.parents) >= 3:
            resolved_root = current_file.parents[3]
        else:
            resolved_root = current_file.parent

    root_str = str(resolved_root)
    os.environ["SL5NET_AURA_PROJECT_ROOT"] = root_str

    if "PYTHONPATH" in os.environ and os.environ["PYTHONPATH"]:
        if root_str not in os.environ["PYTHONPATH"].split(os.pathsep):
            os.environ["PYTHONPATH"] = root_str + os.pathsep + os.environ["PYTHONPATH"]
    else:
        os.environ["PYTHONPATH"] = root_str

    if root_str not in sys.path:
        sys.path.insert(0, root_str)

    return resolved_root
