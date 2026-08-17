# Niezrównana wtyczka szkoleniowa (`1_collect_unmatched_training`)

## Zamiar

Ta wtyczka automatycznie zbiera nierozpoznane dane głosowe i dodaje je
jako nowe warianty wyrażenia regularnego mapy rozmytej. Dzięki temu system może się „samouczyć”
z biegiem czasu, ucząc się na niezrównanych wynikach rozpoznawania.

## Jak to działa

1. Reguła typu catch-all „COLLECT_UNMATCHED” jest uruchamiana, gdy nie pasuje żadna inna reguła.
2. `collect_unmatched.py` jest wywoływane poprzez `on_match_exec` z dopasowanym tekstem.
3. Wyrażenie regularne w wywołaniu `FUZZY_MAP_pre.py` jest automatycznie rozszerzane.

## Użycie

Dodaj tę regułę catch-all na końcu dowolnego pliku „FUZZY_MAP_pre.py”, który chcesz trenować:
__KOD_BLOKU_0__

Etykieta `f'{str(__file__)}'` informuje `collect_unmatched.py` dokładnie, które
`FUZZY_MAP_pre.py` do aktualizacji — aby reguła była przenośna w dowolnej wtyczce.

## Wyłączanie wtyczki

Kiedy zbierzesz wystarczającą ilość danych treningowych, wyłącz:

- Komentowanie zasady catch-all
- Zmiana nazwy folderu na nieprawidłową nazwę (np. dodanie spacji)
- Usunięcie folderu wtyczki z katalogu `maps`

## Struktura pliku
__KOD_BLOKU_1__

## Notatka

Wtyczka modyfikuje plik `FUZZY_MAP_pre.py` w czasie wykonywania. Zatwierdź zaktualizowane
regularnie archiwizuj, aby zachować zebrane dane szkoleniowe.