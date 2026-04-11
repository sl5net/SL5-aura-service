# Integracja WSL (podsystem Windows dla systemu Linux).

WSL umożliwia uruchomienie pełnego środowiska Linux bezpośrednio w systemie Windows. Po skonfigurowaniu integracja z powłoką STT działa **identycznie jak przewodniki Linux Bash lub Zsh** — nie jest wymagana żadna adaptacja specyficzna dla systemu Windows dla samej funkcji powłoki.

> **Zalecane dla:** użytkowników systemu Windows, którzy znają terminal Linux lub którzy mają już zainstalowaną wersję WSL do prac programistycznych. WSL zapewnia najwierniejsze wrażenia i najmniejszą liczbę kompromisów w zakresie kompatybilności.

## Warunki wstępne

### Zainstaluj WSL (jednorazowa konfiguracja)

Otwórz PowerShell lub CMD **jako administrator** i uruchom:

__KOD_BLOKU_0__

To domyślnie instaluje WSL2 z Ubuntu. Uruchom ponownie komputer po wyświetleniu monitu.

Aby zainstalować konkretną dystrybucję:

__KOD_BLOKU_1__

Lista wszystkich dostępnych dystrybucji:

__KOD_BLOKU_2__

### Sprawdź wersję WSL

__KOD_BLOKU_3__

Upewnij się, że kolumna „WERSJA” pokazuje „2”. Jeśli pokazuje „1”, uaktualnij za pomocą:

__KOD_BLOKU_4__

## Integracja powłoki w WSL

Po uruchomieniu WSL otwórz terminal Linux i postępuj zgodnie z **przewodnikiem po powłoce Linuksa** dla preferowanej powłoki:

| Powłoka | Przewodnik |
|-------|-------|
| Bash (domyślnie WSL) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-pllang.md) |
| Zsz | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-pllang.md) |
| Ryba | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-pllang.md) |
| Ksz | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-pllang.md) |
| POSIX sh / Dash | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-pllang.md) |

W przypadku domyślnej konfiguracji WSL Ubuntu/Debian z Bash szybka ścieżka to:

__KOD_BLOKU_5__

## Uwagi specyficzne dla WSL

### Dostęp do plików Windows z WSL

Twoje dyski Windows są zamontowane w `/mnt/`:

__KOD_BLOKU_6__

Jeśli Twój projekt znajduje się w systemie plików Windows (np. `C:\Projects\stt`), ustaw `PROJECT_ROOT` na:

__KOD_BLOKU_7__

Dodaj tę linię do swojego `~/.bashrc` (lub odpowiednika twojej powłoki) **nad** funkcją `s()`.

> **Wskazówka dotycząca wydajności:** Aby uzyskać najlepszą wydajność we/wy, przechowuj pliki projektu w systemie plików WSL (np. `~/projects/stt`), a nie w `/mnt/c/...`. Dostęp między systemami plików pomiędzy WSL i Windows jest znacznie wolniejszy.

### Wirtualne środowisko Pythona w WSL

Utwórz i używaj standardowego środowiska wirtualnego Linux w WSL:

__KOD_BLOKU_8__

Ścieżka `PY_EXEC` w funkcji (`$PROJECT_ROOT/.venv/bin/python3`) będzie działać poprawnie bez zmian.

### Uruchamianie „s” z terminala Windows

[Windows Terminal](https://aka.ms/terminal) to zalecany sposób korzystania z WSL w systemie Windows. Obsługuje wiele kart, paneli i profili dla każdej dystrybucji WSL. Zainstaluj go ze sklepu Microsoft Store lub poprzez:

__KOD_BLOKU_9__

Ustaw swoją dystrybucję WSL jako profil domyślny w ustawieniach terminala Windows, aby uzyskać najbardziej płynne działanie.

### Docker i Kiwix w WSL

Skrypt pomocniczy Kiwix („kiwix-docker-start-if-not-running.sh”) wymaga Dockera. Zainstaluj Docker Desktop dla Windows i włącz integrację WSL 2:

1. Pobierz i zainstaluj [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. W Docker Desktop → Ustawienia → Zasoby → Integracja WSL włącz dystrybucję WSL.
3. Sprawdź w WSL:
__KOD_BLOKU_10__

### Wywołanie funkcji WSL `s` z Windows (opcjonalnie)

Jeśli chcesz wywołać skrót `s` z okna CMD systemu Windows lub PowerShell bez otwierania terminala WSL, możesz go owinąć:

__KOD_BLOKU_11__

__KOD_BLOKU_12__

> Flaga `-i` ładuje interaktywną powłokę, dzięki czemu `~/.bashrc` (i funkcja `s`) są pobierane automatycznie.

## Cechy

- **Pełna kompatybilność z Linuksem**: Wszystkie narzędzia uniksowe (`timeout`, `pgrep`, `mktemp`, `grep`) działają natywnie — nie są potrzebne żadne obejścia.
- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu poprzez zmienną `PROJECT_ROOT` ustawioną w konfiguracji powłoki.
- **Auto-Restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii (musi być uruchomiony Docker).
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.