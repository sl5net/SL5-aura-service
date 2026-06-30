#!/usr/bin/env python3
import os
import re
import sys
import time

# tools/map_tagger.py

# optional:
# .\\.venv\Scripts\python.exe tools\map_tagger.py --yes
# .venv/bin/python tools/map_tagger.py



# -----------------------------------------------------------------------------
# config
# -----------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

MAPS_DIR = os.path.join(PROJECT_ROOT, "config", "maps")
SKIP_ALL_FAILURES = False


TARGET_FILES = ["FUZZY_MAP.py", "FUZZY_MAP_pre.py", 'PUNCTUATION_MAP.py']


try:
    import exrex
    HAS_EXREX = True
except ImportError:
    HAS_EXREX = False
    print("Error: tools/map_tagger.py requires the 'exrex' library.")
    print("Please install it in your virtual environment using:")
    print("source .venv/bin/activate")
    print("pip install exrex")
    print(".venv/bin/python tools/map_tagger.py")
    sys.exit(1)


import argparse

parser = argparse.ArgumentParser(description="Map tagger (non-interactive option)")
parser.add_argument("--yes", "-y", action="store_true", help="Automatically accept suggestions / skip prompts")
args = parser.parse_args()

if args.yes:
    SKIP_ALL_FAILURES = True  # oder separate FLAG_AUTOMATIC = True


# -----------------------------------------------------------------------------
# Smart Sanitizer
# -----------------------------------------------------------------------------
def sanitize_regex_part(text):
    s = text

    s = s.replace(r'\b', '')    # Remove word boundaries to prevent 'b' character leak


    # the order is important
    s = s.replace(r'\d+', '123')
    s = s.replace(r'\d', '1')

    s = s.replace(r'\w*', '')   # Omit \w* entirely
    s = s.replace(r'\w+', 'n')  # Replace \w+ with natural verb ending 'n'
    s = s.replace(r'\w', 'x')   # Keep single \w as 'x'

    s = s.replace(r'\s+', ' ')
    s = s.replace(r'\s*', ' ')
    s = s.replace(r'\s', ' ')

    s = s.replace(r'.+', '.')
    s = s.replace(r'.*', '')

    s = re.sub(r'\?', '', s)

    s = re.sub(r'\[([a-zA-Z0-9üöäÜÖÄß])[^\]]*\]', r'\1', s)
    s = re.sub(r'[^a-zA-Z0-9 äöüÄÖÜß\-_]', ' ', s)

    s = re.sub(r'\{\d*,?\d*\}', '', s)



    s = re.sub(r'\s+', ' ', s).strip()

    return s

def get_smart_suggestion(pattern):
    clean_pat = pattern.strip()
    # if clean_pat.startswith("(") and clean_pat.endswith(")"):
    #     clean_pat = clean_pat[1:-1]

    first_part = clean_pat.split('|')[0]
    sanitized = sanitize_regex_part(first_part)

    if len(sanitized) >= 2:
        return sanitized

    # VERSUCH 2: exrex (Fallback für sehr abstrakte Dinge)
    # if HAS_EXREX:
    #     try:
    #         candidates = list(exrex.generate(pattern, limit=10))
    if HAS_EXREX:
        try:
            exrex_pattern = pattern.replace(r'\b', '').replace('^', '').replace('$', '')
            candidates = list(exrex.generate(exrex_pattern, limit=10))
            if not candidates: return None
            # Nimm das Kürzeste
            candidates.sort(key=lambda s: (len(s), s))
            return candidates[0]
        except:
            return None

    return None

# -----------------------------------------------------------------------------
def has_tag_before_anchor(lines, i):
    """Scans backward to find if an EXAMPLE or TAGS comment already exists for the current rule."""
    tuple_start_count = 0
    for k in range(i - 1, -1, -1):
        prev_line = lines[k].strip()
        if not prev_line:
            continue
        if prev_line.startswith("#"):
            if "# EXAMPLE:" in prev_line or "# TAGS:" in prev_line:
                return True
        else:
            if prev_line.startswith("("):
                tuple_start_count += 1
                if tuple_start_count > 1:
                    break  # Boundary to previous rule reached
            elif prev_line.endswith("),") or prev_line.endswith("})"):
                break  # Boundary to previous rule reached
    return False
