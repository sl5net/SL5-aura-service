# Niezrównana wtyczka szkoleniowa (`a_collect_unmatched_training`)

## Zamiar

Ta wtyczka automatycznie zbiera nierozpoznane dane głosowe i dodaje je
jako nowe warianty wyrażenia regularnego mapy rozmytej. Dzięki temu system może się „samouczyć”
z biegiem czasu, ucząc się na niezrównanych wynikach rozpoznawania.

## Jak to działa

1. Reguła catch-all `COLLECT_UNMATCHED` w `FUZZY_MAP_pre.py` uruchamia się, gdy
żadna inna reguła nie pasowała do wprowadzania głosowego.
2. `collect_unmatched.py` jest wywoływane poprzez `on_match_exec` z dopasowanym tekstem.
3. Tekst jest dodawany do pliku „unmatched_list.txt” (oddzielonego pionkami).
4. Wyrażenie regularne w `FUZZY_MAP_pre.py` zostaje automatycznie rozszerzone o nowy wariant.

## Wyłączanie wtyczki

Kiedy zbierzesz wystarczającą ilość danych treningowych, wyłącz tę wtyczkę w następujący sposób:

- Dezaktywacja w ustawieniach Aury
- Usunięcie folderu wtyczki z katalogu `maps`
- Zmiana nazwy folderu na nieprawidłową nazwę (np. dodanie spacji: `a_collect unmatched_training`)

## Struktura pliku
__KOD_BLOKU_0__

## Notatka

Wtyczka modyfikuje plik `FUZZY_MAP_pre.py` w czasie wykonywania. Pamiętaj, aby się zaangażować
regularnie aktualizowany plik, aby zachować zebrane dane szkoleniowe.