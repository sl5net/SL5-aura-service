# file: scripts/py/func/checks/check_slop_comments.py
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Pattern registry
# Each entry: (regex, reason_key, severity)
# severity: 3=chat artifact, 2=second-person/hedging, 1=narration/language
# ---------------------------------------------------------------------------
SLOP_PATTERNS: list[tuple[re.Pattern, str, int]] = [
    (re.compile(r"#\s+mimics your original\b", re.IGNORECASE),                      "chat-session artifact",          3),
    (re.compile(r"#\s+(du |dein |deinen |deiner |deine )", re.IGNORECASE),           "chat-session artifact (du/dein)", 3),
    (re.compile(r"#\s+Hier wird (es|die) (interessant|Magie)", re.IGNORECASE),       "chat-session artifact",          3),
    (re.compile(r"#.*<=+\s*$"),                                                      "unfinished marker/arrow",        3),
    (re.compile(r"#\s+This is (a |an )?(simple|basic|rough|very rough)\b", re.IGNORECASE), "hedging qualifier",        2),
    (re.compile(r"#\s+You can\b", re.IGNORECASE),                                   "second-person address in source", 2),
    (re.compile(r"#\s+We need to\b", re.IGNORECASE),                                "first-person plural in source",  2),
    (re.compile(r"#\s+In order to\b", re.IGNORECASE),                               "wordy 'in order to' phrasing",   2),
    (re.compile(r"#\s+Make sure\b", re.IGNORECASE),                                 "imperative without context",     2),
    (re.compile(r"#\s+Note:\s+this\b", re.IGNORECASE),                              "redundant 'Note: this' opener",  2),
    (re.compile(r"#\s+This (function|method|class|script|block|code|part|checks? if|is how|would|could|will only)", re.IGNORECASE), "vague 'This X does Y' narration", 1),
    (re.compile(r"#\s+The following\b", re.IGNORECASE),                             "textbook-style lead-in",         1),
    (re.compile(r"#\s+is responsible for\b", re.IGNORECASE),                        "OOP-textbook phrasing",          1),
]

GERMAN_MARKERS = re.compile(
    r"#.*\b(dieser?|diese[sn]?|werden|wurde[n]?|können|möglich|damit|wenn|aber|oder|auch|immer|"
    r"wird|nicht|noch|hier|dann|nach|über|unter|alle[sn]?|bitte|weil|zwischen|wir|prüfen|"
    r"nutzen|bauen|suchen|löschen|laden|schreiben|laufen|passieren|müssen|sollen)\b",
    re.IGNORECASE,
)
GERMAN_SEVERITY = 1

SKIP_PATH_FRAGMENTS = [".i18n", "__pycache__", ".venv", "/venv/", "/docs/"]

SEVERITY_LABEL = {3: "CRITICAL", 2: "WARN", 1: "info"}


# ---------------------------------------------------------------------------
# Config (.slop.toml)
# ---------------------------------------------------------------------------

