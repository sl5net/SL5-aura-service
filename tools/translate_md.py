#!/usr/bin/env python3
# tools/translate_md.py
import os
import glob
import subprocess
import time
import re
import sys
from pathlib import Path

# search_path = script_dir.parent / 'docs' / 'Feature_Spotlight' / 'Implementing*.md'

# ==============================================================================
#           Intelligenter Markdown-Übersetzer (Python-Version)
# ==============================================================================
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

# Setup a simple logger for demonstration
logging.basicConfig(level=logging.INFO, format='%(message)s')
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
        print(f"{original:<40} | {modified:<40}")







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

def process_file(filename):
    """Verarbeitet eine einzelne Markdown-Datei."""
    print(f"Bearbeite Datei: '{filename}'")

    with open(filename, 'r', encoding='utf-8') as f:
        original_lines = [line.rstrip('\n') for line in f.readlines()]

    # --- Schritt 0: Schütze komplette Markdown Links/Bilder ---
    print("   -> Schritt 0: Schütze komplette Markdown Links/Bilder...")
    markdown_links = []
    def link_replacer(match):
        # ### GEÄNDERT: Verwendet das neue, sichere Format ###
        placeholder = MD_LINK_PLACEHOLDER_FORMAT.format(len(markdown_links))
        markdown_links.append(match.group(0))
        return placeholder

    link_regex = re.compile(r'!?(?:\[[^\]]*\])\((?:[^\)]*)\)')
    lines_step0 = [link_regex.sub(link_replacer, line) for line in original_lines]
    print(f"      Markdown-Strukturen gefunden und ersetzt: {len(markdown_links)}")

    # --- Schritt 1 & 2 & 3 bleiben identisch ---
    print("   -> Schritt 1: Ersetze Hard-Breaks (zwei Leerzeichen) durch einen Platzhalter...")
    lines_step1 = []
    hard_breaks_found_count = 0
    for line in lines_step0:
        if line.endswith("  "):
            hard_breaks_found_count += 1
            lines_step1.append(line[:-2] + HARD_BREAK_PLACEHOLDER)
        else:
            lines_step1.append(line)
    print(f"      Hard-Breaks gefunden und ersetzt: {hard_breaks_found_count}")

    print("   -> Schritt 2: Schütze mittige '__' Zeichen...")
    lines_step2 = [line.replace("__", DUNDER_PLACEHOLDER) for line in lines_step1]

    print("   -> Schritt 3: Extrahiere Code-Blöcke...")
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
    print(f"      Code-Blöcke extrahiert: {len(code_blocks)}")

    text_to_translate = "\n".join(lines_for_translation)

    # --- SCHLEIFE DURCH ZIELSPRACHEN ---
    base_name = os.path.splitext(filename)[0]
    for lang in TARGET_LANGS:

        # output_file = script_dir.parent / 'docs' / 'Feature_Spotlight' / 'Implementing*.md'



        # output_file = f"{base_name}-{lang}lang.md"


        # NEU:
        i18n_dir = f"{base_name}.i18n"
        os.makedirs(i18n_dir, exist_ok=True)
        output_file = f"{i18n_dir}/{os.path.basename(base_name)}-{lang}lang.md"



        if os.path.exists(output_file):
            print(f"   -> Überspringe '{output_file}' (existiert bereits).")
            continue

        print(f"   -> Übersetze nach '{lang}' -> '{output_file}'...")
        try:
            process = subprocess.run(
                ['trans', '-brief', f"{SOURCE_LANG}:{lang}"],
                input=text_to_translate, capture_output=True, text=True, encoding='utf-8', check=True
            )
            translated_lines = process.stdout.strip().split('\n')
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"      \033[0;31m[FEHLER]\033[0m bei der Übersetzung: {e}")
            continue

        # --- WIEDERHERSTELLUNG IN UMGEKEHRTER REIHENFOLGE ---

        print("      -> Schritt A: Stelle Code-Blöcke wieder her...")
        restored_step_A = []
        code_block_idx = 0
        for line in translated_lines:
            if re.match(r'^__CODE_BLOCK_\d+__$', line.strip()) and code_block_idx < len(code_blocks):
                restored_step_A.extend(code_blocks[code_block_idx].split('\n'))
                code_block_idx += 1
            else:
                restored_step_A.append(line)

        # ### GEÄNDERT: Logik zur Wiederherstellung der sicheren Platzhalter ###
        print("      -> Schritt B: Stelle Markdown Links/Bilder wieder her...")
