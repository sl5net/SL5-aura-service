#!/usr/bin/env python3
"""
Semantic heading chunker for Algolia indexing.
Parses Sphinx HTML output and generates chunked records grouped by headings.
"""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


class SphinxHTMLChunker(HTMLParser):
    """Extracts sections, headings, anchors, and content chunks from Sphinx HTML."""

    IGNORE_TAGS = {"head", "script", "style", "nav", "footer", "header"}

    def __init__(self, relative_url: str, language: str) -> None:
        super().__init__()
        self.relative_url = relative_url
        self.language = language
        self.records: list[dict] = []
        self.current_h1: str = ""
        self.current_h2: str = ""
        self.current_h3: str = ""
        self.current_anchor: str = ""
        self.in_heading: int | None = None
        self.heading_text: list[str] = []
        self.current_text: list[str] = []
        self.ignore_depth: int = 0
        self.chunk_index: int = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.IGNORE_TAGS:
            self.ignore_depth += 1
            return

        if self.ignore_depth > 0:
            return

        attrs_dict = dict(attrs)

        if tag in ("section", "div", "article") and "id" in attrs_dict and attrs_dict["id"]:
            self.current_anchor = attrs_dict["id"]

        if tag in ("h1", "h2", "h3"):
            self._flush_chunk()
            self.in_heading = int(tag[1])
            self.heading_text = []
            if "id" in attrs_dict and attrs_dict["id"]:
                self.current_anchor = attrs_dict["id"]

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.IGNORE_TAGS:
            self.ignore_depth = max(0, self.ignore_depth - 1)
            return

        if self.ignore_depth > 0:
            return

        if tag in ("h1", "h2", "h3") and self.in_heading:
            text = " ".join("".join(self.heading_text).split())
            if self.in_heading == 1:
                self.current_h1 = text
                self.current_h2 = ""
                self.current_h3 = ""
            elif self.in_heading == 2:
                self.current_h2 = text
                self.current_h3 = ""
            elif self.in_heading == 3:
                self.current_h3 = text
            self.in_heading = None
            self.heading_text = []

    def handle_data(self, data: str) -> None:
        if self.ignore_depth > 0:
            return

        if self.in_heading:
            self.heading_text.append(data)
        else:
            self.current_text.append(data)

    def _flush_chunk(self) -> None:
        raw_text = " ".join("".join(self.current_text).split())
        self.current_text = []
        if not raw_text:
            return

        self.chunk_index += 1
        anchor_suffix = f"#{self.current_anchor}" if self.current_anchor else ""
        object_id = f"{self.relative_url}{anchor_suffix}_{self.chunk_index}"
        full_url = f"{self.relative_url}{anchor_suffix}"

        self.records.append({
            "objectID": object_id,
            "url": full_url,
            "anchor": self.current_anchor,
            "language": self.language,
            "hierarchy": {
                "lvl0": self.current_h1 or self.relative_url,
                "lvl1": self.current_h2,
                "lvl2": self.current_h3,
            },
            "content": raw_text,
            "type": "content",
        })

    def close(self) -> None:
        super().close()
        self._flush_chunk()


def extract_language_from_filename(filename: str) -> str:
    """Extracts language code from filename patterns like 'README-delang.html'."""
    match = re.search(r"-([a-zA-Z]{2}(?:-[a-zA-Z]{2,4})?)lang(?:\.|$)", filename)
    if match:
        return match.group(1).lower()
    return "en"


def generate_algolia_records(html_dir: Path, output_file: Path) -> list[dict]:
    """Scans HTML directory and generates an array of Algolia records."""
    all_records: list[dict] = []

    if not html_dir.exists():
        print(f"Error: HTML directory does not exist: {html_dir}", file=sys.stderr)
        return []

    html_files = sorted(html_dir.rglob("*.html"))
    for html_file in html_files:
        if html_file.name.startswith((".", "_")):
            continue

        relative_path = html_file.relative_to(html_dir).as_posix()
        language = extract_language_from_filename(html_file.name)

        content = html_file.read_text(encoding="utf-8", errors="replace")
        parser = SphinxHTMLChunker(relative_url=relative_path, language=language)
        parser.feed(content)
        parser.close()

        all_records.extend(parser.records)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_records)} Algolia records at {output_file}")
    return all_records


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    build_html_dir = script_dir / "_build" / "html"
    output_json_path = script_dir / "_build" / "algolia_records.json"

    generate_algolia_records(build_html_dir, output_json_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
