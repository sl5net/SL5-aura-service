# scripts/py/setup_config.py
import urllib.request
import sys
import os
import re
import shutil

# ---------------------------------------------------------------------------
# i18n loader
# ---------------------------------------------------------------------------
# Translations live in scripts/py/setup_config.i18n/setup_config-<lang>lang.md
#
# IMPORTANT: matching is strictly by LINE POSITION, never by header/key text.
# Translators are free to rename, mistype, or garble the "# some_key" headers
# above each line (they routinely do) - the parser ignores them completely.
# Only the order in which real content lines appear in the file matters.
#
# The N-th content line found in the file becomes STRING_KEYS[N-1].
# If the file has fewer lines than needed, missing entries are padded from
# the English fallback (with a warning). If it has more, everything after
# the required count is ignored (with a warning) - this is what happens to
# duplicated/copy-pasted blocks, see the --i18n-test output for an example.

STRING_KEYS = [
    "text_detected",     # region/country detection line
    "text_help",         # short help line under it
    "prompt_primary",    # "primary language" prompt
    "prompt_secondary",  # "secondary language" prompt
    "enter_hint",        # "press enter to confirm..." hint
]

# Built-in fallback strings. These are used whenever no matching .md file
# exists, or a .md file doesn't provide enough lines. They also double as
# the reference/template content for translators.
DEFAULT_STRINGS = {
    "de": [
        "Region erkannt: {country} | Vorschlag: {default_primary}",
        "Sprachcode wählen oder 'n' für Terminal-Modus (Keine Sprachen).",
        "Primäre Sprache (de, en... oder 'n' für nein, keine Sprache) - automatische Bestätigung in 8 Sekunden",
        "Sekundäre Sprache (oder 'none' Default) - automatische Bestätigung in 8 Sekunden",
        "Drücken Sie die Eingabetaste zur Bestätigung oder geben Sie einen anderen Sprachcode ein.",
    ],
    "en": [
        "Region detected: {country} | Suggested: {default_primary}",
        "Select language or type 'n' for Terminal Mode (No Langs).",
        "Primary Lang (de, en, etc. or 'n') - auto-confirms in 8s",
        "Secondary Language (or 'none') - auto-confirms in 8s",
        "Press Enter to confirm, or type a different language code.",
    ],
}

FALLBACK_LANG = "en"
I18N_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_config.i18n")

# Country -> language code, used only to pick a *candidate* language for the
# automatic (non-interactive) suggestion. The candidate is only ever used if
# a matching setup_config-<code>lang.md file actually exists (see
# detect_default_lang) - so adding a country here does nothing by itself,
# and a missing entry just means "no code changes needed to support it",
# the file's mere presence is what makes it selectable.
COUNTRY_LANG_MAP = {
    "DE": "de", "AT": "de", "CH": "de",
    "FR": "fr",
    "ES": "es", "MX": "es", "AR": "es", "CO": "es", "CL": "es", "PE": "es", "VE": "es", "UY": "es", "EC": "es",
    "PT": "pt",
    "BR": "pt-BR",
    "PL": "pl",
    "IN": "hi",
    "JP": "ja",
    "KR": "ko",
    "CN": "zh-CN", "TW": "zh-CN", "HK": "zh-CN",
    "SA": "ar", "EG": "ar", "AE": "ar", "MA": "ar", "DZ": "ar", "IQ": "ar", "JO": "ar",
    "KW": "ar", "QA": "ar", "OM": "ar", "BH": "ar", "YE": "ar", "LY": "ar", "TN": "ar",
    "SD": "ar", "LB": "ar", "PS": "ar",
}


def i18n_filename(lang_code):
    return f"setup_config-{lang_code}lang.md"


def list_available_i18n_langs(i18n_dir=I18N_DIR):
    """
    Scans the i18n dir for setup_config-<code>lang.md files and returns the
    codes in their original casing (e.g. 'pt-BR', 'zh-CN'), de-duplicated
    case-insensitively while keeping the first-seen casing.
    """
    seen = {}
    if os.path.isdir(i18n_dir):
        for f in os.listdir(i18n_dir):
            m = re.match(r"^setup_config-(.+)lang\.md$", f, re.IGNORECASE)
            if m:
                code = m.group(1)
                seen.setdefault(code.lower(), code)
    return sorted(seen.values())


