# Rapport d'audit des commandes Git

- Total des commandes Git analysées : 1265

## Opérations critiques/potentiellement risquées

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verify` | `--no-verify\b` | 9 | 0,71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,40% |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `branche\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00% |

## Opérations avancées et conformes aux meilleures pratiques

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,40% |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0,71% |
| `cherry_pick` | `cherry-pick\b` | 0 | 0,00% |
| `cache` | `cache\b` | 42 | 3,32% |
| `bissecter` | `bissecter\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(changer|restaurer)\b` | 20 | 1,58% |

## Opérations générales de flux de travail

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `s'engager` | `valider\b` | 399 | 31,54% |
| `statut` | `statut\b` | 89 | 7,04% |
| `diff` | `diff\b` | 143 | 11,30% |
| `journal` | `log\b` | 113 | 8,93% |
| `checkout` | `checkout\b` | 104 | 8,22% |
| `branche` | `branche\b` | 14 | 1,11% |
| `tirer` | `tirer\b` | 17 | 1,34% |
| `récupérer` | `récupérer\b` | 12 | 0,95% |