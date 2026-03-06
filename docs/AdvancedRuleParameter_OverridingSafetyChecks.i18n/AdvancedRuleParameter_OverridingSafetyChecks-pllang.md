# Dokumentacja silnika reguł aury SL5

## Parametr reguły zaawansowanej: pomijanie kontroli bezpieczeństwa

W niektórych scenariuszach (np. wysoce niezawodne polecenia wewnętrzne lub proste dane wejściowe o dużej pewności) użytkownicy mogą chcieć wymusić wykonanie etapów przetwarzania końcowego (takich jak „fuzzyRules”), nawet jeśli pewność systemu co do początkowego rozpoznawania głosu jest niska.

Domyślnie SL5 Aura wykorzystuje barierę bezpieczeństwa: Jeśli zmiany danych wejściowych są duże (`LT_SKIP_RATIO_THRESHOLD`), narzędzia przetwarzania końcowego są pomijane, aby zapobiec nierzetelnym poprawkom/halucynacjom oraz ze względu na wydajność.


Aby wyłączyć tę kontrolę bezpieczeństwa dla konkretnej reguły, dodaj identyfikator do parametru `skip_list`:

__KOD_BLOKU_0__