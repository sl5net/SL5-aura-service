# Informe de auditoría del repositorio y del comando Git

## Contexto y colaboración del repositorio

- **Nombre del repositorio**: `SL5-aura-service`
- **Sucursal actual**: `git_command_audit`
- **Compromisos totales**: 2338 (Compromisos de fusión: 87)
- **Colaboradores únicos**: 7
- **Duración del proyecto**: 2026-08-22 al 2026-08-22
- **Flujos de trabajo de calidad/CI**: Pre-Commit: Verdadero, Acciones de GitHub: Verdadero, GitLab CI: Falso

- **Total de comandos de Shell Git analizados**: 1273

## Operaciones críticas/potencialmente riesgosas

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verificar` | `--no-verificar\b` | 9 | 0,71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,39% |
| `force_clean` | `limpio\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `rama\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `comprometer\s+.*-n\b` | 0 | 0,00% |

## Operaciones avanzadas y de mejores prácticas

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,39% |
| `rebase_interactiva` | `rebase\s+.*(-i|--interactivo)\b` | 0 | 0,00% |
| `rebase_estándar` | `rebase\s+(?!.*(-i|--interactivo))` | 9 | 0,71% |
| `cherry_pick` | `selección de cereza\b` | 0 | 0,00% |
| `alijo` | `alijo\b` | 42 | 3,30% |
| `biseccionar` | `bisecta\b` | 0 | 0,00% |
| `mantenimiento_gc_repack` | `(gc|reempaquetar|podar)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(cambiar|restaurar)\b` | 20 | 1,57% |

## Operaciones generales de flujo de trabajo

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `comprometer` | `comprometer\b` | 401 | 31,50% |
| `estado` | `estado\b` | 93 | 7,31% |
| `diferencia` | `diferencia\b` | 143 | 11,23% |
| `registro` | `registro\b` | 113 | 8,88% |
| `pagar` | `pagar\b` | 105 | 8,25% |
| `rama` | `rama\b` | 14 | 1,10% |
| `tirar` | `tirar\b` | 17 | 1,34% |
| `buscar` | `buscar\b` | 12 | 0,94% |