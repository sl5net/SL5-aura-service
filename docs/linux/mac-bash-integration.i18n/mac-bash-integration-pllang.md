# Integracja powłoki macOS Bash

> **Domyślna powłoka przed macOS Catalina (10.15).** Od wersji Catalina, macOS jest dostarczany z Zsh jako domyślną powłoką. Jeśli korzystasz z nowoczesnego komputera Mac i nie zmieniłeś powłoki, zamiast tego zapoznaj się z przewodnikiem [macOS Zsh Integration](.././mac-zsh-integration.i18n/mac-zsh-integration-pllang.md).
>
> Możesz sprawdzić swoją obecną powłokę za pomocą:
> ```bzdura
> powtórz $SHELL
> ```

Aby ułatwić interakcję z interfejsem CLI STT (Speech-to-Text), możesz dodać funkcję skrótu do swojego `~/.bash_profile`. Dzięki temu możesz po prostu wpisać „twoje pytanie” w terminalu.

## Instrukcje konfiguracji

1. Otwórz konfigurację Bash w edytorze, który lubisz:
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
Dodaj alias nad funkcją `s()` w swoim `~/.bash_profile`.

- **macOS używa `~/.bash_profile` dla powłok logowania** (Terminal.app domyślnie otwiera powłoki logowania), podczas gdy Linux zazwyczaj używa `~/.bashrc`. Jeśli chcesz, aby funkcja była dostępna we wszystkich kontekstach, możesz skorzystać z jednego z drugiego:
__KOD_BLOKU_5__

- **macOS jest dostarczany z Bash 3.2** (ze względu na licencję GPLv3). Ta funkcja jest w pełni kompatybilna z Bash 3.2+. Jeśli potrzebujesz Bash 5, zainstaluj go poprzez Homebrew:
__KOD_BLOKU_6__

- **Ścieżka Pythona**: Upewnij się, że środowisko wirtualne jest skonfigurowane w `$PROJECT_ROOT/.venv`. Jeśli zarządzasz Pythonem za pomocą `pyenv` lub `conda`, dostosuj odpowiednio `PY_EXEC`.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu za pomocą pliku znacznika `/tmp`.
- **Automatyczny restart**: Jeśli backend nie działa, próbuje uruchomić `start_service` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.