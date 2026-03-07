# wyjaśnienie dokładnego zachowania przepływu pracy w systemie:
XSPACEbreakX
### Poprawione wyjaśnienie zintegrowanego przepływu pracy

pierwsza reguła dla **Transformacji wejściowej** i **Etykietowania** przed wykonaniem ostatecznej akcji wyszukiwania przez drugą regułę.

#### 1. Wejście: „was ist ein haus”

#### 2. Zasada 1: Etykietowanie/Transformacja

__KOD_BLOKU_0__

* **Działanie:** Wprowadzone przez użytkownika „was ist ein haus” zostało pomyślnie dopasowane.
* **Wynik (wewnętrzny):** System generuje wynik/etykietę „was ist ein haus (Begriffsklärung)”`.
* **Kontynuacja:** Ponieważ `fullMatchStop` znajduje się na `listie_pominięć`, dopasowanie reguły **NIE ZATRZYMUJE się**. Proces przechodzi do następnej reguły, przenosząc *przekształconą* lub *oznaczoną* treść.

#### 3. Zasada 2: Ogólna akcja/egzekucja

__KOD_BLOKU_1__

* **Działanie:** System prawdopodobnie dopasowuje teraz **bieżący wynik/etykietę** z poprzedniego kroku, czyli „was ist ein haus (Begriffsklärung)”` (lub pasuje do oryginalnych danych wejściowych, ale wykonany skrypt nadaje priorytet przekształconej etykiecie).
* **Dopasowanie prefiksu:** Przedrostek („był ist”) nadal pasuje.
* **Grupa przechwytująca:** Grupa przechwytująca `(?P<wyszukiwanie>.*)` przechwytuje resztę ciągu:
* Jeśli system używa **Zasady 1 jako nowego wejścia**, przechwytuje: **`haus (Begriffsklärung)`** (lub pełny przekształcony ciąg znaków, który jest następnie analizowany przez skrypt wykonawczy).
* **Wykonanie:** Wykonywany jest skrypt `wikipedia_local.py`.

#### 4. Końcowe działanie:

* Skrypt `wikipedia_local.py` odbiera specjalnie zmodyfikowane wyszukiwane hasło/etykietę.
* Skrypt przeszukuje Wikipedię pod kątem zamierzonego terminu: **`haus (Begriffsklärung)`**.

**Wniosek:**

Ta konfiguracja to elegancki sposób obsługi niejednoznacznych lub ogólnych zapytań. Dzięki modyfikacji danych wejściowych przez konkretną regułę lub wygenerowaniu docelowej etykiety, a następnie wymuszeniu kontynuacji procesu do ogólnej reguły wyszukiwania, masz pewność, że wyszukiwanie w Wikipedii nie zostanie przeprowadzone dla ogólnego „haus”, ale dla konkretnego, jednoznacznego wpisu: **`haus (Begriffsklärung)`**.

Potwierdza to, że wykluczenie `fullMatchStop` jest **niezbędne**, aby umożliwić pierwszej regule wstępne przetworzenie i wzbogacenie zapytania, zanim zostanie zastosowane do reguły wykonania ogólnego przeznaczenia.

(sl5,4.12.'25 12:24 czw)