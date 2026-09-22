# tools/i18n/section_cache.py
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Dict, List, Optional, Union

# Determine log path: two folders up, then "log/i18n_section_cache.log"
SCRIPT_PATH = Path(__file__).resolve()
LOG_PATH = SCRIPT_PATH.parents[2] / "log"
LOG_FILE = LOG_PATH / "i18n_section_cache.log"

# Ensure log dir exists
LOG_PATH.mkdir(parents=True, exist_ok=True)

# Configure module-level logger
logger = logging.getLogger("i18n_section_cache")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if module is reloaded
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

logger.info("Logger initialized. Log file: %s", LOG_FILE)


def compute_section_hash(text: str) -> str:
    logger.info("Computing hash for section (length=%d characters)", len(text))
    try:
        encoded_text = text.encode("utf-8")
        logger.debug("Encoded text to UTF-8 (bytes=%d)", len(encoded_text))
        h = hashlib.sha256(encoded_text).hexdigest()
        logger.info("Successfully computed SHA-256 hash: %s", h)
        return h
    except Exception as exc:
        logger.exception("Failed to compute hash: %s", exc)
        raise


def split_markdown_by_h2(content: str) -> List[str]:
    logger.info("Splitting markdown content into H2 sections (total length=%d)", len(content))
    code_block_pattern = r"(```[\s\S]*?```)"
    try:
        parts = re.split(code_block_pattern, content)
        logger.debug("Content split into %d raw parts (code-block separation)", len(parts))

        sections: List[str] = []
        current: List[str] = []

        for idx, part in enumerate(parts):
            if part.startswith("```") and part.endswith("```"):
                logger.debug("Part %d is a code block, keeping with current section", idx)
                current.append(part)





            else:
                subparts = re.split(r"(?m)(?=^#{2,6} )", part)
                for sub in subparts:
                    if not sub:
                        continue
                        
                    if re.match(r"^#{2,6} ", sub) and current:
                        logger.debug("New H%d+ section encountered. Finalizing previous section", sub.count("#", 0, sub.find(" ")))
                        sections.append("".join(current))
                        current = []

                    table_pieces = [p for p in re.split(r"((?:^[ \t]*\|[^\n]*(?:\n|\Z))+)", sub, flags=re.MULTILINE) if p]
                    for piece in table_pieces:
                        if re.match(r"^[ \t]*\|", piece):
                            if current:
                                sections.append("".join(current))
                                current = []
                            sections.append(piece)
                        else:
                                current.append(piece)




        if current:
            sections.append("".join(current))

        result_sections = sections if sections else [content]
        logger.info("Markdown successfully split into %d section(s)", len(result_sections))
        return result_sections
    except Exception as exc:
        logger.exception("Error while splitting markdown: %s", exc)
        raise


def load_cache(cache_file: Path) -> Dict:
    logger.info("Attempting to load cache from: %s", cache_file)
    if not cache_file.exists():
        logger.info("Cache file does not exist (%s), returning empty cache dict", cache_file)
        return {}

    try:
        logger.info("Reading cache file content: %s", cache_file)
        text = cache_file.read_text(encoding="utf-8")
        logger.debug("Raw cache text read (bytes=%d)", len(text))

        logger.info("Parsing JSON cache data")
        data = json.loads(text)

        if not isinstance(data, dict):
            logger.warning("Cache file %s does not contain a valid JSON object/dict, returning empty cache", cache_file)
            return {}

        logger.info("Successfully loaded cache with %d entries from %s", len(data), cache_file)
        return data
    except Exception as exc:
        logger.exception("Failed to read or parse cache file %s: %s", cache_file, exc)
        return {}


