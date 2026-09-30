# clean_translation_cache.py
# Removes cache entries whose translated text contains a double language
# suffix in .md links (pattern: README-<xx>lang-<yy>lang.md).
# Default is dry-run. Use --apply to write (a backup is created first).
import argparse
import json
import logging
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.py.func.get_project_root import get_aura_project_root

PROJECT_ROOT = Path(get_aura_project_root())
LOG_FILE = PROJECT_ROOT / "log" / "clean_translation_cache.log"
DEFAULT_CACHE = PROJECT_ROOT / "README.i18n" / ".translation_cache.json"

LANG = r"[A-Za-z]{2}(?:-[A-Za-z]{2})?"
DOUBLE_SUFFIX = re.compile(rf"README-{LANG}lang-{LANG}lang\.md")


def setup_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("clean_translation_cache")


def is_bad(value):
    return isinstance(value, str) and DOUBLE_SUFFIX.search(value) is not None


def clean_dict(node, path, removed):
    result = {}
    for key, value in node.items():
        child_path = f"{path}/{str(key)[:12]}"
        if is_bad(value):
            removed.append(child_path)
            continue
        cleaned, changed = clean_node(value, child_path, removed)
        if changed and not cleaned:
            continue
        result[key] = cleaned
    return result


def clean_list(node, path, removed):
    result = []
    for index, value in enumerate(node):
        child_path = f"{path}[{index}]"
        if is_bad(value):
            removed.append(child_path)
            continue
        cleaned, _ = clean_node(value, child_path, removed)
        result.append(cleaned)
    return result


def clean_node(node, path, removed):
    before = len(removed)
    if isinstance(node, dict):
        cleaned = clean_dict(node, path, removed)
    elif isinstance(node, list):
        cleaned = clean_list(node, path, removed)
    else:
        cleaned = node
    return cleaned, len(removed) > before


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def backup_file(path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = PROJECT_ROOT / "log" / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, backup)
    return backup


def write_json(path, data):
    tmp_path = path.with_name(path.name + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def parse_args():
    parser = argparse.ArgumentParser(description="Remove double-suffix entries from the translation cache.")
    parser.add_argument("--cache", default=str(DEFAULT_CACHE))
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    logger = setup_logging()
    cache_path = Path(args.cache)
    if not cache_path.is_file():
        logger.error("Cache file not found: %s", cache_path)
        return 1
    try:
        data = load_json(cache_path)
    except (OSError, json.JSONDecodeError) as exc:
        logger.error("Cannot read cache: %s", exc)
        return 1
    removed = []
    cleaned, _ = clean_node(data, "", removed)
    for match_path in removed:
        logger.info("MATCH %s", match_path)
    logger.info("Total matches: %d", len(removed))
    if not removed:
        return 0
    if not args.apply:
        logger.info("Dry-run only. Use --apply to write.")
        return 0
    backup = backup_file(cache_path)
    write_json(cache_path, cleaned)
    logger.info("Written: %s | backup: %s", cache_path, backup)
    return 0


if __name__ == "__main__":
    sys.exit(main())

