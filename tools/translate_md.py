#!/usr/bin/env python3
# tools/translate_md.py
import os
import glob
import subprocess
import time
import re
from pathlib import Path
import fcntl
import random

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
# Options: "fallback" (on engine failure), "primary" (Argos first), "only" (strictly offline), "off"
ARGOS_MODE = "fallback"
# ARGOS_MODE = "primary"
# ARGOS_MODE = "only"

# pkill -f translate_md.py

# tools/search.sh test_minimal log -e log 



# TARGET_LANGS = ["de", "pt", "es", "fr"]
# TARGET_LANGS = ["de"]
#TARGET_LANGS = ["de","pt","pt-BR","es","fr","ja","ko","hi","zh-CN","pl","ar"]

TARGET_LANGS = ["ar", "de", "en", "es", "fr", "hi", "ja", "ko", "pl", "pt", "pt-BR", "zh-CN"]


# cache_file_i18n = script_dir / "i18n" / ".translation_cache.json"
cooldown_file = script_dir / "i18n" / "engine_cooldowns.json"


log_dir = script_dir.parent / "log"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "translate_md.log"



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


    from tools.i18n.engine_fallback import (
        load_cooldowns,
        translate_with_engine_fallback,
    )
    from tools.i18n.argos_engine import translate_with_argos
    from tools.i18n.detect_language import detect_source_language
    
except ImportError:
    from i18n.argos_engine import translate_with_argos
    from i18n.detect_language import detect_source_language
    from i18n.section_cache import (
        compute_section_hash,
        get_cached_translation,
        load_cache,
        save_cache,
        split_markdown_by_h2,
        store_cached_translation,
    )
    from i18n.engine_fallback import (
        load_cooldowns,
        translate_with_engine_fallback,
    )



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
        if not new_path.startswith('../'):
            new_path = f"../{new_path}"
        new_link = f"{link_text}({new_path})"

        logger.info(f"     + Modifying to: {new_link}")
        return new_link

    # Use re.sub with our replacement function to process all links in the line
    return markdown_link_pattern.sub(replace_link, line)

# 
# def is_translatable_line(line: str) -> bool:
#     s = line.strip()
#     if not s:
#         return False
#     if s.startswith("<!--") and s.endswith("-->"):
#         return False
#     if re.fullmatch(r"(?:XMDLINK\d+X\s*)+", s):
#         return False
#     if re.fullmatch(r"<[^>]+>", s):
#         return False
#     if re.match(r"^__CODE_BLOCK_\d+__$", s):
#         return False
#     return True
# 

