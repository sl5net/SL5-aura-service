### Dokumentacja Markdown (`docs/AHK_SCRIPTS.md`)

# Infrastruktura AutoHotkey dla usługi SL5-Aura

Ponieważ system Windows obsługuje blokady plików i klawisze skrótów systemowych inaczej niż Linux, w tym projekcie zastosowano zestaw skryptów AutoHotkey (v2), aby wypełnić lukę pomiędzy silnikiem Python STT a interfejsem użytkownika systemu Windows.

## Przegląd skryptów

### 1. `trigger-hotkeys.ahk`
* **Cel:** Główny interfejs użytkownika do kontrolowania usługi.
* **Kluczowe cechy:**
* Przechwytuje **F10** i **F11**, aby rozpocząć/zatrzymać dyktowanie.
* Używa „zaczepu klawiatury” do zastąpienia domyślnego zachowania systemu Windows (np. F10 aktywującego pasek menu).
* **Wdrożenie:** Zaprojektowane do rejestracji za pomocą Harmonogramu zadań systemu Windows z „najwyższymi uprawnieniami”, dzięki czemu może przechwytywać skróty klawiszowe nawet wtedy, gdy użytkownik pracuje w aplikacji na poziomie administratora.

### 2. `type_watcher.ahk`
* **Cel:** Działa jako „konsument” w rurociągu STT.
* **Kluczowe cechy:**
* Obserwuje katalog tymczasowy dla przychodzących plików `.txt` generowanych przez silnik Pythona.
* **Maszyna Stanowa (Mapa Zombie):** Implementuje mapę opartą na pamięci, aby mieć pewność, że każdy plik zostanie wpisany dokładnie raz. Zapobiega to „podwójnemu pisaniu” spowodowanemu przez zbędne zdarzenia w systemie plików Windows (dodano/zmodyfikowano).
* **Bezpieczne pisanie:** Używa opcji „SendText”, aby zapewnić poprawną obsługę znaków specjalnych w każdym aktywnym edytorze.
* **Niezawodne czyszczenie:** Zarządza usuwaniem plików za pomocą logiki ponawiania w celu obsługi blokad dostępu do plików w systemie Windows.

### 3. `scripts/ahk/sync_editor.ahk`
* **Cel:** Zapewnia płynną synchronizację pomiędzy dyskiem a edytorem tekstu (np. Notepad++).
* **Kluczowe cechy:**
* **Zapisywanie na żądanie:** Może zostać wywołane przez Pythona w celu wymuszenia `Ctrl+S` w edytorze, zanim silnik odczyta plik.
* **Automatyzator dialogów:** automatycznie wykrywa i potwierdza okna dialogowe ponownego ładowania „Plik zmodyfikowany przez inny program”, zapewniając płynną aktualizację w czasie rzeczywistym.
* **Wizualna informacja zwrotna:** Zapewnia krótkotrwałe powiadomienia informujące użytkownika o wprowadzaniu poprawek.

### 4. `scripts/notification_watcher.ahk`
* **Cel:** Dostarcza informacji zwrotnych do interfejsu użytkownika dla procesów w tle.
* **Kluczowe cechy:**
* Monitoruje określone pliki stanu lub zdarzenia, aby wyświetlać powiadomienia użytkownikowi.
* Oddziela logikę „obliczania” komunikatu (Python) od „wyświetlania” go (AHK), zapewniając, że główny silnik STT nie jest blokowany przez interakcje interfejsu użytkownika.


---

### Opcja zastępcza bez uprawnień administratora
Jeśli aplikacja jest uruchamiana bez uprawnień administratora:
- **Funkcjonalność:** Usługa pozostaje w pełni funkcjonalna.
- **Ograniczenia skrótów klawiszowych:** Klawisze zarezerwowane dla systemu, takie jak **F10**, mogą nadal uruchamiać menu Windows. W takim przypadku zaleca się zmianę skrótów klawiszowych na klawisze niesystemowe (np. `F9` lub `Insert`).
- **Harmonogram zadań:** Jeśli podczas instalacji administracyjnej utworzono zadanie „AuraDictation_Hotkeys”, skrypt będzie działał z wysokimi uprawnieniami nawet dla standardowego użytkownika. Jeśli nie, plik `start_dictation.bat` uruchomi po cichu lokalną instancję na poziomie użytkownika.

---

### 3. Warum "nervige Meldungen" erscheinen und wie man sie im AHK-Code stoppt
Um sicherzustellen, dass das Skript selbst niemals den Nutzer mit Popups stört, füge diese „Silent-Flags” Oben in deine `.ahk` Dateien ein:

__KOD_BLOKU_0__

### 4. Strategia dla skrótów klawiszowych (alternatywa F10)
Da F10 ohne Admin-Rechte for Windows fast unmöglich sauber abzufangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

__KOD_BLOKU_1__

### Zusammenfassung der Verbesserungen:
1. **Data partii:** Nutzt `start "" /b`, um das schwarze Fenster zu vermeiden, und prüft vorher, ob der Admin-Task schon läuft.
2. **Transparenz:** Die Doku erklärt nun offen: „Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10”.
3. **AHK-Skrypt:** Nutzt `#SingleInstance Force`, czyli „Starsza instancja jest uruchomiona” – Dialog zu unterdrücken.

Damit wirkt die Software viel professionaleller („Smooth”), da sie im Hintergrund startet, ohne dass der Nutzer mit technischen Szczegóły lub Bestätigungsfenstern konfrontiert wird.
XSPACEbreakX
XSPACEbreakX
---

### Dlaczego ta dokumentacja jest ważna:
Dokumentując wymagania **„Mapa Zombie”** i **„Harmonogram zadań/administrator”**, wyjaśniasz innym programistom (i sobie w przyszłości), dlaczego kod jest bardziej złożony niż prosty skrypt dla systemu Linux. Zamienia „dziwne obejścia” w „inżynieryjne rozwiązania ograniczeń systemu Windows”.

(s,29.1.'26 11:02 czw)