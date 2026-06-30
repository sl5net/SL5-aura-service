# tools/test_has_tag_before.py
import re

def run_trace(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    for i, line in enumerate(lines):
        if 'name details' in line and 'Name:' in line:
            print(f"Target line found at index {i}: {line.strip()}")
            has_tag_before = False
            tuple_start_count = 0
            print("Backward scan steps:")
            for k in range(i - 1, -1, -1):
                prev_line = lines[k].strip()
                is_comment = prev_line.startswith('#')
                contains_example = '# EXAMPLE:' in prev_line
                print(f"  k={k}: \"{prev_line}\" | is_comment={is_comment} | contains_example={contains_example}")
                if not prev_line:
                    continue
                if prev_line.startswith("#"):
                    if "# EXAMPLE:" in prev_line or "# TAGS:" in prev_line:
                        has_tag_before = True
                        print("  -> FOUND TAG! Setting has_tag_before = True and breaking.")
                        break
                else:
                    if prev_line.startswith("("):
                        tuple_start_count += 1
                        print(f"  -> tuple_start_count={tuple_start_count}")
                        if tuple_start_count > 1:
                            print("  -> Hit previous rule start. Breaking.")
                            break
                    elif prev_line.endswith("),") or prev_line.endswith("})"):
                        print("  -> Hit previous rule end. Breaking.")
                        break
            print(f"Final has_tag_before result: {has_tag_before}\n")

if __name__ == '__main__':
    run_trace('config/maps/koans_english/12_private_macros_demo12_private_macros_demo/en-US/FUZZY_MAP_pre.py')
