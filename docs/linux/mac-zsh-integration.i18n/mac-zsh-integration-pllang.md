# Integracja z powłoką macOS Zsh

> **Domyślna powłoka od macOS Catalina (10.15).** Jeśli korzystasz z systemu macOS Mojave lub starszego, zapoznaj się z przewodnikiem [macOS Bash Integration](.././mac-bash-integration.i18n/mac-bash-integration-pllang.md).

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do pliku `~/.zshrc`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

1. Otwórz konfigurację Zsh w edytorze, który lubisz:
__KOD_BLOKU_0__

2. Wklej następujący blok na końcu pliku:

__KOD_BLOKU_1__

3. Załaduj ponownie swoją konfigurację:
__KOD_BLOKU_2__

## Uwagi specyficzne dla systemu macOS

- ** Limit czasu nie jest wbudowany w macOS.** Zainstaluj go poprzez Homebrew przed użyciem tej funkcji:
__KOD_BLOKU_3__
Po instalacji parametr „timeout” jest dostępny jako „gtimeout”. Dodaj alias lub zamień „timeout” na „gtimeout” w powyższej funkcji:
__KOD_BLOKU_4__
Dodaj alias nad funkcją `s()` w pliku `~/.zshrc`.

- **`pgrep`** jest domyślnie dostępny na macOS.

- **Ścieżka Pythona**: Upewnij się, że środowisko wirtualne jest skonfigurowane w `$PROJECT_ROOT/.venv`. Jeśli zarządzasz Pythonem za pomocą `pyenv` lub `conda`, dostosuj odpowiednio `PY_EXEC`.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.