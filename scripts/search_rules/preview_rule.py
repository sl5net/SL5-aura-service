#!/usr/bin/env python3
# scripts/search_rules/preview_rule.py
import sys
import os
import sqlite3

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

    # 2. Den Code-Kontext als Textblock für das Text-Matching einlesen
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
        # Datenbank im Read-Only-Modus öffnen, um Locks zu vermeiden
        db_uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(db_uri, uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Alle Einträge für diese Map-Datei abfragen
        cursor.execute(
            "SELECT rule_output, final_result, validity_value, cache_id FROM aura_result_cache WHERE map_path LIKE ?",
            (search_path,)
        )
        rows = cursor.fetchall()

        matched_rows = []
        for row in rows:
            rule_output = row['rule_output']
            final_result = row['final_result']

            # Wenn die Ausgabe der Regel im Code vorkommt, haben wir ein Match!
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
            # Falls kein direkter Treffer im Code, schauen wir, ob wir das # EXAMPLE: als Trigger nutzen können
            example = extract_example(file_path, line_num)
            if example:
                print(f"{COLOR_YELLOW}No cached execution found in code context for trigger: '{example}'{COLOR_RESET}")
            else:
                print(f"{COLOR_YELLOW}No cached output matches this code context.{COLOR_RESET}")

        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: preview_rule.py [--extract] <file_path> <line_num>")
        sys.exit(1)

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

    print_code_context(file_path, line_num)
    print_smart_cache_preview(file_path, line_num, project_root)

if __name__ == '__main__':
    main()
