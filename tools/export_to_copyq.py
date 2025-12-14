#!/usr/bin/env python3

readme = """
The script operates in read-only mode regarding your file system:
It reads your map files (.py) and settings_local.py only to extract data.

It sends commands to the external tool CopyQ.

No files in your project folder are modified, deleted, or overwritten by this script.
"""

import os
import re
import sys
import shutil
import subprocess

import importlib.util



# -----------------------------------------------------------------------------
# KONFIGURATION
# -----------------------------------------------------------------------------
COPYQ_TAB_NAME = "SL5-Demo"
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(TOOL_DIR, "..", "config", "maps")
TARGET_FILES = ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]

SETTINGS_FILE = os.path.join(TOOL_DIR, "..", "config", "settings_local.py")

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def load_plugins_config():
    """
    Loads PLUGINS_ENABLED from config/settings_local.py.
    Returns an empty dict if file not found.
    """
    if not os.path.exists(SETTINGS_FILE):
        print(f"logger.info: No settings file found at {SETTINGS_FILE}. Assuming all enabled.")
        return {}

    try:
        spec = importlib.util.spec_from_file_location("settings_local", SETTINGS_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "PLUGINS_ENABLED"):
            print("logger.info: Loaded PLUGINS_ENABLED configuration.")
            return module.PLUGINS_ENABLED
    except Exception as e:
        print(f"logger.info: Error loading settings: {e}")

    return {}



# -----------------------------------------------------------------------------
# CHECK COPYQ & ENVIRONMENT
# -----------------------------------------------------------------------------
if not shutil.which("copyq"):
    print("logger.info: Error: 'copyq' command not found.")
    sys.exit(1)

# Fix for Locale warnings (Qt needs UTF-8)
env = os.environ.copy()
env["LANG"] = "C.UTF-8"
env["LC_ALL"] = "C.UTF-8"

