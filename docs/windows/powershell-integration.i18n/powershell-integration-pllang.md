# Integracja z PowerShellem (Windows)

Aby ułatwić interakcję z interfejsem CLI STT (przetwarzanie mowy na tekst), możesz dodać funkcję skrótu do swojego profilu programu PowerShell. Dzięki temu możesz po prostu wpisać „twoje pytanie” w dowolnym oknie programu PowerShell.

> **Dotyczy:** Windows PowerShell 5.1 i PowerShell 7+ (zalecane). PowerShell 7 można zainstalować z [Microsoft Store](https://aka.ms/powershell) lub poprzez `winget install Microsoft.PowerShell`.

## Instrukcje konfiguracji

### 1. Zezwól na wykonanie skryptu (jednorazowa konfiguracja)

PowerShell domyślnie blokuje skrypty. Otwórz PowerShell **jako administrator** i uruchom:

__KOD_BLOKU_0__

### 2. Otwórz swój profil PowerShell

__KOD_BLOKU_1__

Jeśli plik jeszcze nie istnieje, utwórz go najpierw:

__KOD_BLOKU_2__

### 3. Wklej następujący blok na końcu pliku

__KOD_BLOKU_3__

### 4. Załaduj ponownie swój profil

__KOD_BLOKU_4__

## Uwagi specyficzne dla systemu Windows

- **Ścieżka Pythona**: W systemie Windows plik binarny środowiska wirtualnego znajduje się pod adresem `.venv\Scripts\python.exe` zamiast `.venv/bin/python3`. Dostosuj `$PY_EXEC`, jeśli Twoja konfiguracja jest inna.
- **Zmienna środowiskowa `PROJECT_ROOT`**: Ustaw tę opcję w systemowych zmiennych środowiskowych lub dodaj następujący wiersz nad funkcją w swoim profilu:
__KOD_BLOKU_5__
- **`timeout` / `mktemp`**: Te narzędzia uniksowe nie są dostępne natywnie. Powyższy skrypt używa odpowiedników natywnych dla PowerShell („WaitForExit” z milisekundowym limitem czasu i „GetTempFileName()”).
- **`pgrep`**: Zastąpione przez `Get-Process -Name „streamlit”`.
- **`start_service` / `update_github_ip`**: Muszą być one zdefiniowane jako funkcje PowerShell („Start-Service-STT”, `Update-GithubIp`) w tym samym pliku profilu, przed funkcją `s`.
- **Skrypt WSL Kiwix**: Jeśli dostępny jest `bash` (przez WSL), skrypt pomocniczy `.sh` będzie działał bez zmian. W przeciwnym razie dostosuj go do odpowiednika `.ps1` lub `.bat`.
- **Wiele wersji PowerShell**: `$PROFILE` wskazuje na różne pliki dla Windows PowerShell 5.1 i PowerShell 7. Aby sprawdzić, który plik profilu jest aktywny, uruchom `$PROFILE` w każdej wersji.

## Cechy

- **Ścieżki dynamiczne**: Automatycznie znajduje katalog główny projektu poprzez zmienną środowiskową `PROJECT_ROOT`.
- **Auto-Restart**: Jeśli backend nie działa, próbuje uruchomić `Start-Service-STT` i lokalne usługi Wikipedii.
- **Inteligentne limity czasu**: Najpierw próbuje uzyskać szybką reakcję w ciągu 2 sekund, a następnie powraca do trybu głębokiego przetwarzania trwającego 70 sekund.