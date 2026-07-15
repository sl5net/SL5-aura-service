#!/usr/bin/env python3
# scripts/search_rules/filter_maps_by_reality.py
import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path

# --- PATH LOGIC (cross-platform) ---
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text(encoding="utf-8").strip())
CACHE_FILE = tmp_dir / "sl5_aura" / "active_maps_cache.json"

# --- LOGGING ---
log_file = PROJECT_ROOT / "log" / "search_rules" / f"{Path(__file__).stem}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


def guess_lt_language_from_model(model_name):
    name = model_name.lower()
    if "-de-" in name or name == 'de':
        return "de-DE"
    elif "-en-" in name or name == 'en':
        return "en-US"
    elif "-fr-" in name or name == 'fr':
        return "fr-FR"
    return "de-DE"


def get_current_language():
    model_file = PROJECT_ROOT / "config" / "model_name.txt"
    if not model_file.exists():
        logger.warning("model_name.txt not found, defaulting to de-DE")
        return "de-DE"
    model_name = model_file.read_text(encoding="utf-8").strip()
    return guess_lt_language_from_model(model_name)


def get_compiled_regex(pattern):
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        logger.warning(f"Invalid regex pattern '{pattern}': {e}")
        return None


def is_window_title_skippable(active_title, only_in_list=None, exclude_list=None):
    if not only_in_list and not exclude_list:
        return False
    title_str = str(active_title) if active_title else ""
    if only_in_list:
        if not title_str:
            return True
        found_match = False
        for pattern in only_in_list:
            compiled_p = get_compiled_regex(pattern)
            if compiled_p and compiled_p.search(title_str):
                found_match = True
                break
        if not found_match:
            return True
    if exclude_list and title_str:
        for pattern in exclude_list:
            compiled_p = get_compiled_regex(pattern)
            if compiled_p and compiled_p.search(title_str):
                return True
    return False


def get_active_window_title():
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from scripts.py.func.get_active_window_title import get_active_window_title_safe
        return get_active_window_title_safe()
    except Exception as e:
        logger.warning(f"Failed to get window title via import: {e}")
        return os.environ.get("AURA_ACTIVE_WINDOW_TITLE", "")


def read_cache():
    if not CACHE_FILE.exists():
        logger.info(f"Cache file not found: {CACHE_FILE}")
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read cache: {e}")
        return None


def filter_by_window(cache_data, window_title):
    if not cache_data or "files" not in cache_data:
        logger.warning("Cache data empty or malformed")
        return []
    result = []
    for file_path, file_info in cache_data["files"].items():
        for rule in file_info.get("rules", []):
            opts = rule.get("options", {})
            only_in = opts.get("only_in_windows", [])
            exclude = opts.get("exclude_windows", [])
            if not is_window_title_skippable(window_title, only_in_list=only_in, exclude_list=exclude):
                result.append({
                    "file": file_path,
                    "line": rule.get("line", 0),
                    "match_phrase": rule.get("match_phrase", ""),
                    "replacement": rule.get("replacement", ""),
                })
    logger.info(f"Window filter: {len(result)} rules match title '{window_title}'")
    return result


def fallback_scan(maps_dir, lang_code):
    maps_path = Path(maps_dir).resolve()
    if not maps_path.exists():
        logger.error(f"Maps directory not found: {maps_path}")
        return []
    result = []
    for py_file in maps_path.rglob("*.py"):
        if lang_code in py_file.parts and py_file.name != "__init__.py":
            result.append({
                "file": py_file.as_posix(),
                "line": 1,
                "match_phrase": "",
                "replacement": "",
            })
    logger.info(f"Fallback scan found {len(result)} files for language {lang_code}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Filter maps by reality constraints")
    parser.add_argument("--lang-only", action="store_true", help="Filter by language only")
    parser.add_argument("--window-filter", action="store_true", help="Also filter by window title")
    parser.add_argument("--paths-only", action="store_true", help="Output only file paths")
    parser.add_argument("maps_dir", nargs="?", default="config/maps")
    args = parser.parse_args()

    lang_code = get_current_language()

    if args.lang_only:
        maps_path = Path(args.maps_dir).resolve()
        count = 0
        for py_file in maps_path.rglob("*.py"):
            if lang_code in py_file.parts and py_file.name != "__init__.py":
                print(py_file.as_posix())
                count += 1
        logger.info(f"Lang-only mode: {count} files for {lang_code}")
        return

    cache_data = read_cache()

    if cache_data and args.window_filter:
        window_title = get_active_window_title()
        filtered = filter_by_window(cache_data, window_title)
        for item in filtered:
            if args.paths_only:
                print(item["file"])
            else:
                print(f"{item['file']}:{item['line']}:{item['match_phrase']}")
    elif cache_data:
        for file_path in cache_data.get("files", {}):
            print(Path(file_path).as_posix())
    else:
        logger.warning("No cache found, falling back to direct scan")
        results = fallback_scan(args.maps_dir, lang_code)
        for item in results:
            print(item["file"])


if __name__ == "__main__":
    main()