try:
    subprocess.run(["copyq", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
except Exception as e:
    print("logger.info: Error: Is CopyQ running? Please start it.")
    sys.exit(1)

# -----------------------------------------------------------------------------
# EXTRAKTION
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXTRACTION
# -----------------------------------------------------------------------------
def collect_examples():
    examples = {} # Dictionary: Content -> List of Tags (Ordered)
    total_tags_found = 0
    plugins_enabled = load_plugins_config()

    regex_example = re.compile(r'^\s*#\s*EXAMPLE:\s*(.*)$')
    regex_lang = re.compile(r'^[a-z]{2}-[A-Z]{2}$')

    if not os.path.isdir(MAPS_DIR):
        print(f"logger.info: Error: Directory {MAPS_DIR} not found.")
        sys.exit(1)

    print(f"logger.info: Scanning {os.path.relpath(MAPS_DIR)} ...")

    file_count = 0
    for root, dirs, files in os.walk(MAPS_DIR):
        rel_path = os.path.relpath(root, MAPS_DIR)
        path_parts = rel_path.split(os.sep)

        # -------------------------------------------------------------
        # Filter Logic
        # -------------------------------------------------------------
        is_disabled = False
        for part in path_parts:
            if plugins_enabled.get(part) is False:
                is_disabled = True
                break

        if is_disabled:
            continue

        # -------------------------------------------------------------
        # Tag Logic: Extract folder names (List to preserve order)
        # -------------------------------------------------------------
        # We use a list comprehension to keep the order: Parent -> Child
        current_tags = [
            part for part in path_parts
            if part != "plugins" and part != "." and not regex_lang.match(part)
        ]

        for file in files:
            if file in TARGET_FILES:
                file_path = os.path.join(root, file)
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = regex_example.search(line)
                            if match:
                                content = match.group(1).strip()
                                if content:
                                    total_tags_found += 1

                                    if content not in examples:
                                        examples[content] = []

                                    # Add tags preserving order and avoiding duplicates
                                    for tag in current_tags:
                                        if tag not in examples[content]:
                                            examples[content].append(tag)

                except Exception as e:
                    print(f"logger.info: Warning at {file}: {e}")

    result_list = []
    for text in sorted(examples.keys()):
        # The list is already in folder order (Parent -> Child)
        tags_list = examples[text]

        # If you want Child -> Parent, use: tags_list = examples[text][::-1]

        result_list.append({'text': text, 'tags': tags_list})

    print(f"logger.info: Statistics:")
    print(f"  - Files scanned: {file_count}")
    print(f"  - Entries found: {total_tags_found}")
    print(f"  - Unique entries: {len(result_list)}")

    return result_list


def collect_examples_old_with_random_order():
    examples = {} # Dictionary: Content -> Set of Tags
    total_tags_found = 0
    plugins_enabled = load_plugins_config()

    regex_example = re.compile(r'^\s*#\s*EXAMPLE:\s*(.*)$')
    regex_lang = re.compile(r'^[a-z]{2}-[A-Z]{2}$') # e.g. de-DE

    if not os.path.isdir(MAPS_DIR):
        print(f"logger.info: Error: Directory {MAPS_DIR} not found.")
        sys.exit(1)

    print(f"logger.info: Scanning {os.path.relpath(MAPS_DIR)} ...")

    file_count = 0
    for root, dirs, files in os.walk(MAPS_DIR):

        # -------------------------------------------------------------
        # Tag Logic: Extract folder names
        # -------------------------------------------------------------
        rel_path = os.path.relpath(root, MAPS_DIR)
        path_parts = rel_path.split(os.sep)


        # -------------------------------------------------------------
        # Filter Logic: Check if any folder in path is disabled
        # -------------------------------------------------------------
        is_disabled = False
        for part in path_parts:
            # Only exclude if explicitly set to False in config
            if plugins_enabled.get(part) is False:
                is_disabled = True
                break

        if is_disabled:
            continue # Skip this folder and its files
        # -------------------------------------------------------------




        # Filter: Ignore 'plugins', '.' and language codes (e.g. de-DE)
        current_tags = {
            part for part in path_parts
            if part != "plugins" and part != "." and not regex_lang.match(part)
        }
        # -------------------------------------------------------------

        for file in files:
            if file in TARGET_FILES:
                file_path = os.path.join(root, file)
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = regex_example.search(line)
                            if match:
                                content = match.group(1).strip()
                                if content:
                                    total_tags_found += 1

                                    # Initialize if new
                                    if content not in examples:
                                        examples[content] = set()

                                    # Add the tags found in this folder
                                    examples[content].update(current_tags)
                except Exception as e:
                    print(f"logger.info: Warning at {file}: {e}")

    # list of dictionaries
    # Format: [{'text': 'git commit', 'tags': ['git']}, ...]
    result_list = []
    for text in examples.keys():
        tags_list = list(examples[text])[::-1]
        result_list.append({'text': text, 'tags': tags_list})

    print(f"logger.info: Statistics:")
    print(f"  - Files scanned: {file_count}")
    print(f"  - Entries found: {total_tags_found}")
    print(f"  - Unique entries: {len(result_list)} (Duplicates merged)")

    return result_list

# -----------------------------------------------------------------------------
# COPYQ EXPORT
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# COPYQ EXPORT
# -----------------------------------------------------------------------------
def export_to_copyq(items):
    if not items:
        print("logger.info: No examples found.")
        return

    print(f"logger.info: Resetting tab '{COPYQ_TAB_NAME}' ...")
    try:
        subprocess.run(["copyq", "removetab", COPYQ_TAB_NAME], check=False, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    print(f"logger.info: Creating/Switching to Tab '{COPYQ_TAB_NAME}' ...")
    subprocess.run(["copyq", "tab", COPYQ_TAB_NAME], check=True, env=env)

    print("logger.info: Clearing old content ...")
    subprocess.run(["copyq", "eval", f"tab('{COPYQ_TAB_NAME}'); if(size()>0) remove(0, size())"], check=True, env=env)

    print(f"logger.info: Importing {len(items)} examples ...")

    total = len(items)

    # We iterate 1-by-1.
    # We use 'write' which pushes new items to the top (Stack).
    # Since the main block reverses the list (Z->A), writing Z then Y ... results in A at top.

    for i, item in enumerate(items):
        text = item['text']
        tags = item['tags']

        # Build the command: copyq tab NAME write text/plain "DATA" [application/x-copyq-tags "TAGS"]
        cmd = ["copyq", "tab", COPYQ_TAB_NAME, "write", "text/plain", text]

        if tags:
            tag_string = ", ".join(tags)
            cmd.extend(["application/x-copyq-tags", tag_string])

        try:
            subprocess.run(cmd, check=True, env=env)
        except Exception as e:
            print(f"logger.info: Error adding item '{text}': {e}")

        if (i + 1) % 50 == 0:
            print(f"  ... {i + 1} / {total}")

    print("\nlogger.info: Finished! Good luck with the demo.")

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    data = collect_examples()
    # To make it readable A->Z in CopyQ, we insert Z->A (since CopyQ is a stack).
    # We reverse the entire list.
    data.reverse()
    export_to_copyq(data)
