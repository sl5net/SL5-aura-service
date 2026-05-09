# Powiadomienia o przepływie pracy (alerty dźwiękowe)

Aby zwiększyć produktywność, możesz skonfigurować lokalny alias Git, który wypycha Twój kod i automatycznie ostrzega Cię (głosowo lub dźwiękowo), gdy tylko zakończy się przepływ pracy GitHub Actions. Zapobiega to „zmęczeniu oglądaniem GitHuba” i pozwala skupić się na innych zadaniach.

### Warunki wstępne

Potrzebujesz **GitHub CLI** i mechanizmu zamiany tekstu na mowę lub odtwarzacza dźwięku zainstalowanego w swoim systemie.

**Dla Manjaro/Arch Linux:**
__KOD_BLOKU_0__

### Organizować coś

Uruchom następującą komendę w swoim terminalu, aby utworzyć globalny alias Git o nazwie `pushsound`:

__KOD_BLOKU_1__

### Użycie

Zamiast `git Push` po prostu uruchom:
__KOD_BLOKU_2__
Twój terminal będzie czekać na zakończenie przepływu pracy, a następnie ogłosi: * „cały przepływ pracy na Githubie został zakończony”*.

---

### Personalizacja i alternatywy

W zależności od preferencji możesz chcieć użyć innego aliasu lub metody powiadamiania.

#### 1. Zalecane nazwy aliasów
Jeśli „pushsound” jest za długi do wpisania, rozważ następujące alternatywy:
* `git pw` (Push & Watch) — **Zalecane ze względu na szybkość.**
* `git sync` (oznacza pchanie i czekanie na „zielone światło”)
* `git palert` (alarm push)

#### 2. Style powiadomień
Możesz zamienić część `espeak-ng` na inne typy alertów:

* **Powiadomienie na pulpicie:**
`... && powiadom-wyślij "Akcja GitHub" "Przepływ pracy zakończony!"`
* **Dźwięk systemowy (dzwonek):**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **Kombinacja (dźwięk + głos):**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Gotowe"`

#### 3. Zaawansowane: Wersja bezpieczna dla zespołu
Jeśli wielu programistów jednocześnie przesyła dane do tego samego repozytorium, domyślne polecenie może wyśledzić nieprawidłowe uruchomienie. Użyj tej wersji „Branch-Safe”, aby oglądać tylko swoją własną, bieżącą gałąź:

__KOD_BLOKU_3__

### Rozwiązywanie problemów
* **„Nie znaleziono żadnych uruchomień”:** Dołączamy „uśpienie 3”, ponieważ GitHub potrzebuje chwili na zarejestrowanie wypychania i rozpoczęcie przepływu pracy. Jeśli masz bardzo wolne połączenie, być może będziesz musiał zwiększyć tę wartość do „uśpienia 5”.
* **Sygnały dźwiękowe terminala:** Jeśli `espeak-ng` nie działa, upewnij się, że dźwięk nie jest wyciszony i pakiet jest poprawnie zainstalowany.