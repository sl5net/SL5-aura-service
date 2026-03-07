# dotool – Instalacja i konfiguracja (na platformie Manjaro / Arch)

## Przegląd
`dotool` to narzędzie do symulacji wprowadzania danych niskiego poziomu. W przeciwieństwie do `xdotool`, współdziała bezpośrednio z jądrem Linuksa poprzez `uinput`, dzięki czemu jest kompatybilny zarówno z **X11, jak i Waylandem**.

---

## Instalacja (Manjaro / Arch)

### 1. Zainstaluj pakiet
__KOD_BLOKU_0__

### 2. Uprawnienia i zasady udev
Aby pozwolić `dotool` na symulowanie danych wejściowych bez uprawnień roota, twój użytkownik musi należeć do grupy `input`, a reguła udev musi być aktywna:

1. **Dodaj użytkownika do grupy:** `sudo gpasswd -a wejście $USER`
2. **Utwórz regułę udev:**
__KOD_BLOKU_1__
3. **Załaduj ponownie zasady udev:**
__KOD_BLOKU_2__

**Ważne:** Aby zmiany w grupie zaczęły obowiązywać, musisz **wylogować się i zalogować ponownie**.

---

## Konfiguracja projektu (`config/settings.py`)

__KOD_BLOKU_3__

---

## Implementacja skryptu

### Optymalizacja wydajności (FIFO)
Uruchamianie nowej instancji `dotool` dla każdego słowa jest powolne (opóźnienie ~ 100 ms). Aby osiągnąć „natychmiastowe” pisanie, skrypt wykorzystuje trwały odczyt procesu w tle z potoku FIFO.

__KOD_BLOKU_4__

### Funkcja pisania
__KOD_BLOKU_5__

---

## Rozwiązywanie problemów i notatki
- **Brakujące znaki:** Jeśli pominięte zostaną znaki specjalne (takie jak umlauty), zwiększ wartość `dotool_typedelay` do 5 lub 10.
- **Zgodność aplikacji:** Niektóre aplikacje (Electron, przeglądarki) mogą wymagać większego opóźnienia, aby poprawnie zarejestrować szybkie wprowadzanie danych.
- **Wsparcie Waylanda:** `dotool` jest wymaganym backendem dla Waylanda, ponieważ `xdotool` go nie obsługuje.
- **Automatyczny powrót:** Skrypt automatycznie powraca do `xdotool`, jeśli `dotool` nie jest poprawnie zainstalowany lub skonfigurowany.