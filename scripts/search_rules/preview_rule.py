#!/usr/bin/env python3
# scripts/search_rules/preview_rule.py
import sys
import os
import sqlite3

import re

def extract_pattern(file_path, line_num):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        start_idx = min(line_num - 1, len(lines) - 1)
        end_idx = min(len(lines), start_idx + 6)
        block = "".join(lines[start_idx:end_idx])
        match = re.search(r"r(['\"])(.*?)\1", block)
        if match:
            return match.group(2)
    except Exception:
        pass
    return None

def supports_color():
    return sys.stdout.isatty()

COLOR_BLUE = "\033[1;34m" if supports_color() else ""
COLOR_GREEN = "\033[1;32m" if supports_color() else ""
COLOR_YELLOW = "\033[1;33m" if supports_color() else ""
COLOR_PURPLE = "\033[1;35m" if supports_color() else ""
COLOR_RED = "\033[1;31m" if supports_color() else ""
COLOR_BOLD = "\033[1m" if supports_color() else ""
COLOR_RESET = "\033[0m" if supports_color() else ""

def extract_example(file_path, line_num):
    """Sucht ab der Zeile line_num rückwärts nach dem nächsten '# EXAMPLE:'."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        start_idx = min(line_num - 1, len(lines) - 1)
        for i in range(start_idx, max(-1, start_idx - 6), -1):
            line = lines[i].strip()
            if '# EXAMPLE:' in line:
                return line.split('# EXAMPLE:', 1)[1].strip()
    except Exception:
        pass
    return None

def print_code_context(file_path, line_num):
    """Gibt den Code-Kontext rund um die gefundene Zeile aus."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        start = max(1, line_num - 4)
        end = min(len(lines), line_num + 4)

        print(f"{COLOR_BLUE}=== CODE CONTEXT ==={COLOR_RESET}")
        for nr in range(start, end + 1):
            line = lines[nr - 1].rstrip('\r\n')
            prefix = f"{COLOR_GREEN}>{COLOR_RESET}" if nr == line_num else " "
            print(f"{prefix}{nr:4d}: {line}")
        print()
    except Exception as e:
        print(f"Error reading file: {e}")