def _find_config(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        candidate = parent / ".slop.toml"
        if candidate.exists():
            return candidate
    return None


def _load_config(config_path: Path | None) -> dict:
    if config_path is None:
        return {}
    try:
        with open(config_path, "rb") as fh:
            return tomllib.load(fh)
    except Exception as exc:
        print(f"WARNING: could not parse {config_path}: {exc}", file=sys.stderr)
        return {}


def _build_allowlist(cfg: dict) -> tuple[set[str], list[tuple[str, re.Pattern]]]:
    """Returns (ignored_files, [(file_glob, pattern), ...])."""
    ignored: set[str] = set()
    pattern_allows: list[tuple[str, re.Pattern]] = []

    for entry in cfg.get("ignore_files", {}).get("paths", []):
        ignored.add(entry)

    for entry in cfg.get("allow", []):
        f = entry.get("file", "")
        p = entry.get("pattern", "")
        if f and p:
            try:
                pattern_allows.append((f, re.compile(re.escape(p))))
            except re.error:
                pass

    return ignored, pattern_allows


def _is_allowed(
    py_file: Path,
    line_text: str,
    ignored_files: set[str],
    pattern_allows: list[tuple[str, re.Pattern]],
) -> bool:
    posix = py_file.as_posix()
    for ign in ignored_files:
        if posix.endswith(ign) or ign in posix:
            return True
    for file_glob, pat in pattern_allows:
        if (posix.endswith(file_glob) or file_glob in posix) and pat.search(line_text):
            return True
    return False


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def _skip(path: Path) -> bool:
    s = path.as_posix()
    return any(f in s for f in SKIP_PATH_FRAGMENTS)


def _scan_file(
    py_file: Path,
    ignored_files: set[str],
    pattern_allows: list[tuple[str, re.Pattern]],
) -> list[dict]:
    hits: list[dict] = []
    try:
        lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return hits

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        if _is_allowed(py_file, stripped, ignored_files, pattern_allows):
            continue

        matched = False
        for pattern, reason, severity in SLOP_PATTERNS:
            if pattern.search(stripped):
                hits.append({"file": py_file, "line": lineno, "text": stripped,
                             "reason": reason, "severity": severity})
                matched = True
                break

        if not matched and GERMAN_MARKERS.search(stripped):
            hits.append({"file": py_file, "line": lineno, "text": stripped,
                         "reason": "German in .py comment", "severity": GERMAN_SEVERITY})
    return hits


def scan(
    roots: list[Path],
    ignored_files: set[str],
    pattern_allows: list[tuple[str, re.Pattern]],
) -> list[dict]:
    hits: list[dict] = []
    seen: set[Path] = set()
    for root in roots:
        targets = [root] if root.is_file() else sorted(root.rglob("*.py"))
        for py_file in targets:
            if _skip(py_file) or py_file in seen:
                continue
            seen.add(py_file)
            hits.extend(_scan_file(py_file, ignored_files, pattern_allows))
    return hits


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _file_score_count(file_hits: list[dict]) -> int:
    return len(file_hits)


def _file_score_quality(file_hits: list[dict]) -> int:
    return sum(h["severity"] for h in file_hits)


def _print_results(sorted_files: list[tuple[Path, list[dict]]]) -> None:
    for py_file, file_hits in sorted_files:
        ordered = sorted(file_hits, key=lambda x: x["line"])
        score = sum(h["severity"] for h in file_hits)
        print(f"\n{'='*62}")
        print(f"  {py_file}  ({len(file_hits)} hit(s), quality-score={score})")
        print(f"{'='*62}")
        for h in ordered:
            label = SEVERITY_LABEL[h["severity"]]
            print(f"  :{h['line']:<6} [{label}] {h['reason']}")
            print(f"         {h['text'][:120]}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    strict   = "--strict"          in argv
    by_qual  = "--sort-by=quality" in argv or "--sort-by quality" in " ".join(argv)
    positional = [a for a in argv if not a.startswith("-") and "=" not in a]

    default_roots: list[Path] = [Path("scripts/py"), Path("aura_engine.py")]
    roots = [Path(a) for a in positional] if positional else default_roots

    config_path = _find_config(Path.cwd())
    if config_path:
        print(f"config: {config_path}", file=sys.stderr)
    cfg = _load_config(config_path)
    ignored_files, pattern_allows = _build_allowlist(cfg)

    missing = [r for r in roots if not r.exists()]
    for m in missing:
        print(f"WARNING: path not found: {m}", file=sys.stderr)
    roots = [r for r in roots if r.exists()]
    if not roots:
        print("ERROR: no valid paths to scan", file=sys.stderr)
        return 2

    hits = scan(roots, ignored_files, pattern_allows)
    if not hits:
        print("check_slop_comments: OK")
        return 0

    by_file: dict[Path, list[dict]] = defaultdict(list)
    for h in hits:
        by_file[h["file"]].append(h)

    key_fn = _file_score_quality if by_qual else _file_score_count
    sorted_files = sorted(by_file.items(), key=lambda kv: key_fn(kv[1]), reverse=True)

    _print_results(sorted_files)

    total  = sum(len(v) for v in by_file.values())
    q_total = sum(h["severity"] for v in by_file.values() for h in v)
    sort_label = "quality-score" if by_qual else "hit-count"
    print(f"\n{total} candidate(s) in {len(by_file)} file(s) | total quality-score={q_total} | sorted by {sort_label}",
          file=sys.stderr)
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
