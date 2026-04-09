# file: scripts/py/func/checks/check_slop_comments.py
import re
import sys
from collections import defaultdict
from pathlib import Path

# Patterns typical of LLM-generated comments that add no technical value.
# Each tuple: (regex, human-readable reason)
SLOP_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"#\s+This (function|method|class|script|block|code|part|checks? if|is how|would|could|will only)", re.IGNORECASE), "vague 'This X does Y' narration"),
    (re.compile(r"#\s+In order to\b", re.IGNORECASE),          "wordy 'in order to' phrasing"),
    (re.compile(r"#\s+Make sure\b", re.IGNORECASE),            "imperative without context"),
    (re.compile(r"#\s+We need to\b", re.IGNORECASE),           "first-person plural in source"),
    (re.compile(r"#\s+The following\b", re.IGNORECASE),        "textbook-style lead-in"),
    (re.compile(r"#\s+This is (a |an )?(simple|basic|rough|very rough)\b", re.IGNORECASE), "hedging qualifier"),
    (re.compile(r"#\s+You can\b", re.IGNORECASE),              "second-person address in source"),
    (re.compile(r"#\s+Note:\s+this\b", re.IGNORECASE),         "redundant 'Note: this' opener"),
    (re.compile(r"#\s+is responsible for\b", re.IGNORECASE),   "OOP-textbook phrasing"),
    (re.compile(r"#\s+mimics your original\b", re.IGNORECASE), "chat-session artifact"),
    (re.compile(r"#\s+(du |dein |deinen |deiner |deine )", re.IGNORECASE), "chat-session artifact (du/dein)"),
    (re.compile(r"#\s+Hier wird (es|die) (interessant|Magie)", re.IGNORECASE), "chat-session artifact"),
    (re.compile(r"#.*<=+\s*$"),                                "unfinished marker/arrow"),
]

GERMAN_MARKERS = re.compile(
    r"#.*\b(dieser?|diese[sn]?|werden|wurde[n]?|können|möglich|damit|wenn|aber|oder|auch|immer|"
    r"wird|nicht|noch|hier|dann|nach|über|unter|alle[sn]?|bitte|weil|damit|zwischen|wir|prüfen|"
    r"nutzen|bauen|suchen|löschen|laden|schreiben|laufen|passieren|müssen|sollen|können)\b",
    re.IGNORECASE,
)

SKIP_PATH_FRAGMENTS = [".i18n", "__pycache__", ".venv", "/venv/", "/docs/"]


def _skip(path: Path) -> bool:
    s = path.as_posix()
    return any(f in s for f in SKIP_PATH_FRAGMENTS)


def _scan_file(py_file: Path) -> list[dict]:
    hits: list[dict] = []
    try:
        lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return hits
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        for pattern, reason in SLOP_PATTERNS:
            if pattern.search(stripped):
                hits.append({"file": py_file, "line": lineno, "text": stripped, "reason": reason})
                break
        else:
            if GERMAN_MARKERS.search(stripped):
                hits.append({"file": py_file, "line": lineno, "text": stripped, "reason": "German in .py comment"})
    return hits


def scan(roots: list[Path]) -> list[dict]:
    hits: list[dict] = []
    seen: set[Path] = set()
    for root in roots:
        if root.is_file():
            if root not in seen:
                seen.add(root)
                hits.extend(_scan_file(root))
        else:
            for py_file in sorted(root.rglob("*.py")):
                if _skip(py_file) or py_file in seen:
                    continue
                seen.add(py_file)
                hits.extend(_scan_file(py_file))
    return hits


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    positional = [a for a in argv if not a.startswith("-")]

    default_roots: list[Path] = [Path("scripts/py"), Path("aura_engine.py")]
    roots = [Path(a) for a in positional] if positional else default_roots

    missing = [r for r in roots if not r.exists()]
    for m in missing:
        print(f"WARNING: path not found: {m}", file=sys.stderr)
    roots = [r for r in roots if r.exists()]
    if not roots:
        print("ERROR: no valid paths to scan", file=sys.stderr)
        return 2

    hits = scan(roots)
    if not hits:
        print("check_slop_comments: OK")
        return 0

    by_file: dict[Path, list[dict]] = defaultdict(list)
    for h in hits:
        by_file[h["file"]].append(h)

    sorted_files = sorted(by_file.items(), key=lambda kv: len(kv[1]), reverse=True)

    for py_file, file_hits in sorted_files:
        print(f"\n{'='*60}")
        print(f"  {py_file}  ({len(file_hits)} hit(s))")
        print(f"{'='*60}")
        for h in sorted(file_hits, key=lambda x: x["line"]):
            print(f"  :{h['line']:<6} [{h['reason']}]")
            print(f"         {h['text'][:120]}")

    total = sum(len(v) for v in by_file.values())
    print(f"\n{total} candidate(s) in {len(by_file)} file(s).", file=sys.stderr)
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
