import os
from pathlib import Path
from typing import Iterable, Optional


def find_valid_xauthority(candidate_dirs: Iterable[Path]) -> Optional[Path]:
    """Pure resolver returning the newest valid xauth file from candidate directories."""
    valid_files: list[Path] = []
    for directory in candidate_dirs:
        try:
            if not directory.is_dir():
                continue
            for file_path in directory.glob("xauth_*"):
                try:
                    if file_path.is_file() and file_path.stat().st_size > 0:
                        valid_files.append(file_path)
                except OSError:
                    continue
        except OSError:
            continue

    if not valid_files:
        return None
    valid_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return valid_files[0]


def ensure_xauthority_env() -> Optional[str]:
    """Ensures XAUTHORITY is set to a readable file in os.environ."""
    current = os.environ.get("XAUTHORITY")
    if current and os.path.isfile(current) and os.path.getsize(current) > 0:
        return current

    home_xauth = Path.home() / ".Xauthority"
    if home_xauth.is_file() and home_xauth.stat().st_size > 0:
        os.environ["XAUTHORITY"] = str(home_xauth)
        return str(home_xauth)

    runtime_dir = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))
    candidates = [runtime_dir, Path("/tmp")]
    found = find_valid_xauthority(candidates)
    if found is not None:
        os.environ["XAUTHORITY"] = str(found)
        return str(found)

    return None
