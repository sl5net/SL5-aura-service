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
| `pygame.mixer niedostępny` | Zobacz „Brak dźwięku podczas uruchamiania” poniżej |

---

## Problem: Brak dźwięku podczas uruchamiania (pygame.mixer)

**Objaw:** Ostrzeżenie lub błąd dotyczący `pygame.mixer` jest niedostępny. Zaczyna się aura
ale nie odtwarza żadnych dźwięków.

**Przyczyna:** Kompilacja pygame w Twoim systemie nie obsługuje dźwięku ani SDL2
brakuje bibliotek audio.

**Poprawka w Arch/Manjaro:**
__KOD_BLOKU_2__

**Poprawka w Ubuntu/Debianie:**
__KOD_BLOKU_3__

Aura będzie nadal działać bez dźwięku — nie jest to błąd krytyczny.

---

## Problem: Aura ulega awarii po pierwszym dyktowaniu

**Objaw:** Działa raz, a następnie cicho gaśnie.

**Sprawdź stderr:**
__KOD_BLOKU_4__

**Jeśli widzisz „Błąd segmentacji” lub „Podwójnie wolne”:**

Jest to znany problem w systemach z glibc 2.43+ (CachyOS, nowszy Arch).

__KOD_BLOKU_5__

mimalloc jest automatycznie używany przez skrypt startowy, jeśli jest zainstalowany. Potwierdź, że jest aktywny — powinieneś zobaczyć to przy uruchomieniu:
__KOD_BLOKU_6__

---

## Problem: Klawisz spustowy nic nie robi

**Objaw:** Naciskasz klawisz skrótu, ale nic się nie dzieje — brak dźwięku, brak tekstu.

**Sprawdź, czy przeglądarka plików jest uruchomiona:**
__KOD_BLOKU_7__

Jeśli nic się nie pojawi, uruchom ponownie Aurę:
__KOD_BLOKU_8__

**Sprawdź, czy tworzony jest plik wyzwalacza:**
__KOD_BLOKU_9__

Jeśli plik nigdy nie zostanie utworzony, oznacza to, że klawisz skrótu nie działa — patrz poniżej.

---

## Problem: Klawisz skrótu nie działa w Waylandzie

**Objaw:** CopyQ jest zainstalowany i skonfigurowany, ale naciśnięcie klawisza skrótu działa
nic na sesji Waylanda.

**Przyczyna:** Globalne skróty klawiszowe CopyQ nie działają niezawodnie na Waylandzie bez
dodatkowa konfiguracja. Dotyczy to KDE Plasma, GNOME i innych
Kompozytorzy Waylanda.

### Opcja 1: Ustawienia systemu KDE (zalecane dla plazmy KDE)

1. Otwórz **Ustawienia systemu → Skróty → Skróty niestandardowe**
2. Utwórz nowy skrót typu **Polecenie/URL**
3. Ustaw polecenie na:
__KOD_BLOKU_10__
4. Przypisz preferowaną kombinację klawiszy (np. `F9` lub `Ctrl+Alt+Spacja`)

### Opcja 2: dotool (działa na każdym kompozytorze Waylanda)

__KOD_BLOKU_11__

Następnie użyj menedżera skrótów na pulpicie, aby uruchomić:
__KOD_BLOKU_12__

### Opcja 3: ydotool

__KOD_BLOKU_13__

Następnie skonfiguruj skrót do uruchomienia:
__KOD_BLOKU_14__

### Opcja 4: GNOME (przy użyciu ustawień dconf / GNOME)

1. Otwórz **Ustawienia → Klawiatura → Skróty niestandardowe**
2. Dodaj nowy skrót za pomocą polecenia:
__KOD_BLOKU_15__
3. Przypisz kombinację klawiszy

### Opcja 5: CopyQ z poprawką Waylanda

Niektóre kompozytorzy Waylanda umożliwiają działanie CopyQ, jeśli zostaną uruchomione z:
__KOD_BLOKU_16__

Zmusza to CopyQ do korzystania z XWayland, który obsługuje globalne skróty klawiszowe.

---

## Problem: Tekst pojawia się, ale bez poprawek

**Objaw:** Dyktowanie działa, ale wszystko pozostaje zapisane małymi literami, bez poprawek gramatycznych.

**Sprawdź, czy LanguageTool jest uruchomiony:**
__KOD_BLOKU_17__

Jeśli zwróci błąd, oznacza to, że LanguageTool nie działa. Aura powinna to rozpocząć
automatycznie — sprawdź dziennik pod kątem błędów związanych z LanguageTool:

__KOD_BLOKU_18__

**Sprawdź dziennik LanguageTool:**
__KOD_BLOKU_19__

---

## Problem: Aura zawiesza się w trybie DEV_MODE

**Objaw:** Przy `DEV_MODE = 1`, Aura zawiesza się po pierwszym uruchomieniu i zatrzymuje się
odpowiadanie.

**Przyczyna:** Duża liczba logów z wielu wątków przeciąża system rejestrowania.

**Poprawka:** Dodaj filtr dziennika w `config/filters/settings_local_log_filter.py`:

__KOD_BLOKU_20__

Zapisz plik — Aura automatycznie przeładuje filtr. Nie ma potrzeby ponownego uruchamiania.

---

## Problem: plik plugins.zip rośnie w nieskończoność / Wysoki procesor

**Objaw:** 100% procesora, wentylatory pracują na pełnych obrotach, plik `plugins.zip` rośnie bez przerwy.

**Przyczyna:** Bezpieczny program pakujący przepakowuje pliki w nieskończonej pętli.

**Poprawka:** Upewnij się, że pliki `.blob` i `.zip` są wykluczone ze skanowania sygnatury czasowej.
Sprawdź `scripts/py/func/secure_packer_lib.py` wokół linii 86:

__KOD_BLOKU_21__

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
__KOD_BLOKU_22__
4. Czy ustawiono opcję „tylko_w_oknach” i aktywne jest niewłaściwe okno?
5. Czy najpierw dopasowuje się bardziej ogólną regułę? Reguły są przetwarzane od góry do dołu —
przedkładać szczegółowe zasady nad ogólne.

---

## Zbieranie dzienników w celu raportowania błędów

Zgłaszając problem, podaj:

__KOD_BLOKU_23__

Wyślij do: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)