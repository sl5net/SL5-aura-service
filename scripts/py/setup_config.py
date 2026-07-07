# scripts/py/setup_config.py
import urllib.request
import sys
import os
import shutil

def get_country():
    try:
        with urllib.request.urlopen("https://ipapi.co/country/", timeout=2) as response:
            return response.read().decode().strip()
    except Exception as e:
        return f"Unknown{e}"


def timed_input(prompt, default, timeout=8):
    import os
    import time
    sys.stderr.write(f"{prompt} [{default}]: ")
    sys.stderr.flush()

    if os.name == 'nt':
        # Windows native timed input using msvcrt
        import msvcrt
        start_time = time.time()
        input_chars = []
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getwche()
                if char in ('\r', '\n'):  # Enter key pressed
                    sys.stderr.write("\n")
                    sys.stderr.flush()
                    res = ''.join(input_chars).strip()
                    return res if res else default
                elif char == '\b':  # Backspace handling
                    if input_chars:
                        input_chars.pop()
                        sys.stderr.write(' \b')
                        sys.stderr.flush()
                else:
                    input_chars.append(char)
            if (time.time() - start_time) > timeout:
                sys.stderr.write("\n")
                sys.stderr.flush()
                return default
            time.sleep(0.05)
    else:
        # Linux/macOS standard select.select input
        import select
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            res = sys.stdin.readline().strip()
            return res if res else default
        sys.stderr.write("\n")
        sys.stderr.flush()
        return default


def find_folder_counts(root):
    """
    Returns a dict with counts and file lists for docs, doc_sources and i18n translation files.
    """
    info = {
        'docs_exists': False,
        'doc_sources_exists': False,
        'docs_files': [],
        'doc_sources_files': [],
        # i18n: mapping folder -> list of files
        'i18n_folders': {}
    }

    docs_path = os.path.join(root, 'docs')
    doc_sources_path = os.path.join(root, 'doc_sources')

    if os.path.isdir(docs_path):
        info['docs_exists'] = True
        for dirpath, _, filenames in os.walk(docs_path):
            for f in filenames:
                full = os.path.join(dirpath, f)
                info['docs_files'].append(full)

    if os.path.isdir(doc_sources_path):
        info['doc_sources_exists'] = True
        for dirpath, _, filenames in os.walk(doc_sources_path):
            for f in filenames:
                full = os.path.join(dirpath, f)
                info['doc_sources_files'].append(full)

    # Find *.i18n directories anywhere in repo (or directly under root)
    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d.endswith('.i18n'):
                i18n_full = os.path.join(dirpath, d)
                matched = []
                for ipath, _, ifiles in os.walk(i18n_full):
                    for f in ifiles:
                        # Example patterns: AuraStart-arlang.md, etc.
                        if f.lower().endswith('.md'):
                            matched.append(os.path.join(ipath, f))
                info['i18n_folders'][i18n_full] = matched
                # don't recursively re-scan nested .i18n if present
                dirnames.remove(d)
    return info


def print_counts(info):
    print("Repository documentation summary:")
    print(f"  docs folder exists: {info['docs_exists']}, files: {len(info['docs_files'])}")
    print(f"  doc_sources folder exists: {info['doc_sources_exists']}, files: {len(info['doc_sources_files'])}")
    if info['i18n_folders']:
        print("  i18n folders found:")
        for k, v in info['i18n_folders'].items():
            print(f"    {k} -> {len(v)} .md files")
    else:
        print("  no .i18n folders found.")


def delete_path(path):
    # safe delete with shutil.rmtree
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleted: {path}")
    else:
        print(f"Not found (so not deleted): {path}")


def delete_non_primary_md(info, primary):
    """
    Delete markdown files whose language code does not match primary.
    Pattern assumptions:
      - In .i18n folders: files named like BaseName-<lang>lang.md e.g. AuraStart-delang.md
      - In docs folder: primary english file may be docs/AuraStart.md (default english)
    This function tries to be conservative: only deletes files whose name clearly indicates a language suffix
    and that suffix != primary.
    """
    deleted = []
    skipped = []
    # pattern: name-<code>lang.md, we treat <code> as language code token before 'lang'
    for folder, files in info['i18n_folders'].items():
        for f in files:
            fname = os.path.basename(f)
            # attempt to extract pattern like BaseName-<code>lang.md
            if '-' in fname and fname.lower().endswith('lang.md'):
                base, suffix = fname.rsplit('-', 1)
                # suffix like 'delang.md' -> extract the portion before 'lang'
                if suffix.lower().endswith('lang.md'):
                    code_part = suffix[:-len('lang.md')]
                    code = code_part.strip().lower()
                    if code != primary.lower():
                        try:
                            os.remove(f)
                            deleted.append(f)
                        except Exception as e:
                            skipped.append((f, str(e)))
                    else:
                        skipped.append((f, 'primary language — kept'))
                else:
                    skipped.append((f, 'pattern mismatch'))
            else:
                skipped.append((f, 'pattern mismatch'))

    # In docs/ we consider deleting any *.md that looks like it's language-specific (e.g. AuraStart-xx.md)
    docs_md = [f for f in info['docs_files'] if f.lower().endswith('.md')]
    for f in docs_md:
        fname = os.path.basename(f)
        # skip primary english default which is BaseName.md (no suffix)
        # delete files with -<code>.md where code != primary
        if '-' in fname:
            name_part, ext = os.path.splitext(fname)
            possible_code = name_part.split('-')[-1].lower()
            # basic heuristic: if code is two letters or matches known codes, treat as lang suffix
            if len(possible_code) in (2, 3) and possible_code != primary.lower():
                try:
                    os.remove(f)
                    deleted.append(f)
                except Exception as e:
                    skipped.append((f, str(e)))
            else:
                skipped.append((f, 'not recognized as language-suffixed'))
        else:
            skipped.append((f, 'no suffix — assumed primary english'))

    return deleted, skipped


