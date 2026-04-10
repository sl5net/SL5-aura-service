# file: scripts/py/func/checks/check_slop_comments.py
import re
import sys
import subprocess
import tomllib
from collections import defaultdict
from pathlib import Path

#     (re.compile(r"#.*\(original:'[^\)]*'\)"),                                         "bilingual translation artifact",  3),


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

# Detects German characters or common German-only words – used to guard
# against calling trans on already-English text.
GERMAN_CHAR_RE = re.compile(
    r"[äöüÄÖÜß]|"
    r"\b(der|die|das|ein|eine|ist|sind|wird|nicht|auch|noch|aber|wenn|dann|weil|damit|über|unter|nach)\b",
    re.IGNORECASE,
)

GERMAN_SEVERITY = 1
LOCALE_DIR_RE = re.compile(r"[a-z]{2,3}-[A-Z]{2,3}")
SKIP_PATH_FRAGMENTS = [".i18n", "__pycache__", ".venv", "/venv/", "/docs/"]
SEVERITY_LABEL = {3: "CRITICAL", 2: "WARN", 1: "info"}


# ---------------------------------------------------------------------------
# Translation via tools/simple_translate.py
# ---------------------------------------------------------------------------

def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "tools" / "simple_translate.py").exists():
            return parent
    return start


def _translate(text: str, project_root: Path) -> str | None:
    """Translate comment body to English. Returns None if not German or translation fails."""
    body = re.sub(r"^#+\s*", "", text).strip()
    if not body:
        return None
    # Only call trans when the text is actually German – avoids round-trip
    # returning the original unchanged for English input.
    if not GERMAN_CHAR_RE.search(body):
        return None
    script = project_root / "tools" / "simple_translate.py"
    if not script.exists():
        return None
    try:
        result = subprocess.run(
            [sys.executable, str(script), body, "en"],
            capture_output=True, text=True, encoding="utf-8", timeout=10
        )
        translated = result.stdout.strip()
        if result.returncode == 0 and translated and translated != body:
            return "# " + translated
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


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

def _has_locale_dir(path: Path) -> bool:
    return any(LOCALE_DIR_RE.fullmatch(part) for part in path.parts)


def _skip(path: Path) -> bool:
    if _has_locale_dir(path):
        return True
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
                             "reason": reason, "severity": severity,
                             "original_line": line})
                matched = True
                break

        if not matched and GERMAN_MARKERS.search(stripped):
            hits.append({"file": py_file, "line": lineno, "text": stripped,
                         "reason": "German in .py comment", "severity": GERMAN_SEVERITY,
                         "original_line": line})
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
# Interactive fix mode
# ---------------------------------------------------------------------------

def _read_single_key() -> str:
    try:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
    except Exception:
        return sys.stdin.readline().strip() or "\r"


def _apply_replacement(py_file: Path, lineno: int, new_comment: str) -> bool:
    try:
        lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        idx = lineno - 1
        if idx >= len(lines):
            return False
        indent = len(lines[idx]) - len(lines[idx].lstrip())
        new_comment = new_comment.strip()
        if not new_comment.startswith("#"):
            new_comment = "# " + new_comment
        lines[idx] = " " * indent + new_comment + "\n"
        py_file.write_text("".join(lines), encoding="utf-8")
        return True
    except OSError:
        return False


def _delete_line(py_file: Path, lineno: int) -> bool:
    try:
        lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        del lines[lineno - 1]
        py_file.write_text("".join(lines), encoding="utf-8")
        return True
    except OSError:
        return False


def _add_to_allowlist(config_path: Path, py_file: Path, line_text: str) -> None:
    body = re.sub(r"^#+\s*", "", line_text).strip()[:60]
    entry = (
        f'\n[[allow]]\n'
        f'file    = "{py_file.as_posix()}"\n'
        f'pattern = "{body}"\n'
        f'reason  = "reviewed and accepted"\n'
    )
    with open(config_path, "a", encoding="utf-8") as fh:
        fh.write(entry)


def _wants_translation(h: dict) -> bool:
    # Only attempt translation for German comments – not for English slop patterns
    # which need manual rewording, not language conversion.
    return h["reason"] == "German in .py comment"


