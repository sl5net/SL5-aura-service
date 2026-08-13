#!/usr/bin/env python3
# tools/translate_maps.py

import argparse
import re
import subprocess
import time
from pathlib import Path

HEADER_TEMPLATE = """# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

"""

# Common regex keywords and commands to keep untranslated
PRESERVED_KEYWORDS = {
    "git", "diff", "status", "re", "ignorecase", "systemd", "run",
    "clear", "python", "python3", "bash", "echo", "nohup", "xdg-open",
    "curl", "wget", "install", "ollama"
}

# def is_private_path(path_str: str) -> bool:
#     """Returns True if path belongs to a private folder starting with /_."""
#     return "/_" in path_str or "\\_" in path_str

def is_private_path(path: Path) -> bool:
    """Returns True if any path part (directory) starts with '_'."""
    for part in path.parts[:-1]:  # optional: include last part if you also want files named _foo.py excluded
        if part.startswith("_"):
            return True
    return False

def is_url_or_cli_line(text: str) -> bool:
    """Returns True if text contains URLs or CLI installation commands."""
    return bool(re.search(r"https?://|ftp://|curl\s+|wget\s+|pip\s+install|install\.sh", text, re.IGNORECASE))


def translate_text(text: str, target_lang: str) -> str:
    """Translates text using translate-shell (trans) CLI tool."""
    if not text.strip() or is_url_or_cli_line(text):
        return text

    cli_lang = target_lang.split("-")[0]
    try:
        res = subprocess.run(
            ["trans", "-b", "-s", "de", "-t", cli_lang, text],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode == 0 and res.stdout.strip():
            time.sleep(0.05)
            return res.stdout.strip()
    except Exception as e:
        print(f"Warning: Translation failed for '{text[:20]}...': {e}")
    return text


def translate_regex_pattern(pattern: str, target_lang: str) -> str:
    """Translates spoken words inside regex string while preserving operators and Python f-string variables."""
    def replace_token(match):
        token = match.group(0)
        # Preserve Python variables in f-strings like {unterstrichen}
        if token.startswith("{") and token.endswith("}"):
            return token
        if token.lower() in PRESERVED_KEYWORDS or len(token) <= 1:
            return token
        return translate_text(token, target_lang)

    return re.sub(r"\{[a-zA-Z0-9_]+\}|[a-zA-ZäöüÄÖÜß]+", replace_token, pattern)

def process_line(line: str, target_lang: str) -> str:
    """Processes and translates a single line of a Python map file."""
    if "# EXAMPLE:" in line:
        parts = line.split("# EXAMPLE:", 1)
        translated_example = translate_text(parts[1].strip(), target_lang)
        return f"{parts[0]}# EXAMPLE: {translated_example}\n"

    if line.strip().startswith("#") and not line.strip().startswith("#!"):
        comment_text = line.strip().lstrip("#").strip()
        if comment_text and not comment_text.startswith("="):
            translated_comment = translate_text(comment_text, target_lang)
            indent = line[:line.find("#")]
            return f"{indent}# {translated_comment}\n"

    def replace_raw_string(match):
        prefix = match.group(1)
        content = match.group(2)
        quote = match.group(3)
        translated = translate_regex_pattern(content, target_lang)
        return f"{prefix}{translated}{quote}"

    line = re.sub(r'(r[\'"])(.*?)([\'"])', replace_raw_string, line)
    return line


def translate_map_file(source_path: Path, target_path: Path, target_lang: str, force: bool = False) -> bool:
    """Translates a source de-DE map file to target language if source is newer."""
    if not force and target_path.exists():
        if target_path.stat().st_mtime >= source_path.stat().st_mtime:
            return False

    print(f"Translating: {source_path.name} -> {target_lang}")
    try:
        source_content = source_path.read_text(encoding="utf-8")
        lines = source_content.splitlines()

        translated_lines = []
        for line in lines:
            translated_lines.append(process_line(line, target_lang))

        target_path.parent.mkdir(parents=True, exist_ok=True)
        final_content = HEADER_TEMPLATE + "\n".join(translated_lines) + "\n"
        target_path.write_text(final_content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error translating '{source_path}': {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AURA Map Auto-Translator (de-DE -> target language)")
    parser.add_argument("--target-lang", default="en-US", help="Target language code (e.g. en-US, es-ES)")
    parser.add_argument("--force", action="store_true", help="Force translation even if target is up-to-date")
    parser.add_argument("--demo", "--dry-run", action="store_true", help="Demo mode: list target files without translating or writing")
    args = parser.parse_args()



    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    maps_dir = project_root / "config" / "maps"


    all_source_files = list(maps_dir.glob("**/de-DE/*.py"))

    # Filter out private folders starting with /_
    # source_files = [f for f in all_source_files if not is_private_path(str(f))]
    source_files = [f for f in all_source_files if not is_private_path(f)]

    total_files = len(source_files)
    print(f"Found {total_files} public de-DE map files (ignored {len(all_source_files) - total_files} private files).")





    translated_count = 0
    start_time = time.time()

    for i, src in enumerate(source_files):
        target_path_str = str(src).replace("/de-DE/", f"/{args.target_lang}/")
        target_path = Path(target_path_str)

        processed = i + 1
        elapsed = time.time() - start_time
        avg_time = elapsed / processed if processed > 0 else 0
        remaining = total_files - processed
        eta_sec = remaining * avg_time
        eta_str = f"{int(eta_sec)}s" if eta_sec < 60 else f"{int(eta_sec/60)}m {int(eta_sec%60)}s"
        pct = int((processed / total_files) * 100)

        rel_src = src.relative_to(maps_dir)
        print(f"[{processed:2d}/{total_files} | {pct:3d}% | ETA: {eta_str:6s}] Processing: {rel_src}")

        if args.demo:
            print(f"[{processed:2d}/{total_files} | {pct:3d}% | DEMO] Would translate: {rel_src} -> {target_path}")
            translated_count += 1
        else:
            if translate_map_file(src, target_path, args.target_lang, force=args.force):
                translated_count += 1

        # print(f"\nTranslation completed. Updated {translated_count} map files for '{args.target_lang}'.")

        summary_action = "Would update" if args.demo else "Updated"
        print(f"\nCompleted. {summary_action} {translated_count} map files for '{args.target_lang}'.")


if __name__ == "__main__":
    main()