def print_smart_cache_preview(file_path, line_num, project_root):
    """Sucht intelligent nach passenden Cache-Einträgen für diese Code-Zeile."""
    abs_file_path = os.path.abspath(file_path)

    # 1. Relativen Map-Pfad für das SQL-Wildcard-Matching ermitteln
    if 'config/maps/' in abs_file_path:
        rel_path = abs_file_path.split('config/maps/', 1)[1]
        search_path = f"%config/maps/{rel_path}"
    else:
        search_path = f"%{os.path.basename(file_path)}"

    context_text = ""
    try:
        with open(abs_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        # Zeilen rund um den Cursor zusammenführen
        start_idx = max(0, line_num - 4)
        end_idx = min(len(lines), line_num + 3)
        context_text = "".join(lines[start_idx:end_idx])
    except Exception:
        pass

    db_path = os.path.join(project_root, 'data', '_aura_result_cache.db')
    if not os.path.exists(db_path) or not context_text:
        return

    try:
        db_uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(db_uri, uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT rule_output, final_result, validity_value, cache_id FROM aura_result_cache WHERE map_path LIKE ?",
            (search_path,)
        )
        rows = cursor.fetchall()

        matched_rows = []
        for row in rows:
            rule_output = row['rule_output']
            final_result = row['final_result']

            if rule_output and rule_output.strip() and rule_output.strip() in context_text:
                matched_rows.append(row)
            elif final_result and final_result.strip() and final_result.strip() in context_text:
                matched_rows.append(row)

        if matched_rows:
            print(f"{COLOR_PURPLE}=== SQLITE CACHE PREVIEW ==={COLOR_RESET}")
            for row in matched_rows:
                print(f"{COLOR_GREEN}Rule Output:{COLOR_RESET}     {row['rule_output']}")
                print(f"{COLOR_GREEN}Final Result:{COLOR_RESET}    {row['final_result']}")
                if row['validity_value'] and row['validity_value'] != '0':
                    print(f"{COLOR_YELLOW}Validity:{COLOR_RESET}        {row['validity_value']}")
                print(f"{COLOR_BLUE}Cache ID:{COLOR_RESET}        {row['cache_id']}")
                print("-" * 30)
        else:
            example = extract_example(file_path, line_num)
            if example:
                pattern = extract_pattern(file_path, line_num)
                if pattern and not re.search(pattern, example, re.IGNORECASE):
                    print(f"{COLOR_RED}⚠ EXAMPLE '{example}' not match Regex{COLOR_RESET}")
                print(f"{COLOR_YELLOW}No cached execution found in code context for trigger: '{example}'{COLOR_RESET}")
            else:
                print(f"{COLOR_YELLOW}No cached output matches this code context.{COLOR_RESET}")
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def get_gitignore_status():
    """Reads gitignore state from file and returns ON or OFF."""
    state_file = os.path.join(os.path.expanduser("~"), ".search_rules_respect_gitignore")
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return "ON" if f.read().strip() == "1" else "OFF"
    except Exception:
        return "OFF"


def get_one_per_file_status():
    """Reads one-per-file state from file and returns ON or OFF."""
    state_file = os.path.join(os.path.expanduser("~"), ".search_rules_one_per_file")
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return "ON" if f.read().strip() == "1" else "OFF"
    except Exception:
        return "OFF"

def get_ditto_status():
    """Reads ditto state from file and returns ON or OFF."""
    state_file = os.path.join(os.path.expanduser("~"), ".search_rules_ditto")
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return "ON" if f.read().strip() == "1" else "OFF"
    except Exception:
        return "OFF"

def get_single_gui_status():
    """Reads single gui state from file and returns ON or OFF."""
    state_file = os.path.join(os.path.expanduser("~"), ".search_rules_single_gui")
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return "ON" if f.read().strip() == "1" else "OFF"
    except Exception:
        return "ON"

def print_window_active_status(file_path, line_num):
    """Prints text status indicators showing whether rule matches AURA_ACTIVE_WINDOW_TITLE."""
    active_win = os.getenv("AURA_ACTIVE_WINDOW_TITLE", "").strip()
    if not active_win:
        return

    # legend_state_file = os.path.join(os.path.expanduser("~"), ".search_rules_legend_state")
    # try:
    #     with open(legend_state_file, "r", encoding="utf-8") as f:
    #         legend_on = f.read().strip() != "off"
    # except Exception:
    #     legend_on = True
    # if legend_on:
    #     print(f"📜 ⏵ ⬟…{get_proot_display()} 🗺️map 🧩plugin |※.punct ⚙️pre 📄post| 〃same")

    legend_state_file = os.path.join(os.path.expanduser("~"), ".search_rules_legend_state")
    try:
        with open(legend_state_file, "r", encoding="utf-8") as f:
            legend_on = f.read().strip() != "off"
    except Exception:
        legend_on = True

    if legend_on:
        gitignore_st = get_gitignore_status()
        one_pf_st = get_one_per_file_status()
        ditto_st = get_ditto_status()
        single_gui_st = get_single_gui_status()
        # ﹘ "﹘" else "͹≣"
        # ﹘
        icon_f = "﹘" if one_pf_st == "ON" else "≣"
        icon_i = "🔐" if gitignore_st == "ON" else "🔓Ո"
        icon_g = "〃" if ditto_st == "ON" else "⬟"
        icon_u = "🎯" if single_gui_st == "ON" else "⁘"
        print("⬟: AuraRoot | 🗺️: Maps | 🧩: Plugin")
        print(f"🗺️ .../{get_proot_display()}")
        print("📜 ※.punct ⚙️pre 📄post| 〃same")
        print(f"📜 F1:📜 Alt+G:{icon_g} Alt+F:{icon_f} Alt+I:{icon_i} Alt+U:{icon_u}")
        print("📜 Alt+R:ResetPROOT 2xClick:SetPROOT RClick:Up")
        print("Ctrl+E:Edit | Ctrl+R:RunPrompt | Ctrl+G:GitHub | Ctrl+Z/Y:History")
    else:
        print("F1: show 📜 Legend")
    # print("⬟:proot 📄:map 🧩:plugin ※:punct ⚙️:pre 📄:post 〃:same")
    print(f"=== 🔵 [{active_win}] ===")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if "only_in_windows" in content:
            win_clean = active_win.lower()
            if any(w in content.lower() for w in ["0ad", "0 a.d.", win_clean]):
                print(">>> STATUS: MATCHES ACTIVE WINDOW <<<")
            else:
                print(">>> STATUS: WINDOW MISMATCH <<<")
        else:
            print(">>> STATUS: GLOBAL RULE (All windows) <<<")
        print()
    except Exception as e:
        print(f"Window status error: {e}")

def print_file_header(file_path):
    """Prints the last 68 characters of the file path in the preview header."""
    clean_path = str(file_path).replace("\\", "/")
    if len(clean_path) > 68:
        display_path = "…" + clean_path[-45:]
    else:
        display_path = clean_path


    icon_symbol_dict = {
        "PUNCTUATION_MAP.py": "※",
        "FUZZY_MAP_pre.py" : "⚙️",
        "FUZZY_MAP.py": "📄",
    }
    icon_symbol = next(
        (symbol for name, symbol in icon_symbol_dict.items() if name in clean_path),
        "🔴"  # default fallback
    )
    if "/_" in clean_path:
        icon_symbol += "🔐"

    print(f"{icon_symbol} {display_path}] {icon_symbol}")


def save_last_selected_path(file_path):
    """Saves the highlighted map file path for fzf scoped reload state."""
    try:
        state_file = os.path.join(os.path.expanduser("~"), ".search_rules_last_path")
        with open(state_file, "w", encoding="utf-8") as f:
            f.write(os.path.abspath(file_path))
    except Exception:
        pass


def get_proot_display():
    """Reads current PROOT-State and returns it shortened for display."""
    project_root = os.environ.get('SL5NET_AURA_PROJECT_ROOT', '')
    try:
        state_file = os.path.join(os.path.expanduser("~"), ".search_rules_proot")
        with open(state_file, "r", encoding="utf-8") as f:
            proot_path = f.read().strip()
        base = os.path.join(project_root, "config", "maps")
        proot_path_abs = os.path.normpath(os.path.abspath(os.path.expanduser(proot_path)))
        base_abs = os.path.normpath(os.path.abspath(base))
        proj_abs = os.path.normpath(os.path.abspath(project_root))

        if proot_path_abs == base_abs:
            return "config/maps"

        try:
            rel_base = os.path.relpath(proot_path_abs, base_abs)
            if not rel_base.startswith(os.pardir):
                return f"config/maps/{rel_base}"
        except Exception:
            pass

        try:
            rel_proj = os.path.relpath(proot_path_abs, proj_abs)
            if not rel_proj.startswith(os.pardir):
                return rel_proj
        except Exception:
            pass

        return proot_path
    except Exception:
        return ""

    

def main():
    if len(sys.argv) < 3:
        print("Usage: preview_rule.py [--extract] <file_path> <line_num>")
        sys.exit(1)

    save_last_selected_path(sys.argv[1])

    if sys.argv[1] == '--extract':
        file_path = sys.argv[2]
        line_num = int(sys.argv[3])
        example = extract_example(file_path, line_num)
        if example:
            print(example)
        sys.exit(0)

    file_path = sys.argv[1]
    line_num = int(sys.argv[2])

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))

    print_file_header(file_path)
    print_window_active_status(file_path, line_num)
    print_code_context(file_path, line_num)
    print_smart_cache_preview(file_path, line_num, project_root)

if __name__ == '__main__':
    main()

