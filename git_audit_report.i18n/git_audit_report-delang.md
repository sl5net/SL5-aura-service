# Git-Befehls-Audit-Bericht

- Insgesamt analysierte Git-Befehle: 1265

## Kritische/potenziell riskante Vorgänge

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16 % |
| `no_verify` | `--no-verify\b` | 9 | 0,71 % |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,40 % |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0,00 % |
| `force_delete_branch` | `branch\s+.*-D\b` | 1 | 0,08 % |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00 % |

## Erweiterte und Best-Practice-Operationen

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,40 % |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00 % |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0,71 % |
| `cherry_pick` | `Cherry-Pick\b` | 0 | 0,00 % |
| `Stash` | `stash\b` | 42 | 3,32 % |
| „halbieren“ | `halbieren\b` | 0 | 0,00 % |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0,08 % |
| `modern_switch_restore` | `(switch|restore)\b` | 20 | 1,58 % |

## Allgemeine Workflow-Operationen

| Kategorie | Muster | Zählen | Prozentsatz |
| :--- | :--- | :--- | :--- |
| `commit` | `commit\b` | 399 | 31,54 % |
| `Status` | `status\b` | 89 | 7,04 % |
| `diff` | `diff\b` | 143 | 11,30 % |
| `log` | `log\b` | 113 | 8,93 % |
| `zur Kasse` | `checkout\b` | 104 | 8,22 % |
| `Zweig` | `Zweig\b` | 14 | 1,11 % |
| `ziehen` | `pull\b` | 17 | 1,34 % |
| `holen` | `fetch\b` | 12 | 0,95 % |