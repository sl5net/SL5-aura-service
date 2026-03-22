# Rozwiązywanie problemów z SL5 Aura

## Szybka diagnoza

Zawsze zaczynaj tutaj:

__KOD_BLOKU_0__

---

## Problem: Aura nie uruchamia się

**Objaw:** Brak dźwięku uruchamiania, brak widocznego procesu w `pgrep`.

**Sprawdź dziennik:**
__KOD_BLOKU_1__

**Częste przyczyny:**

| Błąd w logu | Napraw |
|---|---|
| `ModuleNotFoundError` | Uruchom ponownie skrypt instalacyjny: `bash setup/manjaro_arch_setup.sh` |
| `Brak modułu o nazwie 'objgraph'` | Odtworzono plik `.venv` — zainstaluj ponownie: `pip install -r wymagania.txt` |
| `Adres już używany` | Zabij stary proces: `pkill -9 -f aura_engine` |
| `Nie znaleziono modelu` | Uruchom ponownie instalację, aby pobrać brakujące modele |

---

## Problem: Aura ulega awarii po pierwszym dyktowaniu

**Objaw:** Działa raz, a następnie cicho gaśnie.

**Sprawdź stderr:**
__KOD_BLOKU_2__

**Jeśli widzisz „Błąd segmentacji” lub „Podwójnie wolny”:**

Jest to znany problem w systemach z glibc 2.43+ (CachyOS, nowszy Arch).

__KOD_BLOKU_3__

mimalloc jest automatycznie używany przez skrypt startowy, jeśli jest zainstalowany. Potwierdź, że jest aktywny — powinieneś zobaczyć to przy uruchomieniu:
__KOD_BLOKU_4__

---

## Problem: Klawisz spustowy nic nie robi

**Objaw:** Naciskasz klawisz skrótu, ale nic się nie dzieje — brak dźwięku, brak tekstu.

**Sprawdź, czy przeglądarka plików jest uruchomiona:**
__KOD_BLOKU_5__

Jeśli nic się nie pojawi, uruchom ponownie Aurę:
__KOD_BLOKU_6__

**Sprawdź, czy tworzony jest plik wyzwalacza:**
__KOD_BLOKU_7__

Jeśli plik nigdy nie zostanie utworzony, oznacza to, że konfiguracja klawiszy skrótu (CopyQ / AHK) nie działa.
Zobacz sekcję dotyczącą konfiguracji klawiszy skrótu w [README.md](../../README.i18n/README-pllang.md#configure-your-hotkey).

---

## Problem: Tekst pojawia się, ale bez poprawek

**Objaw:** Dyktowanie działa, ale wszystko pozostaje zapisane małymi literami, bez poprawek gramatycznych.

**Sprawdź, czy LanguageTool jest uruchomiony:**
__KOD_BLOKU_8__

Jeśli zwróci błąd, oznacza to, że LanguageTool nie działa. Aura powinna to rozpocząć
automatycznie — sprawdź dziennik pod kątem błędów związanych z LanguageTool:

__KOD_BLOKU_9__

**Sprawdź dziennik LanguageTool:**
__KOD_BLOKU_10__

---

## Problem: Aura zawiesza się w trybie DEV_MODE

**Objaw:** Przy `DEV_MODE = 1`, Aura zawiesza się po pierwszym uruchomieniu i zatrzymuje się
odpowiadanie.

**Przyczyna:** Duża liczba logów z wielu wątków przeciąża system rejestrowania.

**Poprawka:** Dodaj filtr dziennika w `config/filters/settings_local_log_filter.py`:

__KOD_BLOKU_11__

Zapisz plik — Aura automatycznie przeładuje filtr. Nie ma potrzeby ponownego uruchamiania.

---

## Problem: plik plugins.zip rośnie w nieskończoność / Wysoki procesor

**Objaw:** 100% procesora, wentylatory pracują na pełnych obrotach, plik `plugins.zip` rośnie bez przerwy.

**Przyczyna:** Bezpieczny program pakujący przepakowuje pliki w nieskończonej pętli.

**Poprawka:** Upewnij się, że pliki `.blob` i `.zip` są wykluczone ze skanowania sygnatury czasowej.
Sprawdź `scripts/py/func/secure_packer_lib.py` wokół linii 86:

__KOD_BLOKU_12__

Jeśli brakuje tej linii, dodaj ją.

---

## Problem: Reguły nie uruchamiają się

**Objaw:** Dyktujesz frazę wyzwalającą, ale reguła nic nie daje.

**Lista kontrolna:**

1. Czy reguła znajduje się we właściwym pliku? (`FUZZY_MAP_pre.py` = przed LanguageTool,
`FUZZY_MAP.py` = po)
2. Czy plik mapy został zapisany? Aura ładuje się ponownie po zapisaniu — sprawdź dziennik
`Załadowano ponownie pomyślnie`.
3. Czy wzór odpowiada temu, co faktycznie transkrybuje Vosk? Sprawdź dziennik
surowa transkrypcja:
__KOD_BLOKU_13__
4. Czy ustawiono opcję „tylko_w_oknach” i aktywne jest niewłaściwe okno?
5. Czy najpierw dopasowuje się bardziej ogólną regułę? Reguły są przetwarzane od góry do dołu —
przedkładać szczegółowe zasady nad ogólne.

---

## Zbieranie dzienników w celu raportowania błędów

Zgłaszając problem, podaj:

__KOD_BLOKU_14__

Wyślij do: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)