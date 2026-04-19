# Ogólnosystemowy głos offline na polecenia lub tekst, system podłączany

## Szybki start
1. Pobierz lub sklonuj to repozytorium
2. Uruchom skrypt instalacyjny dla swojego systemu operacyjnego (zobacz folder `setup/`):
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
===> 🧩 przeczytaj [docs/LINUX_WAYLAND_dotool](../docs/LINUX_WAYLAND_dotool.i18n/LINUX_WAYLAND_dotool-pllang.md)
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Uruchom Aurę: `./scripts/restart_venv_and_run-server.sh`
4. Naciśnij klawisz skrótu i mów — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-pllang.md)**


**⚠️ Wymagania systemowe i kompatybilność**

* **Windows:** ✅ W pełni obsługiwane (używa AutoHotkey/PowerShell).
* **macOS:** ✅ W pełni obsługiwany (używa AppleScript).
* **Linux (X11/Xorg):** ✅ W pełni obsługiwane.
* **Linux (Wayland):** ✅ Pełne wsparcie (testowane na KDE Plasma 6 / Wayland).
* **Linux (wersja krocząca oparta na CachyOS / Arch):** ✅ W pełni obsługiwane.
Wymaga mimalloc (`sudo pacman -S mimalloc`) ze względu na kompatybilność z glibc 2.43.
XSPACEbreakX
SL5 Aura to kompletny **asystent głosowy offline** zbudowany na bazie **Vosk** (dla zamiany mowy na tekst) i **LanguageTool** (dla gramatyki/stylu), wyposażony w opcjonalną funkcję **Local LLM (Ollama) Fallback** do kreatywnych odpowiedzi i zaawansowanego dopasowywania rozmytego. Przekształca Twój głos w precyzyjne działania i tekst, zaprojektowany z myślą o maksymalnej personalizacji poprzez podłączany system reguł i dynamiczny silnik skryptowy.
XSPACEbreakX
Tłumaczenia: Ten dokument istnieje również w [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Uwaga: Wiele tekstów to wygenerowane maszynowo tłumaczenia oryginalnej dokumentacji w języku angielskim i mają one wyłącznie charakter ogólny. W przypadku rozbieżności lub niejasności, zawsze obowiązuje wersja angielska. Czekamy na pomoc społeczności w ulepszaniu tego tłumaczenia!

### 📺 Wersja demonstracyjna terminala

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Wskazówka:** Aby uzyskać lepszą obsługę terminala, zobacz [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-pllang.md).

### 🎥 Samouczek wideo
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Link alternatywny: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*


## Kluczowe funkcje

* **Offline i prywatnie:** 100% lokalnie. Żadne dane nigdy nie opuszczają Twojej maszyny.
* **Dynamiczny silnik skryptowy:** Wyjdź poza zastępowanie tekstu. Reguły mogą uruchamiać niestandardowe skrypty Pythona (`on_match_exec`) w celu wykonywania zaawansowanych działań, takich jak wywoływanie interfejsów API (np. przeszukiwanie Wikipedii), interakcja z plikami (np. zarządzanie listą zadań do wykonania) lub generowanie zawartości dynamicznej (np. kontekstowe powitanie e-mail).
* **Reguły uwzględniające kontekst:** Ogranicz reguły do określonych aplikacji. Używając opcji `only_in_windows`, możesz mieć pewność, że reguła zostanie wyzwolona tylko wtedy, gdy aktywny będzie określony tytuł okna (np. „Terminal”, „Kod VS” lub „Przeglądarka”). Działa to na wielu platformach (Linux, Windows, macOS).
* **Silnik transformacji o wysokim poziomie kontroli:** implementuje oparty na konfiguracji, wysoce konfigurowalny potok przetwarzania. Priorytet reguł, wykrywanie poleceń i transformacje tekstu są określane wyłącznie na podstawie kolejności reguł w Fuzzy Maps, co wymaga **konfiguracji, a nie kodowania**.
* **Oszczędne wykorzystanie pamięci RAM:** Inteligentnie zarządza pamięcią, wstępnie ładując modele tylko wtedy, gdy dostępna jest wystarczająca ilość wolnej pamięci RAM, zapewniając, że inne aplikacje (takie jak gry komputerowe) zawsze mają priorytet.
* **Wiele platform:** działa na systemach Linux, macOS i Windows.
* **W pełni zautomatyzowany:** Zarządza własnym serwerem LanguageTool (ale możesz także użyć zewnętrznego).
* **Niezwykła szybkość:** Inteligentne buforowanie zapewnia natychmiastowe powiadomienia „Słuchanie…” i szybkie przetwarzanie.

## Dokumentacja

Aby uzyskać pełne informacje techniczne, w tym wszystkie moduły i skrypty, odwiedź naszą oficjalną stronę dokumentacji. Jest generowany automatycznie i zawsze aktualny.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### Stan kompilacji
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/29xiwIW1ZHQ )
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**Przeczytaj to w innych językach:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-pllang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-pllang.md) | [🇪🇸 Español](../README.i18n/README-eslang-pllang.md) | [🇫🇷 Français](../README.i18n/README-frlang-pllang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-pllang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-pllang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-pllang.md) | [🇵🇱 Polski](../README.i18n/README-pllang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-pllang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-pllang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-pllang.md)

