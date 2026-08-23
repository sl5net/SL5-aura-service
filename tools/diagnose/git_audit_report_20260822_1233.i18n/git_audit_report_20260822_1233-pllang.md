# Raport z audytu poleceń Git i repozytorium

## Kontekst repozytorium i współpraca

- **Nazwa repozytorium**: `SL5-aura-service`
- **Bieżąca gałąź**: `git_command_audit`
- **Całkowite zatwierdzenia**: 2338 (Zatwierdzenia połączenia: 87)
- **Wyjątkowi współtwórcy**: 7
- **Czas trwania projektu**: 22.08.2026 do 22.08.2026
- **Przepływy pracy związane z jakością / CI**: Wstępne zatwierdzenie: Prawda, Akcje GitHub: Prawda, GitLab CI: Fałsz

- ** Całkowita liczba przeanalizowanych poleceń powłoki Git**: 1273

## Operacje krytyczne/potencjalnie ryzykowne

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| `force_push_unprotected` | `push\s+.*(?<!-)(--force(?!-z-dzierżawą)|-f\b)` | 2 | 0,16% |
| `no_weryfikuj` | `--no-verify\b` | 9 | 0,71% |
| `twardy_reset` | `reset\s+--twardy\b` | 5 | 0,39% |
| `force_clean` | `czysty\s+.*(-f|-x)` | 0 | 0,00% |
| `force_delete_branch` | `oddział\s+.*-D\b` | 1 | 0,08% |
| `skip_hooks_commit` | `zatwierdź\s+.*-n\b` | 0 | 0,00% |

## Zaawansowane i najlepsze praktyki

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| `force_with_lease` | `push\s+.*--force-with-lease\b` | 5 | 0,39% |
| `interaktywna_baza` | `rebase\s+.*(-i|--interactive)\b` | 0 | 0,00% |
| `rebase_standard` | `rebase\s+(?!.*(-i|--interaktywny))` | 9 | 0,71% |
| `wiśniowy_wybór` | `wiśniowy\b` | 0 | 0,00% |
| `skrytka` | `skrytka\b` | 42 | 3,30% |
| „na pół” | `przepołać\b` | 0 | 0,00% |
| `maintenance_gc_repack` | `(gc|przepakuj|przycinaj)\b` | 1 | 0,08% |
| `przywracanie_nowoczesnego_przełącznika` | `(przełącz|przywróć)\b` | 20 | 1,57% |

## Ogólne operacje przepływu pracy

| Kategoria | Wzór | Hrabia | Procent |
| :--- | :--- | :--- | :--- |
| „popełnij” | `zatwierdź\b` | 401 | 31,50% |
| `stan` | `stan\b` | 93 | 7,31% |
| `różnica` | `różnica\b` | 143 | 11,23% |
| `log` | `log\b` | 113 | 8,88% |
| `kasa` | `kasa\b` | 105 | 8,25% |
| `gałąź` | `gałąź\b` | 14 | 1,10% |
| ,,pociągnij” | `pociągnij\b` | 17 | 1,34% |
| „przynieś” | `pobierz\b` | 12 | 0,94% |