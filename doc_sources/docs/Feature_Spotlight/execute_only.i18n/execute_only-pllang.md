# Atrybut reguły: `execute_only` (eksperymentalny, 7.7.'26 wtorek)

Atrybut `execute_only` to eksperymentalna opcja konfiguracji zaprojektowana dla reguł, które uruchamiają tylko zewnętrzne skrypty bez modyfikowania lub zastępowania tekstu wejściowego.

## Przegląd
- **Typ:** `bool` (np. `True` lub `False`)
- **Główny przypadek użycia:** Zwykle używany w połączeniu z `on_match_exec` do uruchamiania zewnętrznych skryptów.

## Jak to działa i obecne zachowanie
- **Optymalizacja szybkości:** (tylko kilka milisekund) Omija procedury przetwarzania końcowego i zastępowania tekstu, przyspieszając natychmiastowe wykonanie wywołanej akcji.
- **Brak skutków ubocznych wykluczenia/przechodzenia:** Ustawienie `execute_only` na `True` **nie** uniemożliwia innym pasującym regułom ocenę tego samego tekstu wejściowego.
- **Zatrzymanie przepływu:** Jeśli chcesz zatrzymać przetwarzanie tego samego tekstu wejściowego przez kolejne reguły, obecnie musisz ręcznie zakończyć przepływ wykonywania (np. zgłaszając wyjątek na końcu uruchomionego skryptu lub procedury obsługi zestawu reguł).

## Przykładowa konfiguracja

__KOD_BLOKU_0__