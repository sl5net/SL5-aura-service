# Relatório de auditoria de comando e repositório Git

## Contexto e colaboração do repositório

- **Nome do repositório**: `SL5-aura-service`
- **Filial Atual**: `git_command_audit`
- **Total de confirmações**: 2.338 (Mesclar confirmações: 87)
- **Contribuidores Únicos**: 7
- **Prazo do projeto**: 22/08/2026 a 22/08/2026
- **Fluxos de trabalho de qualidade/CI**: pré-comprometimento: verdadeiro, ações do GitHub: verdadeiro, CI do GitLab: falso

- **Total de comandos Shell Git analisados**: 1273

## Operações críticas/potencialmente arriscadas

| Categoria | Padrão | Contagem | Porcentagem |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verify` | `--no-verify\b` | 9 | 0,71% |
| `hard_reset` | `redefinir\s+--hard\b` | 5 | 0,39% |
| `force_clean` | `limpar\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `ramo\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `commit\s+.*-n\b` | 0 | 0,00% |

## Operações avançadas e de melhores práticas

| Categoria | Padrão | Contagem | Porcentagem |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,39% |
| `interativo_rebase` | `rebase\s+.*(-i|--interativo)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interativo))` | 9 | 0,71% |
| `cherry_pick` | `escolher a cereja\b` | 0 | 0,00% |
| `esconderijo` | `esconderijo\b` | 42 | 3,30% |
| `bissectar` | `bissectar\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|reembalar|prune)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(switch|restaurar)\b` | 20 | 1,57% |

## Operações gerais de fluxo de trabalho

| Categoria | Padrão | Contagem | Porcentagem |
| :--- | :--- | :--- | :--- |
| `comprometer` | `comprometer\b` | 401 | 31,50% |
| `estado` | `status\b` | 93 | 7,31% |
| `diferença` | `diferença\b` | 143 | 11,23% |
| `log` | `log\b` | 113 | 8,88% |
| `checkout` | `checkout\b` | 105 | 8,25% |
| `filial` | `filial\b` | 14 | 1,10% |
| `puxar` | `puxar\b` | 17 | 1,34% |
| `buscar` | `buscar\b` | 12 | 0,94% |