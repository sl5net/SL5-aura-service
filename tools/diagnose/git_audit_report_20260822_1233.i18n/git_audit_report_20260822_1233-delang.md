# Git Command & Repository-Audit-Bericht

## Repository-Kontext und Zusammenarbeit

- **Repository-Name**: „SL5-aura-service“.
- **Aktueller Zweig**: `git_command_audit`
- **Gesamt-Commits**: 2338 (Merge-Commits: 87)
- **Einzigartige Mitwirkende**: 7
- **Projektzeitraum**: 22.08.2026 bis 22.08.2026
- **Qualität/CI-Workflows**: Pre-Commit: True, GitHub Actions: True, GitLab CI: False

- **Gesamtzahl der analysierten Shell-Git-Befehle**: 1273

## Kritische/potenziell riskante Vorgänge

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16 % |
| `no_verify` | `--no-verify\b` | 9 | 0,71 % |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,39 % |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0,00 % |
| `force_delete_branch` | `branch\s+.*-D\b` | 1 | 0,08 % |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00 % |

## Erweiterte und Best-Practice-Operationen

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,39 % |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00 % |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0,71 % |
| `cherry_pick` | `Cherry-Pick\b` | 0 | 0,00 % |
| `Stash` | `stash\b` | 42 | 3,30 % |
| „halbieren“ | `halbieren\b` | 0 | 0,00 % |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0,08 % |
| `modern_switch_restore` | `(switch|restore)\b` | 20 | 1,57 % |

## Allgemeine Workflow-Operationen

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `commit` | `commit\b` | 401 | 31,50 % |
| `Status` | `status\b` | 93 | 7,31 % |
| `diff` | `diff\b` | 143 | 11,23 % |
| `log` | `log\b` | 113 | 8,88 % |
| `zur Kasse` | `checkout\b` | 105 | 8,25 % |
| `Zweig` | `Zweig\b` | 14 | 1,10 % |
| `ziehen` | `pull\b` | 17 | 1,34 % |
| `holen` | `fetch\b` | 12 | 0,94 % |