def _run_interactive(
    sorted_files: list[tuple[Path, list[dict]]],
    project_root: Path,
    config_path: Path | None,
) -> None:
    total = sum(len(v) for _, v in sorted_files)
    done = 0

    print("\nInteractive fix mode")
    print("Enter=accept  Space=skip  e=edit  d=delete  a=allowlist  q=quit\n")

    for py_file, file_hits in sorted_files:
        ordered = sorted(file_hits, key=lambda x: x["line"])
        print(f"\n{'='*62}")
        print(f"  {py_file}  ({len(file_hits)} hit(s))")
        print(f"{'='*62}")

        for h in ordered:
            done += 1
            label = SEVERITY_LABEL[h["severity"]]

            suggestion = None
            if _wants_translation(h):
                suggestion = _translate(h["text"], project_root)

            # Auto-skip: German comment but trans returned nothing useful
            if _wants_translation(h) and suggestion is None:
                print(f"\n[{done}/{total}] :{h['line']}  [{label}] {h['reason']}")
                print(f"  ⚠️  original : {h['text'][:110]}")
                print("  ⏭️  auto-skipped – not German or no translation available")
                continue

            print(f"\n[{done}/{total}] :{h['line']}  [{label}] {h['reason']}")
            print(f"  ⚠️  original : {h['text'][:110]}")

            if suggestion:
                print(f"  💡 suggested: {suggestion[:110]}")
                print("  [Enter=accept  Space=skip  e=edit  d=delete  a=allowlist  q=quit] ", end="", flush=True)
            else:
                # English slop pattern – no translation, manual action only
                print("  [Space=skip  e=edit  d=delete  a=allowlist  q=quit] ", end="", flush=True)

            ch = _read_single_key()
            print(ch)

            if ch in ("\r", "\n", "") and suggestion:
                if _apply_replacement(py_file, h["line"], suggestion):
                    print("  → applied")
                else:
                    print("  → write failed")

            elif ch == " ":
                print("  → skipped")

            elif ch == "e":
                prefill = suggestion or h["text"]
                print("  edit (modify and press Enter):")
                print("  > ", end="", flush=True)
                try:
                    import readline
                    readline.set_startup_hook(lambda: readline.insert_text(prefill))
                    edited = input()
                    readline.set_startup_hook(None)
                except Exception:
                    edited = input()
                if edited.strip():
                    if _apply_replacement(py_file, h["line"], edited):
                        print("  → applied")
                    else:
                        print("  → write failed")

            elif ch == "d":
                if _delete_line(py_file, h["line"]):
                    print("  → deleted")
                else:
                    print("  → delete failed")

            elif ch == "a":
                if config_path:
                    _add_to_allowlist(config_path, py_file, h["text"])
                    print(f"  → added to {config_path}")
                else:
                    print("  → no .slop.toml found; create one in project root first")

            elif ch in ("q", "\x03"):
                print("\nquit.")
                return


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

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
    strict      = "--strict"          in argv
    by_qual     = "--sort-by=quality" in argv
    interactive = "--fix"             in argv
    positional  = [a for a in argv if not a.startswith("-") and "=" not in a]

    default_roots: list[Path] = [Path("scripts/py"), Path("aura_engine.py")]
    roots = [Path(a) for a in positional] if positional else default_roots

    config_path = _find_config(Path.cwd())
    if config_path:
        print(f"config: {config_path}", file=sys.stderr)
    cfg = _load_config(config_path)
    ignored_files, pattern_allows = _build_allowlist(cfg)
    project_root = _find_project_root(Path.cwd())

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

    key_fn = _file_score_quality if by_qual else len
    sorted_files = sorted(by_file.items(), key=lambda kv: key_fn(kv[1]), reverse=True)

    if interactive:
        _run_interactive(sorted_files, project_root, config_path)
        return 0

    _print_results(sorted_files)

    total   = sum(len(v) for v in by_file.values())
    q_total = sum(h["severity"] for v in by_file.values() for h in v)
    sort_label = "quality-score" if by_qual else "hit-count"
    print(f"\n{total} candidate(s) in {len(by_file)} file(s) | total quality-score={q_total} | sorted by {sort_label}",
          file=sys.stderr)
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
