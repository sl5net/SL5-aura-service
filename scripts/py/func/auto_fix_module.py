import os
import re
import ast
import time
import shutil

# from pygments.styles.dracula import comment


def try_auto_fix_module(file_path, exception_obj, logger):
    """
    Versucht, Syntaxfehler in Map-Dateien automatisch zu beheben.

    Trigger: NameError (z.B. durch Einfügen von Text ohne Anführungszeichen).
    Aktion:
      1. Korrigiert fehlende Header (Dateipfad, import re).
      2. Wandelt das unbekannte Wort in ein Tupel ('wort', 'wort'), um.
    """
    if not os.path.exists(file_path):
        logger.info(f"{file_path} not found  -> return False")
        return False


    # FIX: Only allow specific map filenames
    filename = os.path.basename(file_path)
    if filename not in ["PUNCTUATION_MAP.py", "FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
        logger.info(f"{filename} not found  -> return False")
        return False    

    error_msg = str(exception_obj)

    # Prüfen auf NameError: "name 'lauffe' is not defined"
    if isinstance(exception_obj, NameError):
        match = re.search(r"name '(\w+)' is not defined", error_msg)
        if match:
            bad_name = match.group(1)
            logger.info(f"Auto-Fix: NameError für '{bad_name}' erkannt. Repariere Datei...")
            return _apply_fix_name_error(file_path, bad_name, logger)
    else:
        return _apply_fix_name_error(file_path, None, logger)

    logger.info(f"try_auto_fix_module({str(file_path)}, {str(exception_obj)}..) -> return False")
    return False


def _apply_fix_name_error(file_path, bad_name, logger):
    filename = os.path.basename(file_path)
    # if filename not in ["PUNCTUATION_MAP.py", "FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
    #     return False

    logger.info(f"def _apply_fix_name_error( '{filename}' {bad_name} ...")

    # 1. File age check: only fix files modified in the last 10 minutes
    age = time.time() - os.path.getmtime(file_path)
    if age > 600:
        logger.info(f"Auto-fix skipped: {filename} is too old ({int(age)}s).")
        return False

    # 2. Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines(keepends=True)

            # Abort if file contains real Python code
            code_indicators = ['def ', 'class ', 'async def ', 'lambda ']
            for line in lines:
                stripped = line.strip()
                if any(stripped.startswith(kw) for kw in code_indicators):
                    logger.info(f"Auto-fix aborted: {filename} contains Python code ('{stripped[:30]}').")
                    return False

    except Exception as e:
        logger.error(f"Auto-fix: could not read {filename}: {e}")
        return False

    # 3. ast.parse: if already valid Python, don't touch
    try:
        ast.parse(content)
        logger.info(f"Auto-fix skipped: {filename} is already valid Python.")
        return False
    except SyntaxError:
        pass  # proceed with fix

    # 4. Smart ratio: valid tuples vs bare words
    valid_tuples = sum(1 for line in lines if line.strip().startswith("('"))
    bare_words = sum(1 for line in lines if re.match(r"^\s*[\w\u00c0-\u017e][\w\u00c0-\u017e\s\-]*\s*,?\s*$", line))
    if valid_tuples > bare_words * 2:
        logger.info(f"Auto-fix skipped: {filename} looks mostly complete ({valid_tuples} tuples, {bare_words} bare words).")
        return False

    # 5. Backup before fix
    backup_path = file_path + ".auto_fix_backup"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Auto-fix: backup created at {backup_path}")




    # 1. Check file size (1KB = 1024 bytes)
    if os.path.getsize(file_path) > 4096:
        logger.info(f"Auto-fix skipped: {os.path.basename(file_path)} is too large (> 1KB).")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        fixed_content = False

        # --- HEADER BEREINIGUNG & UPDATE START ---

        # 1. Den korrekten, aktuellen Pfad berechnen
        try:
            # Versuche relativen Pfad (sieht schöner aus: config/maps/...)
            clean_path = os.path.relpath(file_path)
        except ValueError:
            clean_path = file_path  # Fallback auf absolut

        correct_header = f"# {clean_path}\n"


        # 2. Existierenden Header prüfen/ersetzen
        if lines and lines[0].strip().startswith("#") and ".py" in lines[0]:
            # Zeile 1 ist schon ein Pfad-Kommentar -> WIR ÜBERSCHREIBEN IHN (Update!)
            lines[0] = correct_header

            # 3. DUPLIKATE LÖSCHEN:
            # Prüfen, ob Zeile 2, 3... auch Pfad-Kommentare sind (dein "Zähne"-Problem)
            # Wir löschen alles, was direkt danach kommt und wie ein Header aussieht.
            while len(lines) > 1 and lines[1].strip().startswith("#") and ".py" in lines[1]:
                logger.info(f"   -> Entferne doppelten Header: {lines[1].strip()}")
                del lines[1]
                fixed_content = True  # Wir haben aufgeräumt -> Speichern nötig
        else:
            # Zeile 1 ist kein Header -> Neuen einfügen
            lines.insert(0, correct_header)
            fixed_content = True

        # 4. Import prüfen (Zeile 2 muss 'import re' sein)
        # Wir schauen in die ersten 5 Zeilen.
        has_import = any("import re" in line for line in lines[:5])
        if not has_import and filename in ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
            # Nach dem Header (Zeile 0) einfügen
            lines.insert(1, "import re # noqa: F401\n")
            fixed_content = True

        # --- HEADER BEREINIGUNG ENDE ---

        # 2. Import re
        has_import = any("import re" in line for line in lines[:5])
        if not has_import and filename in ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
            lines.insert(1, "import re # noqa: F401\n")
            fixed_content = True

        # --- NEU: LISTEN-DEFINITION (FUZZY_MAP = [) ---
        filename = os.path.basename(file_path)
        # target_var = "FUZZY_MAP_pre" if "_pre" in filename else "PUNCTUATION_MAP" if "PUNCTUATION_MAP" in filename else "FUZZY_MAP"
        target_var = "FUZZY_MAP_pre" if "_pre" in filename \
            else "FUZZY_MAP" if "FUZZY_MAP" in filename \
            else "PUNCTUATION_MAP" if "PUNCTUATION_MAP" in filename \
            else ""


        # Prüfen, ob die Variable schon definiert wird

        # has_var_def = "PUNCTUATION_MAP = [" if "PUNCTUATION_MAP" in filename else "]" if "PUNCTUATION_MAP" in filename else ""
        if "PUNCTUATION_MAP" in filename:
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*" + r"\{", line) for line in lines[:270])
        else:
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*\[", line) for line in lines[:270])

        if 'PUNCTUATION_MAP' in filename:
            open_bracket = '{'
        else:
            open_bracket = '['

        if 'PUNCTUATION_MAP' in filename:
            closing_bracket = '}'
        else:
            closing_bracket = ']'


        needs_closing_bracket = False

        if not has_var_def:
            logger.info(f"   -> add Definition: {target_var} = {open_bracket}")
            if 'PUNCTUATION_MAP' in filename:
                comment2add = '# from->too'
            else:
                comment2add = '# too<-from'

            lines.insert(2, f"\n{comment2add}\n{target_var} = {open_bracket}\n")
            fixed_content = True
            needs_closing_bracket = True


        # scripts/py/func/auto_fix_module.py:136
        # --- HAUPTSCHLEIFE (Inhalt fixen) ---
            # scripts/py/func/auto_fix_module.py

        already_closed = False



        inside_list = False
        for line in lines:
            original_line = line
            stripped = line.strip()

            # Track if we are inside the list definition
            if re.search(rf"^\s*{target_var}\s*=\s*[\[\{{]", line):
                inside_list = True
            if stripped == closing_bracket:
                inside_list = False
                new_lines.append(line)
                continue

            # Only fix bare words inside the list
            if not inside_list:
                new_lines.append(line)
                continue

            match = re.search("^\\s*(?P<name>[\\w\u00c0-\u017e][\\w\u00c0-\u017e\\s\\-]*?)\\s*,?\\s*(?P<comment>#.*)?$", line)
            if match and match.group('name').strip() not in [target_var, 'import', 're', 'True', 'False', 'import re', 'noqa']:

                #if match and match.group('name') not in [target_var, 'import', 're', 'True', 'False']:
                current_word = match.group('name')
                indent = line[:len(line) - len(line.lstrip())] or '    '
                comment = ""
                if not already_closed:
                    already_closed = any(line.strip() == closing_bracket for line in new_lines)
                # comment = "  " + match.group('comment') if match.group('comment') else ""
                if already_closed:
                    comment = f"  # TODO: move this line before the {closing_bracket}"

                # seperator = ':' if 'PUNCTUATION_MAP.py' in filename else ','

                if 'PUNCTUATION_MAP.py' in filename:
                    seperator = ':'
                    line = f"{indent}'{current_word}'{seperator} '{current_word}',{comment}\n"
                else:
                    seperator = ','
                    line = f"{indent}('{current_word}'{seperator} r'^{re.escape(current_word)}$'),{comment}\n"

                # line = f"{indent}('{current_word}'{seperator} '{current_word}'),{comment}\n"
                logger.info(f"   -> Bulk-Fix: {original_line.strip()} => {line.strip()}")
                fixed_content = True

            new_lines.append(line)


        # # --- NEU: Einträge nach ] vor ] verschieben ---
        # closing_idx = None
        # for i, l in enumerate(new_lines):
        #     if l.strip() == closing_bracket:
        #         closing_idx = i
        #         break
        # if closing_idx is not None:
        #     after_closing = [l for l in new_lines[closing_idx+1:]
        #                      if l.strip() and not l.strip().startswith('#')]
        #     to_keep = [l for l in new_lines[closing_idx+1:]
        #                if not l.strip() or l.strip().startswith('#')]
        #     if after_closing:
        #         new_lines = (new_lines[:closing_idx]
        #                      + after_closing
        #                      + [new_lines[closing_idx]]
        #                      + to_keep)
        #         fixed_content = True
        # # --- NEU: KLAMMER SCHLIESSEN ] ---


        # Wenn wir oben die Liste geöffnet haben, müssen wir sie unten schließen,
        # sonst gibt es SyntaxError: unexpected EOF

        if needs_closing_bracket:
            # Prüfen, ob die letzte Zeile schon eine Klammer ist
            last_line_clean = new_lines[-1].strip() if new_lines else ""
            if last_line_clean != closing_bracket:
                new_lines.append(f"{closing_bracket}\n")
                logger.info("   -> Füge schließende Klammer ] or ) hinzu.")

        if fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

    except Exception as e:
        logger.error(f"Auto-Fix fehlgeschlagen: {e}")
        return False



def _apply_fix_name_error_backup_202601031751(file_path, bad_name, logger):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        fixed_content = False

        # --- HEADER BEREINIGUNG & UPDATE START ---

        # 1. Den korrekten, aktuellen Pfad berechnen
        try:
            # Versuche relativen Pfad (sieht schöner aus: config/maps/...)
            clean_path = os.path.relpath(file_path)
        except ValueError:
            clean_path = file_path  # Fallback auf absolut

        correct_header = f"# {clean_path}\n"

        # 2. Existierenden Header prüfen/ersetzen
        if lines and lines[0].strip().startswith("#") and ".py" in lines[0]:
            # Zeile 1 ist schon ein Pfad-Kommentar -> WIR ÜBERSCHREIBEN IHN (Update!)
            lines[0] = correct_header

            # 3. DUPLIKATE LÖSCHEN:
            # Prüfen, ob Zeile 2, 3... auch Pfad-Kommentare sind (dein "Zähne"-Problem)
            # Wir löschen alles, was direkt danach kommt und wie ein Header aussieht.
            while len(lines) > 1 and lines[1].strip().startswith("#") and ".py" in lines[1]:
                logger.info(f"   -> Entferne doppelten Header: {lines[1].strip()}")
                del lines[1]
                fixed_content = True  # Wir haben aufgeräumt -> Speichern nötig
        else:
            # Zeile 1 ist kein Header -> Neuen einfügen
            lines.insert(0, correct_header)
            fixed_content = True

        # 4. Import prüfen (Zeile 2 muss 'import re' sein)
        # Wir schauen in die ersten 5 Zeilen.
        has_import = any("import re" in line for line in lines[:5])
        if not has_import:
            # Nach dem Header (Zeile 0) einfügen
            lines.insert(1, "import re # noqa: F401\n")
            fixed_content = True

        # --- HEADER BEREINIGUNG ENDE ---


        # --- HAUPTSCHLEIFE ---
        for line in lines:
            original_line = line

            # Nur bearbeiten, wenn der Fehler-Name in der Zeile steckt
            if re.search(r'\b' + re.escape(bad_name) + r'\b', line):

                # Vorbereitung: Code vom Kommentar trennen & säubern
                stripped = line.strip()
                code_part = stripped.split('#')[0].strip()
                comment = ""
                if "#" in stripped:
                    comment = "  #" + stripped.split('#', 1)[1]

                # Einrückung ermitteln (Default 4 Spaces)
                indent = line[:len(line) - len(line.lstrip())]
                if not indent: indent = '    '

                # --- FALL 1: Das "Einsame Wort" (Singleton) ---
                # Wir entfernen existierende Syntax (, ' " ( ) ), um den Kern zu sehen
                clean_core = code_part.replace(',', '').replace("'", "").replace('"', "").replace('(', "").replace(')',
                                                                                                                   "").strip()

                # Wenn der Kern exakt dem bad_name entspricht, ist es ein Einzelgänger!
                # Beispiel: "lauffe" oder "'lauffe'" oder "lauffe,"
                if clean_core == bad_name:
                    # ZIEL: ('lauffe', 'lauffe'),
                    line = f"{indent}('{bad_name}', '{bad_name}'),{comment}\n"

                    if line != original_line:
                        logger.info(f"   -> Auto-Fix (Singleton->Paar): {stripped} => {line.strip()}")
                        new_lines.append(line)
                        fixed_content = True
                        continue

                # --- FALL 2: Es ist schon ein Paar, aber Syntax fehlt ---
                # Beispiel: lauffe, laufen -> ('lauffe', 'laufen'),

                # A) Quotes hinzufügen (wo sie fehlen)
                pattern = r"(?<!['\"])\b" + re.escape(bad_name) + r"\b(?!['\"])"
                current_text = re.sub(pattern, f"'{bad_name}'", code_part)

                # B) Klammern und Komma erzwingen
                needs_fix = False

                if not current_text.startswith('('):
                    current_text = "(" + current_text
                    needs_fix = True

                if not current_text.endswith(','):
                    current_text += ","
                    needs_fix = True

                if not current_text.endswith('),'):
                    # Wir haben xxx, -> machen xxx), draus
                    current_text = current_text[:-1] + "),"
                    needs_fix = True

                if needs_fix or current_text != code_part:
                    line = f"{indent}{current_text}{comment}\n"
                    logger.info(f"   -> Auto-Fix (Struktur): {stripped} => {line.strip()}")
                    fixed_content = True

            new_lines.append(line)

        if fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

    except Exception as e:
        logger.error(f"Auto-Fix fehlgeschlagen: {e}")
        return False
