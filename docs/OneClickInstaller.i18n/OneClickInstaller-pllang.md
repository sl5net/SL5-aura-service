> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# Instalator 1-Click (Bez konfiguracji)

Uruchom **Aura** na swoim komputerze za pomocą jednego kliknięcia. Nie jest wymagana żadna wiedza programistyczna, polecenia w terminalu ani ręczna konfiguracja Pythona.

---

## Zero Wymagań Wstępnych

Nie potrzebujesz:
- Python wstępnie zainstalowany
- Git lub repozytoria kodu
- Doświadczenie w pracy z wierszem poleceń lub terminalem

---

## Szybki start

### Metoda 1: Jednolinijkowiec internetowy (Najszybsza i zalecana dla Linux / macOS)
Oszczędza około 30 sekund ręcznego obsługiwania plików i uruchamia się od razu w twoim terminalu:

**Linux i macOS:**
#### Kod jednowierszowy Web CodeBerg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
lub
#### Jednolinijkowy Web GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Kod jednowierszowy Web CodeBerg

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
lub
#### Web One-Liner github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Metoda 2: Samodzielny plik binarny (Windows i kliknięcie na pulpicie)

### 2.1 Pobierz instalator
Pobierz pojedynczy plik instalacyjny odpowiadający Twojemu systemowi operacyjnemu z [Najnowszego wydania na GitHub]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Uruchom Instalator

zmień nazwę aura-installer-windows.exe.zip na aura-installer-windows.exe

Kliknij dwukrotnie pobrany plik. Pojawi się okno instalacyjne i automatycznie przygotuje środowisko.

### 2.3. Rozpocznij dyktowanie
Po zakończeniu Aura tworzy skrót na pulpicie i zaczyna nasłuchiwać od razu.

---

## Co dzieje się automatycznie?

Kiedy uruchamiasz instalator, Aura automatycznie:
- Konfiguruje lokalny, prywatny silnik rozpoznawania mowy.
- Pobiera domyślne modele głosowe.
- Ustawia wszystkie niezbędne skróty systemowe i ikony uruchamiania na pulpicie.

---

## Szczegóły instalacji i wymagania

- **Czas instalacji:** Około 2–3 minut.
- **Wymagana przestrzeń dyskowa:** Minimum ~1,5 GB (do 2,5 GB w zależności od wybranych modeli językowych).
- **Katalog instalacji:**
  - **Linux i macOS:** `~/opt/sl5-aura-service`
  - **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Kolejne kroki

- **Tryb Babci:** Wpisz jedno słowo do swojego pliku zasad i obserwuj, jak Aura automatycznie tworzy zasady.
- **Ucz się z koanami:** Poznaj koncepcje krok po kroku w [Getting Started](../GettingStarted.i18n/GettingStarted-pllang.md).
