#!/usr/bin/env python3
import os
import re
import subprocess
import time

# scripts/py/func/checks/check_settings_usage.py:7

# --- Configuration ---
SETTINGS_FILE = "config/settings.py"
# The base grep command you provided

# settings\.([a-zA-Z0-9_]+)(?!\s*\()

GREP_COMMAND = (
    'grep -rnP "\\bsettings\\.([a-zA-Z0-9_]+)(?!\\s*\\()\\b" --include="*.py" . '
    '| grep -v ".venv" | grep -v "venv" | grep -v "__pycache__" | grep -v "/_" | grep -v "/docs" | grep -v "/doc_sources"'
)

def get_defined_settings():
    """
    Parses config/settings.py to find all defined variables.
    Matches lines like: MY_VARIABLE = "value"
    """
    defined_vars = set()
    if not os.path.exists(SETTINGS_FILE):
        print(f"⚠️  Critical Error: {SETTINGS_FILE} not found!")
        return defined_vars

    # Regex to find variable names at the start of a line followed by '='
    pattern = re.compile(r'^([a-zA-Z0-9_]+)\s*=')

    with open(SETTINGS_FILE, "r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                defined_vars.add(match.group(1))

    return defined_vars

def analyze_usages(defined_vars):
    start_time = time.time()
    """
    Runs the grep command to find 'settings . variable' in source code
    and compares them against the defined list.
    """
    print("🔍 Analyzing source code for 'settings.' usages...")

    try:
        # Run the shell command
        result = subprocess.run(GREP_COMMAND, shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
    except Exception as e:
        print(f"❌ Error running grep: {e}")
        return

    # Regex to extract the variable name after 'settings.'
    # Matches 'settings.my_var' -> extracts 'my_var'
    usage_pattern = re.compile(r'settings\.([a-zA-Z0-9_]+)')

    missing_count = 0
    found_count = 0

    for line in lines:


        # Grep output format is usually: filename:line_number:text
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue

        filename = parts[0]
        line_num = parts[1]
        content  = parts[2]

        if re.match(r'^\s*#', content) or content.lstrip().startswith('#'):
            continue


        matches = usage_pattern.findall(content)
        for var_name in matches:
            found_count += 1
            if var_name not in defined_vars and var_name != "py":
                missing_count += 1
                print(f"\n🚨  UNDEFINED SETTING DETECTED! {var_name}")
                print(f"    👉 Variable: 'settings.{var_name}'")
                print(f"    {filename}:{line_num}")
                print(f"    💡 Fix: Add '{var_name} = ...' to {SETTINGS_FILE}")
                print(f"\ncontent=\n{content}")


    end_time = time.time()
    duration = end_time - start_time

    #print("\n" + "="*40)
    if missing_count == 0:
        print(f"✅ Analysis complete. All {found_count} settings found in config. ⏱️duration: {duration:.3f}s")
    else:
        print(f"❌ Finished with {missing_count} errors! Please check the list above. ⏱️duration: {duration:.3f}s")
    #print("="*40)

def check_settings_usage():

    # 1. Get definitions
    definitions = get_defined_settings()

    # 2. Check usages
    if definitions:
        analyze_usages(definitions)
    else:
        print("🛑 Could not extract settings from config. Aborting.")




if __name__ == "__main__":
    check_settings_usage()

    # 1. Get definitions
    # definitions = get_defined_settings()

    # 2. Check usages
    # if definitions:
    #     analyze_usages(definitions)
    # else:
    #     print("🛑 Could not extract settings from config. Aborting.")


