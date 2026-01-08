import os
import re

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

    logger.info(f"try_auto_fix_module({file_path}, {exception_obj}..) -> return False")
    return False


def _apply_fix_name_error(file_path, bad_name, logger):
    filename = os.path.basename(file_path)
    # if filename not in ["PUNCTUATION_MAP.py", "FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
    #     return False

    logger.info(f"def _apply_fix_name_error( '{filename}' {bad_name} ...")

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
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*" + r"\{", line) for line in lines[:10])
        else:
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*\[", line) for line in lines[:10])

        if 'PUNCTUATION_MAP' in filename:
            open_bracket = '{'
        else:
            open_bracket = '{'

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
        for line in lines:
            original_line = line
            # Erkennt Wörter am Zeilenanfang (auch ohne Komma)
            match = re.search(r"^\s*(?P<name>[a-zA-Z_]\w*)\s*,?\s*(?P<comment>#.*)?$", line)

            # Falls ein "nacktes" Wort gefunden wurde (und es nicht die Map-Variable ist)
            if match and match.group('name') not in [target_var, 'import', 're', 'True', 'False']:
                current_word = match.group('name')
                indent = line[:len(line) - len(line.lstrip())] or '    '
                comment = "  " + match.group('comment') if match.group('comment') else ""

                # Fix: In ('word', 'word'), konvertieren

                seperator = ':' if 'PUNCTUATION_MAP.py' in filename else ','

                line = f"{indent}('{current_word}'{seperator} '{current_word}'),{comment}\n"
                logger.info(f"   -> Bulk-Fix: {original_line.strip()} => {line.strip()}")
                fixed_content = True

            new_lines.append(line)


        # --- NEU: KLAMMER SCHLIESSEN ] ---
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
