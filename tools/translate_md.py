#!/usr/bin/env python3
# tools/translate_md.py
import os
import glob
import subprocess
import time
import re
# import sys
from pathlib import Path

# search_path = script_dir.parent / 'docs' / 'Feature_Spotlight' / 'Implementing*.md'

# ==============================================================================
#           Intelligenter Markdown-Übersetzer (Python-Version)
# ==============================================================================

# 3. Überspringe bereits übersetzte Dateien (Suffix-Check)
# if re.search(r'-[a-z]{2,3}lang\.md$', filename):
# continue


#
# Version 7.1: Verwendet einen "kugelsicheren" Platzhalter für Links (z.B.
#              XMDLINK20X), um zu verhindern, dass der Übersetzer den
#              Platzhalter selbst verändert.
#
# ANFORDERUNGEN:
# - Python 3
# - `translate-shell` muss im System-PATH installiert sein (`trans` Befehl)
#

script_dir = Path(__file__).resolve().parent

# --- KONFIGURATION ---
SOURCE_LANG = "en"
# TARGET_LANGS = ["de", "pt", "es", "fr"]
# TARGET_LANGS = ["de"]
#TARGET_LANGS = ["de","pt","pt-BR","es","fr","ja","ko","hi","zh-CN","pl","ar"]
TARGET_LANGS = ["ar","de","es","fr","hi","ja","ko","pl","pt","pt-BR","zh-CN"]





DUNDER_PLACEHOLDER = "XDUNDERX"
HARD_BREAK_PLACEHOLDER = "XSPACEBREAKX"

# ### NEU: Ein kugelsicherer Platzhalter für Links ###
MD_LINK_PLACEHOLDER_FORMAT = "XMDLINK{}X"
# --- ENDE KONFIGURATION ---


import logging
import sys

try:
    from tools.i18n.section_cache import (
        compute_section_hash,
        get_cached_translation,
        load_cache,
        save_cache,
        split_markdown_by_h2,
        store_cached_translation,
    )
except ImportError:
    from i18n.section_cache import (
        compute_section_hash,
        get_cached_translation,
        load_cache,
        save_cache,
        split_markdown_by_h2,
        store_cached_translation,
    )

cache_file = script_dir / "i18n" / "translation_cache.json"
log_dir = script_dir.parent / "log"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "translate_md.log"


class LogTee:

    def __init__(self, target_file, stream):
        self.file = open(target_file, "a", encoding="utf-8")
        self.stream = stream

    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stream.write(data)
        self.stream.flush()

    def flush(self):
        self.file.flush()
        self.stream.flush()


tee_stdout = LogTee(log_file, sys.stdout)
sys.stdout = tee_stdout
sys.stderr = tee_stdout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger()


def test_translation_links():
    # Test-Konfiguration
    test_lang = "de"

    # Testfälle: (Eingabezeile, Beschreibung)
    test_cases = [
        ('[Normaler Link](about.md)', "Standard Markdown Link"),
        ('[Link mit Anker](contact.md#form)', "Markdown Link mit Anker"),
        ('[Die README](README.md)', "Spezialfall README"),
        ('![Ein Bild](images/logo.png)', "Asset / Bild (kein MD)"),
        ('[Extern](https://google.com)', "Absoluter Link (sollte gleich bleiben)"),
        ('[Anker](#abschnitt)', "Interner Anker (sollte gleich bleiben)"),
        ('[](../about-delang.md)', "Bereits korrigierter Link (Idempotenz)"),
    ]

    print(f"{'INPUT':<40} | {'OUTPUT':<40}")
    print("-" * 85)

    for original, description in test_cases:
        modified = add_lang_to_md_links(original, test_lang)
        print(f"…{str(original)[-40:]} | …{str(modified)[-40:]} | …{str(description)[-40:]}")







def add_lang_to_md_links(line: str, lang: str) -> str:
    """
    Finds all relative Markdown links to .md files in a line and appends a language suffix.

    - Ignores absolute URLs (http, https).
    - Ignores links that already have a language suffix (e.g., 'file-delang.md').
    - Correctly handles links with anchors (e.g., 'file.md#section').

    Args:
        line: The string (line of text) to process.
        lang: The language code to append (e.g., 'de').

    Returns:
        The processed line with modified links.
    """
    logger.info(f"Processing line for language '{lang}': \"{line.strip()}\"")

    # Pattern to find Markdown links: [text](url)
    # The URL part is captured for processing.
    # markdown_link_pattern = re.compile(r'(\[.*?\])\((.*?)\)')

    markdown_link_pattern = re.compile(r'(\[!?.*?\])\((.*?)\)')

    def replace_link(match):
        """This function is called for every link found by re.sub."""
        link_text = match.group(1)
        url = match.group(2)

        logger.info(f"  -> Found link: {match.group(0)}")

        # --- Conditions to NOT modify the link ---
        # 1. It's an absolute URL
        if url.startswith(('http://', 'https://', '#', 'mailto:', '/')):
            logger.info("     - Skipping: It's an absolute URL.")
            return match.group(0) # Return the original full match


        # 3. It already seems to have a language suffix
        # if re.search(r'-\w{2}lang\.md', url):
        #     logger.info("     - Skipping: Already has a language suffix.")
        #     return match.group(0)

        # --- Modify the link ---
        # Separate the path from a potential anchor
        if '#' in url:
            path, anchor = url.split('#', 1)
            anchor = '#' + anchor
        else:
            path, anchor = url, ''

        # Remove the .md extension and add the suffix
        base_path = path[:-3] # Remove '.md'
        if base_path == 'README':
            new_path = f"{base_path}.md{anchor}"
        else:
            if '.md' in path and f"-{lang}lang.md" not in path:
                new_path = f"{base_path}-{lang}lang.md{anchor}"
            else:
                new_path = path

        # if not new_path.startswith(('/')):
        new_path = f"../{new_path}"
        new_link = f"{link_text}({new_path})"

        logger.info(f"     + Modifying to: {new_link}")
        return new_link

    # Use re.sub with our replacement function to process all links in the line
    return markdown_link_pattern.sub(replace_link, line)





def translate_section(section_text: str, lang: str) -> str:
    original_lines = section_text.splitlines()

    markdown_links = []

    def link_replacer(match):
        placeholder = MD_LINK_PLACEHOLDER_FORMAT.format(len(markdown_links))
        markdown_links.append(match.group(0))
        return placeholder

    link_regex = re.compile(r"!?(?:\[[^\]]*\])\((?:[^\)]*)\)")
    lines_step0 = [link_regex.sub(link_replacer, line) for line in original_lines]

    lines_step1 = []
    for line in lines_step0:
        if line.endswith("  "):
            lines_step1.append(line[:-2] + HARD_BREAK_PLACEHOLDER)
        else:
            lines_step1.append(line)

    lines_step2 = [line.replace("__", DUNDER_PLACEHOLDER) for line in lines_step1]

    lines_for_translation = []
    code_blocks = []
    in_code_block = False
    current_block = []
    for line in lines_step2:
        if line.strip().startswith("```") and not in_code_block:
            in_code_block = True
            current_block.append(line)
            lines_for_translation.append(f"__CODE_BLOCK_{len(code_blocks)}__")
        elif line.strip().startswith("```") and in_code_block:
            in_code_block = False
            current_block.append(line)
            code_blocks.append("\n".join(current_block))
            current_block = []
        elif in_code_block:
            current_block.append(line)
        else:
            lines_for_translation.append(line)

    text_to_translate = "\n".join(lines_for_translation)
    if not text_to_translate.strip():
        return section_text

    try:
        process = subprocess.run(
            ["trans", "-e", "bing", "-brief", f"{SOURCE_LANG}:{lang}"],
            input=text_to_translate,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=60,
        )
        translated_lines = process.stdout.strip().split("\n")
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ) as e:
        print(f"      [ERROR] Section translation failed: {e}")
        return section_text

    restored_step_A = []
    for line in translated_lines:
        code_match = re.match(r"^__CODE_BLOCK_(\d+)__$", line.strip())
        if code_match:
            idx = int(code_match.group(1))
            if idx < len(code_blocks):
                restored_step_A.extend(code_blocks[idx].split("\n"))
                continue
        restored_step_A.append(line)

    restored_step_B = []
    placeholder_regex = re.compile(r"(XMDLINK\d+X)")
    for line in restored_step_A:
        restored_line = line
        placeholders_in_line = placeholder_regex.findall(restored_line)
        for placeholder in placeholders_in_line:
            link_index = int(re.search(r"\d+", placeholder).group())
            if link_index < len(markdown_links):
                original_link = markdown_links[link_index]
                modified_link = add_lang_to_md_links(original_link, lang)
                restored_line = restored_line.replace(placeholder, modified_link, 1)
        restored_step_B.append(restored_line)

    restored_step_C = [
        line.replace(DUNDER_PLACEHOLDER, "__") for line in restored_step_B
    ]
    final_lines = [
        line.replace(HARD_BREAK_PLACEHOLDER, "  ") for line in restored_step_C
    ]
    return "\n".join(final_lines)