def save_cache(cache_file: Union[str, Path], cache_data: Dict) -> None:
    """
    Atomically save cache_data to cache_file. Refuses to overwrite with non-dict or empty dict.
    Uses a tempfile in the same directory, fsyncs file contents, atomically replaces,
    and attempts to fsync the directory entry for maximum durability on POSIX.
    """
    cache_file = Path(cache_file)
    logger.info("Starting save_cache process for: %s", cache_file)

    # Step 1: Validate input
    if not isinstance(cache_data, dict):
        logger.error("Validation failed: cache_data must be a dict, got %s", type(cache_data).__name__)
        raise TypeError("cache_data must be a dict")

    if not cache_data:
        logger.warning(
            "Refusing to save: cache_data is empty (no entries). Not overwriting %s",
            cache_file,
        )
        return

    logger.info("Validating cache data: %d section hashes to persist", len(cache_data))

    # Step 2: Ensure target directory exists
    parent_dir = cache_file.parent
    logger.info("Ensuring target directory exists: %s", parent_dir)
    parent_dir.mkdir(parents=True, exist_ok=True)

    # Step 3: Serialize to JSON
    logger.info("Serializing cache_data to JSON")
    try:
        text = json.dumps(cache_data, ensure_ascii=False, indent=2)
        logger.info("JSON serialization complete (size=%d bytes)", len(text.encode("utf-8")))
    except Exception as exc:
        logger.exception("Failed to serialize cache data to JSON: %s", exc)
        raise

    tmp_path: Optional[Path] = None

    # Step 4: Write to temporary file in the same directory
    try:
        logger.info("Creating temporary file in directory: %s", parent_dir)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(parent_dir)) as tmp:
            tmp_path = Path(tmp.name)
            logger.info("Created temp file: %s. Writing payload", tmp_path)
            tmp.write(text)

            logger.debug("Flushing buffer to disk")
            tmp.flush()

            logger.debug("Executing os.fsync on file descriptor")
            os.fsync(tmp.fileno())
            logger.info("Temp file write and fsync completed successfully")

        # Step 5: Atomic replacement
        logger.info("Atomically replacing %s with temp file %s", cache_file, tmp_path)
        tmp_path.replace(cache_file)
        logger.info("Atomic replace succeeded: %s updated", cache_file)

        # Step 6: Fsync parent directory (POSIX durability)
        logger.debug("Attempting to fsync parent directory: %s", parent_dir)
        try:
            dir_fd = os.open(str(parent_dir), os.O_DIRECTORY | os.O_RDONLY)
            try:
                os.fsync(dir_fd)
                logger.debug("Parent directory fsync succeeded")
            finally:
                os.close(dir_fd)
        except Exception:
            # Best-effort: nicht kritisch auf Systemen ohne Directory-Fsync-Support (z. B. Windows)
            logger.debug("Directory fsync not supported or failed on this platform (ignorable)", exc_info=True)

        logger.info(
            "Cache successfully saved to %s (entries=%d, bytes=%d)",
            cache_file,
            len(cache_data),
            len(text),
        )
    except Exception as exc:
        logger.exception("Failed to save cache to %s: %s", cache_file, exc)
        # Step 7: Clean up temp file on failure
        if tmp_path is not None and tmp_path.exists():
            logger.warning("Cleaning up temporary file after failure: %s", tmp_path)
            try:
                tmp_path.unlink()
                logger.info("Temporary file %s removed", tmp_path)
            except Exception:
                logger.exception("Failed to remove temp file %s", tmp_path)
        raise


def get_cached_translation(cache_data: Dict, section_hash: str, lang: str) -> Optional[str]:
    logger.info("Fetching cached translation for hash=%s, lang=%s", section_hash, lang)
    try:
        section_entry = cache_data.get(section_hash)
        if section_entry is None:
            logger.info("Cache miss: section hash %s not found in cache", section_hash)
            return None

        result = section_entry.get(lang)
        if result is not None:
            logger.info("Cache hit: found translation for hash=%s, lang=%s (len=%d)", section_hash, lang, len(result))
        else:
            logger.info("Cache miss: hash %s exists, but lang '%s' not present", section_hash, lang)
        return result
    except Exception as exc:
        logger.exception("Error accessing cache for hash=%s, lang=%s: %s", section_hash, lang, exc)
        return None


def store_cached_translation(
        cache_data: Dict, section_hash: str, lang: str, translated: str
) -> None:
    logger.info(
        "Storing translation in cache dict for hash=%s, lang=%s (translated_len=%d)",
        section_hash,
        lang,
        len(translated),
    )
    try:
        if section_hash not in cache_data:
            logger.debug("Creating new cache bucket for hash=%s", section_hash)
            cache_data[section_hash] = {}

        is_overwrite = lang in cache_data[section_hash]
        cache_data[section_hash][lang] = translated

        if is_overwrite:
            logger.info("Updated existing translation for hash=%s, lang=%s in-memory", section_hash, lang)
        else:
            logger.info("Stored new translation for hash=%s, lang=%s in-memory", section_hash, lang)

        logger.debug("Note: Translation is in-memory only; call save_cache() to persist to disk")
    except Exception as exc:
        logger.exception("Failed to store translation in-memory for hash=%s: %s", section_hash, exc)
        raise


# Optional small helper for CLI testing
if __name__ == "__main__":
    logger.info("Module run as script. Running a quick self-test.")
    sample = "# Title\n\n## Section A\nSome text\n\n## Section B\nMore text\n"
    try:
        logger.info("Running self-test step 1: Splitting markdown sample")
        sections = split_markdown_by_h2(sample)

        logger.info("Running self-test step 2: Computing section hashes")
        for idx, s in enumerate(sections):
            h = compute_section_hash(s)
            logger.info("Section %d hash: %s", idx, h)

        cache_fp = SCRIPT_PATH.parents[1] / "cache" / "i18n_sections.json"
        logger.info("Running self-test step 3: Loading cache from %s", cache_fp)
        cache = load_cache(cache_fp)

        logger.info("Running self-test step 4: Storing translation in memory")
        first_hash = compute_section_hash(sections[0])
        store_cached_translation(cache, first_hash, "es", "Traducción de prueba")

        logger.info("Running self-test step 5: Saving cache to disk")
        save_cache(cache_fp, cache)

        logger.info("Self-test completed successfully (OK)")
    except Exception:
        logger.exception("Self-test failed")
        sys.exit(1)
        
        
