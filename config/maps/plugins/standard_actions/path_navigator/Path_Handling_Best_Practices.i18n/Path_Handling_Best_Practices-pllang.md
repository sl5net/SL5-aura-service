# Katalog domowy i obsługa ścieżek między platformami

Aura została zaprojektowana do pracy na wielu systemach operacyjnych. Aby mieć pewność, że polecenia nawigacji w systemie plików będą działać niezależnie od tego, czy korzystasz z systemu Linux, macOS czy Windows, ciągi ścieżek są analizowane dynamicznie przed zarejestrowaniem ich w aktywnych mapach rozmytych.

---

## Logika normalizacji ścieżki (`FUZZY_MAP_pre.py`)

Logika dynamicznego mapowania ścieżek opiera się na następujących standardowych praktykach:

### 1. Redukcja tyldy (POSIX)
W systemach zgodnych z POSIX (Linux i macOS) ścieżki bezwzględne pasujące do katalogu domowego użytkownika (np. `/home/nazwa użytkownika/`) są konwertowane na ścieżki względne `~` podczas uruchamiania. Dzięki temu długość ciągów jest krótsza i sprawia, że wygenerowane reguły można przenosić pomiędzy różnymi użytkownikami tego samego systemu operacyjnego:

__KOD_BLOKU_0__

### 2. Absolutne zachowanie ścieżki (Windows)
System Windows nie ocenia znaku `~` w standardowym wierszu poleceń (`cmd.exe`) lub w środowiskach PowerShell. Dlatego też, gdy wtyczka wykryje środowisko Windows (`sys.platform == 'win32'`), zachowuje w pełni kwalifikowaną ścieżkę bezwzględną (np. `C:\Users\nazwa użytkownika\...`), aby mieć pewność, że wykonanie polecenia nie zakończy się niepowodzeniem.

### 3. Normalizacja ukośnika (`as_posix()`)
Aura używa wewnętrznie ukośników w stylu POSIX (`/`) dla map konfiguracyjnych. Skrypt normalizuje wszystkie separatory ścieżek zależne od systemu operacyjnego, wykorzystując metodę Pythona `pathlib.Path.as_posix()`, która automatycznie czyści ukośniki odwrotne (`\`) w środowiskach Windows.