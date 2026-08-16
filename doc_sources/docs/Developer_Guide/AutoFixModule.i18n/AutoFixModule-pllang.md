# Moduł automatycznej naprawy (tryb szybkiego wprowadzania reguł)

## Co to robi

Kiedy wpisujesz zwykłe słowo (bez cudzysłowów i składni Pythona) do pliku mapy
jak `FUZZY_MAP_pre.py`, system automatycznie konwertuje go na prawidłową regułę.

To najszybszy sposób tworzenia nowych reguł — nie trzeba pamiętać formatu.

## Przykład

Wpisz to w `FUZZY_MAP_pre.py`:

__KOD_BLOKU_0__

Moduł automatycznej naprawy wykrywa błąd „NameError” (samo słowo, niepoprawny język Python)
i automatycznie przekształca plik w:

__KOD_BLOKU_1__

Teraz edytuj regułę do tego, czego faktycznie potrzebujesz:

__KOD_BLOKU_2__

## Jak to działa

Moduł `scripts/py/func/auto_fix_module.py` jest uruchamiany automatycznie
gdy Aura wykryje błąd „NameError” podczas ładowania pliku mapy.

To wtedy:
1. Dodaje poprawny nagłówek ścieżki pliku
2. Dodaje „importuj ponownie”, jeśli go brakuje
3. Dodaje definicję listy `FUZZY_MAP_pre = [`
4. Konwertuje same słowa na krotki `('słowo', 'słowo'),`
5. Zamyka listę za pomocą `]`

## Zasady i ograniczenia

- Działa tylko na plikach mniejszych niż **1KB** (limit bezpieczeństwa)
- Dotyczy tylko: `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCTUATION_MAP.py`
- Plik musi znajdować się w prawidłowym folderze językowym (np. `de-DE/`)
- Działa dla wielu słów na raz (np. z listy książki telefonicznej)

## Znane problemy (nie w pełni przetestowane)

> ⚠️ Ten moduł jest funkcjonalny, ale nie został wyczerpująco przetestowany. Następujące przypadki mogą nie działać poprawnie:

- **Liczby** – „5” lub „6” nie są prawidłowymi identyfikatorami Pythona, automatyczna naprawa może ich nie obsłużyć
- **Znaki specjalne** – słowa z `-`, `.` i umlautami nie mogą powodować błędu `NameError`
- **Wpisy wielowyrazowe** – „thomas mueller” (ze spacją) powoduje „SyntaxError”, a nie „NameError”, więc automatyczna naprawa może nie zostać uruchomiona
- **Wartości oddzielone przecinkami** – `drei, vier` można wstawić w niezmienionej postaci, nie stając się właściwą krotką

Jeśli automatyczna naprawa nie zostanie uruchomiona, dodaj regułę ręcznie:
__KOD_BLOKU_3__

## Komentarz `# też<-od`

Ten komentarz jest dodawany automatycznie jako przypomnienie kierunku reguły:

__KOD_BLOKU_4__

Znaczenie: **wyjście** (też) ← **wejście** (z). Na pierwszym miejscu jest wymiana.

Dla `PUNCTUATION_MAP.py` kierunek jest odwrócony: `# od->też`

## Zbiorczy wpis z listy

Możesz wkleić wiele słów na raz:

__KOD_BLOKU_5__

Każde nagie słowo staje się swoją własną zasadą:

__KOD_BLOKU_6__

Następnie edytuj każde zastąpienie według potrzeb.

## Plik: `scripts/py/func/auto_fix_module.py`