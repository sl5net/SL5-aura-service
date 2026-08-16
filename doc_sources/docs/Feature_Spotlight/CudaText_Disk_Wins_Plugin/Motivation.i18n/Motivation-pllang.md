# Motywacja: Dlaczego „Dysk wygrywa”?

## Problem w trybie babci Aury

W [Aura Oma Mode](../../../GettingStarted.i18n/GettingStarted-pllang.md) (patrz linia 67) Aura działa w dużej mierze autonomicznie:
użytkownik wypowiada polecenia, a Aura samodzielnie zapisuje pliki —
konfiguracje, skrypty, wpisy do dziennika, wygenerowany tekst.

Ciągle powtarza się następujący scenariusz:

1. Użytkownik ma otwarty plik w edytorze (np. plik reguł lub skrypt).
2. Zapominają, że edytor jest nadal aktywny i wypowiadają polecenie Aury.
3. Aura zmienia plik na dysku.
4. Redaktor wykrywa zewnętrzną zmianę i **pyta**.

Ten monit jest **przeszkodą** w trybie Oma:
- Użytkownik może siedzieć na kanapie i korzystać z wprowadzania głosowego,
i nie można zobaczyć ani dotrzeć do okna dialogowego.
- Albo przypadkowo nacisnęli klawisz w edytorze, bufor jest teraz
„zmodyfikowany”, a każda zmiana zewnętrzna blokuje się za pomocą a
„Załaduj ponownie? / Zachowaj lokalnie?” dialog.
- Wynik: Aura nadal działa, ale edytor pokazuje nieaktualną wersję.
Użytkownik myśli, że patrzy na bieżący plik, ale opiera się na edycjach
na starym państwie — chaos gwarantowany.

## Czego potrzebujemy

Zachowanie edytora, które **zawsze nadaje priorytet dyskowi**.
Kiedy Aura (lub inne narzędzie) zmienia plik, edytor musi to zrobić
natychmiast i **bez monitu** pokaż nową treść.
Niezapisane dane wejściowe w edytorze można po cichu odrzucić — ponieważ in
Tryb Oma, Aura jest źródłem prawdy, a nie danych wprowadzanych za pomocą ludzkiej klawiatury.

## Dlaczego standardowi redaktorzy zawodzą

Prawie wszystkie popularne edytory (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText od razu po wyjęciu z pudełka) posiadają mechanizm zabezpieczający:
gdy tylko bufor zawiera niezapisane zmiany, **zawsze** pytają
gdy nastąpi zmiana zewnętrzna. Jest to funkcja normalna
praca programistów — ale błąd w trybie Aura Oma.

Ta wtyczka zamyka dokładnie tę lukę dla CudaText.

## Odbiorcy docelowi

- Użytkownicy trybu Aura Oma, którzy równolegle przeglądają pliki w edytorze.
- Scenariusze automatyzacji, w których proces zapisuje pliki i edytor
służy wyłącznie jako widz na żywo.
- Każdy, dla kogo „dysk zawsze wygrywa” jest pożądanym zachowaniem.