# ---
def is_translatable_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s.startswith("<!--") and s.endswith("-->"):
        return False
    cleaned = re.sub(r"XMDLINK\d+X", "", s)
    cleaned = re.sub(r"XINLINECODE\d+X", "", cleaned)
    cleaned = re.sub(r"XHTMLTAG\d+X", "", cleaned)
    
    cleaned = re.sub(r"__CODE_BLOCK_\d+__", "", cleaned)
    cleaned = re.sub(r"XDUNDERX|XSPACEBREAKX", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = re.sub(r"\[\s*\]\([^\)]*\)", "", cleaned)
    return bool(re.search(r"[a-zA-Z]", cleaned))


# ---
def translate_section(section_text: str, lang: str, source_lang: str = SOURCE_LANG) -> str | None:    
    original_lines = section_text.split("\n")

    markdown_links = []

    def link_replacer(match):
        placeholder = MD_LINK_PLACEHOLDER_FORMAT.format(len(markdown_links))
        markdown_links.append(match.group(0))
        return placeholder

    # link_regex = re.compile(r"!?(?:\[[^\]]*\])\((?:[^\)]*)\)")
    link_regex = re.compile(r"\[\s*!\[[^\]]*\]\([^\)]*\)\s*\]\([^\)]*\)|!?\[[^\]]*\]\([^\)]*\)")

    html_tags = []

    def html_replacer(match):
        placeholder = f"XHTMLTAG{len(html_tags)}X"
        html_tags.append(match.group(0))
        return placeholder

    # link2_tags = [] #     (http
    # def link2_replacer(match):
    #     placeholder = f"link2LTAG{len(html_tags)}X"
    #     link2_tags.append(match.group(0))
    #     return placeholder

    inline_codes = []

    def inline_code_replacer(match):
        placeholder = f"XINLINECODE{len(inline_codes)}X"
        inline_codes.append(match.group(0))
        return placeholder

    inline_code_regex = re.compile(r"`[^`\n]+`")
    
    # html_tag_regex = re.compile(r"<[^>]+>")
    html_tag_regex = re.compile(r"<(?!/?summary\b)[^>]+>")
    
    lines_step_link = [link_regex.sub(link_replacer, line) for line in original_lines]
    lines_step_inline = [inline_code_regex.sub(inline_code_replacer, line) for line in lines_step_link]
    lines_step0 = [html_tag_regex.sub(html_replacer, line) for line in lines_step_inline]

    lines_step2 = [line.replace("__", DUNDER_PLACEHOLDER) for line in lines_step0]
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


    translatable_indices = [
        idx for idx, line in enumerate(lines_for_translation) if is_translatable_line(line)
    ]
    raw_lines_to_send = [lines_for_translation[idx] for idx in translatable_indices]

    line_prefixes = []
    line_suffixes = []
    lines_to_send = []
    for line in raw_lines_to_send:

        p = ""
        m_p = re.match(r"^(\s*[>│├└─┌┬┴\s]+)", line)
        if m_p:
            p += m_p.group(1)
        rest = line[len(p):]
        if rest.startswith("<summary>"):
            p += "<summary>"
            rest = rest[len("<summary>"):]

        m_list = re.match(r"^([-*+]\s+|\d+\.\s+)", rest)
        if m_list:
            p += m_list.group(1)
            rest = rest[len(m_list.group(1)):]

        s = ""


        if rest.rstrip().endswith("</summary>"):
            idx = rest.rfind("</summary>")
            s = rest[idx:]
            rest = rest[:idx]
        
        m_s = re.search(r"([\U00010000-\U0010ffff\u2600-\u27bf\s]+)$", rest)
        if m_s:
            cand = m_s.group(1)
            if any(ord(c) > 127 for c in cand) or cand.endswith("  ") or cand.endswith("\t"):
                s = cand + s
                rest = rest[:-len(cand)]

        line_prefixes.append(p)
        line_suffixes.append(s)
        lines_to_send.append(rest)        
    if not lines_to_send:
        translated_lines = list(lines_for_translation)
    else:
        text_to_translate = "\n".join(lines_to_send)

        raw_translated = None
        if ARGOS_MODE in ("primary", "only"):
            raw_translated = translate_with_argos(text_to_translate, source_lang, lang)

        if not raw_translated and ARGOS_MODE != "only":
            cooldowns = load_cooldowns(cooldown_file)
            raw_translated = translate_with_engine_fallback(
                text=text_to_translate,
                source_lang=source_lang,
                target_lang=lang,
                cooldowns=cooldowns,
                cooldown_file=cooldown_file,
                timeout=40,
            )
    
            if not raw_translated and ARGOS_MODE == "fallback":
                raw_translated = translate_with_argos(text_to_translate, source_lang, lang)



        if not raw_translated:
            last_error_file = log_dir / "i18n_last_error_segment.log"
            last_error_file.write_text(section_text, encoding="utf-8")
            print(f"      [ERROR] All translation engines failed for '{lang}'.")
            return None

        if len(raw_translated) != len(lines_to_send):
            logger.warning(
                "Line count mismatch for '%s': expected %d, got %d",
                lang,
                len(lines_to_send),
                len(raw_translated),
            )
            return None

        translated_lines = list(lines_for_translation)
        for idx, prefix, suffix, trans_line in zip(
            translatable_indices, line_prefixes, line_suffixes, raw_translated
        ):
            translated_lines[idx] = f"{prefix}{trans_line}{suffix}"

            restored_step_a = []
            for line in translated_lines:
                code_match = re.match(r"^__CODE_BLOCK_(\d+)__$", line.strip())
                if code_match:
                    idx = int(code_match.group(1))
                    if idx < len(code_blocks):
                        restored_step_a.extend(code_blocks[idx].split("\n"))
                        continue
                restored_step_a.append(line)

            restored_step_b = []
            placeholder_regex = re.compile(r"(XMDLINK\d+X)")
            for line in restored_step_a:
                restored_line = line
                placeholders_in_line = placeholder_regex.findall(restored_line)
                for placeholder in placeholders_in_line:
                    link_index = int(re.search(r"\d+", placeholder).group())
                    if link_index < len(markdown_links):
                        original_link = markdown_links[link_index]
                        modified_link = add_lang_to_md_links(original_link, lang)
                        restored_line = restored_line.replace(placeholder, modified_link, 1)
                restored_step_b.append(restored_line)

        
        
        
            html_placeholder_regex = re.compile(r"(XHTML[TL]*TAG\d+X)")
            
            restored_step_html = []
            for line in restored_step_b:
                restored_line = line
                placeholders_in_line = html_placeholder_regex.findall(restored_line)
                for placeholder in placeholders_in_line:
                    idx = int(re.search(r"\d+", placeholder).group())
                    if idx < len(html_tags):
                        restored_line = restored_line.replace(placeholder, html_tags[idx], 1)
                restored_step_html.append(restored_line)
        
            inline_placeholder_regex = re.compile(r"(XINLINECODE\d+X)")
            
            restored_step_inline = []
            for line in restored_step_html:
                restored_line = line
                placeholders_in_line = inline_placeholder_regex.findall(restored_line)
                for placeholder in placeholders_in_line:
                    idx = int(re.search(r"\d+", placeholder).group())
                    if idx < len(inline_codes):
                        restored_line = restored_line.replace(placeholder, inline_codes[idx], 1)
                restored_step_inline.append(restored_line)

            restored_step_c = [
                line.replace(DUNDER_PLACEHOLDER, "__") for line in restored_step_inline
            ]

            guaranteed_lines = []
            for i, line in enumerate(restored_step_c):
                guaranteed_lines.append(line)
                if "</summary>" in line and i + 1 < len(restored_step_c) and restored_step_c[i + 1].strip() != "":
                    guaranteed_lines.append("")

            return "\n".join(guaranteed_lines)        
        
        
        
def compute_adaptive_delay(content_length: int, base_seconds: float = 12.0, char_rate: float = 100.0) -> float:
    jitter = random.uniform(14.0, 18.0)
    return base_seconds + (content_length / char_rate) + jitter

def harmonize_newlines(reference_text: str, target_text: str) -> str:
    cleaned_target = re.sub(r"(?i)XSPACE\s*BREAK\s*X", "  ", target_text)
    cleaned_target = re.sub(r"(</summary>[ \t]*\n)(?!\s*\n)", r"\1\n", cleaned_target)

    ref_lines = reference_text.split("\n")
    tgt_lines = cleaned_target.split("\n")
    if len(ref_lines) == len(tgt_lines):
        for i, ref_l in enumerate(ref_lines):
            if ref_l.endswith("  ") and not tgt_lines[i].endswith("  "):
                tgt_lines[i] = tgt_lines[i].rstrip() + "  "
        cleaned_target = "\n".join(tgt_lines)

    leading_count = len(reference_text) - len(reference_text.lstrip("\n"))
    trailing_count = len(reference_text) - len(reference_text.rstrip("\n"))
    return ("\n" * leading_count) + cleaned_target.strip("\n") + ("\n" * trailing_count)

def process_file(filename):
    
    with open(filename, "r", encoding="utf-8") as f:
        raw_content = f.read()

    source_lang = detect_source_language(raw_content, default=SOURCE_LANG)
    sections = split_markdown_by_h2(raw_content)
    base_name = os.path.splitext(filename)[0]
    i18n_dir = f"{base_name}.i18n"
    # global cache_file_i18n
    cache_file_i18n = Path(i18n_dir) / ".translation_cache.json"
    cache_data = load_cache(cache_file_i18n)


    target_languages = [lang for lang in TARGET_LANGS if lang != source_lang]
        
    for lang in target_languages:
        
        os.makedirs(i18n_dir, exist_ok=True)
        output_file = f"{i18n_dir}/{os.path.basename(base_name)}-{lang}lang.md"

        output_path = Path(output_file)
        if (
                output_path.exists()
                and output_path.stat().st_mtime > Path(filename).stat().st_mtime
        ):
            continue

        print(f"📁📄  -> Processing '{lang}' -> '{output_file}'…")

        translated_sections = []
        has_cache_miss = False
        section_failed = False

        for section in sections:
            sec_hash = compute_section_hash(section)
            cached_text = get_cached_translation(cache_data, sec_hash, lang)

            if cached_text is not None:
                translated_sections.append(harmonize_newlines(section, cached_text))
            else:
                has_cache_miss = True

                translated = translate_section(section, lang, source_lang=source_lang)
                if translated is None:
                    print(f"      [SKIP] Failed to translate section for '{lang}', aborting file write.")
                    section_failed = True
                    break
                translated = harmonize_newlines(section, translated)
                store_cached_translation(cache_data, sec_hash, lang, translated)
                
                save_cache(cache_file_i18n, cache_data)          
                logger.info(f"      -> Section cached (hash={sec_hash[:8]}…, lang='{lang}')")

                translated_sections.append(translated)
                delay_sec = compute_adaptive_delay(len(section))
                time.sleep(delay_sec)
                
        if section_failed:
            continue

        full_output = "".join(translated_sections)


        output_lines = full_output.splitlines()

        if len(output_lines) < 1:
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
        
        
        if any(
                line.strip().startswith("https://translate.google.com")
                for line in output_lines
        ):
            print(
                f"      [SKIP] Output for '{lang}' contains redirect URL, skipping write."
            )
            return 
        if len(full_output) < (len(raw_content) * 0.35):
            print(
                f"      [SKIP] Output for '{lang}' is suspiciously short, skipping write."
            )
            return 

        orig_name = os.path.basename(filename)
        disclaimer = (
            f"> ℹ️ *This is a machine-translated document. "
            f"In case of discrepancies, refer to the [original document](../{orig_name}).*\n\n"
        )
        if not full_output.startswith("> ℹ️ *This is a machine-translated document"):
            full_output = disclaimer + full_output

        print(f"📁📄      -> Saving file '{output_file}'…")
        with open(output_file, "w", encoding="utf-8") as f:

            f.write(full_output)
            time.sleep(7)

        # def save_cache(cache_file: Path, cache_data: dict) -> None:
        if has_cache_miss:
            time.sleep(7)

def main():

    lock_file = open(log_dir / "translate_md.lock", "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        logger.warning("Another instance of translate_md.py is already running. Exiting. Tips/Idea:")
        logger.info("pkill -f translate_md.py")
        logger.info("________________________")
        sys.exit(0)

    # test_translation_links()
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

        if not re.search(r'-[a-z]{2,10}lang\.md$', filename):

            base_name = os.path.splitext(filename)[0]
            
            def is_fresh(l):
                tr = Path(f"{base_name}.i18n/{os.path.basename(base_name)}-{l}lang.md")
                return tr.exists() and tr.stat().st_mtime >= Path(filename).stat().st_mtime

            try:
                with open(filename, "r", encoding="utf-8") as f_check:
                    file_head = f_check.read(1500)
                file_source_lang = detect_source_language(file_head, default=SOURCE_LANG)
            except Exception:
                file_source_lang = SOURCE_LANG

            active_targets = [l for l in TARGET_LANGS if l != file_source_lang]
            already_done = all(is_fresh(lang) for lang in active_targets)
            if already_done:
                skipCount = skipCount + 1

                continue

        logger.info(f"Processing: …{str(filename)[-40:]}")
        process_file(filename)
        
    logger.info(f'->line 365: skipCount already translated: {skipCount}')
    logger.info("----------------------------------------------------")

if __name__ == "__main__":
    main()
