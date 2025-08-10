# scripts/py/func/checks/setup_validator.py
#
# Validate the application's environment and run lightweight static analysis.
# Upgrades:
# - CLI with rich options (include/exclude, thresholds, JSON output, exit codes)
# - Safer logging + consistent formatting
# - Auto-create required folders (opt-in)
# - Faster single-pass AST parsing with reusable visitors
# - Unused functions (improved), frequent calls, unused imports, docstring checks
# - Simple cyclomatic complexity budget
# - TODO/FIXME scanner
# - External allowlists (.staticcheckexternals) and ignore markers (# static: keep)
#
# Run:
#   python scripts/py/func/checks/setup_validator.py --help

from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from collections import Counter

MIN_PYTHON = (3, 9)

# ==============================================================================
# 0. UTIL / LOGGING
# ==============================================================================

def _setup_logger(verbosity: int) -> logging.Logger:
    level = logging.WARNING
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO

    logger = logging.getLogger("setup_validator")
    logger.setLevel(level)

    # Avoid duplicate handlers if re-run in same process
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(message)s")
        handler.setFormatter(fmt)
        handler.setLevel(level)
        logger.addHandler(handler)
    return logger


def _rel(project_root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(project_root))
    except Exception:
        return str(p)


# ==============================================================================
# 1. CORE VALIDATION
# ==============================================================================

def validate_python_version(logger: logging.Logger) -> None:
    if sys.version_info < MIN_PYTHON:
        logger.error(
            f"FATAL: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required. "
            f"Found: {sys.version_info.major}.{sys.version_info.minor}"
        )
        sys.exit(1)
    logger.debug("DEBUG: Python version OK.")


def validate_setup(project_root: Path, logger: logging.Logger,
                   required_dirs: Iterable[str] = ("log",),
                   create_missing: bool = False) -> None:
    """
    Verifies that essential directories exist (or creates them if requested).
    """
    logger.info("INFO: Running setup validation...")
    missing = []
    for d in required_dirs:
        path = project_root / d
        if not path.is_dir():
            missing.append(path)

    if missing and not create_missing:
        logger.error("FATAL: Setup validation failed. Missing directories:")
        for m in missing:
            logger.error(f"  - {m}")
        logger.error("       Tip: run with --create-missing-dirs to auto-create.")
        sys.exit(1)

    for m in missing:
        try:
            m.mkdir(parents=True, exist_ok=True)
            logger.info(f"INFO: Created missing directory: {m}")
        except Exception as e:
            logger.error(f"FATAL: Could not create directory {m}: {e}")
            sys.exit(1)

    logger.info("INFO: [OK] Setup validation successful.")


# ==============================================================================
# 2. STATIC ANALYSIS HELPERS (AST Visitors)
# ==============================================================================

IGNORE_MARKERS = ("static: keep", "noqa: unused")

@dataclass
class FunctionDefInfo:
    name: str
    qualname: str
    file: Path
    lineno: int
    has_docstring: bool


class DefinitionVisitor(ast.NodeVisitor):
    """
    Collects public function definitions (including methods).
    Produces both simple names and qualified names (Class.func).
    """
    def __init__(self, file: Path):
        self.defined: List[FunctionDefInfo] = []
        self._class_stack: List[str] = []
        self.file = file

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Skip dunder & private by default
        if node.name.startswith("_") and not node.name.startswith("__init__"):
            self.generic_visit(node)
            return

        qual = ".".join(self._class_stack + [node.name]) if self._class_stack else node.name
        has_doc = ast.get_docstring(node) is not None

        # Honor ignore markers in leading comments (best effort).
        if hasattr(node, "lineno"):
            # We can't read comments via AST easily; allow-line markers can be in docstring too
            doc = ast.get_docstring(node) or ""
            if any(marker in doc for marker in IGNORE_MARKERS):
                self.generic_visit(node)
                return

        self.defined.append(FunctionDefInfo(
            name=node.name, qualname=qual, file=self.file,
            lineno=getattr(node, "lineno", 0), has_docstring=has_doc
        ))
        self.generic_visit(node)


class CallVisitor(ast.NodeVisitor):
    """
    Counts function calls by simple name.
    Only registers actual call expressions (no variable names in args).
    """
    def __init__(self):
        self.called_functions: Counter[str] = Counter()

    def visit_Call(self, node: ast.Call):
        # func could be Name or Attribute; store simple terminal name for heuristic matching
        name: Optional[str] = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr  # e.g., obj.method -> "method"
        if name and not name.startswith("_"):
            self.called_functions[name] += 1
        self.generic_visit(node)


