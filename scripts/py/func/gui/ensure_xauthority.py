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


def find_valid_display(current_uid: Optional[int] = None) -> Optional[str]:
    """Pure resolver returning the X11 display socket owned by current user."""
    uid = os.getuid() if current_uid is None else current_uid
    x11_dir = Path("/tmp/.X11-unix")
    if not x11_dir.is_dir():
        return None

    try:
        user_sockets = []
        for sock in x11_dir.glob("X*"):
            try:
                stat = sock.stat()
                if stat.st_uid == uid and sock.name[1:].isdigit():
                    user_sockets.append((int(sock.name[1:]), stat.st_mtime))
            except OSError:
                continue
        if user_sockets:
            user_sockets.sort(key=lambda item: item[1], reverse=True)
            return f":{user_sockets[0][0]}"
    except OSError:
        pass
    return None


def ensure_xauthority_env() -> Optional[str]:
    """Ensures XAUTHORITY and DISPLAY are properly set for current user."""
    user_display = find_valid_display()
    current_display = os.environ.get("DISPLAY")
    if user_display and (not current_display or current_display == ":0"):
        os.environ["DISPLAY"] = user_display

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
