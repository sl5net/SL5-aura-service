> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

SL5 Aura - Twój głos. Twoje zasady.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% offline, prywatne-pierwszy głos asystent ramy.  
> Zdefiniuj dokładnie co twój głos robi - z jednego słowa  
> do pełnych skryptów Pythona. Nie ma chmur. Brak danych opuszcza twoją maszynę.  
> Działa w terminalu, przeglądarce lub jako usługa w tle - na Linux, MacOS i Windows.

124; Beginner 124; Beginner 124; Beginner Deweloper 124;
|---|---|---|
[grandma-mode](../docs/GettingStarted.i18n/GettingStarted-pllang.md#the-oma-modus-beginner-shortcut): po prostu napisz słowo, Aura robi resztę Xi124; Ucz się z Koans - jedna koncepcja na raz Xi124; Full Python scripting, plugins, API wzywa Xi124;
Description

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

* * ~ 2.87 J * * * za test (39 testów bez LanguageTool ponad 800 map @ 0.07s ciepła / 0.36s zimna mierzona za pomocą [Eco-CI](https://metrics.green-coding.io/index.html)) · bez obliczeń w chmurze

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

* * Pełny zestaw testowy: * * 94 testy z LanguageTool w całym > 800 map @ 0.07s ciepła / 0.46s zimna · bez obliczeń w chmurze

<details>
<summary>Szybki start</summary>

# Quick Start

### Opcja A: instalacja jednym kliknięciem i siecią (zalecana)

Jednowierszowe polecenie lub samodzielny instalator dla systemów Linux, macOS i Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-pllang.md)**

---

# # # Opcja B: Instalacja ręczna (programiści / Git)

1. Pobierz lub sklonuj to repozytorium
2. Uruchom skrypt konfiguracji dla systemu operacyjnego (patrz folder `setup/`):
   - Linux (Arch / Manjaro): `bash setup/manjaro_arch_setup.sh`
   - Linux (Ubuntu / Debian): `bash setup/ubuntu_setup.sh`
   - Linux (openSUSE): `bash setup/suse_setup.sh`
   - Linux (NixOS): `nix-shell setup/shell.nix` następnie `bash setup/nixos_setup.sh`
   = = = > Experimental - niesprawdzone przez autorów, opinie mile widziane!   
   - MAKOS: `bash setup/macos_setup.sh`
   - Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Start Aura: `./scripts/restart_venv_and_run-server.sh`
4. Naciśnij swój hotkey i mówić - * * [full guide →](../docs/GettingStarted.i18n/GettingStarted-pllang.md) * *

---

# # Deinstalacja
Aby usunąć usługi tła SL5 Aura, wpisy autostart i środowiska wirtualne:
- * * Linux / macOS: * * `bash setup/uninstall.sh`
- * * Windows (PowerShell): * * `powershell -File setup/uninstall.ps1`
* (Twoje własne zasady w `config/maps/` są domyślnie bezpieczne, chyba że podasz `--purge`). *

---


Wymagania systemowe i zgodność * *

*   * * Windows: * * Description Full obsługiwane (używa AutoHotkey / PowerShell).
*   * * MacOS: * * Environment Full support (wykorzystuje AppleScript).
*   * * Linux (X11 / Xorg): * * W pełni wspierane.
*   * * Linuksa (Wayland): * * Całkowicie obsługiwane (testowane na Plazmie 6 / Wayland KDE).
*   * * Linux (CachyOS / Arch- based rolling release): * * W pełni wspierane.
    Wymaga mimalloc (`sudo pacman -S mimalloc`) ze względu na kompatybilność glibc 2.43.
*   * * Linux (NixOS): * * Independent Experimental - community- contributed setup, jeszcze nie przetestowany.
    Jeśli spróbujesz, proszę otworzyć problem lub PR ze swoimi ustaleniami!    
*   * * Linux (Manjaro): * * Nowy: Szeroki systemowy hotkey otwiera interfejs fzf- like, keyboard- driven, dzięki czemu można uruchomić polecenia Aura z dowolnego miejsca na pulpicie (całkowicie oddzielone od aktywnego okna). Wyrzutnia ta jest obecnie wdrażana i testowana na Linuksie (Manjaro); Inne dystrybucje mogą działać, ale wymagają ustawienia. Patrz: [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-pllang.md)    


    
SL5 Aura jest kompletną, * * asystentką głosową offline * * zbudowaną na * * Vosk * * (dla Speech- to- Text) i * * LanguageTool * * (dla Grammar / Style), z opcjonalnym * * Local LLM (Ollama) Fallback * * dla kreatywnych odpowiedzi i zaawansowanych fuzzy dopasowania. Przekształca twój głos w dokładne działania i tekst, zaprojektowany do ostatecznego dostosowania poprzez system podłączanych zasad i dynamiczny silnik skryptowy.
    
Tłumaczenie: Dokument ten istnieje również w [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Uwaga: Wiele tekstów jest generowanych maszynowo tłumaczeń oryginalnej angielskiej dokumentacji i jest przeznaczonych wyłącznie do ogólnych wskazówek. W przypadku rozbieżności lub niejasności zawsze dominuje wersja angielska. Zapraszamy do pomocy ze strony społeczności, aby poprawić to tłumaczenie!

</details>

<details>
<summary>Demo</summary>

{C: $aaccff} Tłumaczenie:

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> * * Tip: * * Aby uzyskać lepsze doświadczenie końcowe, patrz [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-pllang.md).

Tłumaczenie:
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

* (Alternatywny link: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw)) *

</details>

<details>
<summary>Główne cechy</summary>

# # Cechy kluczowe

*   * * Offline & Private: * * 100% lokalnych. Żadne dane nie opuszczają twojej maszyny.
*   * * Dynamiczny silnik skryptowy: * * Wyjść poza wymianę tekstu. Zasady mogą wykonywać własne skrypty Pythona (`on_match_exec`) do wykonywania zaawansowanych działań, takich jak wywołanie API (np. wyszukiwanie Wikipedii), interakcja z plikami (np., zarządzanie listą zadań) lub generowanie dynamicznych treści (np. wiadomości e-mail z context- aware).
*   * * Context- Aware Rules: * * Restrict rules to specific applications. Za pomocą `only_in_windows` można zapewnić, że reguła uruchamia się tylko wtedy, gdy aktywny jest określony tytuł okna (np. "Terminal", "VS Code" lub "Przeglądarka"). To działa cross- platform (Linux, Windows, MacOS).
*  * * Silnik transformacyjny High- Control: * * Wprowadza konfigurowalny, wysoce konfigurowalny rurociąg procesowy. Priorytet zasady, wykrywanie poleceń i transformacje tekstowe są określane wyłącznie kolejnością reguł w Mapach Fuzzy, wymagających konfiguracji * *, a nie kodowania * *.
*   * * Conservetive RAM Usage: * * Inteligentnie zarządza pamięcią, wstępnie ładuje modele tylko wtedy, gdy dostępna jest wystarczająca ilość wolnego RAM, zapewniając, że inne aplikacje (jak gry PC) zawsze mają pierwszeństwo.
*   * * Cross platform: * * Działa na Linuksie, MacOS i Windows.
*   * * W pełni zautomatyzowany: * * Zarządza własnym serwerem LanguageTool (ale można również używać zewnętrznego serwera).
*   * * Blazing Fast: * * Inteligentne buforowanie zapewnia natychmiastowe "Słuchanie"... powiadomienia i szybkie przetwarzanie.
*   * * Dynamic State Management via Trino: * * Silnik konfiguracyjny posiadający wiedzę na temat interfejsu
    oddziela ustawienia dla `speech`, `terminal` i `web` - zmienić jeden bez
    Narażam innych. Zawiera real- time * * Admin Dashboard * * (port 8084).
</details>

<details>
<summary>Integracje ready- to- use</summary>
    
## 🔌 Gotowe do użycia integracje

SL5-Aura jest wyposażony w rozbudowany ekosystem ponad **100 wstępnie skonfigurowanych wtyczek**. Oto kilka najważniejszych elementów:

OkuliX / SikuliX IDE Voice Control
SL5- Aura zapewnia obsługę głosu pierwszej klasy dla * * OculiX * * i * * SikuliX IDE * *. Ta integracja pozwala na "mówienie" kodu automatyki.

*   * * Voice- to- Snippet: * * Powiedz "click", "wait" lub "find all", a usługa natychmiast wpisuje poprawny kod Pythona (np. `click("image.png")`) do IDE.
*   * * Window- Aware: * * Wtyczka jest delikatna; aktywuje się tylko wtedy, gdy okno OculiX / SikuliX jest skoncentrowane.
*   * * Smart English Support: * * Optimized for `en-US` ze szczególnym uwzględnieniem nierodzimych akcentów (np. fonetyki niemiecko-angielskiej), zapewniając wysoką dokładność rozpoznawania społeczności światowej.
*   * * Extensible: * * Używa łatwego do edycji formatu `FUZZY_MAP_pre.py`.

> / Stan: Rozpoznany jako wtyczka społeczności przez zespół OculiX (patrz [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Kontrola głosowa LibreOffice IDE

### 0 A.D. Sterowanie głosem

---

</details>


<details>
<summary>Dokumentacja</summary>

## Dokumentacja

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=pl)

Aby uzyskać kompletny podręcznik techniczny, obejmujący wszystkie moduły i skrypty, odwiedź naszą oficjalną stronę dokumentacji. Jest ona generowana automatycznie i zawsze aktualna.

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

# # Feature Spotlights
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-pllang.md) - Dual- pan `fzf` rule search, live context previews, instant command execution via `Enter` / `Ctrl+R`, and editor integration via `Ctrl+E`. Obsługiwane przez globalny hotkey (`Super+S`) i wiele dedykowanych środowisk wyszukiwania skonfigurowanych za pomocą komend głosowych.

* * Build status *

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

Przeczytaj to w innych językach:

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-pllang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-pllang.md) | [🇪🇸 Español](../README.i18n/README-eslang-pllang.md) | [🇫🇷 Français](../README.i18n/README-frlang-pllang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-pllang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-pllang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-pllang.md) | [🇵🇱 Polski](../README.i18n/README-pllang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-pllang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-pllang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-pllang.md)

---

<details>
<summary>Instalacja</summary>

# # Instalacja

# # # Szybka instalacja bez umiarkowania (Manjaro / Arch Video)
Obejrzyj cały proces konfiguracji 6- minutowego:
* * * Pobieranie: ~ 3 minuty
* * * Setup & First Start: * * ~ 3 minuty (w tym Wizard powitalny)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


Konfiguracja jest procesem dwuetapowym:
1.  Pobierz najnowszą wersję Release or master (https: / / github.com / sl5net / SL5-aura- service / archive / master.zip) lub sklonuj to repozytorium do komputera.
2.  Uruchom skrypt konfiguracji dla systemu operacyjnego.

Skrypty konfiguracji zajmują się wszystkim: zależnościami systemowymi, środowiskiem Pythona i pobieraniem niezbędnych modeli i narzędzi (~ 4GB) bezpośrednio z naszych GitHub Releases dla maksymalnej prędkości.


Dla Linuksa, MacOS i Windows (z opcjonalnym wyłączeniem językowym)

Aby zaoszczędzić przestrzeń dyskową i szerokość pasma, podczas konfiguracji można wyłączyć specyficzne modele językowe (`de`, `en`) lub wszystkie opcjonalne modele (`all`). * * Składniki rdzeniowe (LanguageTool, lid.176) są zawsze włączone. /

Otwórz terminal w katalogu głównym projektu i uruchom skrypt dla Twojego systemu:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

Dla Windows
Uruchom skrypt konfiguracji z uprawnieniami administratora.

* * Zainstaluj narzędzie do odczytu i uruchomienia, np. [CopyQ](https://github.com/hluk/CopyQ) lub [AutoHotkey v2](https://www.autohotkey.com/) * *. Jest to wymagane dla obserwatora tekstowego.

Instalacja jest w pełni zautomatyzowana i zajmuje około * * 8- 10 minut * * przy użyciu 2 modeli na świeżym systemie.

1. Przejdź do folderu `setup`.
2. Kliknij dwukrotnie na * * `windows11_setup_with_ahk_copyq.bat` * *.
   * * Skrypt będzie automatycznie wywoływał uprawnienia administratora. *
   * * Instaluje system bazowy, modele językowe, * * AutoHotkey v2 * *, i * * CopyQ * *. *
3. Po zakończeniu instalacji, dyktowanie * * Aura zostanie automatycznie uruchomione.

> * * Note: * * Nie trzeba wcześniej instalować Pythona lub Gita; Scenariusz zajmuje się wszystkim.

---

# # # Advanced / Custom Instalacja
Jeśli wolisz nie instalować narzędzi klienta (AHK / CopyQ) lub chcesz zapisać przestrzeń dyskową przez wyłączenie konkretnych języków, możesz uruchomić skrypt rdzeniowy za pomocą linii poleceń:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>Zastosowanie</summary>

# # Usage

Rozpocząć usługi

Na Linuksie i MacOS
Jeden scenariusz zajmuje się wszystkim. Rozpoczyna usługę głównego dyktowania i obserwatora plików automatycznie w tle.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

Na Windows
Uruchomienie usługi to dwuetapowy proces ręczny * * *:

1.  * * Uruchom usługę główną: * * Uruchom `start_aura.bat`. lub uruchom od `.venv` usługę z `python3`

Konfiguracja klucza

Aby wywołać dyktowanie, potrzebujesz globalnego klucza, który tworzy określony plik. Serdecznie polecamy narzędzie cross- platform [CopyQ](https://github.com/hluk/CopyQ).

#### Nasza rekomendacja: CopyQ

Utwórz nowe polecenie w CopyQ za pomocą globalnego skrótu.

**Polecenie dla systemu Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Polecenie dla Windows przy użyciu [CopyQ](https://github.com/hluk/CopyQ):**
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**Polecenie dla Windows przy użyciu [AutoHotkey](https://AutoHotkey.com):**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 script
#SingleInstance Force ; Ensures only one instance of the script runs

;===================================================================
; Hotkey to trigger Aura
; Press Ctrl + Alt + T to write the trigger file.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger activated!")
    SetTimer(() => ToolTip(), -1500)
}
```


# # # 3rd Start Dictating!
Kliknij w dowolnym polu tekstowym, naciśnij swój hotkey, a pojawi się "Słuchanie"... Mów wyraźnie, a potem pauza. Poprawiony tekst zostanie napisany dla Ciebie.

</details>

---


<details>
<summary>Zaawansowana konfiguracja (opcjonalnie)</summary>

# # Zaawansowana konfiguracja (opcjonalnie)

Możesz dostosować zachowanie aplikacji poprzez utworzenie pliku ustawień lokalnych.

1.  Przejdź do katalogu `config/`.
2.  Utwórz kopię `config/settings_local.py_Example.txt` i zmień nazwę na `config/settings_local.py`.
3.  Edycja `config/settings_local.py` (nadpisuje wszelkie ustawienia z głównego pliku `config/settings.py`).

Ten plik `config/settings_local.py` jest domyślnie ignorowany przez Gita, więc Twoje osobiste zmiany nie zostaną nadpisane przez aktualizacje.

Wtyczka w strukturze i logice

Modularność systemu pozwala na solidne rozszerzenie poprzez wtyczki / katalog.

Silnik przetwórczy ściśle przylega do hierarchicznego łańcucha priorytetowego * * *:

1. * * Moduł Zamówienie ładowania (wysoki priorytet): * * Zasady wczytane z podstawowych pakietów językowych (de- DE, en- US) mają pierwszeństwo przed zasadami wczytanymi z wtyczki / katalogu (które ładują ostatnio alfabetycznie).
    
2. * * In- File Order (Micro Priority): * * W obrębie dowolnego pliku mapy (FUZZY MAP pre.py), zasady są przetwarzane ściśle przez * * numer linii * * (top- to- bottom).
    

Architektura ta zapewnia ochronę podstawowych zasad systemowych, podczas gdy zasady specyficzne dla danego projektu lub jego wiedzy (takie jak te dla CodeIgniter lub kontroli gry) mogą być łatwo dodawane jako rozszerzenia o niskim priorytecie za pomocą wtyczek.

</details>

<details>
<summary>Kluczowe skrypty dla użytkowników systemu Windows</summary>






## Kluczowe skrypty dla użytkowników systemu Windows

Oto lista najważniejszych skryptów do skonfigurowania, aktualizacji i uruchomienia aplikacji na systemie Windows.

### Instalacja i aktualizacja

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: Główny skrypt do **początkowej jednorazowej konfiguracji** środowiska.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Uruchom to z folderu projektu, aby **pobrać najnowszy kod i zależności**.

### Uruchamianie aplikacji
*   `start_aura.bat`: Główny skrypt do **uruchamiania usługi dyktowania**.

### Podstawowe i pomocnicze skrypty
*   `aura_engine.py`: Główna usługa Pythona (zwykle uruchamiana jednym ze skryptów powyżej).
*   `get_suggestions.py`: Skrypt pomocniczy do określonych funkcji.

</details>



## 🚀 Kluczowe funkcje i zgodność z systemami operacyjnymi

<details>
<summary>Legenda kompatybilności systemu operacyjnego</summary>

Legenda dla zgodności z systemem operacyjnym:  
*   🐧 **Linux** (np. Arch, Ubuntu)  
    *   🍏 **macOS**  
*   🪟 **Okna**  
*   📱 **Android** (dla funkcji specyficznych dla urządzeń mobilnych)  

---

</details>



# # # * * Core Speech-to-Text (Aura) Engine * *
    Nasz główny silnik do rozpoznawania mowy offline i przetwarzania dźwięku.

    
<details>
<summary>Rdzeń aury</summary>

* * Aura-Core / * * 🐧 🍏 🪟  
├─ `aura_engine.py` (Główny serwis Pythona organizujący aurę) 🐧 🍏 🪟  
├┬ * * Live Hot- Reload * * (Konfiguracja i mapy) 🐧 🍏 🪟  
│├ * * Secure Private Map Loading (Integraty- First) * * 🔒  🐧 🍏 🪟  
││ * * * Workflow * * Wczytuje archiwa ZIP chronione hasłem.   
│├ * * Text Processing & Correction / * * Grupowana według języka (np. `de-DE`, `en-US`,...)   
│├ 1. `normalize_punctuation.py` (Standaryzuje interpunkcję po transkrypcji) 🐧 🍏 🪟  
│├ 2. * * Inteligentna korekta wstępna * * (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-pllang.md)) 🐧 🍏 🪟  
││ * * * Dynamic Script Execution: Rules może uruchomić własne skrypty Python (`on_match_exec`) do wykonywania zaawansowanych działań, takich jak wywołania API, plik I / O lub generowanie odpowiedzi dynamicznych.  
││ * * * Cascading Execution: * * Zasady są przetwarzane kolejno, a ich skutki są * * skumulowane * *. Późniejsze zasady mają zastosowanie do tekstu zmienionego przez wcześniejsze zasady.  
││ * * * Najwyższe kryterium Priority Stop: * * Jeśli reguła osiąga * * Full Match * * (^... $), cały rurociąg przetwarzania dla tego tokena zatrzymuje się natychmiast. Mechanizm ten ma kluczowe znaczenie dla wdrażania niezawodnych poleceń głosowych.  
│├ 3. `correct_text_by_languagetool.py` (Integrates LanguageTool for gramatyka / korekta stylu) 🐧 🍏 🪟  
│├ * * 4. Hierarchiczny RegEx Rule Engine z Ollama AI Fallback * * 🐧 🍏 🪟  
││ * * * Deterministic Control: * * Uses RegEx Rule Engine for precysic, high-priority command and text control.  
│├ * Vector- Search Plugin * * (Lazy loading): Włącza semantyczne wyszukiwanie łącząc lokalne osadzenia wektorowe z warstwą Ollama / LLM 🐧  
││ * * * Ollama AI (Local LLM) Fallback: * * Służy jako opcjonalny, niskopriorytetowy sprawdzian dla * * kreatywnych odpowiedzi, Q & A, i zaawansowany Fuzzy Matching * *, gdy nie spełnia się żadnej reguły deterministycznej.  
││ * * * Status: * * Lokalna integracja LLM.
│└ 5. * * Intelligent Post- Correction * * (`FuzzyMap`) * * - Post- LT Refinement * * 🐧 🍏 🪟  
││ * Stosowany po LanguageTool w celu skorygowania specyficznych wyjść LT. Śledzi taką samą ścisłą logikę kaskadowania jak warstwa przed korekcją.  
││ * * Dynamic Script Execution: Rules może uruchomić własne skrypty Python ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-pllang.md)) do wykonywania zaawansowanych działań, takich jak wywołania API, plik I / O, lub generowanie odpowiedzi dynamicznych.  
││ * * * Fuzzy Fallback * * * * FUZY SUPLIarity Check * * (kontrolowany przez próg, np. 85%) działa jako najniższa warstwa błędu priorytetowego. Jest on wykonywany tylko wtedy, gdy cała poprzednia reguła determinaristic / cascading nie uda się znaleźć dopasowania (obecna reguła dopasowana jest fałszywa), optymalizując wydajność poprzez unikanie powolnych, rozmytych kontroli w miarę możliwości.  
├┬ * * Model Management / * *   
│├─ `prioritize_model.py` (optymalizuje model załadunku / rozładunku w zależności od zastosowania) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Konfiguracja modelu po raz pierwszy) 🐧 🍏 🪟  
├─ * * Adaptacyjny VAD Czas. 🐧 🍏 🪟  
├─ * * Adaptive Hotkey (Start / Stop) 🐧 🍏 🪟  
├─ * * Instant Language Switching * * (Experimental via model preloading) 🐧 🍏         
├─ * * Orchestracja przepływu powietrza * * (automatyzacja przepływu pracy oparta na DAG) 🐧 🍏 🪟
│   Wymaga Docker · Interfejs: `http://localhost:8081` 🐧 🍏 🪟  
├─ * * Trino State Engine * 🐧 🍏 🪟
└─  Wymaga Docker · Admin UI: `http://localhost:8084` 🐧 🍏 🪟  

* * SystemNarzędzia / * *   
├┬ * * LanguageTool Server Management / * *   
│├─ `start_languagetool_server.py` (Inicjuje lokalny serwer LanguageTool) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Wyłącza serwer LanguageTool) 🐧 🍏 
├─ `monitor_mic.sh` (np. do stosowania z zestawem słuchawkowym bez użycia klawiatury i monitora) 🐧 🍏 🪟  

### **Zarządzanie modelem i pakietem**  
    Narzędzia do solidnego obsługiwania dużych modeli językowych.  

**ZarządzanieModelem/** 🐧 🍏 🪟  
├─ **Robust Model Downloader** (chunki wydań GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (narzędzie dla właścicieli repozytoriów do dzielenia dużych plików i generowania sum kontrolnych) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Narzędzie dla użytkowników końcowych do pobierania, weryfikowania i składania plików wieloczęściowych) 🐧 🍏 🪟  

</details>


<details>
<summary>Pomocnicy w zakresie rozwoju i wdrażania</summary>

# # # # * Rozwój i rozwój Pomocników # *  
    Skrypty dotyczące konfiguracji środowiska, testowania i wykonywania usług.  

* Wskazówka: glogg umożliwia korzystanie z wyrażeń regularnych w poszukiwaniu ciekawych zdarzeń w plikach dziennika. *     
Proszę zaznaczyć pole wyboru podczas instalacji, aby powiązać je z plikami dziennika.    
https: / / glogg.bonnefon.org /     
    
Wskazówka: Po zdefiniowaniu wzorców regex, uruchom `python3 tools/map_tagger.py`, aby automatycznie wygenerować przykłady do przeszukiwania dla narzędzi CLI. Szczegóły znajdują się w [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-pllang.md). *

To może podwójne kliknięcie
`log/aura_engine.log`
    
* * DevHelpers * *  
├┬ * * Wirtualne zarządzanie środowiskiem * *  
│├ `scripts/restart_venv_and_run-server.sh` (Linux / macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ * * System- wide Dictation Integration / * *  
│├ Integracja słuchaczy systemu Vosk 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (monitorowanie mikrofonu specyficznego dla Linuksa) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey słucha rozpoznanego tekstu i wypisuje go system- wide) 🪟  
└─ * * CI / CD Automation / * *  
    └─ Rozszerzone przepływy pracy GitHub (instalacja, testowanie, wdrażanie dokumentów)  

</details>

<details>
<summary>Cechy doświadczalne</summary>
    
* * * Upcoming / Experimental Features * *  
    Funkcje obecnie opracowywane lub w projekcie statusu.  

* * Experimentalne funkcje / * *  
├─ * * ENTER AFTER DICTATION REGEX * * Przykład zasady aktywacji "(ExampleAplicationThatNotExist Amend124; Pi, Twoja osobista AI)" 🐧  
├┬Wtyczki  
│Relaks * * Live Lazy- Reload * * * (*) 🐧 🍏 🪟  
(* Zmiany aktywacji / dezaktywacji wtyczki oraz ich konfiguracje są stosowane w następnym procesie przetwarzania bez ponownego uruchomienia usługi. *)  
│ ├ * * komendy git * (Kontrola głosu dla poleceń git) 🐧 🍏 🪟  
│ ├ * * wannweil * * (Mapa lokalizacji Niemiec - Wannweil) 🐧 🍏 🪟  
│ ├ * * Wtyczka Poker (Draft) * * (Kontrola głosowa dla aplikacji pokerowych) 🐧 🍏 🪟  
│ └ * * 0 A.D. Plugin (Draft) * * (Voice Control for 0 A.D. game) 🐧   
├─ * * Wyjście dźwiękowe przy starcie lub zakończeniu sesji * * (Opis oczekujący) 🐧   
├─ * * Wyjście przemowy dla Visual Impailed * * (Opis oczekujący) 🐧 🍏 🪟  
└─ * SL5 Aura Android Prototyp * * (Jeszcze nie w pełni offline) 📱  

---

* (Uwaga: Specyficzne dystrybucje Linuksa takie jak Arch (ARL) lub Ubuntu (UBT) są objęte ogólnym symbolem symbolu Linux). Szczegółowe rozróżnienia mogą być ujęte w przewodnikach instalacyjnych. *
</details>

<details>
<summary>Kliknij, aby zobaczyć polecenie używane do wygenerowania tej listy skryptów</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>Graficzny przegląd architektury</summary>

### Graficzny przegląd architektury:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Używane modele</summary>

## Używane modele:

Rekomendacja: używaj modeli z Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (prawdopodobnie szybsze)

Te spakowane modele muszą być zapisane w folderze `models/`

`mv vosk-model-*.zip models/`


Reg.
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
124; [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) X124; 1.8G X124; 5.69 (librispeech test- clean) <br/>6.05 (tedlium) <br/>29.78 (callcenter) X124; Accurate generyczny amerykański model angielski X124; Apache 2.0 X124;
124; [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) XXX124; 1.9G XXX124; 9.83 (Tuda- de test) <br/>24.00 (podcast) <br/>12.82 (cv- test) <br/>12.42 (mls) <br/>33.26 (mtedx) <br/>24.00 (podcast) <br/>12.82 (cv- test) XHTMLTAG412.42 (mls) <br/>33.26 (mtedx) X124; Duży niemiecki model telefonii i serwera 124; Apache 2.0 XI124;

Ta tabela przedstawia przegląd różnych modeli Vosk, w tym ich rozmiar, współczynnik błędów słów lub prędkość, uwagi oraz informacje o licencji.


- **Modele Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**Licencja LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## Wspieraj projekt
Jeśli uważasz to narzędzie za przydatne, rozważ proszę kupienie nam kawy! Twoje wsparcie pomaga w finansowaniu przyszłych ulepszeń.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