# -----------------------------------------------------------------------------
def process_file(filepath):
    global SKIP_ALL_FAILURES

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()



    modified = False
    shift_offset = 0

    # 1. Ensure File Header (Relative Path)
    rel_path = os.path.relpath(filepath, PROJECT_ROOT)
    expected_header = f"# {rel_path}\n"

    if not lines or not lines[0].startswith("# config/maps/"):
        lines.insert(0, expected_header)
        modified = True
        print(f"Header added to: {rel_path}")
    elif lines[0] != expected_header:
        lines[0] = expected_header
        modified = True
        print(f"Header updated in: {rel_path}")

    new_lines = []

    # PATTERN = r"..."
    # regex_finder = re.compile(r'=\s*r["\']([\^"\']+)["\']')
    regex_finder = re.compile(r'[:=,\(\s]\s*(?:fr|rf|r)(?P<q>"{3}|\'{3}|"|\')(?P<p>.*?)(?P=q)', re.DOTALL)

    # Dictionary-Keys: 'key':
    dict_finder = re.compile(r"^\s*(?P<q>['\"])(?P<p>[^'\"]+)(?P=q)\s*:")



    for i, line in enumerate(lines):
        time.sleep(.005)

        # Skip lines with no indentation (e.g., global variables or list definitions)
        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            new_lines.append(line)
            continue

        # match = regex_finder.search(line)
        matches = list(regex_finder.finditer(line))
        match = matches[-1] if matches else None

        # has_tag_before = (i > 0) and ("# EXAMPLE:" in lines[i-1] or "# TAGS:" in lines[i-1])
        has_tag_before = has_tag_before_anchor(lines, i)
        # print(f'DEBUG has_tag_before: {has_tag_before}')

        if not match and "PUNCTUATION_MAP.py" in filepath:
            match = dict_finder.search(line)

            # print(f"2026-0108-1436: {filepath} : {i}")
            # sys.exit(1)


        if match and not has_tag_before:
            found_pattern = match.group('p').strip()
            # print(f'tools/map_tagger.py:164 found_pattern={found_pattern}')


            # --- NEU: Strukturelle Prüfung auf Regel-Tupel (Klammer-Prüfung) ---
            anchor_idx = i
            for j in range(i - 1, -1, -1):
                prev = lines[j].strip()
                if not prev or prev.startswith('#'):
                    continue
                anchor_idx = j
                break

            anchor_is_tuple_start = lines[anchor_idx].lstrip().startswith('(')
            current_is_tuple_start = line.lstrip().startswith('(')

            # Skip if neither the current line nor the anchor line starts with '(' (not a rule tuple)
            if not anchor_is_tuple_start and not current_is_tuple_start:
                new_lines.append(line)
                continue
            # -------------------------------------------------------------------










            if not found_pattern:
                new_lines.append(line)


            # Skip lines that are purely comments or empty
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                new_lines.append(line)
                continue

            # get Smart Suggestion
            suggestion = str(get_smart_suggestion(found_pattern)).strip()
            # suggestion = validate_and_cleanup_example(suggestion,  , )
            suggestion = validate_and_cleanup_example(suggestion, found_pattern, f"{filepath}:{i+1}")

            if not suggestion:
                new_lines.append(line)
                continue

            success = (suggestion is not None and suggestion != 'None')
            display_suggestion = suggestion if success else "(no Suggestion)"

            if not success and SKIP_ALL_FAILURES:
                new_lines.append(line)
                continue

            # remove PROJECT_ROOT from filepath in print
            if filepath.startswith(PROJECT_ROOT):
                filepath_short = filepath[len(PROJECT_ROOT):].lstrip("/")  # remove leading slash if present
            else:
                filepath_short = filepath

            print(f"\n_________________\n{filepath_short}:{i+1}")
            # print(f"Pattern:   {found_pattern}")
            if not found_pattern:
                print(f'line: {line.strip()}')
                continue

            color_code = "\033[92m" if success else ""
            reset_code = "\033[0m" if success else ""
            print(f'line: {line.strip()}')
            print(f"Pattern:   {found_pattern}")
            print(f"Suggestion: {color_code}'{display_suggestion}'{reset_code}")

            prompt_parts = ["ENTER (nehmen)", "Text (eigenes)", "'s' (skip)", "'q' (quit)"]
            if not success: prompt_parts.append("'sa' (skip failures)")

            if args.yes:
                if success:
                    final_example = suggestion
                else:
                    new_lines.append(line)
                    continue
            else:
                print(f"[{' | '.join(prompt_parts)}]")
                user_input = input("> ").strip()

                if user_input.lower() == 'q':
                    print("Beendet.")
                    sys.exit(0)
                if user_input.lower() == 'sa':
                    SKIP_ALL_FAILURES = True
                    new_lines.append(line)
                    continue
                if user_input.lower() == 's':
                    new_lines.append(line)
                    continue

                final_example = ""
                if user_input:
                    final_example = user_input
                elif success:
                    final_example = suggestion
                else:
                    new_lines.append(line)
                    continue

                if final_example:
                    final_example = validate_and_cleanup_example(final_example, found_pattern, f"{filepath}:{i+1}")

            # anchor_idx = i
            # for j in range(i - 1, -1, -1):
            #     prev = lines[j].strip()
            #     if not prev or prev.startswith('#'):
            #         continue
            #     anchor_idx = j
            #     break

            insert_at_idx = i
            if not lines[i].lstrip().startswith('('):
                # Only search backwards for the tuple start if current line is not the start
                for j in range(i - 1, -1, -1):
                    prev = lines[j].strip()
                    if not prev or prev.startswith('#'):
                        continue
                    if prev.startswith('('):
                        insert_at_idx = j
                    break

            # anchor_is_tuple_start = lines[anchor_idx].lstrip().startswith('(')
            # insert_at_idx = anchor_idx if anchor_is_tuple_start else i


            has_tag_before = has_tag_before_anchor(lines, i)
            # print(f'DEBUG has_tag_before: {has_tag_before}')

            if has_tag_before:
                new_lines.append(line)
                continue


            indent = lines[insert_at_idx][:len(lines[insert_at_idx]) - len(lines[insert_at_idx].lstrip())]
            example_line = f"{indent}# EXAMPLE: {final_example}\n"

            # if insert_at_idx <= len(new_lines):
            #     new_lines.insert(insert_at_idx, example_line)
            # else:
            #     # Fallback:
            #     new_lines.append(example_line)

            insert_pos = insert_at_idx + shift_offset
            if insert_pos <= len(new_lines):
                new_lines.insert(insert_pos, example_line)
                shift_offset += 1
            else:
                new_lines.append(example_line)
                shift_offset += 1


            new_lines.append(line)
            modified = True
            print("-> Gespeichert.")

        else:
            new_lines.append(line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def validate_and_cleanup_example(example, regex_str, file_info):
    try:
        clean_regex = re.sub(r"\{[^}]+\}", r".*", regex_str)
        compiled_rx = re.compile(clean_regex, re.IGNORECASE)
    except Exception as e:
        print(f"Warning: Invalid regex '{regex_str}' in {file_info}: {e}")
        return example

    if compiled_rx.search(example):
        return example

    words = example.split()
    cleaned_words = [w for w in words if len(w) > 1 or w.lower() in ['a', 'i']]
    simplified = " ".join(cleaned_words)

    if simplified != example and compiled_rx.search(simplified):
        print(f"-> Automatically simplified example to: '{simplified}'")
        return simplified

    print(f"-> WARNING: Example '{example}' still does not match regex '{regex_str}' in {file_info} after cleanup!")
    return example

def main():
    if not os.path.isdir(MAPS_DIR):
        print(f"Fehler: '{MAPS_DIR}' nothing found.")
        sys.exit(1)

    print(f"Scanne {MAPS_DIR} ...")
    for root, dirs, files in os.walk(MAPS_DIR):
        time.sleep(.005)
        for file in files:

            if file not in TARGET_FILES:
                continue


            time.sleep(.005)
            if file.endswith(".py"):
                process_file(os.path.join(root, file))
    print("\n finished / Fertig.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # fallback for cases where KeyboardInterrupt is delivered
        print("\nInterrupted (KeyboardInterrupt). Exiting.")
        sys.exit(0)