class ImportVisitor(ast.NodeVisitor):
    """
    Collects imported names & alias used in a module.
    Reports unused imports later by comparing with NameUsageVisitor.
    """
    def __init__(self):
        self.imported: Set[str] = set()
        self.star_imports: bool = False

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imported.add(alias.asname or alias.name.split(".")[0])

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module is None:
            return
        for alias in node.names:
            if alias.name == "*":
                self.star_imports = True
                continue
            self.imported.add(alias.asname or alias.name)


class NameUsageVisitor(ast.NodeVisitor):
    """Collects all Name identifiers that appear in a module."""
    def __init__(self):
        self.names: Set[str] = set()

    def visit_Name(self, node: ast.Name):
        self.names.add(node.id)
        self.generic_visit(node)


# ==============================================================================
# 3. STATIC ANALYSIS CORE FUNCTIONS
# ==============================================================================

DEFAULT_INCLUDE_GLOBS = ("*.py",)
DEFAULT_EXCLUDE_GLOBS = (".venv/*", "venv/*", ".git/*", "__pycache__/*", "build/*", "dist/*", ".mypy_cache/*", ".pytest_cache/*")

def _should_include(path: Path, include: Tuple[str, ...], exclude: Tuple[str, ...], project_root: Path) -> bool:
    rel = _rel(project_root, path)
    if any(fnmatch(rel, pat) for pat in exclude):
        return False
    return any(fnmatch(rel, pat) for pat in include)


def parse_all_files(project_root: Path, logger: logging.Logger,
                    include_globs: Tuple[str, ...] = DEFAULT_INCLUDE_GLOBS,
                    exclude_globs: Tuple[str, ...] = DEFAULT_EXCLUDE_GLOBS) -> Dict[Path, ast.AST]:
    """
    Parses all relevant Python files ONCE and returns {path: AST}.
    """
    logger.info("\n--- Parsing project files for analysis ---")
    t0 = time.time()
    parsed: Dict[Path, ast.AST] = {}

    # Seed specific files (if present)
    seeds = [
        project_root / "dictation_service.py",
    ]
    for s in seeds:
        if s.exists() and _should_include(s, include_globs, exclude_globs, project_root):
            try:
                parsed[s] = ast.parse(s.read_text(encoding="utf-8"), filename=str(s))
            except Exception as e:
                logger.warning(f"WARNING: Could not parse file: {_rel(project_root, s)} ({e})")

    # Recursively add others
    for p in project_root.rglob("*.py"):
        if p in parsed:
            continue
        if not _should_include(p, include_globs, exclude_globs, project_root):
            continue
        try:
            parsed[p] = ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except Exception as e:
            logger.warning(f"WARNING: Could not parse file: {_rel(project_root, p)} ({e})")

    logger.info(f"INFO: Parsed {len(parsed)} file(s) in {time.time() - t0:.2f}s.")
    return parsed


