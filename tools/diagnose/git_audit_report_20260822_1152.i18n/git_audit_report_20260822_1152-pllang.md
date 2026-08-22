# Raport z audytu poleceń Git

- Całkowita liczba przeanalizowanych poleceń Git: 1265

## Operacje krytyczne/potencjalnie ryzykowne

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-z-dzierżawą)|-f\b)` | 2 | 0,16% |
| `no_weryfikuj` | `--no-verify\b` | 9 | 0,71% |
| `twardy_reset` | `reset\s+--twardy\b` | 5 | 0,40% |
| `force_clean` | `czysty\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `oddział\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `zatwierdź\s+.*-n\b` | 0 | 0,00% |

## Zaawansowane i najlepsze praktyki

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,40% |
| `interaktywna_baza` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interaktywny))` | 9 | 0,71% |
| `wiśniowy_wybór` | `wiśniowy\b` | 0 | 0,00% |
| `skrytka` | `skrytka\b` | 42 | 3,32% |
| „na pół” | `przepołać\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|przepakuj|przycinaj)\b` | 1 | 0,08% |
| `przywracanie_nowoczesnego_przełącznika` | `(przełącz|przywróć)\b` | 20 | 1,58% |

## Ogólne operacje przepływu pracy

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| „popełnij” | `zatwierdź\b` | 399 | 31,54% |
| `stan` | `stan\b` | 89 | 7,04% |
| `różnica` | `różnica\b` | 143 | 11,30% |
| `log` | `log\b` | 113 | 8,93% |
| `kasa` | `kasa\b` | 104 | 8,22% |
| `gałąź` | `gałąź\b` | 14 | 1,11% |
| ,,pociągnij” | `pociągnij\b` | 17 | 1,34% |
| „przynieś” | `pobierz\b` | 12 | 0,95% |