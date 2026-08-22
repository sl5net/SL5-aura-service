# Informe de auditoría de comandos de Git

- Total de comandos de Git analizados: 1265

## Operaciones críticas/potencialmente riesgosas

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-with-lease)|-f\b)` | 2 | 0,16% |
| `no_verificar` | `--no-verificar\b` | 9 | 0,71% |
| `hard_reset` | `reset\s+--hard\b` | 5 | 0,40% |
| `force_clean` | `limpio\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `rama\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `comprometer\s+.*-n\b` | 0 | 0,00% |

## Operaciones avanzadas y de mejores prácticas

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,40% |
| `rebase_interactiva` | `rebase\s+.*(-i|--interactivo)\b` | 0 | 0,00% |
| `rebase_estándar` | `rebase\s+(?!.*(-i|--interactivo))` | 9 | 0,71% |
| `cherry_pick` | `selección de cereza\b` | 0 | 0,00% |
| `alijo` | `alijo\b` | 42 | 3,32% |
| `biseccionar` | `bisecta\b` | 0 | 0,00% |
| `mantenimiento_gc_repack` | `(gc|reempaquetar|podar)\b` | 1 | 0,08% |
| `modern_switch_restore` | `(cambiar|restaurar)\b` | 20 | 1,58% |

## Operaciones generales de flujo de trabajo

| Categoría | Patrón | Contar | Porcentaje |
| :--- | :--- | :--- | :--- |
| `comprometer` | `comprometer\b` | 399 | 31,54% |
| `estado` | `estado\b` | 89 | 7,04% |
| `diferencia` | `diferencia\b` | 143 | 11,30% |
| `registro` | `registro\b` | 113 | 8,93% |
| `pagar` | `pagar\b` | 104 | 8,22% |
| `rama` | `rama\b` | 14 | 1,11% |
| `tirar` | `tirar\b` | 17 | 1,34% |
| `buscar` | `buscar\b` | 12 | 0,95% |