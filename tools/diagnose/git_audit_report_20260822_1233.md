# Git Command & Repository Audit Report

## Repository Context & Collaboration

- **Repository Name**: `SL5-aura-service`
- **Current Branch**: `git_command_audit`
- **Total Commits**: 2338 (Merge Commits: 87)
- **Unique Contributors**: 7
- **Project Timespan**: 2026-08-22 to 2026-08-22
- **Quality / CI Workflows**: Pre-Commit: True, GitHub Actions: True, GitLab CI: False

- **Total Shell Git Commands Analyzed**: 1273

## Critical / Potentially Risky Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0.16% |
| `no_verify` | `--no-verify\b` | 9 | 0.71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0.39% |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0.00% |
| `force_delete_branch` | `branch\s+.*-D\b` | 1 | 0.08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0.00% |

## Advanced & Best-Practice Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0.39% |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0.00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0.71% |
| `cherry_pick` | `cherry-pick\b` | 0 | 0.00% |
| `stash` | `stash\b` | 42 | 3.30% |
| `bisect` | `bisect\b` | 0 | 0.00% |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0.08% |
| `modern_switch_restore` | `(switch|restore)\b` | 20 | 1.57% |

## General Workflow Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `commit` | `commit\b` | 401 | 31.50% |
| `status` | `status\b` | 93 | 7.31% |
| `diff` | `diff\b` | 143 | 11.23% |
| `log` | `log\b` | 113 | 8.88% |
| `checkout` | `checkout\b` | 105 | 8.25% |
| `branch` | `branch\b` | 14 | 1.10% |
| `pull` | `pull\b` | 17 | 1.34% |
| `fetch` | `fetch\b` | 12 | 0.94% |
