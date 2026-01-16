"""
    Run the script: py

tools/tests/analyze_path_headroom.py

    Result: It will tell you exactly:

        Which file is the "culprit" (the longest one).

        How many characters your installation folder (e.g. C:\Users\...\Downloads\Project) currently uses.

        How many characters it is allowed to have max.

Example Output:
code Text

Longest internal file:   ...\models\vosk-model-de-0.21\rescore\G.fst
Internal path length:    45 characters
------------------------------------------------------------
Maximum allowed length
for Project Root Folder: 214 characters
------------------------------------------------------------
Current Root Path:       C:\Users\User\Downloads\Very_Long_Folder_Name\Project
Current Root Length:     230 characters
------------------------------------------------------------
❌ CRITICAL FAIL: The path is already too long by 16 characters!
"""



import os
import sys
from pathlib import Path

# Standard Windows API limit
MAX_PATH_LIMIT = 260

def analyze_path_headroom():
    # 1. Determine Project Root
    # Assuming this script is located in: [PROJECT_ROOT]/tools/tests/
    # We go up two levels from the script's location.
    script_location = Path(__file__).parent.resolve()

    # Adjust .parents[1] if your folder structure is different (e.g., just tools/)
    # .parents[1] means: tools/tests -> tools -> PROJECT_ROOT
    project_root = script_location.parents[1]

    print(f"--- PATH ANALYSIS TOOL ---")
    print(f"Script location: {script_location}")
    print(f"Detected Project Root: {project_root}")
    print("-" * 60)

    max_internal_length = 0
    longest_file_rel = ""
    longest_file_abs = ""

    print("Scanning project files...")

    # 2. Walk through the project to find the file with the longest internal path
    for root, dirs, files in os.walk(project_root):
        # Optional: Skip .git folder to focus on application files
        if ".git" in dirs:
            dirs.remove(".git")

        for name in files:
            abs_path = Path(root) / name
            try:
                # Get path relative to project root (e.g., "models/vosk.../README")
                rel_path = abs_path.relative_to(project_root)
                rel_path_str = str(rel_path)

                # We need the length of this string + 1 (for the leading slash when joined)
                current_internal_len = len(rel_path_str)

                if current_internal_len > max_internal_length:
                    max_internal_length = current_internal_len
                    longest_file_rel = rel_path_str
                    longest_file_abs = str(abs_path)
            except ValueError:
                # Should not happen if walking inside project_root
                continue

    if max_internal_length == 0:
        print("❌ Error: No files found. Check the project root detection.")
        return

    # 3. Calculate Limits
    # The formula: Total_Path = (Installation_Dir_Length) + 1 (Separator) + (Internal_File_Length)
    # Therefore: Max_Installation_Dir = 260 - 1 - Internal_File_Length

    max_allowed_installation_path_len = MAX_PATH_LIMIT - 1 - max_internal_length
    current_root_len = len(str(project_root))

    headroom = max_allowed_installation_path_len - current_root_len

    # 4. Output Report
    print("\n📊 ANALYSIS RESULTS")
    print("-" * 60)
    print(f"Longest internal file:   ...\\{longest_file_rel}")
    print(f"Internal path length:    {max_internal_length} characters")
    print("-" * 60)
    print(f"Windows Max Path Limit:  {MAX_PATH_LIMIT} characters")
    print(f"Maximum allowed length \nfor Project Root Folder: {max_allowed_installation_path_len} characters")
    print("-" * 60)
    print(f"Current Root Path:       {project_root}")
    print(f"Current Root Length:     {current_root_len} characters")
    print("-" * 60)

    if headroom < 0:
        print(f"❌ CRITICAL FAIL: The path is already too long by {abs(headroom)} characters!")
        print("   This is why 'models not found' or crashes occur.")
    elif headroom < 15:
        print(f"⚠️ WARNING: You are very close to the limit.")
        print(f"   You only have {headroom} characters left for folder renaming.")
    else:
        print(f"✅ PASS: The current path structure is safe.")
        print(f"   You have {headroom} characters 'buffer' before it crashes.")

    print("-" * 60)

    # 5. Suggestion for Simulation
    print("\n💡 SIMULATION:")
    print("If you were to move this project to the desktop, would it work?")
    user_home = Path.home()
    desktop_path = user_home / "Desktop" / project_root.name
    desktop_len = len(str(desktop_path))

    if (desktop_len + 1 + max_internal_length) >= MAX_PATH_LIMIT:
        print(f"   -> NO. Even on Desktop ({desktop_len} chars), it would crash.")
    else:
        print(f"   -> YES. Moving to Desktop ({desktop_len} chars) would fix it.")

if __name__ == "__main__":
    analyze_path_headroom()
    input("\nPress ENTER to close...")