def detect_default_lang(country_code, i18n_dir=I18N_DIR, fallback_lang=FALLBACK_LANG):
    """
    Picks the language to auto-suggest based on the detected country, but
    ONLY if a matching setup_config-<code>lang.md file actually exists.
    This is what makes the detection dynamic: dropping a new translation
    file into the i18n folder plus one line in COUNTRY_LANG_MAP is enough
    for the script to start suggesting it automatically - it no longer
    hardcodes a de/en-only choice regardless of what's available.
    """
    candidate = COUNTRY_LANG_MAP.get((country_code or "").upper())
    if candidate and os.path.isfile(os.path.join(i18n_dir, i18n_filename(candidate))):
        return candidate
    return fallback_lang


def parse_i18n_md(path):
    """
    Parses a translation markdown file into an ordered list of content strings.
    Only the ORDER of lines matters, never any key/heading text next to them.

    Ignored (not counted as content):
      - blank lines
      - heading/comment lines starting with '#' (any amount of '#', with or
        without a space after it - translators are inconsistent here)
      - HTML comments '<!-- ... -->'
      - fenced code blocks (``` ... ```), including their contents

    Everything else is kept, with common list/quote markers ('1. ', '- ',
    '* ', '> ') stripped from the start of the line.
    """
    lines_out = []
    in_code_block = False
    in_comment_block = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n").strip()

            if in_comment_block:
                if "-->" in line:
                    in_comment_block = False
                continue
            if line.startswith("<!--"):
                if "-->" not in line:
                    in_comment_block = True
                continue

            if line.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if not line:
                continue
            if line.startswith("#"):
                continue
            stripped = re.sub(r"^(\d+[\.\)]\s+|[-*+]\s+|>\s+)", "", line)
            lines_out.append(stripped)
    return lines_out


def safe_format(template, **kwargs):
    """
    Substitutes only known literal placeholder tokens, e.g. '{country}'.
    Deliberately NOT using str.format(**kwargs): translators sometimes
    rename placeholders (e.g. '{país}' instead of '{country}') or leave
    stray braces in free text, and str.format() would raise KeyError/
    crash the whole script on that. Unknown tokens are simply left as-is
    in the output so the mismatch is visible instead of fatal.
    """
    result = template
    for key, value in kwargs.items():
        result = result.replace("{" + key + "}", str(value))
    return result


def load_translations(lang_code, i18n_dir=I18N_DIR, fallback_lang=FALLBACK_LANG, quiet=False):
    """
    Loads the ordered raw (un-formatted) string list for lang_code.
    Returns (strings, source) where source is 'md', 'md+fallback' (padded),
    'md+truncated', or 'fallback'.
    """
    fallback = DEFAULT_STRINGS.get(lang_code, DEFAULT_STRINGS[fallback_lang])
    path = os.path.join(i18n_dir, i18n_filename(lang_code))

    if not os.path.isfile(path):
        return fallback, "fallback"

    try:
        parsed = parse_i18n_md(path)
    except Exception as e:
        if not quiet:
            sys.stderr.write(f"[i18n] Warning: failed to parse {path}: {e}\n")
        return fallback, "fallback"

    needed = len(STRING_KEYS)
    if len(parsed) < needed:
        if not quiet:
            sys.stderr.write(
                f"[i18n] Warning: {path} only has {len(parsed)}/{needed} usable lines - "
                f"padding the missing {needed - len(parsed)} entr"
                f"{'y' if needed - len(parsed) == 1 else 'ies'} with '{fallback_lang}' fallback text.\n"
            )
        parsed = parsed + fallback[len(parsed):]
        return parsed, "md+fallback"

    if len(parsed) > needed:
        if not quiet:
            sys.stderr.write(
                f"[i18n] Warning: {path} has {len(parsed)} usable lines but only {needed} are used. "
                f"Everything after line {needed} is ignored - check for duplicated/copy-pasted "
                f"blocks in the file.\n"
            )
        parsed = parsed[:needed]
        return parsed, "md+truncated"

    return parsed, "md"


