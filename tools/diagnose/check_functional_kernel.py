#!/usr/bin/env python3
# tools/diagnose/check_functional_kernel.py
import ast
import sys
from pathlib import Path
from typing import List, Dict, Any

readme = """
PYTHONUTF8=1 python3 tools/diagnose/check_functional_kernel.py scripts/py/func/process_text_in_background.py

PYTHONUTF8=1 python3 tools/diagnose/check_functional_kernel.py scripts/py/func
"""


MUTATING_METHODS = {
    "append", "extend", "insert", "remove", "pop", "clear",
    "update", "setdefault", "add", "discard"
}

# Configuration
ONLY_HIGH_PRIORITY = True   # Set True to show only HIGH priority issues
MAX_DISPLAY_LINES = 1      # Max number of issues to show per file (0 = unlimited)

RULE_PRIORITY = {
    "GLOBAL_STATE": (1, "HIGH (Runtime/Concurrency)"),
    "MUTABLE_DEFAULT": (1, "HIGH (State Leak/Performance)"),
    "PARAM_MUTATION": (2, "MEDIUM (Shared State/Mutation)"),
    "NONLOCAL_STATE": (2, "MEDIUM (Closure Scope)"),
    "PARAM_REASSIGN": (3, "LOW (Immutability/Hygiene)"),
    "NO_RETURN_VALUE": (3, "LOW (Purity/Side-Effect)"),
}



class FunctionalLinter(ast.NodeVisitor):
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        self.issues: List[Dict[str, Any]] = []
        self.current_func: str = ""
        self.current_params: set = set()
        self.has_return_val: bool = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_func(node)

    def _check_func(self, node: Any) -> None:
        prev_func = self.current_func
        prev_params = self.current_params
        prev_return = self.has_return_val

        self.current_func = node.name
        self.current_params = {arg.arg for arg in node.args.args + node.args.kwonlyargs}
        self.has_return_val = False

        for default in node.args.defaults + [d for d in node.args.kw_defaults if d]:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append({
                    "line": default.lineno,
                    "col": default.col_offset,
                    "rule": "MUTABLE_DEFAULT",
                    "msg": f"Function '{node.name}' has a mutable default argument."
                })

        self.generic_visit(node)

        if not node.name.startswith("_") and not self.has_return_val:
            self.issues.append({
                "line": node.lineno,
                "col": node.col_offset,
                "rule": "NO_RETURN_VALUE",
                "msg": f"Function '{node.name}' has no return statement with a value."
            })

        self.current_func = prev_func
        self.current_params = prev_params
        self.has_return_val = prev_return

    def visit_Global(self, node: ast.Global) -> None:
        for name in node.names:
            self.issues.append({
                "line": node.lineno,
                "col": node.col_offset,
                "rule": "GLOBAL_STATE",
                "msg": f"Use of 'global {name}' modifies global state."
            })

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        for name in node.names:
            self.issues.append({
                "line": node.lineno,
                "col": node.col_offset,
                "rule": "NONLOCAL_STATE",
                "msg": f"Use of 'nonlocal {name}' modifies outer scope state."
            })

    def visit_Assign(self, node: ast.Assign) -> None:
        if self.current_func:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in self.current_params:
                    self.issues.append({
                        "line": node.lineno,
                        "col": node.col_offset,
                        "rule": "PARAM_REASSIGN",
                        "msg": f"Parameter '{target.id}' reassigned in '{self.current_func}'."
                    })
                elif isinstance(target, ast.Subscript):
                    if isinstance(target.value, ast.Name) and target.value.id in self.current_params:
                        self.issues.append({
                            "line": node.lineno,
                            "col": node.col_offset,
                            "rule": "PARAM_MUTATION",
                            "msg": f"In-place subscript mutation on parameter '{target.value.id}'."
                        })
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if self.current_func and isinstance(node.func, ast.Attribute):
            if node.func.attr in MUTATING_METHODS:
                if isinstance(node.func.value, ast.Name) and node.func.value.id in self.current_params:
                    self.issues.append({
                        "line": node.lineno,
                        "col": node.col_offset,
                        "rule": "PARAM_MUTATION",
                        "msg": f"Mutating method '{node.func.attr}()' called on parameter '{node.func.value.id}'."
                    })
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        if node.value is not None:
            self.has_return_val = True
        self.generic_visit(node)


def scan_file(path: Path) -> List[Dict[str, Any]]:
    try:
        content = path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(path))
        linter = FunctionalLinter(path)
        linter.visit(tree)
        return linter.issues
    except Exception as exc:
        return [{"line": 1, "col": 0, "rule": "PARSE_ERROR", "msg": str(exc)}]


def main() -> int:
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["scripts/py/func/process_text_in_background.py"]
    total_issues = 0

    for target in targets:
        p = Path(target)
        files = [p] if p.is_file() else list(p.rglob("*.py")) if p.is_dir() else []
        for file_path in files:
            issues = scan_file(file_path)
            if issues:
                total_issues += len(issues)
                issues.sort(key=lambda x: (RULE_PRIORITY.get(x["rule"], (99, ""))[0], x["line"]))
                if ONLY_HIGH_PRIORITY:
                    issues = [i for i in issues if RULE_PRIORITY.get(i["rule"], (99, ""))[0] == 1]
                print(f"[{file_path}] Found {len(issues)} issue(s) (sorted by Performance/Priority):")
                displayed = issues[:MAX_DISPLAY_LINES] if MAX_DISPLAY_LINES > 0 else issues
                for item in displayed:
                    prio_label = RULE_PRIORITY.get(item["rule"], (99, "UNKNOWN"))[1]
                    print(f"  [{prio_label}] Line {item['line']}:{item['col']} [{item['rule']}] {item['msg']}")
                if MAX_DISPLAY_LINES > 0 and len(issues) > MAX_DISPLAY_LINES:
                    print(f"  ... ({len(issues) - MAX_DISPLAY_LINES} more issues hidden by MAX_DISPLAY_LINES)")
    print(f"\nTotal functional programming issues found: {total_issues}")
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

