
import hashlib
import json
from pathlib import Path
import re


def compute_section_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_markdown_by_h2(content: str) -> list[str]:
    code_block_pattern = r"(```[\s\S]*?```)"
    parts = re.split(code_block_pattern, content)
    sections = []
    current: list[str] = []

    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            current.append(part)
        else:
            subparts = re.split(r"(?m)(?=^## )", part)
            for sub in subparts:
                if not sub:
                    continue
                if sub.startswith("## ") and current:
                    sections.append("".join(current))
                    current = [sub]
                else:
                    current.append(sub)

    if current:
        sections.append("".join(current))

    return sections if sections else [content]


def load_cache(cache_file: Path) -> dict:
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache_file: Path, cache_data: dict) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = cache_file.with_suffix(".tmp")
    temp_file.write_text(
        json.dumps(cache_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_file.replace(cache_file)


def get_cached_translation(cache_data: dict, section_hash: str, lang: str) -> str | None:
    return cache_data.get(section_hash, {}).get(lang)


def store_cached_translation(
    cache_data: dict, section_hash: str, lang: str, translated: str
) -> None:
    if section_hash not in cache_data:
        cache_data[section_hash] = {}
    cache_data[section_hash][lang] = translated
