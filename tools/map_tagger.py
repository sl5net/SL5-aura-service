#!/usr/bin/env python3
import os
import re
import sys
import time

# tools/map_tagger.py:7

# -----------------------------------------------------------------------------
# KONFIGURATION
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

# -----------------------------------------------------------------------------
# LOGIK: Smart Sanitizer
# -----------------------------------------------------------------------------
def sanitize_regex_part(text):
    """
    Verwandelt einen Regex-Schnipsel in lesbaren Text.
    Ersetzt abstrakte Muster durch konkrete Platzhalter.
    # """
    s = text

    # 1. Bekannte Regex-Klassen durch lesbare Beispiele ersetzen
    # Reihenfolge ist wichtig!
    s = s.replace(r'\d+', '123')
    s = s.replace(r'\d', '1')

    s = s.replace(r'\w+', 'text')
    s = s.replace(r'\w', 'x')

    s = s.replace(r'\s+', ' ')
    s = s.replace(r'\s*', ' ')
    s = s.replace(r'\w*', ' ')

    s = s.replace(r'.+', '.')
    s = s.replace(r'.*', '')

    # 2. Übrige Regex-Syntax entfernen (Klammern, Sonderzeichen)
    # Wir behalten nur Buchstaben, Zahlen, Umlaute, Bindestriche und Leerzeichen.
    s = re.sub(r'[^a-zA-Z0-9 äöüÄÖÜß\-_]', ' ', s)

    # 3. Doppelte Leerzeichen entfernen und trimmen
    s = re.sub(r'\s+', ' ', s).strip()

    return s

def get_smart_suggestion(pattern):
    """
    Versucht, das beste Beispiel zu finden.
    Priorität:
    1. Der erste Teil des Patterns (vor der Pipe |), bereinigt um Regex-Syntax.
    2. Fallback auf exrex, falls das Ergebnis leer ist.
    """

    # Äußere Klammern entfernen: (A|B) -> A|B
    clean_pat = pattern.strip()
    if clean_pat.startswith("(") and clean_pat.endswith(")"):
        clean_pat = clean_pat[1:-1]

    # Am ersten Pipe splitten
    # (Dies ist robust genug für deine Wortlisten)
    first_part = clean_pat.split('|')[0]

    # VERSUCH 1: Den ersten Teil lesbar machen (Deine Idee + Platzhalter)
    sanitized = sanitize_regex_part(first_part)

    # Wenn dabei was Sinnvolles rauskommt (mindestens 2 Zeichen), nehmen wir das!
    if len(sanitized) >= 2:
        return sanitized

    # VERSUCH 2: exrex (Fallback für sehr abstrakte Dinge)
    if HAS_EXREX:
        try:
            candidates = list(exrex.generate(pattern, limit=10))
            if not candidates: return None
            # Nimm das Kürzeste
            candidates.sort(key=lambda s: (len(s), s))
            return candidates[0]
        except:
            return None

    return None

# -----------------------------------------------------------------------------
# HAUPTPROGRAMM
# -----------------------------------------------------------------------------
def process_file(filepath):
    global SKIP_ALL_FAILURES

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()



    modified = False

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



    # Findet: PATTERN = r"..."
    # regex_finder = re.compile(r'=\s*r["\']([\^"\']+)["\']')
    regex_finder = re.compile(r'[:=,\(\s]\s*(?:fr|rf|r)(?P<q>"{3}|\'{3}|"|\')(?P<p>.*?)(?P=q)', re.DOTALL)

    # Findet Dictionary-Keys: 'key':
    dict_finder = re.compile(r"^\s*(?P<q>['\"])(?P<p>[^'\"]+)(?P=q)\s*:")



    for i, line in enumerate(lines):
        time.sleep(.005)
        match = regex_finder.search(line)

        # Prüfen, ob Tag/Example davor existiert
        has_tag_before = (i > 0) and ("# EXAMPLE:" in lines[i-1] or "# TAGS:" in lines[i-1])

        if not match and "PUNCTUATION_MAP.py" in filepath:
            match = dict_finder.search(line)

            # print(f"2026-0108-1436: {filepath} : {i}")
            # sys.exit(1)

        if match and not has_tag_before:
            # found_pattern = match.group(1)
            found_pattern = match.group('p').strip()


            if not found_pattern:
                new_lines.append(line)
                continue

            # Skip lines that are purely comments or empty
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                new_lines.append(line)
                continue

            # Smart Suggestion holen
            suggestion = str(get_smart_suggestion(found_pattern)).strip()
            if not suggestion:
                new_lines.append(line)
                continue


            success = suggestion is not None
            display_suggestion = suggestion if success else "(Kein Vorschlag)"

            if not success and SKIP_ALL_FAILURES:
                new_lines.append(line)
                continue

            # print(f"\n--- {os.path.basename(filepath)} | Zeile {i+1} ---")
            print(f"\n--- {filepath} | Zeile {i+1} ---")
            print(f"Pattern:   {found_pattern}")

            # Ausgabe Farbe für Vorschlag
            color_code = "\033[92m" if success else "" # Grün
            reset_code = "\033[0m" if success else ""
            print(f"Vorschlag: {color_code}'{display_suggestion}'{reset_code}")

            prompt_parts = ["ENTER (nehmen)", "Text (eigenes)", "'s' (skip)", "'q' (quit)"]
            if not success: prompt_parts.append("'sa' (skip failures)")

            print(f"[{' | '.join(prompt_parts)}]")
            user_input = input("> ").strip()

            # --- Input Logic ---
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

            # Schreiben
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}# EXAMPLE: {final_example}\n")
            new_lines.append(line)
            modified = True
            print("-> Gespeichert.")

        else:
            new_lines.append(line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    if not os.path.isdir(MAPS_DIR):
        print(f"Fehler: '{MAPS_DIR}' nicht gefunden.")
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
    main()
