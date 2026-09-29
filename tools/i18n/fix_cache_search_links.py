
import json
import re
from pathlib import Path

cache_file = Path("README.i18n/.translation_cache.json")
if cache_file.exists():
    with open(cache_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for sec_hash, translations in data.items():
        if isinstance(translations, dict):
            for lang, text in translations.items():
                if isinstance(text, str) and "search_online.html?lang=" in text:
                    translations[lang] = re.sub(
                        r"(search_online\.html\?lang=)[a-zA-Z0-9_-]+",
                        rf"\g<1>{lang}",
                        text,
                    )

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
