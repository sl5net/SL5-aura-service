import os
import re
import ast
import time
import shutil

def try_auto_fix_module(file_path, exception_obj, logger):
    """
    Tries to auto-fix syntax errors in map files.
    Trigger: NameError (e.g. by inserting text without quotes).
    Action:
      1. Fixes missing header (file path, import re).
      2. Converts unknown word into a tuple ('word', 'word').
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
    # Check for NameError: "name 'lauffe' is not defined"
    if isinstance(exception_obj, NameError):
        match = re.search(r"name '(\w+)' is not defined", error_msg)
        if match:
            bad_name = match.group(1)
            logger.info(f"Auto-Fix: NameError for '{bad_name}' detected. Repairing file...")
            return _apply_fix_name_error(file_path, bad_name, logger)
    else:
        return _apply_fix_name_error(file_path, None, logger)
    logger.info(f"try_auto_fix_module({str(file_path)}, {str(exception_obj)}..) -> return False")
    return False


def _apply_fix_name_error(file_path, bad_name, logger):
    filename = os.path.basename(file_path)
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

    # 3. Check if list definition exists
    target_var_check = "FUZZY_MAP_pre" if "_pre" in filename \
        else "FUZZY_MAP" if "FUZZY_MAP" in filename \
        else "PUNCTUATION_MAP" if "PUNCTUATION_MAP" in filename \
        else ""
    if "PUNCTUATION_MAP" in filename:
        has_var_def_check = any(re.search(rf"^\s*{target_var_check}\s*=\s*\{{", line) for line in lines)
    else:
        has_var_def_check = any(re.search(rf"^\s*{target_var_check}\s*=\s*\[", line) for line in lines)

    # 4. Check for bare words (anywhere in file, including after ])
    _bare_re = re.compile(r"^\s*[\w][\w\s-]*\s*,?\s*$")
    _skip = {target_var_check, "import", "re", "True", "False", "import re", "noqa"}
    bare_words = sum(1 for line in lines if _bare_re.match(line) and line.strip() not in _skip)

    # 5. ast.parse: only skip if structure is complete AND no bare words
    try:
        ast.parse(content)
        if has_var_def_check and bare_words == 0:
            logger.info(f"Auto-fix skipped: {filename} is complete and valid.")
            return False
        # valid Python but missing structure or has bare words -> proceed
    except SyntaxError:
        pass  # proceed with fix

    # 5. File size check (4KB limit)
    if os.path.getsize(file_path) > 4096:
        logger.info(f"Auto-fix skipped: {os.path.basename(file_path)} is too large (> 4KB).")
        return False

    # 6. Backup before fix
    backup_path = file_path + ".auto_fix_backup"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Auto-fix: backup created at {backup_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        fixed_content = False

        # --- HEADER CLEANUP START ---
        try:
            clean_path = os.path.relpath(file_path)
        except ValueError:
            clean_path = file_path

        correct_header = f"# {clean_path}\n"

        if lines and lines[0].strip().startswith("#") and ".py" in lines[0]:
            lines[0] = correct_header
            while len(lines) > 1 and lines[1].strip().startswith("#") and ".py" in lines[1]:
                logger.info(f"   -> Remove duplicate header: {lines[1].strip()}")
                del lines[1]
                fixed_content = True
        else:
            lines.insert(0, correct_header)
            fixed_content = True

        has_import = any("import re" in line for line in lines[:5])
        if not has_import and filename in ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]:
            lines.insert(1, "import re # noqa: F401\n")
            fixed_content = True
        # --- HEADER CLEANUP END ---

        # --- LIST DEFINITION ---
        target_var = "FUZZY_MAP_pre" if "_pre" in filename \
            else "FUZZY_MAP" if "FUZZY_MAP" in filename \
            else "PUNCTUATION_MAP" if "PUNCTUATION_MAP" in filename \
            else ""

        if "PUNCTUATION_MAP" in filename:
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*" + r"\{", line) for line in lines[:270])
            open_bracket = '{'
            closing_bracket = '}'
            comment2add = '# from->too'
            separator = ':'
        else:
            has_var_def = any(re.search(rf"^\s*{target_var}\s*=\s*\[", line) for line in lines[:270])
            open_bracket = '['
            closing_bracket = ']'
            comment2add = '# too<-from'
            separator = ','

        needs_closing_bracket = False
        if not has_var_def:
            logger.info(f"   -> add Definition: {target_var} = {open_bracket}")
            lines.insert(2, f"\n{comment2add}\n{target_var} = {open_bracket}\n")
            fixed_content = True
            needs_closing_bracket = True

        # --- MAIN LOOP (fix content inside list) ---
        def fix_bare_word(line, target_var, filename, separator, closing_bracket, logger):
            """Convert a bare word line into a proper tuple/dict entry. Returns fixed line or None."""
            original = line
            stripped = line.strip()
            # Skip structural lines
            skip_words = [target_var, 'import', 're', 'True', 'False', 'import re', 'noqa',
                          open_bracket, closing_bracket, comment2add]
            if stripped in skip_words:
                return None
            if stripped.startswith('#') or stripped.startswith('(') or stripped.startswith("'"):
                return None
            match = re.match(
                r"^\s*(?P<word>[\w][\w\s\-]*)\s*,?\s*(?P<comment>#.*)?\s*$",
                line
            )
            if not match:
                return None
            current_word = match.group('word').strip()
            if not current_word or current_word in skip_words:
                return None
            indent = line[:len(line) - len(line.lstrip())] or '    '
            comment = ""
            if match.group('comment'):
                comment = f"  {match.group('comment')}"
            if 'PUNCTUATION_MAP.py' in filename:
                fixed = f"{indent}'{current_word}'{separator} '{current_word}',{comment}\n"
            else:
                fixed = f"{indent}('{current_word}'{separator} r'^{re.escape(current_word)}$'),{comment}\n"
            logger.info(f"   -> Bulk-Fix: {original.strip()} => {fixed.strip()}")
            return fixed

        inside_list = needs_closing_bracket  # already open if we just inserted the definition
        closing_idx = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            if re.search(rf"^\s*{target_var}\s*=\s*[\[\{{]", line):
                inside_list = True

            if stripped == closing_bracket:
                inside_list = False
                closing_idx = len(new_lines)  # remember position of ]
                new_lines.append(line)
                continue

            if inside_list:
                fixed = fix_bare_word(line, target_var, filename, separator, closing_bracket, logger)
                if fixed:
                    new_lines.append(fixed)
                    fixed_content = True
                    continue

            new_lines.append(line)

        # --- Move lines after ] to before ] ---
        if closing_idx is not None:
            after_closing = []
            kept_after = []
            for line in new_lines[closing_idx + 1:]:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    kept_after.append(line)
                else:
                    # Try to fix bare word before moving it inside
                    fixed = fix_bare_word(line, target_var, filename, separator, closing_bracket, logger)
                    if fixed:
                        after_closing.append(fixed)
                        fixed_content = True
                    else:
                        after_closing.append(line)
                        fixed_content = True

            if after_closing:
                logger.info(f"   -> Moving {len(after_closing)} line(s) from after {closing_bracket} to inside list.")
                new_lines = (
                    new_lines[:closing_idx]
                    + after_closing
                    + [new_lines[closing_idx]]
                    + kept_after
                )

        # --- Close bracket if we opened one ---
        if needs_closing_bracket:
            last_line_clean = new_lines[-1].strip() if new_lines else ""
            if last_line_clean != closing_bracket:
                new_lines.append(f"{closing_bracket}\n")
                logger.info(f"   -> Added closing bracket {closing_bracket}.")

        if fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

    except Exception as e:
        logger.error(f"Auto-Fix failed: {e}")
        return False


def _apply_fix_name_error_backup_202601031751(file_path, bad_name, logger):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        fixed_content = False

        try:
            clean_path = os.path.relpath(file_path)
        except ValueError:
            clean_path = file_path

        correct_header = f"# {clean_path}\n"

        if lines and lines[0].strip().startswith("#") and ".py" in lines[0]:
            lines[0] = correct_header
            while len(lines) > 1 and lines[1].strip().startswith("#") and ".py" in lines[1]:
                logger.info(f"   -> Entferne doppelten Header: {lines[1].strip()}")
                del lines[1]
                fixed_content = True
        else:
            lines.insert(0, correct_header)
            fixed_content = True

        has_import = any("import re" in line for line in lines[:5])
        if not has_import:
            lines.insert(1, "import re # noqa: F401\n")
            fixed_content = True

        for line in lines:
            original_line = line
            if re.search(r'\b' + re.escape(bad_name) + r'\b', line):
                stripped = line.strip()
                code_part = stripped.split('#')[0].strip()
                comment = ""
                if "#" in stripped:
                    comment = "  #" + stripped.split('#', 1)[1]
                indent = line[:len(line) - len(line.lstrip())]
                if not indent:
                    indent = '    '
                clean_core = code_part.replace(',', '').replace("'", "").replace('"', "").replace('(', "").replace(')', "").strip()
                if clean_core == bad_name:
                    line = f"{indent}('{bad_name}', '{bad_name}'),{comment}\n"
                    if line != original_line:
                        logger.info(f"   -> Auto-Fix (Singleton->Paar): {stripped} => {line.strip()}")
                        new_lines.append(line)
                        fixed_content = True
                        continue
                pattern = r"(?<!['\"])\b" + re.escape(bad_name) + r"\b(?!['\"])"
                current_text = re.sub(pattern, f"'{bad_name}'", code_part)
                needs_fix = False
                if not current_text.startswith('('):
                    current_text = "(" + current_text
                    needs_fix = True
                if not current_text.endswith(','):
                    current_text += ","
                    needs_fix = True
                if not current_text.endswith('),'):
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
