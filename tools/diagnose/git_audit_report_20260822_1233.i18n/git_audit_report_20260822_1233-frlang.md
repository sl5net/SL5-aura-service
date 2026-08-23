# Rapport d'audit des commandes et du référentiel Git

## Contexte du référentiel et collaboration

- **Nom du référentiel** : `SL5-aura-service`
- **Branche actuelle** : `git_command_audit`
- **Total des commits** : 2338 (Fusion des commits : 87)
- **Contributeurs uniques** : 7
- **Durée du projet** : 2026-08-22 au 2026-08-22
- **Workflows qualité/CI** : pré-engagement : vrai, actions GitHub : vrai, GitLab CI : faux

- **Total des commandes Shell Git analysées** : 1 273

## Opérations critiques/potentiellement risquées

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verify` | `--no-verify\b` | 9 | 0,71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,39% |
| `force_clean` | `clean\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `branche\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00% |

## Opérations avancées et conformes aux meilleures pratiques

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,39% |
| `interactive_rebase` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interactive))` | 9 | 0,71% |
| `cherry_pick` | `cherry-pick\b` | 0 | 0,00% |
| `cache` | `cache\b` | 42 | 3,30% |
| `bissecter` | `bissecter\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|repack|prune)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(changer|restaurer)\b` | 20 | 1,57% |

## Opérations générales de flux de travail

| Catégorie | Modèle | Comte | Pourcentage |
| :--- | :--- | :--- | :--- |
| `s'engager` | `valider\b` | 401 | 31,50% |
| `statut` | `statut\b` | 93 | 7,31% |
| `diff` | `diff\b` | 143 | 11,23% |
| `journal` | `log\b` | 113 | 8,88% |
| `checkout` | `checkout\b` | 105 | 8,25% |
| `branche` | `branche\b` | 14 | 1,10% |
| `tirer` | `tirer\b` | 17 | 1,34% |
| `récupérer` | `récupérer\b` | 12 | 0,94% |