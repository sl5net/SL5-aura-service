# Git Command Audit Report

- Total Git Commands Analyzed: 1265

## Critical / Potentially Risky Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0.16% |
| `no_verify` | `--no-verify\b` | 9 | 0.71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0.40% |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0.00% |
| `force_delete_branch` | `branch\s+.*-D\b` | 1 | 0.08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0.00% |

## Advanced & Best-Practice Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0.40% |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0.00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0.71% |
| `cherry_pick` | `cherry-pick\b` | 0 | 0.00% |
| `stash` | `stash\b` | 42 | 3.32% |
| `bisect` | `bisect\b` | 0 | 0.00% |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0.08% |
| `modern_switch_restore` | `(switch|restore)\b` | 20 | 1.58% |

## General Workflow Operations

| Category | Pattern | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `commit` | `commit\b` | 399 | 31.54% |
| `status` | `status\b` | 89 | 7.04% |
| `diff` | `diff\b` | 143 | 11.30% |
| `log` | `log\b` | 113 | 8.93% |
| `checkout` | `checkout\b` | 104 | 8.22% |
| `branch` | `branch\b` | 14 | 1.11% |
| `pull` | `pull\b` | 17 | 1.34% |
| `fetch` | `fetch\b` | 12 | 0.95% |