---







## Instalacja

### 🎥 Szybka instalacja bez moderacji (Manjaro/Arch Video)
Obejrzyj cały 6-minutowy proces konfiguracji:
* **Pobieranie:** ~3 minuty
* **Konfiguracja i pierwsze uruchomienie:** ~3 minuty (w tym kreator powitalny)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


Konfiguracja jest procesem dwuetapowym:
1. Pobierz ostatnią wersję lub master (https://github.com/sl5net/SL5-aura-service/archive/master.zip) lub sklonuj to repozytorium na swój komputer.
2. Uruchom jednorazowy skrypt instalacyjny dla swojego systemu operacyjnego.

Skrypty instalacyjne obsługują wszystko: zależności systemowe, środowisko Python i pobieranie niezbędnych modeli i narzędzi (~4 GB) bezpośrednio z naszych wydań GitHub w celu uzyskania maksymalnej szybkości.


#### Dla systemów Linux, macOS i Windows (z opcjonalnym wykluczeniem języka)

Aby zaoszczędzić miejsce na dysku i przepustowość, możesz podczas instalacji wykluczyć określone modele językowe („de”, „en”) lub wszystkie opcjonalne modele („all”). **Podstawowe komponenty (LanguageTool, lid.176) są zawsze uwzględnione.**

Otwórz terminal w katalogu głównym projektu i uruchom skrypt dla swojego systemu:

__KOD_BLOKU_0__

#### Dla systemu Windows
Uruchom skrypt instalacyjny z uprawnieniami administratora.

**Zainstaluj narzędzie do odczytu i uruchamiania, np. [CopyQ](https://github.com/hluk/CopyQ) lub [AutoHotkey v2](https://www.autohotkey.com/)**. Jest to wymagane dla obserwatora wpisując tekst.

Instalacja jest w pełni zautomatyzowana i zajmuje około **8-10 minut** w przypadku użycia 2 modeli w nowym systemie.

1. Przejdź do folderu „setup”.
2. Kliknij dwukrotnie **`windows11_setup_with_ahk_copyq.bat`**.
* *Skrypt automatycznie wyświetli monit o uprawnienia administratora.*
* *Instaluje system podstawowy, modele językowe, **AutoHotkey v2** i **CopyQ**.*
3. Po zakończeniu instalacji **Aura Dictation** uruchomi się automatycznie.

> **Uwaga:** Nie musisz wcześniej instalować Pythona ani Gita; skrypt obsługuje wszystko.

---

#### Instalacja zaawansowana/niestandardowa
Jeśli nie chcesz instalować narzędzi klienckich (AHK/CopyQ) lub chcesz zaoszczędzić miejsce na dysku, wykluczając określone języki, możesz uruchomić podstawowy skrypt za pomocą wiersza poleceń:

__KOD_BLOKU_1__


---

## Użycie

### 1. Uruchom usługi

#### W systemie Linux i macOS
Wszystko obsługuje jeden skrypt. Uruchamia główną usługę dyktowania i przeglądarkę plików automatycznie w tle.
__KOD_BLOKU_2__

#### W systemie Windows
Uruchomienie usługi jest **dwuetapowym procesem ręcznym**:

1. **Uruchom usługę główną:** Uruchom `start_aura.bat`. lub rozpocznij usługę od `.venv` za pomocą `python3`

### 2. Skonfiguruj swój skrót

Aby uruchomić dyktowanie, potrzebujesz globalnego skrótu, który tworzy określony plik. Gorąco polecamy narzędzie wieloplatformowe [CopyQ](https://github.com/hluk/CopyQ).

#### Nasza rekomendacja: CopyQ

Utwórz nowe polecenie w CopyQ za pomocą globalnego skrótu.

**Polecenie dla systemu Linux/macOS:**
__KOD_BLOKU_3__

**Polecenie dla Windows przy użyciu [CopyQ](https://github.com/hluk/CopyQ):**
__KOD_BLOKU_4__


**Polecenie dla Windows przy użyciu [AutoHotkey](https://AutoHotkey.com):**
__KOD_BLOKU_5__


### 3. Zacznij dyktować!
Kliknij dowolne pole tekstowe, naciśnij klawisz skrótu, a pojawi się powiadomienie „Słucham…”. Mów wyraźnie, a potem pauzuj. Poprawiony tekst zostanie wpisany za Ciebie.

---


## Zaawansowana konfiguracja (opcjonalnie)

Możesz dostosować zachowanie aplikacji, tworząc plik ustawień lokalnych.

1. Przejdź do katalogu `config/`.
2. Utwórz kopię pliku `config/settings_local.py_Example.txt` i zmień jej nazwę na `config/settings_local.py`.
3. Edytuj plik `config/settings_local.py` (zastępuje to wszelkie ustawienia z głównego pliku `config/settings.py`).

Ten plik `config/settings_local.py` jest domyślnie ignorowany przez Git, więc Twoje osobiste zmiany nie zostaną nadpisane przez aktualizacje.

### Struktura i logika wtyczek

Modułowość systemu pozwala na solidną rozbudowę poprzez katalog plugins/.

Silnik przetwarzający ściśle przestrzega **hierarchicznego łańcucha priorytetów**:

1. **Kolejność ładowania modułów (wysoki priorytet):** Reguły załadowane z podstawowych pakietów językowych (de-DE, en-US) mają pierwszeństwo przed regułami załadowanymi z katalogu plugins/ (które ładują się jako ostatnie w kolejności alfabetycznej).
XSPACEbreakX
2. **Kolejność w pliku (mikropriorytet):** W dowolnym pliku mapy (FUZZY_MAP_pre.py) reguły są przetwarzane ściśle według **numeru wiersza** (od góry do dołu).
XSPACEbreakX

Architektura ta zapewnia ochronę podstawowych reguł systemowych, podczas gdy reguły specyficzne dla projektu lub kontekstowe (takie jak te dla CodeIgniter lub kontroli gier) można łatwo dodać jako rozszerzenia o niskim priorytecie za pośrednictwem wtyczek.
## Kluczowe skrypty dla użytkowników systemu Windows

Oto lista najważniejszych skryptów do konfigurowania, aktualizowania i uruchamiania aplikacji w systemie Windows.

### Konfiguracja i aktualizacja

* `chmod +x aktualizacja.sh; ./update.sh`
* `setup/setup.bat`: Główny skrypt do **wstępnej jednorazowej konfiguracji** środowiska.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Uruchom PowerShell -Polecenie "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat`: Uruchom je z folderu projektu **pobierz najnowszy kod i zależności**.

### Uruchamianie aplikacji
* `start_aura.bat`: Podstawowy skrypt do **uruchamiania usługi dyktowania**.

### Skrypty podstawowe i pomocnicze
* `aura_engine.py`: podstawowa usługa Pythona (zwykle uruchamiana przez jeden z powyższych skryptów).
* `get_suggestions.py`: Skrypt pomocniczy dla określonych funkcjonalności.




## 🚀 Kluczowe funkcje i zgodność z systemem operacyjnym

Legenda dotycząca zgodności systemu operacyjnego:XSPACEbreakX
* 🐧 **Linux** (np. Arch, Ubuntu)XSPACEbreakX
* 🍏 **macOS**XSPACEbreakX
* 🪟 **Windows**XSPACEbreakX
* 📱 **Android** (dla funkcji przeznaczonych dla urządzeń mobilnych)XSPACEbreakX

---

### **Podstawowy silnik zamiany mowy na tekst (Aura)**
Nasz główny silnik do rozpoznawania mowy w trybie offline i przetwarzania dźwięku.

XSPACEbreakX
**Aura-Rdzeń/** 🐧 🍏 🪟XSPACEbreakX
├─ `aura_engine.py` (Główna usługa Pythona zarządzająca Aurą) 🐧 🍏 🪟XSPACEbreakX
├┬ **Przeładuj na żywo** (konfiguracja i mapy) 🐧 🍏 🪟XSPACEbreakX
│├ **Bezpieczne ładowanie prywatnej mapy (na pierwszym miejscu jest integralność)** 🔒 🐧 🍏 🪟XSPACEbreakX
││ * **Przebieg pracy:** Ładuje archiwa ZIP chronione hasłem. XSPACEbreakX
│├ **Przetwarzanie i korekta tekstu/** Pogrupowane według języka (np. `de-DE`, `en-US`, ... ) XSPACEbreakX
│├ 1. `normalize_punstanding.py` (Standaryzuje interpunkcję po transkrypcji) 🐧 🍏 🪟XSPACEbreakX
│├ 2. **Inteligentna korekta wstępna** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-pllang.md)) 🐧 🍏 🪟XSPACEbreakX
││ * **Dynamiczne wykonywanie skryptów:** reguły mogą uruchamiać niestandardowe skrypty Pythona (on_match_exec) w celu wykonywania zaawansowanych działań, takich jak wywołania API, operacje we/wy plików lub generowanie odpowiedzi dynamicznych.XSPACEbreakX
││ * **Wykonanie kaskadowe:** Reguły są przetwarzane sekwencyjnie, a ich efekty są **kumulatywne**. Późniejsze reguły mają zastosowanie do tekstu zmodyfikowanego przez wcześniejsze reguły.XSPACEbreakX
││ * **Kryterium zatrzymania o najwyższym priorytecie:** Jeśli reguła osiągnie **Pełne dopasowanie** (^...$), cały potok przetwarzania dla tego tokena zostanie natychmiast zatrzymany. Mechanizm ten ma kluczowe znaczenie dla realizacji niezawodnych poleceń głosowych.XSPACEbreakX
│├ 3. `correct_text_by_languagetool.py` (integruje narzędzie LanguageTool do poprawiania gramatyki/stylu) 🐧 🍏 🪟XSPACEbreakX
│├ **4. Hierarchiczny silnik reguł RegEx z rezerwą Ollama AI** 🐧 🍏 🪟XSPACEbreakX
││ * **Kontrola deterministyczna:** Wykorzystuje silnik RegEx-Rule-Engine do precyzyjnego sterowania poleceniami i tekstem o wysokim priorytecie.XSPACEbreakX
││ * **Awaryjny algorytm Ollama AI (lokalny LLM):** służy jako opcjonalna kontrola o niskim priorytecie w przypadku **kreatywnych odpowiedzi, pytań i odpowiedzi oraz zaawansowanego dopasowywania rozmytego**, gdy nie jest spełniona żadna reguła deterministyczna.XSPACEbreakX
││ * **Status:** Lokalna integracja LLM.
│└ 5. **Inteligentna korekcja końcowa** (`FuzzyMap`)** – Udoskonalanie po LT** 🐧 🍏 🪟
││ * Stosowane po LanguageTool w celu skorygowania wyników specyficznych dla LT. Działa zgodnie z tą samą ścisłą logiką priorytetów kaskadowych, co warstwa wstępnej korekty.XSPACEbreakX
││ * **Dynamiczne wykonywanie skryptów:** reguły mogą uruchamiać niestandardowe skrypty w języku Python ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-pllang.md)) w celu wykonywania zaawansowanych działań, takich jak wywołania API, operacje we/wy plików lub generowanie odpowiedzi dynamicznych.XSPACEbreakX
││ * **Fuzzy Fallback:** **Rozmyta kontrola podobieństwa** (kontrolowana przez próg, np. 85%) działa jako warstwa korekcji błędów o najniższym priorytecie. Jest wykonywana tylko wtedy, gdy w całym poprzedzającym uruchomieniu reguły deterministycznej/kaskadowej nie znaleziono dopasowania (bieżąca_rule_matched ma wartość False), optymalizując wydajność poprzez unikanie, jeśli to możliwe, powolnych kontroli rozmytych.XSPACEbreakX
├┬ **Zarządzanie modelami/** XSPACEbreakX
│├─ `prioritize_model.py` (optymalizuje ładowanie/rozładowywanie modelu w oparciu o wykorzystanie) 🐧 🍏 🪟XSPACEbreakX
│└─ `setup_initial_model.py` (Konfiguruje pierwszą konfigurację modelu) 🐧 🍏 🪟XSPACEbreakX
├─ **Adaptacyjny limit czasu VAD** 🐧 🍏 🪟XSPACEbreakX
├─ **Adaptacyjny klawisz skrótu (Start/Stop)** 🐧 🍏 🪟XSPACEbreakX
└─ **Natychmiastowe przełączanie języka** (eksperymentalnie poprzez wstępne ładowanie modelu) 🐧 🍏 XSPACEbreakX

**Narzędzia systemowe/** XSPACEbreakX
├┬ **Zarządzanie serwerem LanguageTool/** XSPACEbreakX
│├─ `start_languagetool_server.py` (Inicjuje lokalny serwer LanguageTool) 🐧 🍏 🪟XSPACEbreakX
│└─ `stop_languagetool_server.py` (zamyka serwer LanguageTool) 🐧 🍏
├─ `monitor_mic.sh` (np. do użytku z zestawem słuchawkowym bez użycia klawiatury i monitora) 🐧 🍏 🪟XSPACEbreakX

### **Zarządzanie modelami i pakietami**XSPACEbreakX
Narzędzia do niezawodnej obsługi dużych modeli językowych.XSPACEbreakX

**Zarządzanie modelem/** 🐧 🍏 🪟XSPACEbreakX
├─ ** Solidny program do pobierania modeli ** (fragmenty wersji GitHub) 🐧 🍏 🪟XSPACEbreakX
├─ `split_and_hash.py` (Narzędzie dla właścicieli repozytoriów umożliwiające dzielenie dużych plików i generowanie sum kontrolnych) 🐧 🍏 🪟XSPACEbreakX
└─ `download_all_packages.py` (Narzędzie dla użytkowników końcowych do pobierania, weryfikowania i ponownego składania plików wieloczęściowych) 🐧 🍏 🪟XSPACEbreakX


### **Pomocnicy w programowaniu i wdrażaniu**XSPACEbreakX
Skrypty do konfiguracji środowiska, testowania i wykonywania usług.XSPACEbreakX

*Wskazówka: glogg umożliwia używanie wyrażeń regularnych do wyszukiwania interesujących zdarzeń w plikach dziennika.* XSPACEbreakX
Podczas instalacji zaznacz pole wyboru, aby powiązać je z plikami dziennika.  XSPACEbreakX
https://translate.google.com/translate?hl=en&sl=en&tl=pl&u=https://glogg.bonnefon.org/     
XSPACEbreakX
*Wskazówka: Po zdefiniowaniu wzorców wyrażeń regularnych uruchom `python3 Tools/map_tagger.py`, aby automatycznie wygenerować możliwe do przeszukiwania przykłady dla narzędzi CLI. Aby uzyskać szczegółowe informacje, zobacz [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-pllang.md).*

Wtedy może kliknij dwukrotnie
`log/aura_engine.log`
XSPACEbreakX
XSPACEbreakX
**Pomocnicy deweloperów/**XSPACEbreakX
├┬ **Zarządzanie środowiskiem wirtualnym/**XSPACEbreakX
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏XSPACEbreakX
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Ogólnosystemowa integracja dyktowania/**XSPACEbreakX
│├ Integracja Vosk-System-Słuchacz 🐧 🍏 🪟XSPACEbreakX
│├ `scripts/monitor_mic.sh` (monitorowanie mikrofonu specyficzne dla Linuksa) 🐧XSPACEbreakX
│└ `scripts/type_watcher.ahk` (AutoHotkey nasłuchuje rozpoznanego tekstu i wpisuje go w całym systemie) 🪟XSPACEbreakX
└─ **Automatyka CI/CD/**XSPACEbreakX
└─ Rozszerzone przepływy pracy GitHub (instalacja, testowanie, wdrażanie dokumentów) 🐧 🍏 🪟 *(Działa w akcjach GitHub)*XSPACEbreakX

### **Nadchodzące/eksperymentalne funkcje**XSPACEbreakX
Funkcje obecnie w fazie opracowywania lub w wersji roboczej.XSPACEbreakX

**Funkcje eksperymentalne/**XSPACEbreakX
├─ **ENTER_AFTER_DICTATION_REGEX** Przykładowa reguła aktywacji „(ExampleAplicationThatNotExist|Pi, Twoja osobista sztuczna inteligencja)” 🐧XSPACEbreakX
├┬WtyczkiXSPACEbreakX
│╰┬ **Lenno na żywo – przeładuj** (*) 🐧 🍏 🪟XSPACEbreakX
(*Zmiany dotyczące aktywacji/dezaktywacji wtyczki i ich konfiguracji zostaną zastosowane przy następnym uruchomieniu przetwarzania bez ponownego uruchomienia usługi.*)XSPACEbreakX
│ ├ **polecenia git** (sterowanie głosowe przy wysyłaniu poleceń git) 🐧 🍏 🪟XSPACEbreakX
│ ├ **wannweil** (Mapa lokalizacji Niemcy-Wannweil) 🐧 🍏 🪟XSPACEbreakX
│ ├ **Wtyczka pokerowa (wersja robocza)** (Sterowanie głosowe w aplikacjach pokerowych) 🐧 🍏 🪟XSPACEbreakX
│ └ **Wtyczka 0 A.D. (wersja robocza)** (Sterowanie głosowe dla gry 0 A.D.) 🐧 XSPACEbreakX
├─ **Wyjście dźwięku podczas rozpoczynania lub kończenia sesji** (opis w toku) 🐧 XSPACEbreakX
├─ **Mowa dla osób niedowidzących** (opis w oczekiwaniu na opis) 🐧 🍏 🪟XSPACEbreakX
└─ **Prototyp Androida SL5 Aura** (jeszcze nie w pełni offline) 📱XSPACEbreakX

---

*(Uwaga: określone dystrybucje Linuksa, takie jak Arch (ARL) lub Ubuntu (UBT), są oznaczone ogólnym symbolem Linuksa 🐧. Szczegółowe rozróżnienia mogą być omówione w przewodnikach instalacji.)*









<szczegóły>
<summary>Kliknij, aby zobaczyć polecenie użyte do wygenerowania tej listy skryptów</summary>

__KOD_BLOKU_6__
</details>


### Graficzny przegląd architektury:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

XSPACEbreakX
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)


# Używane modele:

Zalecenie: użyj modeli z Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (prawdopodobnie szybciej)

Te spakowane modele muszą być zapisane w folderze `models/`

`mv vosk-model-*.zip models/`


| Modelka | Rozmiar | Poziom błędów/prędkość słów | Notatki | Licencja |
| ------------------------------------------------------------------------------------------------ | ---- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5,69 (czysty test librispeech)<br/>6,05 (tedlium)<br/>29,78 (callcenter) | Dokładny ogólny model w języku angielskim w USA | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9,83 (test Tuda-de)<br/>24,00 (podcast)<br/>12,82 (test CV)<br/>12,42 (mls)<br/>33,26 (mtedx) | Duży niemiecki model telefonii i serwerów | Apache 2.0 |

Ta tabela zawiera przegląd różnych modeli Vosk, w tym ich rozmiar, współczynnik błędów lub prędkość, uwagi i informacje licencyjne.


- **Modele Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **Narzędzie językowe:**XSPACEbreakX
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**Licencja na LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Wesprzyj projekt
Jeśli uznasz to narzędzie za przydatne, rozważ zakup nam kawy! Twoje wsparcie pomaga w napędzaniu przyszłych ulepszeń.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)