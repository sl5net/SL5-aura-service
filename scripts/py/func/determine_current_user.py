import getpass
import os
from typing import Tuple

def determine_current_user() -> Tuple[str, str]:
    """Return (username, source). Tries getpass.getuser(), then env vars, else 'unknown_user'."""
    try:
        user = getpass.getuser()
    except Exception:
        user = None

    if user and user.strip():
        return user, "getpass"

    for env_var in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        user_env = os.environ.get(env_var)
        if user_env and user_env.strip():
            return user_env, f"env:{env_var}"

    return "unknown_user", "fallback"
