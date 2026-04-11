# Integracja z wierszem poleceń (CMD) (Windows)

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text) z wiersza poleceń systemu Windows, możesz utworzyć plik wsadowy `s.bat` i umieścić go w ścieżce `PATH`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w dowolnym oknie CMD.

> **Uwaga:** CMD (cmd.exe) to starsza powłoka systemu Windows, która ma znaczne ograniczenia w porównaniu z powłokami PowerShell i Unix. Aby uzyskać bogatsze wrażenia, rozważ zamiast tego użycie [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-pllang.md) lub [WSL Integration](.././wsl-integration.i18n/wsl-integration-pllang.md).

## Instrukcje konfiguracji

### 1. Utwórz katalog na swoje osobiste skrypty (jeśli jeszcze tego nie zrobiłeś)

__KOD_BLOKU_0__

### 2. Dodaj ten katalog do swojej PATH (jednorazowa konfiguracja)

Otwórz **Właściwości systemu → Zmienne środowiskowe** i dodaj `%USERPROFILE%\bin` do zmiennej `PATH` użytkownika.

Alternatywnie uruchom to w wierszu polecenia CMD z podwyższonym poziomem uprawnień (obowiązuje po ponownym otwarciu CMD):

__KOD_BLOKU_1__

### 3. Utwórz plik wsadowy

Otwórz Notatnik lub dowolny edytor tekstu i zapisz następujące dane jako `%USERPROFILE%\bin\s.bat`:

__KOD_BLOKU_2__

### 4. Przetestuj

Otwórz nowe okno CMD (aby załadowana została zaktualizowana PATH) i wpisz:

__KOD_BLOKU_3__

## Uwagi specyficzne dla CMD

- **Brak natywnego limitu czasu procesu**: CMD nie ma odpowiednika uniksowego limitu czasu. Ten skrypt deleguje logikę limitu czasu do funkcji „WaitForExit” programu PowerShell. PowerShell musi być dostępny (jest we wszystkich nowoczesnych systemach Windows).
- **`PROJECT_ROOT`**: Ustaw tę opcję jako stałą zmienną środowiskową użytkownika poprzez Właściwości systemu lub zakoduj na stałe ścieżkę w pliku `.bat`.
- **Skrypty pomocnicze**: `update_github_ip.bat` i `start_service.bat` muszą istnieć w Twojej `PATH` lub w `%USERPROFILE%\bin`. Są to odpowiedniki CMD funkcji powłoki `update_github_ip` i `start_service`.
- **`bash` dla skryptu Kiwix**: Jeśli zainstalowany jest WSL, `bash` jest dostępny w CMD i skrypt `.sh` zostanie uruchomiony bezpośrednio. W przeciwnym razie dostosuj `kiwix-docker-start-if-not-running.sh` do odpowiednika `.bat`.
- **Obsługa ofert**: CMD ma rygorystyczne i niestabilne zasady dotyczące kwotowań. Jeśli zapytanie zawiera znaki specjalne (`&`, `|`, `>`, `<`), umieść całe zapytanie w cudzysłowie: `s "Twoje i pytanie"`.
- **`ograniczenie set /p`**: `set /p` czyta tylko pierwszą linię pliku. W przypadku wyjścia wielowierszowego użyj `type`, aby bezpośrednio wydrukować plik (tak jak zrobiono to w gałęzi o długim czasie oczekiwania).

## Cechy

- **Ścieżki dynamiczne**: Automatycznie rozpoznaje ścieżki poprzez zmienną środowiskową `PROJECT_ROOT`.
- **Auto-Restart**: Jeśli backend nie działa, wywołuje `start_service.bat` i próbuje uruchomić lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.