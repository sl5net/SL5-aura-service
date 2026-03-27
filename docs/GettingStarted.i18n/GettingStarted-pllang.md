# Pierwsze kroki z SL5 Aura

> **Wymagania wstępne:** Ukończyłeś skrypt instalacyjny i skonfigurowałeś skrót klawiszowy.
> Jeśli nie, zobacz [Installation section in README.md](../../README.i18n/README-pllang.md#installation).

---

## Krok 1: Twoje pierwsze dyktando

1. Uruchom Aurę (jeśli jeszcze nie działa):
__KOD_BLOKU_0__
Poczekaj na dźwięk uruchamiania — to oznacza, że Aura jest gotowa.

2. Kliknij dowolne pole tekstowe (edytor, przeglądarka, terminal).
3. Naciśnij klawisz skrótu, powiedz **„Hello World”**, naciśnij klawisz skrótu ponownie.
4. Obserwuj, jak pojawia się tekst.

> **Nic się nie stało?** Sprawdź `log/aura_engine.log` pod kątem błędów.
> Wspólna poprawka dla CachyOS/Arch: `sudo pacman -S mimalloc`

---

## Krok 2: Napisz swoją pierwszą regułę

Najszybszy sposób dodania reguły osobistej:

1. Otwórz `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Dodaj regułę wewnątrz `FUZZY_MAP_pre = [...]`:
__KOD_BLOKU_1__
3. **Zapisz** — Aura ładuje się automatycznie. Nie ma potrzeby ponownego uruchamiania.
4. Podyktuj „Witaj świecie” i zobacz, jak zmienia się w „Hello World”.

> Zobacz `docs/FuzzyMapRuleGuide.md`, aby uzyskać pełne informacje o regułach.

### Oma-Modus (skrót dla początkujących)

Nie znasz jeszcze wyrażenia regularnego? Bez problemu.

1. Otwórz pusty plik `FUZZY_MAP_pre.py` w piaskownicy
2. Napisz zwykłe słowo w osobnej linii (bez cudzysłowów i krotki):
__KOD_BLOKU_2__
3. Zapisz — system Auto-Fix automatycznie wykrywa samo słowo
konwertuje go na prawidłowy wpis reguły.
4. Następnie możesz ręcznie edytować tekst zastępczy.

Nazywa się to **Oma-Modus** — przeznaczony dla użytkowników, którzy chcą wyników bez
najpierw naucz się wyrażeń regularnych.

---

## Krok 3: Ucz się z Koanami

Koany to małe ćwiczenia, z których każde uczy jednego pojęcia.
Mieszkają w `configmaps/koans deutsch/` i `configmaps/koans english/`.

Zacznij tutaj:

| Folder | Czego się uczysz |
|---|---|
| `00_koan_oma-modus` | Automatyczna naprawa, pierwsza reguła bez wyrażenia regularnego |
| `01_koan_erste_schritte` | Twoja pierwsza zasada, podstawy rurociągów |
| `02_koan_słuchaj` | Praca z listami |
| `03_koan_schwierige_namen` | Rozmyte dopasowanie do trudnych do rozpoznania nazw |
| `04_koan_kleine_helper` | Przydatne skróty |

Każdy folder koanów zawiera plik `FUZZY_MAP_pre.py` z skomentowanymi przykładami.
Odkomentuj regułę, zapisz, podyktuj frazę wyzwalającą i gotowe.

---

## Krok 4: Idź dalej

| Co | Gdzie |
|---|---|
| Pełne odniesienie do przepisów | `docs/FuzzyMapRuleGuide.md` |
| Stwórz własną wtyczkę | `docs/CreatingNewPluginModules.md` |
| Uruchamiaj skrypty Pythona z reguł | `docs/advanced-scripting.md` |
| DEV_MODE + konfiguracja filtra dziennika | `docs/Developer_Guide/dev_mode_setup.md` |
| Reguły kontekstowe (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |