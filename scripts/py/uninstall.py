import argparse
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# i18n Definitions (compatible with tools/py2md.py)
# ---------------------------------------------------------------------------
STRING_KEYS = [
    "prompt_confirm",
    "prompt_keep_maps",
    "msg_stopping",
    "msg_autostart_del",
    "msg_backup_done",
    "msg_removing_files",
    "msg_done",
    "msg_aborted",
]

DEFAULT_STRINGS = {
    "en": [
        "Are you sure you want to uninstall SL5 Aura? (y/N)",
        "Keep custom maps and user configurations in 'config/maps/'? (Y/n)",
        "Stopping running Aura processes…",
        "Removing autostart configurations…",
        "Backup of custom maps created at: {backup_path}",
        "Removing application files and virtual environments…",
        "SL5 Aura has been successfully uninstalled.",
        "Uninstallation cancelled by user.",
    ],
}

FALLBACK_LANG = "en"
I18N_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uninstall.i18n")


def parse_i18n_md(path):
    lines_out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            stripped = re.sub(r"^(\d+[\.\)]\s+|[-*+]\s+|>\s+)", "", line)
            lines_out.append(stripped)
    return lines_out


def load_translations(lang_code, i18n_dir=I18N_DIR, fallback_lang=FALLBACK_LANG):
    fallback = DEFAULT_STRINGS.get(lang_code, DEFAULT_STRINGS[fallback_lang])
    md_path = os.path.join(i18n_dir, f"uninstall-{lang_code}lang.md")
    if not os.path.isfile(md_path):
        return fallback
    try:
        parsed = parse_i18n_md(md_path)
        needed = len(STRING_KEYS)
        if len(parsed) < needed:
            parsed = parsed + fallback[len(parsed):]
        return parsed[:needed]
    except Exception:
        return fallback


def get_strings(lang_code, **fmt_kwargs):
    values = load_translations(lang_code)
    formatted = []
    for val in values:
        for k, v in fmt_kwargs.items():
            val = val.replace("{" + k + "}", str(v))
        formatted.append(val)
    return dict(zip(STRING_KEYS, formatted))


def detect_installed_language(repo_root):
    model_file = os.path.join(repo_root, "config", "model_name.txt")
    try:
        if os.path.isfile(model_file):
            with open(model_file, "r", encoding="utf-8") as f:
                content = f.read().strip().lower()
            if "vosk-model-de" in content or "german" in content:
                return "de"
            if "vosk-model-fr" in content or "french" in content:
                return "fr"
            if "vosk-model-es" in content or "spanish" in content:
                return "es"
            if "vosk-model-it" in content or "italian" in content:
                return "it"
    except Exception:
        pass
    return "en"


# ---------------------------------------------------------------------------
# Uninstaller Actions
# ---------------------------------------------------------------------------
def stop_processes():
    system = platform.system()
    try:
        if system in ("Linux", "Darwin"):
            subprocess.run(["pkill", "-f", "restart_venv_and_run-server.sh"], stderr=subprocess.DEVNULL, check=False)
            subprocess.run(["pkill", "-f", "aura_engine"], stderr=subprocess.DEVNULL, check=False)
            shutil.rmtree("/tmp/sl5_aura", ignore_errors=True)
        elif system == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "aura_engine.exe"], stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        print(f"[WARN] Error while stopping processes: {e}", file=sys.stderr)


def remove_autostart():
    system = platform.system()
    try:
        if system == "Linux":
            autostart_dir = os.path.expanduser("~/.config/autostart")
            for filename in ("aura_engine.desktop", "aura_engine.sh.desktop"):
                path = os.path.join(autostart_dir, filename)
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"[OK] Removed autostart entry: {path}", file=sys.stderr)
        elif system == "Darwin":
            plist_file = os.path.expanduser("~/Library/LaunchAgents/com.sl5net.aura.plist")
            if os.path.isfile(plist_file):
                subprocess.run(["launchctl", "unload", plist_file], stderr=subprocess.DEVNULL, check=False)
                os.remove(plist_file)
                print(f"[OK] Removed LaunchAgent: {plist_file}", file=sys.stderr)
        elif system == "Windows":
            appdata = os.environ.get("APPDATA")
            if appdata:
                bat_file = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "aura_engine.bat")
                if os.path.isfile(bat_file):
                    os.remove(bat_file)
                    print(f"[OK] Removed startup batch file: {bat_file}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] Failed to clean autostart: {e}", file=sys.stderr)


def backup_maps(repo_root):
    maps_dir = os.path.join(repo_root, "config", "maps")
    if not os.path.isdir(maps_dir):
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.expanduser(f"~/sl5_aura_maps_backup_{timestamp}.tar.gz")
    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(maps_dir, arcname="maps")
        return backup_path
    except Exception as e:
        print(f"[WARN] Failed to create backup: {e}", file=sys.stderr)
        return None


def clean_application_files(repo_root, keep_maps=True, purge=False):
    if purge:
        print(f"[INFO] Purging directory: {repo_root}", file=sys.stderr)
        # Handle opt install directory removal
        parent_dir = os.path.dirname(repo_root)
        if os.path.basename(parent_dir) == "opt" and os.path.basename(repo_root) == "sl5-aura-service":
            shutil.rmtree(repo_root, ignore_errors=True)
            return

    # Clean runtime artifacts and virtualenvs
    targets = [".venv", ".tmp", "aura_engine.log", "__pycache__"]
    for target in targets:
        target_path = os.path.join(repo_root, target)
        if os.path.isdir(target_path):
            shutil.rmtree(target_path, ignore_errors=True)
        elif os.path.isfile(target_path):
            os.remove(target_path)

    if not keep_maps:
        maps_dir = os.path.join(repo_root, "config", "maps")
        if os.path.isdir(maps_dir):
            shutil.rmtree(maps_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="SL5 Aura Uninstaller")
    parser.add_argument("--purge", action="store_true", help="Remove all files including custom maps")
    parser.add_argument("--yes", "-y", action="store_true", help="Non-interactive confirmation")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    lang_code = detect_installed_language(repo_root)
    strings = get_strings(lang_code)

    if not args.yes:
        confirm = input(f"🗑️ {strings['prompt_confirm']} ").strip().lower()
        if confirm not in ("y", "yes"):
            print(f"ℹ️ {strings['msg_aborted']}", file=sys.stderr)
            sys.exit(0)

    keep_maps = True
    if args.purge:
        keep_maps = False
    elif not args.yes:
        ans_maps = input(f"🛡️ {strings['prompt_keep_maps']} ").strip().lower()
        if ans_maps in ("n", "no"):
            keep_maps = False

    print(f"🛑 {strings['msg_stopping']}", file=sys.stderr)
    stop_processes()

    print(f"⚙️ {strings['msg_autostart_del']}", file=sys.stderr)
    remove_autostart()

    # Always create a safety backup if maps are being deleted
    if not keep_maps:
        backup_file = backup_maps(repo_root)
        if backup_file:
            msg = strings['msg_backup_done'].replace("{backup_path}", backup_file)
            print(f"💾 {msg}", file=sys.stderr)

    print(f"🗑️ {strings['msg_removing_files']}", file=sys.stderr)
    clean_application_files(repo_root, keep_maps=keep_maps, purge=args.purge)

    print(f"✅ {strings['msg_done']}", file=sys.stderr)


if __name__ == "__main__":
    main()