def process_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw_content = f.read()

    sections = split_markdown_by_h2(raw_content)
    base_name = os.path.splitext(filename)[0]
    cache_data = load_cache(cache_file)

    for lang in TARGET_LANGS:
        i18n_dir = f"{base_name}.i18n"
        os.makedirs(i18n_dir, exist_ok=True)
        output_file = f"{i18n_dir}/{os.path.basename(base_name)}-{lang}lang.md"

        output_path = Path(output_file)
        if (
            output_path.exists()
            and output_path.stat().st_mtime > Path(filename).stat().st_mtime
        ):
            continue

        print(f"   -> Processing '{lang}' -> '{output_file}'…")
        translated_sections = []
        has_cache_miss = False

        for section in sections:
            sec_hash = compute_section_hash(section)
            cached_text = get_cached_translation(cache_data, sec_hash, lang)

            if cached_text is not None:
                translated_sections.append(cached_text)
            else:
                has_cache_miss = True
                translated = translate_section(section, lang)
                store_cached_translation(cache_data, sec_hash, lang, translated)
                translated_sections.append(translated)
                time.sleep(1)

        full_output = "".join(translated_sections)
        output_lines = full_output.splitlines()

        if len(output_lines) <= 2:
            print(
                f"      [SKIP] Output for '{lang}' has only {len(output_lines)} lines, skipping write."
            )
            continue
        if any(
            line.strip().startswith("https://translate.google.com")
            for line in output_lines
        ):
            print(
                f"      [SKIP] Output for '{lang}' contains redirect URL, skipping write."
            )
            continue
        if len(full_output) < (len(raw_content) * 0.35):
            print(
                f"      [SKIP] Output for '{lang}' is suspiciously short, skipping write."
            )
            continue

        print(f"      -> Saving file '{output_file}'…")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_output)

        if has_cache_miss:
            save_cache(cache_file, cache_data)        
        
        
        
        
        
        
        
        
        
    #logger.info(f'-> line 297: skipCount already translated: {skipCount}')

def main():

    # test_translation_links()
    # sys.exit(1)
    current_branch = os.environ.get("GITHUB_REF_NAME", "")
    if not current_branch:
        try:
            current_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            current_branch = ""
    if current_branch and current_branch not in {"master", "HEAD"}:
        logger.info(f"Skipping translations: current branch '{current_branch}' is not 'master'.")
        return

    logger.info("Starte die intelligente Übersetzung von Markdown-Dateien…")
    logger.info(f"Quellsprache: {SOURCE_LANG}")
    logger.info(f"Zielsprachen: {TARGET_LANGS}")


    # search_path = script_dir.parent / 'docs' / 'Feature_Spotlight' / 'Implementing*.md'
    # search_path = script_dir.parent / 'README.md' # alt
    search_path = script_dir.parent / '**' / '*.md' # neu


    #logger.info(f"---- {search_path} ------------------------------------------------")
    # for filename in glob.glob(str(search_path)):
    skipCount = 0
    for filename in glob.glob(str(search_path), recursive=True):

        path_parts = filename.split(os.sep)

        # 1. Überspringe, wenn IRGENDEIN Teil des Pfades mit einem Punkt beginnt
        # (aber ignoriere den aktuellen Ordner '.' am Anfang)
        if any(part.startswith('.') for part in path_parts if part not in ['.', '..']):
            continue

            # 2. Überspringe bekannte System-Ordner ohne Punkt (wie venv oder node_modules)
        if any(ignored in path_parts for ignored in ["venv", "__pycache__", "node_modules"]):
            continue

        # 3. Überspringe bereits übersetzte Dateien (Suffix-Check)
        if re.search(r'-[a-z]{2,3}lang\.md$', filename):
            continue

        # 4. skip .i18n
        if ".i18n" in filename:
            continue

        minimum_chars_changed = 30

        # 5. Skip files with fewer than 10 non-whitespace characters
        try:
            if Path(filename).stat().st_size < minimum_chars_changed:
                continue
            if len(Path(filename).read_text(encoding="utf-8", errors="ignore").strip()) < minimum_chars_changed:
                continue
        except OSError:
            continue

        source_file = Path(filename)






     
        if not re.search(r'-[a-z]{2,10}lang\.md$', filename):

            base_name = os.path.splitext(filename)[0]
            
            def is_fresh(l):
                tr = Path(f"{base_name}.i18n/{os.path.basename(base_name)}-{l}lang.md")
                return tr.exists() and tr.stat().st_mtime >= Path(filename).stat().st_mtime
            already_done = all(is_fresh(lang) for lang in TARGET_LANGS)

            if already_done:
                skipCount = skipCount + 1

                continue

        logger.info(f"Processing: …{str(filename)[-40:]}")
        process_file(filename)
        
        
        
        
    logger.info(f'->line 365: skipCount already translated: {skipCount}')

    #logger.info("----------------------------------------------------")
    logger.info("Alle Übersetzungen abgeschlossen!")

if __name__ == "__main__":
    main()