# ---------------------------
# Main flow
# ---------------------------

country = get_country()
default_primary = "de" if country in ["DE", "AT", "CH"] else "en"

if default_primary == "de":
    text_detected = f"Region erkannt: {country} | Vorschlag: {default_primary}"
    text_help = "Sprachcode wählen oder 'n' für Terminal-Modus (Keine Sprachen)."
    prompt_p = "Primäre Sprache (de, en... oder 'n' für nein, keine Sprache) - automatische Bestätigung in 8 Sekunden"
    prompt_s = "Sekundäre Sprache (oder 'none' Default) - automatische Bestätigung in 8 Sekunden"
    sys.stderr.write("Drücken Sie die Eingabetaste zur Bestätigung oder geben Sie einen anderen Sprachcode ein.\n")
else:
    text_detected = f"Region detected: {country} | Suggested: {default_primary}"
    text_help = "Select language or type 'n' for Terminal Mode (No Langs)."
    prompt_p = "Primary Lang (de, en, etc. or 'n') - auto-confirms in 8s"
    prompt_s = "Secondary Language (or 'none') - auto-confirms in 8s"
    sys.stderr.write("Press Enter to confirm, or type a different language code.\n")

sys.stderr.write(f"{text_detected}\n{text_help}\n")

primary = timed_input(prompt_p, default_primary)

if primary in ["n", "none", "0"]:
    # If terminal mode is selected, we exclude all languages
    secondary = "none"
    excludes = []
    excludes_str = "all"
else:
    secondary = timed_input(prompt_s, "none")
    all_langs = ["de", "en", "fr", "es"]
    excludes = [lang for lang in all_langs if lang != primary and lang != secondary]
    excludes_str = ",".join(excludes)

# Print environment variables as before
if os.name == 'nt':
    print(f"$env:SELECTED_LANG='{primary}'")
    print(f"$env:SECOND_LANG='{secondary}'")
    print(f"$env:EXCLUDE_LANGUAGES='{excludes_str}'")
else:
    print(f"export SELECTED_LANG='{primary}'")
    print(f"export SECOND_LANG='{secondary}'")
    print(f"export EXCLUDE_LANGUAGES='{excludes_str}'")

# --- New: show docs/doc_sources/i18n counts and ask about deletions ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # adjust if script location differs
# If you prefer script to run relative to current working dir, use os.getcwd() instead:
repo_root = os.getcwd()

info = find_folder_counts(repo_root)
print("")  # spacer
print_counts(info)
print("")

# Ask whether user wants to delete entire docs and/or doc_sources
if info['docs_exists'] or info['doc_sources_exists']:
    # default to 'n' (no) after timeout
    ans_all = timed_input("Delete entire docs and doc_sources folders? (y/n)", "n", timeout=8).lower()
    if ans_all in ("y", "yes"):
        if info['docs_exists']:
            delete_path(os.path.join(repo_root, 'docs'))
        if info['doc_sources_exists']:
            delete_path(os.path.join(repo_root, 'doc_sources'))
    else:
        # Offer the more granular option: delete only non-primary language md files
        ans_partial = timed_input("Delete only docs md files that are NOT the selected primary language? (y/n)", "n", timeout=8).lower()
        if ans_partial in ("y", "yes"):
            deleted, skipped = delete_non_primary_md(info, primary)
            print("")
            print(f"Deleted {len(deleted)} files (attempted).")
            if deleted:
                for d in deleted:
                    print(f"  - {d}")
            if skipped:
                print(f"{len(skipped)} entries skipped or failed:")
                for s in skipped[:50]:
                    if isinstance(s, tuple):
                        print(f"  - {s[0]}: {s[1]}")
                    else:
                        print(f"  - {s}")
else:
    print("No docs or doc_sources folders detected; nothing to delete.")

# End