# Instalator jednym kliknięciem (konfiguracja zerowa)

Uruchom **Aurę** na swoim komputerze jednym kliknięciem. Nie jest wymagana żadna wiedza programistyczna, polecenia terminala ani ręczna konfiguracja języka Python.

---

## Zero wymagań wstępnych

**nie** potrzebujesz:
- Preinstalowany Python
- Repozytoria Git lub kodu
- Doświadczenie z wiersza poleceń lub terminala

---

## Szybki start

### Metoda 1: internetowa (najszybsza i zalecana dla systemu Linux/macOS)
Oszczędza ~30 sekund ręcznej obsługi plików i uruchamia się natychmiast w terminalu:

**Linux i macOS:**

__KOD_BLOKU_0__

**Windows (PowerShell):**
__KOD_BLOKU_1__

Metoda 2: Samodzielny plik binarny (kliknięcie w systemie Windows i na komputerze)

### 2.1 Pobierz instalator
Pobierz pojedynczy plik instalacyjny pasujący do Twojego systemu operacyjnego z [najnowszej wersji GitHub]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Uruchom instalatora

zmień nazwę aura-installer-windows.exe.zip na aura-installer-windows.exe

Kliknij dwukrotnie pobrany plik. Pojawi się okno konfiguracji i automatycznie przygotuje środowisko.

### 2.3. Zacznij dyktować
Po zakończeniu Aura tworzy skrót na pulpicie i natychmiast rozpoczyna słuchanie.

---

## Co dzieje się automatycznie?

Po uruchomieniu instalatora Aura automatycznie:
- Konfiguruje lokalny, prywatny silnik rozpoznawania mowy.
- Pobiera domyślne modele głosu.
- Konfiguruje wszystkie niezbędne skróty systemowe i programy uruchamiające na pulpicie.

---

## Szczegóły i wymagania dotyczące instalacji

- **Czas instalacji:** Około 2–3 minuty.
- **Wymagane miejsce na dysku:** Minimum ~1,5 GB (do 2,5 GB w zależności od wybranych modeli językowych).
- **Katalog instalacyjny:**
- **Linux i macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Następne kroki

- **Tryb babci:** Wpisz pojedyncze słowo do pliku reguł i zobacz, jak Aura automatycznie tworzy reguły.
- **Ucz się z Koansem:** Poznaj szczegółowe koncepcje w [Getting Started](../GettingStarted.i18n/GettingStarted-pllang.md).