# ### KORRIGIERT: Logik zur Wiederherstellung und Anpassung der Links ###
        print("      -> Schritt B: Stelle Markdown Links/Bilder wieder her und passe sie an...")
        restored_step_B = []
        placeholder_regex = re.compile(r'(XMDLINK\d+X)')

        for line in restored_step_A:
            restored_line = line
            # Finde alle Platzhalter in der aktuellen Zeile
            placeholders_in_line = placeholder_regex.findall(restored_line)

            for placeholder in placeholders_in_line:
                # Extrahiere die Indexnummer aus dem Platzhalter (z.B. 0 aus 'XMDLINK0X')
                link_index = int(re.search(r'\d+', placeholder).group())

                if link_index < len(markdown_links):
                    # 1. Hole den originalen Link aus der Liste
                    original_link = markdown_links[link_index]

                    # 2. Wende die Modifikationsfunktion auf den originalen Link an
                    #    Die Funktion ist robust genug, um eine Zeile zu verarbeiten, die nur aus einem Link besteht.
                    modified_link = add_lang_to_md_links(original_link, lang)

                    # 3. Ersetze den Platzhalter durch den MODIFIZIERTEN Link
                    restored_line = restored_line.replace(placeholder, modified_link, 1)

            restored_step_B.append(restored_line)


        print("      -> Schritt C: Stelle mittige '__' wieder her...")
        restored_step_C = [line.replace(DUNDER_PLACEHOLDER, "__") for line in restored_step_B]

        print(f"      -> Schritt D: Stelle {hard_breaks_found_count} Hard-Break(s) aus Platzhaltern wieder her...")
        final_lines = [line.replace(HARD_BREAK_PLACEHOLDER, "  ") for line in restored_step_C]

        print(f"      -> Speichere Datei '{output_file}'...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(final_lines))

        time.sleep(2)

def main():

    # test_translation_links()
    # sys.exit(1)

    print("Starte die intelligente Übersetzung von Markdown-Dateien...")
    print(f"Quellsprache: {SOURCE_LANG}")
    print(f"Zielsprachen: {TARGET_LANGS}")


    # search_path = script_dir.parent / 'docs' / 'Feature_Spotlight' / 'Implementing*.md'
    # search_path = script_dir.parent / 'README.md' # alt
    search_path = script_dir.parent / '**' / '*.md' # neu


    print(f"---- {search_path} ------------------------------------------------")
    # for filename in glob.glob(str(search_path)):
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

        # 4. Überspringe, wenn die Datei in einem .i18n Ordner liegt
        if ".i18n" in filename:
            continue

        # eng ? de? fr?
        if not re.search(r'-([a-z]{2,3})\.md$', filename):

            # ALT:
            if not re.search(r'-([a-z]{2,3})\.md$', filename):
                process_file(filename)

                # NEU – angepasst an "lang"-Suffix-Format:
                if not re.search(r'-[a-z]{2,10}lang\.md$', filename):

                    base_name = os.path.splitext(filename)[0]
                    # Prüfe ob ALLE Zielsprachen bereits im .i18n Ordner existieren
                    already_done = all(
                        os.path.exists(f"{base_name}.i18n/{os.path.basename(base_name)}-{lang}lang.md")
                        for lang in TARGET_LANGS
                    )
                    if already_done:
                        print(f"   -> Überspringe '{filename}' (alle Übersetzungen bereits vorhanden).")
                        continue
                    process_file(filename)


            print(f"process_file({filename})")
            process_file(filename)
            print("")
    print("----------------------------------------------------")
    print("Alle Übersetzungen abgeschlossen!")

if __name__ == "__main__":
    main()
