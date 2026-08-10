# scripts/py/func/get_project_root.py
import os
import platform
from pathlib import Path


def get_project_root() -> Path:
    """Resolves project root using environment variable, cache file, or relative paths."""
    # Stage 1: Environment variables
    for env_var in ("SL5NET_AURA_PROJECT_ROOT"):
        env_val = os.environ.get(env_var, "").strip()
        if env_val:
            p = Path(env_val)
            if p.is_dir():
                return p

    # Stage 2: Cached project root file in temp directory
    tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
    if root_file.is_file():
        try:
            cached_val = root_file.read_text(encoding="utf-8").strip()
            if cached_val:
                p = Path(cached_val)
                if p.is_dir():
                    os.environ["SL5NET_AURA_PROJECT_ROOT"] = str(p)
                    return p
        except Exception as e_20260810_1002:
            print(f"Failed to read sl5net_aura_project_root from temp. 20260810_1002:{e_20260810_1002}")
            pass

    # Stage 3: Relative path calculation (assumes file is in scripts/py/func/)
    current_file = Path(__file__).resolve()
    if len(current_file.parents) >= 3:
        computed_root = current_file.parents[3]
    else:
        computed_root = current_file.parent

    os.environ["SL5NET_AURA_PROJECT_ROOT"] = str(computed_root)
    return computed_root

