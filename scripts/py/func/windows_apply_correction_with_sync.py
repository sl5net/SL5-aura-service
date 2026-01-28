import os
import shutil
# scripts/py/func/windows_apply_correction_with_sync.py


import subprocess
import time
from pathlib import Path

windows_apply_correction_LAST_NOTIFY_TIME = 0

def windows_apply_correction_with_sync():

    windows_apply_correction_notify_cooldown = 3.0

    current_time = time.time()
    global windows_apply_correction_LAST_NOTIFY_TIME
    # global PROJECT_ROOT
    if (current_time - windows_apply_correction_LAST_NOTIFY_TIME) < windows_apply_correction_notify_cooldown:
        return

    # ahk_path = "AutoHotkey.exe"


    ahk_path = shutil.which("AutoHotkey.exe")

    if not ahk_path:
        standard_paths = [
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\v1.1\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"
        ]
        for p in standard_paths:
            if os.path.exists(p):
                ahk_path = p
                break

    if not ahk_path:
        print("error: AutoHotkey not found!")

    # scripts/py/func/process_text_in_background.py:2013
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

    script_path = PROJECT_ROOT / "scripts" / "ahk" / "sync_editor.ahk"

    # subprocess.run([ahk_path, script_path, "save"])

    #with open(file_path, "w", encoding="utf-8") as f:
    #    f.write(corrected_text)

    subprocess.run([ahk_path, script_path, "notify"])
    windows_apply_correction_LAST_NOTIFY_TIME = current_time