def _load_externals(project_root: Path, logger: logging.Logger) -> Set[str]:
    externals = {
        'on_created', 'audio_callback', 'visit_FunctionDef', 'visit_Call',
        'visit_Assign', 'visit_Dict', 'on_any_event', 'setUp', 'on_modified', 'filter',
        'test_transcription_with_long_pause_yields_multiple_chunks',
        'test_transcription_with_short_pause_yields_one_chunk',
        '__init__',
    }
    f = project_root / ".staticcheckexternals"
    if f.is_file():
        try:
            more = {line.strip() for line in f.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")}
            externals |= more
            logger.info(f"INFO: Loaded {len(more)} external names from {_rel(project_root, f)}")
        except Exception as e:
            logger.warning(f"WARNING: Failed to read externals file {_rel(project_root, f)}: {e}")
    return externals


@dataclass
class UnusedFunctionFinding:
    name: str
    qualname: str
    file: Path
    lineno: int


def check_for_unused_functions(parsed: Dict[Path, ast.AST],
                               project_root: Path,
                               logger: logging.Logger) -> List[UnusedFunctionFinding]:
    """Finds unused (apparently dead) public functions/methods."""
    logger.info("\n--- Checking for unused functions ---")
    externals = _load_externals(project_root, logger)

    definitions: List[FunctionDefInfo] = []
    for file, tree in parsed.items():
        v = DefinitionVisitor(file)
        v.visit(tree)
        definitions.extend(v.defined)

    # Count calls globally by simple name (heuristic)
    call_visitor = CallVisitor()
    for tree in parsed.values():
        call_visitor.visit(tree)
    called_names = set(call_visitor.called_functions.keys()) | externals

    # Build findings
    findings: List[UnusedFunctionFinding] = []
    for info in definitions:
        # ignore private-like names & test files
        if info.name.startswith("_"):
            continue
        rel_file = _rel(project_root, info.file)
        if rel_file.startswith("tests/") or rel_file.endswith("_test.py"):
            continue
        # ignore if code contains ignore markers on the line or nearby (best effort via docstring)
        if info.has_docstring:
            # Already filtered via DefinitionVisitor if marker in docstring
            pass
        if info.name not in called_names:
            findings.append(UnusedFunctionFinding(info.name, info.qualname, info.file, info.lineno))

    if not findings:
        logger.info("INFO: No unused functions found. ✅")
    else:
        logger.error("FATAL: The following functions/methods appear unused:")
        for f in findings:
            logger.error(f"  - {f.qualname:<40} | {_rel(project_root, f.file)}:{f.lineno}")
        logger.error("  -> Consider removing, testing, or mark with '# static: keep' or add to .staticcheckexternals")
    return findings


def check_for_frequent_calls(parsed: Dict[Path, ast.AST],
                             logger: logging.Logger,
                             threshold: int = 1) -> List[Tuple[str, int]]:
    """Finds functions called more often than the threshold."""
    logger.info(f"\n--- Checking for functions called more than {threshold} time(s) ---")
    allowed = {
        'info', 'debug', 'warning', 'error', 'critical', 'exception', 'print', 'join',
        'format', 'open', 'close', 'read', 'write', 'add', 'update', 'append', 'extend',
        'get', 'set', 'pop', 'startswith', 'endswith', 'strip', 'replace', 'split',
        'lower', 'upper', 'is_dir', 'is_file', 'exists', 'mkdir', 'relative_to', 'glob',
        'len', 'range', 'enumerate', 'sorted', 'sum', 'min', 'max', 'any', 'all',
    }

    visitor = CallVisitor()
    for tree in parsed.values():
        visitor.visit(tree)

    hot: List[Tuple[str, int]] = []
    for name, count in visitor.called_functions.items():
        if count > threshold and name not in allowed:
            hot.append((name, count))

    if not hot:
        logger.info("INFO: No excessively frequent function calls found. ✅")
    else:
        logger.warning("WARNING: Frequently called functions (review for performance/redundancy):")
        for name, count in sorted(hot, key=lambda item: item[1], reverse=True):
            logger.warning(f"  - {name:<30} | called {count}×")
    return hot


@dataclass
class UnusedImportFinding:
    name: str
    file: Path
    lineno: int


def _collect_unused_imports(file: Path, tree: ast.AST) -> List[UnusedImportFinding]:
    imp = ImportVisitor()
    imp.visit(tree)
    if imp.star_imports:
        return []  # Skip files with star imports (ambiguous)

    names = NameUsageVisitor()
    names.visit(tree)

    unused = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name == "*":
                    continue
                alias_name = alias.asname or alias.name.split(".")[0]
                if alias_name not in names.names:
                    unused.append(UnusedImportFinding(alias_name, file, getattr(node, "lineno", 0)))
    return unused


def check_for_unused_imports(parsed: Dict[Path, ast.AST],
                             project_root: Path,
                             logger: logging.Logger) -> List[UnusedImportFinding]:
    logger.info("\n--- Checking for unused imports ---")
    findings: List[UnusedImportFinding] = []
    for file, tree in parsed.items():
        findings.extend(_collect_unused_imports(file, tree))

    if not findings:
        logger.info("INFO: No unused imports detected. ✅")
    else:
        logger.warning("WARNING: Unused imports (remove to speed cold starts and improve clarity):")
        for f in findings:
            logger.warning(f"  - {f.name:<20} | {_rel(project_root, f.file)}:{f.lineno}")
    return findings


@dataclass
class ComplexityFinding:
    qualname: str
    file: Path
    lineno: int
    complexity: int


class _ComplexityVisitor(ast.NodeVisitor):
    """
    Compute a naive cyclomatic complexity:
      complexity = 1 + (# decision points)
    Decision points: If, For, While, Try, BoolOp, IfExp, Comprehension, With
    """
    def __init__(self):
        self.score = 1

    def visit_If(self, node):         self.score += 1; self.generic_visit(node)
    def visit_For(self, node):        self.score += 1; self.generic_visit(node)
    def visit_AsyncFor(self, node):   self.score += 1; self.generic_visit(node)
    def visit_While(self, node):      self.score += 1; self.generic_visit(node)
    def visit_Try(self, node):        self.score += 1; self.generic_visit(node)
    def visit_With(self, node):       self.score += 1; self.generic_visit(node)
    def visit_AsyncWith(self, node):  self.score += 1; self.generic_visit(node)
    def visit_IfExp(self, node):      self.score += 1; self.generic_visit(node)
    def visit_BoolOp(self, node):     self.score += max(1, len(getattr(node, "values", [])) - 1); self.generic_visit(node)
    def visit_comprehension(self, node): self.score += 1; self.generic_visit(node)


def check_cyclomatic_complexity(parsed: Dict[Path, ast.AST],
                                project_root: Path,
                                logger: logging.Logger,
                                threshold: int = 10) -> List[ComplexityFinding]:
    logger.info(f"\n--- Checking cyclomatic complexity (threshold = {threshold}) ---")
    findings: List[ComplexityFinding] = []

    for file, tree in parsed.items():
        def_visitor = DefinitionVisitor(file)
        def_visitor.visit(tree)

        # Rewalk original tree to access nodes by function qualname
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Build qualname using class stack is tricky here; approximate by name only
                name = node.name
                if name.startswith("_"):
                    continue
                cv = _ComplexityVisitor()
                cv.visit(node)
                if cv.score > threshold:
                    findings.append(ComplexityFinding(
                        qualname=name, file=file, lineno=getattr(node, "lineno", 0), complexity=cv.score
                    ))

    if not findings:
        logger.info("INFO: No high-complexity functions found. ✅")
    else:
        logger.warning("WARNING: High cyclomatic complexity (consider refactor / split):")
        for f in sorted(findings, key=lambda x: x.complexity, reverse=True):
            logger.warning(f"  - {f.qualname:<30} | Cmplx {f.complexity:<3} | {_rel(project_root, f.file)}:{f.lineno}")
    return findings


@dataclass
class DocstringFinding:
    qualname: str
    file: Path
    lineno: int


def check_docstrings(parsed: Dict[Path, ast.AST],
                     project_root: Path,
                     logger: logging.Logger) -> List[DocstringFinding]:
    logger.info("\n--- Checking for missing docstrings (public defs) ---")
    findings: List[DocstringFinding] = []
    for file, tree in parsed.items():
        v = DefinitionVisitor(file)
        v.visit(tree)
        for info in v.defined:
            # ignore tests
            rel = _rel(project_root, info.file)
            if rel.startswith("tests/") or rel.endswith("_test.py"):
                continue
            if not info.has_docstring:
                findings.append(DocstringFinding(info.qualname, info.file, info.lineno))

    if not findings:
        logger.info("INFO: All public functions/methods have docstrings. ✅")
    else:
        logger.warning("WARNING: Missing docstrings:")
        for f in findings:
            logger.warning(f"  - {f.qualname:<30} | {_rel(project_root, f.file)}:{f.lineno}")
    return findings


@dataclass
class TodoFinding:
    file: Path
    lineno: int
    text: str


def check_todos(project_root: Path,
                logger: logging.Logger,
                include_globs: Tuple[str, ...],
                exclude_globs: Tuple[str, ...]) -> List[TodoFinding]:
    logger.info("\n--- Scanning TODO/FIXME ---")
    findings: List[TodoFinding] = []
    pat = re.compile(r"#\s*(TODO|FIXME|HACK)\b(.*)", re.IGNORECASE)
    for p in project_root.rglob("*.py"):
        if not _should_include(p, include_globs, exclude_globs, project_root):
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
                m = pat.search(line)
                if m:
                    findings.append(TodoFinding(p, i, m.group(0).strip()))
        except Exception:
            continue

    if not findings:
        logger.info("INFO: No TODO/FIXME comments found. ✅")
    else:
        logger.info(f"INFO: Found {len(findings)} TODO/FIXME/HACK comments (track & triage):")
        for f in findings[:50]:  # cap output
            logger.info(f"  - {_rel(project_root, f.file)}:{f.lineno} | {f.text}")
        if len(findings) > 50:
            logger.info(f"  ... and {len(findings) - 50} more")
    return findings


# ==============================================================================
# 4. SCRIPT EXECUTION
# ==============================================================================

@dataclass
class Report:
    unused_functions: List[Dict] = field(default_factory=list)
    frequent_calls: List[Tuple[str, int]] = field(default_factory=list)
    unused_imports: List[Dict] = field(default_factory=list)
    complexities: List[Dict] = field(default_factory=list)
    missing_docstrings: List[Dict] = field(default_factory=list)
    todos: List[Dict] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, default=str)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate setup and run static analysis.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4],
                        help="Project root path (default: 4 parents up from this file).")
    parser.add_argument("--create-missing-dirs", action="store_true",
                        help="Auto-create required directories (e.g., log).")
    parser.add_argument("--require-dirs", nargs="*", default=["log"],
                        help="List of directories (relative to root) required for setup.")
    parser.add_argument("--include", nargs="*", default=list(DEFAULT_INCLUDE_GLOBS),
                        help="Glob(s) to include (relative to root).")
    parser.add_argument("--exclude", nargs="*", default=list(DEFAULT_EXCLUDE_GLOBS),
                        help="Glob(s) to exclude (relative to root).")
    parser.add_argument("--freq-threshold", type=int, default=1,
                        help="Flag functions called more than this count.")
    parser.add_argument("--complexity-threshold", type=int, default=10,
                        help="Warn if function complexity exceeds this value.")
    parser.add_argument("--json-output", type=Path, default=None,
                        help="Write machine-readable JSON report to this path.")
    parser.add_argument("--exit-zero", action="store_true",
                        help="Never fail the process (CI-friendly dry run).")
    parser.add_argument("-v", "--verbose", action="count", default=1,
                        help="Increase logging verbosity (-v, -vv).")

    args = parser.parse_args(argv)
    logger = _setup_logger(args.verbose)

    validate_python_version(logger)
    project_root: Path = args.root

    validate_setup(project_root, logger,
                   required_dirs=args.require_dirs,
                   create_missing=args.create_missing_dirs)

    parsed = parse_all_files(project_root, logger,
                             include_globs=tuple(args.include),
                             exclude_globs=tuple(args.exclude))

    report = Report()

    # Run checks
    unused_funcs = check_for_unused_functions(parsed, project_root, logger)
    report.unused_functions = [
        {"name": f.name, "qualname": f.qualname, "file": _rel(project_root, f.file), "line": f.lineno}
        for f in unused_funcs
    ]

    hot_calls = check_for_frequent_calls(parsed, logger, threshold=args.freq_threshold)
    report.frequent_calls = hot_calls

    unused_imports = check_for_unused_imports(parsed, project_root, logger)
    report.unused_imports = [
        {"name": f.name, "file": _rel(project_root, f.file), "line": f.lineno}
        for f in unused_imports
    ]

    complexities = check_cyclomatic_complexity(parsed, project_root, logger, threshold=args.complexity_threshold)
    report.complexities = [
        {"qualname": f.qualname, "complexity": f.complexity, "file": _rel(project_root, f.file), "line": f.lineno}
        for f in complexities
    ]

    doc_missing = check_docstrings(parsed, project_root, logger)
    report.missing_docstrings = [
        {"qualname": f.qualname, "file": _rel(project_root, f.file), "line": f.lineno}
        for f in doc_missing
    ]

    todos = check_todos(project_root, logger, tuple(args.include), tuple(args.exclude))
    report.todos = [
        {"file": _rel(project_root, f.file), "line": f.lineno, "text": f.text}
        for f in todos
    ]

    # Summarize & decide exit code
    problems = 0
    if unused_funcs:
        problems += len(unused_funcs)
    # Not fatal by default:
    #   hot_calls, unused_imports, complexities, doc_missing, todos are warnings
    # Make unused imports + complexity optionally fatal later if needed.

    if args.json_output:
        try:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(report.to_json(), encoding="utf-8")
            logger.info(f"\nINFO: Wrote JSON report → {args.json_output}")
        except Exception as e:
            logger.error(f"ERROR: Failed to write JSON report: {e}")

    if problems and not args.exit_zero:
        logger.error("\n❌ Static analysis found fatal issues.")
        return 1

    logger.info("\n✅ All static analysis checks completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