def get_strings(lang_code, quiet=False, **fmt_kwargs):
    """Returns (dict of STRING_KEYS -> formatted string, source)."""
    values, source = load_translations(lang_code, quiet=quiet)
    formatted = [safe_format(v, **fmt_kwargs) for v in values]
    return dict(zip(STRING_KEYS, formatted)), source


# ---------------------------------------------------------------------------
# Manual test entrypoint (no interactive flow, no network calls)
# ---------------------------------------------------------------------------
def run_i18n_test(argv):
    """
    Usage:
      python setup_config.py --i18n-langs
          Lists every language for which a setup_config-<code>lang.md exists.

      python setup_config.py --i18n-test <lang> [--country XX]
          Loads and prints the resolved strings for <lang> without running
          the actual setup flow. --country lets you fake the {country}
          placeholder value (default: 'XX').

    Returns True if it handled the request (caller should exit afterwards).
    """
    if "--i18n-langs" in argv:
        found = list_available_i18n_langs()
        print("Available i18n languages (from *.md files):")
        print(", ".join(found) if found else "(none found - only built-in 'de'/'en' fallback exist)")
        return True

    if "--i18n-test" in argv:
        idx = argv.index("--i18n-test")
        lang = argv[idx + 1] if idx + 1 < len(argv) else FALLBACK_LANG

        test_country = "XX"
        if "--country" in argv:
            cidx = argv.index("--country")
            if cidx + 1 < len(argv):
                test_country = argv[cidx + 1]

        strings, source = get_strings(lang, country=test_country, default_primary=lang)
        print(f"--- i18n test: lang='{lang}' | source={source} ---")
        for key in STRING_KEYS:
            print(f"{key}: {strings[key]}")
        print("--- end i18n test ---")
        return True

    return False


if run_i18n_test(sys.argv):
    sys.exit(0)


# ---------------------------------------------------------------------------
# Original helpers (unchanged)
# ---------------------------------------------------------------------------
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
    print(f"Repository documentation summary:")
    print(f"  docs folder exists: {info['docs_exists']}, files: {len(info['docs_files'])}", file=sys.stderr)
    print(f"  doc_sources folder exists: {info['doc_sources_exists']}, files: {len(info['doc_sources_files'])}", file=sys.stderr)
    if info['i18n_folders']:
        print(f"  i18n folders found:")
        for k, v in info['i18n_folders'].items():
            print(f"    {k} -> {len(v)} .md files", file=sys.stderr)
    else:
        print(f"  no .i18n folders found.")


def delete_path(path):
    # safe delete with shutil.rmtree
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleted: {path}")
    else:
        print(f"Not found (so not deleted): {path}", file=sys.stderr)


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
default_primary = detect_default_lang(country)

strings, i18n_source = get_strings(default_primary, country=country, default_primary=default_primary)
text_detected = strings["text_detected"]
text_help = strings["text_help"]
prompt_p = strings["prompt_primary"]
prompt_s = strings["prompt_secondary"]

sys.stderr.write(f"{strings['enter_hint']}\n")
sys.stderr.write(f"{text_detected}\n{text_help}\n")

primary = timed_input(prompt_p, default_primary)
if primary in ["n", "none", "0"]:
    # If terminal mode is selected, we exclude all languages
    secondary = "none"
    excludes = []
    excludes_str = "all"
else:
    secondary = timed_input(prompt_s, "none")
    all_langs = sorted(set(list_available_i18n_langs()) | {FALLBACK_LANG})
    excludes = [lang for lang in all_langs if lang.lower() != primary.lower() and lang.lower() != str(secondary).lower()]
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
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
info = find_folder_counts(repo_root)
print(f"")  # spacer
print_counts(info)
print(f"")
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
            print(f"")
            print(f"Deleted {len(deleted)} files (attempted).", file=sys.stderr)
            if deleted:
                for d in deleted:
                    print(f"  - {d}", file=sys.stderr)
            if skipped:
                print(f"{len(skipped)} entries skipped or failed:", file=sys.stderr)
                for s in skipped[:50]:
                    if isinstance(s, tuple):
                        print(f"  - {s[0]}: {s[1]}", file=sys.stderr)
                    else:
                        print(f"  - {s}", file=sys.stderr)
else:
    print(f"No docs or doc_sources folders detected; nothing to delete.", file=sys.stderr)
# End
