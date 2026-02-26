import shutil
import subprocess

def find_espeak_candidates():
    candidates = ["espeak-ng", "espeak"]
    # On Windows someone might have espeak.exe explicitly, but shutil.which handles extensions
    for name in candidates:
        path = shutil.which(name)
        if path:
            # Verify by calling `--version` or `--help` to ensure it's the expected tool
            try:
                out = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True, timeout=2)
                # basic sanity check: output mentions 'espeak' or 'espeak-ng'
                if "espeak" in out.lower():
                    return path
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # falls through to try next candidate
                pass
    return None

def espeak_check(settings):
    if settings.USE_AS_PRIMARY_SPEAK == "ESPEAK" or settings.USE_ESPEAK_FALLBACK:
        espeak_path = find_espeak_candidates()
        if not espeak_path:
            print("espeak-ng not found, please install espeak-ng.")
            print("  Arch: sudo pacman -S espeak-ng")
            print("  Ubuntu: sudo apt install espeak-ng")
            print("  macOS: brew install espeak")

