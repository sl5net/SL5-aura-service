import os
import re
from typing import Dict, List, Tuple
from collections import Counter

readme = """
python tools/diagnose/git_command_audit.py "$HISTFILE" git_audit_report.md
"""
print(f"readme=\n{readme}\n\n")

AUDIT_GROUPS: Dict[str, Dict[str, str]] = {
    "Critical / Potentially Risky Operations": {
        "force_push_unprotected": r"push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)",
        "no_verify": r"--no-verify\b",
        "hard_reset": r"reset\s+--hard\b",
        "force_clean": r"clean\s+.*(-f|-x)",
        "force_delete_branch": r"branch\s+.*-D\b",
        "skip_hooks_commit": r"commit\s+.*-n\b",
    },
    "Advanced & Best-Practice Operations": {
        "force_with_lease": r"push\s+.*--force-with-lease\b",
        "interactive_rebase": r"rebase\s+.*(-i|--interactive)\b",
        "rebase_standard": r"rebase\s+(?!.*(-i|--interactive))",
        "cherry_pick": r"cherry-pick\b",
        "stash": r"stash\b",
        "bisect": r"bisect\b",
        "maintenance_gc_repack": r"(gc|repack|prune)\b",
        "modern_switch_restore": r"(switch|restore)\b",
    },
    "General Workflow Operations": {
        "commit": r"commit\b",
        "status": r"status\b",
        "diff": r"diff\b",
        "log": r"log\b",
        "checkout": r"checkout\b",
        "branch": r"branch\b",
        "pull": r"pull\b",
        "fetch": r"fetch\b",
    },
}


def parse_zsh_history_line(line: str) -> str:
    cleaned = line.strip()
    if cleaned.startswith(":"):
        parts = cleaned.split(";", 1)
        if len(parts) == 2:
            return parts[1].strip()
    return cleaned


def extract_git_commands(raw_lines: List[str]) -> List[str]:
    commands = (parse_zsh_history_line(line) for line in raw_lines)
    return [cmd for cmd in commands if cmd.startswith("git ") or cmd == "git"]


def analyze_command_groups(command: str) -> List[Tuple[str, str]]:
    matches = []
    for group_name, patterns in AUDIT_GROUPS.items():
        for category, pattern in patterns.items():
            if re.search(pattern, command):
                matches.append((group_name, category))
    return matches


def compute_statistics(git_commands: List[str]) -> Tuple[int, Dict[str, Dict[str, int]]]:
    total_git = len(git_commands)
    counts: Dict[str, Counter[str]] = {group: Counter() for group in AUDIT_GROUPS}
    for cmd in git_commands:
        for group_name, category in analyze_command_groups(cmd):
            counts[group_name][category] += 1
    return total_git, {grp: dict(cnt) for grp, cnt in counts.items()}


def build_markdown_report(total_git: int, group_counts: Dict[str, Dict[str, int]]) -> str:
    lines = [
        "# Git Command Audit Report",
        "",
        f"- Total Git Commands Analyzed: {total_git}",
        "",
    ]
    for group_name, patterns in AUDIT_GROUPS.items():
        lines.append(f"## {group_name}")
        lines.append("")
        lines.append("| Category | Pattern | Count | Percentage |")
        lines.append("| :--- | :--- | :--- | :--- |")
        counts = group_counts.get(group_name, {})
        for category, pattern in patterns.items():
            count = counts.get(category, 0)
            pct = (count / total_git * 100) if total_git > 0 else 0.0
            lines.append(f"| `{category}` | `{pattern}` | {count} | {pct:.2f}% |")
        lines.append("")
    return "\n".join(lines)


def run_audit(history_file_path: str, output_file_path: str = "") -> str:
    resolved_path = os.path.expanduser(os.path.expandvars(history_file_path))
    if not os.path.isfile(resolved_path):
        return f"File not found: {resolved_path}"

    with open(resolved_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    git_commands = extract_git_commands(lines)
    total, group_counts = compute_statistics(git_commands)
    report = build_markdown_report(total, group_counts)

    if output_file_path:
        out_path = os.path.expanduser(os.path.expandvars(output_file_path))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)

    return report


if __name__ == "__main__":
    import sys

    hist_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.zsh_history")
    out_file = sys.argv[2] if len(sys.argv) > 2 else "git_audit_report.md"
    report_output = run_audit(hist_path, out_file)
    print(report_output)
    if not report_output.startswith("File not found"):
        print(f"\nReport saved to: {out_file}")
