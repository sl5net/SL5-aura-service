# Relatório de auditoria de comando Git

- Total de comandos Git analisados: 1265

## Operações críticas/potencialmente arriscadas

| Categoria | Padrão | Contagem | Porcentagem |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verify` | `--no-verify\b` | 9 | 0,71% |
| `hard_reset` | `redefinir\s+--hard\b` | 5 | 0,40% |
| `force_clean` | `limpar\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `ramo\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00% |

## Operações avançadas e de melhores práticas

| Categoria | Padrão | Contagem | Porcentagem |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,40% |
| `interativo_rebase` | `rebase\s+.*(-i|--interativo)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interativo))` | 9 | 0,71% |
| `cherry_pick` | `escolher a cereja\b` | 0 | 0,00% |
| `esconderijo` | `esconderijo\b` | 42 | 3,32% |
| `bissectar` | `bissectar\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|reembalar|prune)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(switch|restaurar)\b` | 20 | 1,58% |




| :--- | :--- | :--- | :--- |

| `estado` | `status\b` | 89 | 7,04% |
| `diferença` | `diferença\b` | 143 | 11,30% |
| `log` | `log\b` | 113 | 8,93% |

| `filial` | `filial\b` | 14 | 1,11% |