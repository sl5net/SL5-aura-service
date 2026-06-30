import subprocess
import sys

TARGET = "config/maps/koans_deutsch/12_private_macros_demo/de-DE/FUZZY_MAP_pre.py"

def test_file():
    with open(TARGET, "r", encoding="utf-8") as f:
        content = f.read()
    lines = [l.strip() for l in content.splitlines() if l.strip()]

    # Unit Test 1: Check for consecutive non-comment duplicates
    for i in range(len(lines) - 1):
        if lines[i] == lines[i+1] and not lines[i].startswith("#"):
            raise AssertionError(f"Unit Test Failed: Duplicate found -> {lines[i]}")

    # Unit Test 2: Check if EXAMPLE tags are generated
    assert "# EXAMPLE:" in content, "Unit Test Failed: No # EXAMPLE: tags found"
    print("All Unit Tests Passed successfully.")

def main():
    print("Step 1: Cleaning examples...")
    subprocess.run([sys.executable, "tools/clean_examples.py", TARGET], check=True)

    print("Step 2: Running map_tagger...")
    subprocess.run([".venv/bin/python", "tools/map_tagger.py", "--yes", TARGET], check=True)

    print("Step 3: Running Unit Tests...")
    test_file()

if __name__ == "__main__":
    main()
