> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Twój Głos. Twoje Zasady.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% offline, priorytetowo traktujący prywatność framework asystenta głosowego.  
> Zdefiniuj dokładnie, co robi Twój głos — od pojedynczego słowa
> do pełnych skryptów Pythona. Żadnej chmury. Żadne dane nie opuszczają twojego komputera.
> Działa w terminalu, przeglądarce lub jako usługa w tle — na Linuxie, macOS i Windows.
| 👵 Początkujący | 🎓 Uczeń | 🧑‍💻 Programista |
|---|---|---|
| [grandma-mode](../docs/GettingStarted-pllang.md#the-oma-modus-beginner-shortcut) : po prostu wpisz słowo, resztę zrobi Aura | Ucz się z Koans — po jednej koncepcji naraz | Pełne skrypty w Pythonie, wtyczki, wywołania API |
| 🗄️ Zarządzanie Stanem | Orkiestracja Trino + Airflow, fzf, CopyQ, polecenia głosowe/terminalowe, interfejsy przeglądarki |
[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** na test (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · bez obliczeń w chmurze

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Pełny zestaw testów:** 94 testy z LanguageTool na ponad 800 mapach @ 0,07 s ciepło / 0,46 s zimno · bez przetwarzania w chmurze

<details>
<summary>Szybki start</summary>
## Szybki start
### Opcja A: Instalator 1-Click & Web (Recommended)

Jednolinijkowe polecenie lub samodzielny instalator dla systemów Linux, macOS i Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller-pllang.md)**

---
# # # Opcja B: Instalacja ręczna (programiści / Git)

1. Pobierz lub sklonuj to repozytorium
2. Uruchom skrypt konfiguracji dla systemu operacyjnego (patrz folder `setup/`):
- Linux (Arch / Manjaro): `bash setup/manjaro_arch_setup.sh`
- Linux (Ubuntu / Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` następnie `bash setup/nixos_setup.sh`
= = = > Experimental - niesprawdzone przez autorów, opinie mile widziane!   
- MacOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Start aura: `./scripts/restart_venv_and_run-server.sh`
4. Naciśnij swój hotkey i mówić - * * [full guide →](../docs/GettingStarted-pllang.md)

---
# # Deinstalacja
Aby usunąć usługi tła SL5 Aura, wpisy autostart i środowiska wirtualne:
- * * Linux / macOS: * * `bash setup/uninstall.sh`
- * * Windows (PowerShell): * * `powershell -File setup/uninstall.ps1`
* (Twoje własne zasady w `config/maps/` są domyślnie bezpieczne, chyba że podasz `--purge`). *

---


* * Requirements Wymagania Systemowe i kompatybilność * *

* * * Windows: * * Supported Full (używa AutoHotkey / PowerShell).
* * * MacOS: * * Environment Full support (wykorzystuje AppleScript).
* * * Linux (X11 / Xorg): * * W pełni wspierane.
* * * Linuksa (Wayland): * * Całkowicie obsługiwane (testowane na Plazmie 6 / Wayland KDE).
* * * Linux (CachyOS / Arch- based rolling release): * * W pełni wspierane.
Wymaga mimalloc (`sudo pacman -S mimalloc`) ze względu na kompatybilność glibc 2.43.
* * * Linux (NixOS): * * Independent Experimental - community- contributed setup, jeszcze nie przetestowany.
Jeśli spróbujesz, proszę otworzyć problem lub PR ze swoimi ustaleniami!   
* * * Linux (Manjaro): * * Nowy: Szeroki systemowy hotkey otwiera interfejs fzf- like, keyboard- driven, dzięki czemu można uruchomić polecenia Aura z dowolnego miejsca na pulpicie (całkowicie oddzielone od aktywnego okna). Wyrzutnia ta jest obecnie wdrażana i testowana na Linuksie (Manjaro); inne dystrybucje mogą działać, ale wymagają ustawienia. Patrz: [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s-pllang.md)   


    
SL5 Aura jest kompletną, * * asystentką głosową offline * * zbudowaną na * * Vosk * * (dla Speech- to- Text) i * * LanguageTool * * (dla Grammar / Style), z opcjonalnym * * Local LLM (Ollama) Fallback * * dla kreatywnych odpowiedzi i zaawansowanych fuzzy dopasowania. Przekształca twój głos w dokładne działania i tekst, zaprojektowany do ostatecznego dostosowania poprzez system podłączanych zasad i dynamiczny silnik skryptowy.
    
Tłumaczenie: Dokument ten istnieje również w [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Uwaga: Wiele tekstów jest generowanych maszynowo tłumaczeń oryginalnej angielskiej dokumentacji i jest przeznaczonych wyłącznie do ogólnych wskazówek. W przypadku rozbieżności lub niejasności zawsze dominuje wersja angielska. Zapraszamy do pomocy ze strony społeczności, aby poprawić to tłumaczenie!

</details>

<details>
<summary>Demo</summary>
{C: $aaccff} Tłumaczenie:

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> * * Tip: * * Aby uzyskać lepsze doświadczenie końcowe, patrz [Zsh Integration](../docs/linux/zsh-integration-pllang.md).
Tłumaczenie:
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

* (Alternatywny link: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw)) *

</details>

<details>
<summary>Klucz Features</summary>
# # Kluczowe cechy

* * * Offline & Private: * * 100% lokalnych. Żadne dane nie opuszczają twojej maszyny.
* * * Dynamiczny silnik skryptowy: * * Wyjść poza wymianę tekstu. Zasady mogą wykonywać własne skrypty Pythona (`on_match_exec`) do wykonywania zaawansowanych działań, takich jak wywołanie API (np. wyszukiwanie Wikipedii), interakcja z plikami (np., zarządzanie listą zadań) lub generowanie dynamicznych treści (np. wiadomości e-mail z context- aware).
* * * Context- Aware Rules: * * Restrict rules to specific applications. Za pomocą `only_in_windows` można zapewnić, że reguła uruchamia się tylko wtedy, gdy aktywny jest określony tytuł okna (np. "Terminal", "VS Code" lub "Przeglądarka"). To działa cross- platform (Linux, Windows, MacOS).
* * * Silnik transformacyjny High- Control: * * Wprowadza konfigurowalny, wysoce konfigurowalny rurociąg procesowy. Priorytet zasady, wykrywanie poleceń i transformacje tekstowe są określane wyłącznie kolejnością reguł w Mapach Fuzzy, wymagających konfiguracji * *, a nie kodowania * *.
* * * Conservetive RAM Usage: * * Inteligentnie zarządza pamięcią, wstępnie ładuje modele tylko wtedy, gdy dostępna jest wystarczająca ilość wolnego RAM, zapewniając, że inne aplikacje (jak gry PC) zawsze mają pierwszeństwo.
* * * Cross- Platforma: * * Działa na Linuksie, MacOS i Windows.
* * * W pełni zautomatyzowany: * * Zarządza własnym serwerem LanguageTool (ale można również używać zewnętrznego serwera).
* * * Blazing Fast: * * Inteligentne buforowanie zapewnia natychmiastowe "Słuchanie"... powiadomienia i szybkie przetwarzanie.
* * * Dynamic State Management via Trino: * * Silnik konfiguracyjny posiadający wiedzę na temat interfejsu
oddziela ustawienia dla `speech`, `terminal` i `web` - zmienić jeden bez
na innych. Zawiera real- time * * Admin Dashboard * * (port 8084).
</details>

<details>
<summary> Ready- to- Use Integrations</summary>
    {C: $aaccff} Tłumaczenie:

SL5- Aura ma ogromny ekosystem ponad * * 100 + wstępnie skonfigurowane wtyczki * *. Oto kilka atrakcji:
# # OculiX / SikuliX IDE Voice Control
SL5- Aura zapewnia obsługę głosu pierwszej klasy dla * * OculiX * * i * * SikuliX IDE * *. Ta integracja pozwala na "mówienie" kodu automatyki.

* * * Voice- to- Snippet: * * Powiedz "click", "wait" lub "find all", a usługa natychmiast wpisuje poprawny kod Pythona (np. `click("image.png")`) do IDE.
* * * Window- Aware: * * Wtyczka jest delikatna; aktywuje się tylko wtedy, gdy okno OculiX / SikuliX jest skoncentrowane.
* * * Smart English Support: * * Optimized for `en-US` ze szczególnym naciskiem na nierodzime akcenty (np. fonetyka niemiecko-angielska), zapewniając wysoką dokładność rozpoznawania społeczności światowej.
* * * Extensible: * * Używa łatwego do edycji formatu `FUZZY_MAP_pre.py`.

> / Stan: Rozpoznany jako wtyczka społeczności przez zespół OculiX (patrz [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).
LibreOffice IDE Voice Control
# # 0 A.D. Voice Control

---

</details>


<details>
<summary>Documentation</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)
# # Dokumentacja

Aby uzyskać pełne odniesienie techniczne, w tym wszystkie moduły i skrypty, odwiedź naszą oficjalną stronę dokumentacji. Jest ona automatycznie generowana i zawsze aktualizowana.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)
# # Feature Spotlights
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run-pllang.md) - Dual- pan `fzf` rule search, live context previews, instant command execution via `Enter` / `Ctrl+R`, and editor integration via `Ctrl+E`. Obsługiwane przez globalny hotkey (`Super+S`) i wiele dedykowanych środowisk wyszukiwania skonfigurowanych za pomocą komend głosowych.
# # Build Status

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

* * Przeczytaj to w innych językach: * *

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-pllang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-pllang.md) | [🇪🇸 Español](../README.i18n/README-eslang-pllang.md) | [🇫🇷 Français](../README.i18n/README-frlang-pllang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-pllang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-pllang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-pllang.md) | [🇵🇱 Polski](../README.i18n/README-pllang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-pllang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-pllang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-pllang.md)

---

<details>
<summary>Installation</summary>
# # Instalacja
# # # Szybka instalacja bez umiarkowania (Manjaro / Arch Video)
Obejrzyj cały proces konfiguracji 6- minutowego:
* * * Pobierz: * * ~ 3 minuty
* * * Setup & First Start: * * ~ 3 minuty (w tym Wizard powitalny)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


Konfiguracja jest procesem dwuetapowym:
1. Pobierz najnowsze wydanie lub master (https: / / github.com / sl5net / SL5-aura- service / archive / master.zip) lub sklonuj to repozytorium do komputera.
2. Uruchom skrypt konfiguracji dla systemu operacyjnego.

Skrypty konfiguracji zajmują się wszystkim: zależnościami systemowymi, środowiskiem Pythona i pobieraniem niezbędnych modeli i narzędzi (~ 4GB) bezpośrednio z naszych GitHub Releases dla maksymalnej prędkości.

#### Dla systemów Linux, macOS i Windows (z opcjonalnym wykluczeniem języka)

Aby zaoszczędzić miejsce na dysku i przepustowość, możesz wykluczyć konkretne modele językowe (`de`, `en`) lub wszystkie opcjonalne modele (`all`) podczas konfiguracji. **Podstawowe komponenty (LanguageTool, lid.176) są zawsze uwzględniane.**

Otwórz terminal w katalogu głównym projektu i uruchom skrypt dla swojego systemu:

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

1. Przejdź do katalogu `setup`.
2. Kliknij dwukrotnie na * * `windows11_setup_with_ahk_copyq.bat` * *.
* * Skrypt będzie automatycznie wywoływał uprawnienia administratora. *
* * Instaluje system podstawowy, modele językowe, * * AutoHotkey v2 * *, i * * CopyQ * *. *
3. Po zakończeniu instalacji, dyktowanie * * Aura zostanie automatycznie uruchomione.

> * * Note: * * Nie trzeba instalować Pythona lub Gita wcześniej; skrypt obsługuje wszystko.

---
#### Zaawansowana / Niestandardowa instalacja
Jeśli wolisz nie instalować narzędzi klienckich (AHK/CopyQ) lub chcesz zaoszczędzić miejsce na dysku, wykluczając konkretne języki, możesz uruchomić główny skrypt za pomocą wiersza poleceń:

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
<summary>Użycie</summary>
## Użytkowanie
### 1. Uruchom usługi
#### Na Linuxie i macOS
Jeden skrypt obsługuje wszystko. Automatycznie uruchamia główną usługę dyktowania i monitor plików w tle.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```
#### Na Windows
Uruchamianie usługi to **dwustopniowy proces ręczny**:

1.  **Uruchom główną usługę:** Uruchom `start_aura.bat`. lub rozpocznij od `.venv` usługę za pomocą `python3`
### 2. Skonfiguruj swój skrót klawiszowy

Aby uruchomić dyktowanie, potrzebny jest globalny skrót klawiszowy, który tworzy określony plik. Zdecydowanie polecamy narzędzie wieloplatformowe [CopyQ](https://github.com/hluk/CopyQ).
#### Nasza rekomendacja: CopyQ

Utwórz nowe polecenie w CopyQ z globalnym skrótem klawiszowym.

**Polecenie dla Linux/macOS:**
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
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```

Zacznij dyktować!
Kliknij w dowolnym polu tekstowym, naciśnij swój hotkey, a pojawi się "Słuchanie"... Mów wyraźnie, a potem pauza. Poprawiony tekst zostanie napisany dla Ciebie.

</details>

---


<details>
<summary>Zaawansowana konfiguracja (opcjonalnie) </summary>
# # Zaawansowana konfiguracja (opcjonalnie)

Możesz dostosować zachowanie aplikacji poprzez utworzenie pliku ustawień lokalnych.

1. Przejdź do katalogu `config/`.
2. Utwórz kopię `config/settings_local.py_Example.txt` i zmień nazwę na `config/settings_local.py`.
3. Edycja `config/settings_local.py` (nadpisuje wszelkie ustawienia z głównego pliku `config/settings.py`).

Ten plik `config/settings_local.py` jest domyślnie ignorowany przez Gita, więc Twoje osobiste zmiany nie zostaną nadpisane przez aktualizacje.
Wtyczka w strukturze i logice

Modularność systemu pozwala na solidne rozszerzenie poprzez wtyczki / katalog.

Silnik przetwórczy ściśle przylega do hierarchicznego łańcucha priorytetowego * *:

1. * * Moduł Zamówienie ładowania (wysoki priorytet): * * Zasady wczytane z podstawowych pakietów językowych (de- DE, en- US) mają pierwszeństwo przed zasadami wczytanymi z wtyczki / katalogu (które ładują ostatnio alfabetycznie).
    
2. * * In- File Order (Micro Priority): * * W obrębie dowolnego pliku mapy (FUZZY _ MAP _ pre.py), zasady są przetwarzane ściśle przez * * numer linii * * (top- to- bottom).
    

Architektura ta zapewnia ochronę podstawowych zasad systemowych, podczas gdy zasady specyficzne dla danego projektu lub jego wiedzy (takie jak te dla CodeIgniter lub kontroli gry) mogą być łatwo dodawane jako rozszerzenia o niskim priorytecie za pomocą wtyczek.

</details>

<details>
Skrypty <summary>Key dla Windows Users</summary>





# # Kluczowe skrypty dla użytkowników systemu Windows

Oto lista najważniejszych skryptów do skonfigurowania, aktualizacji i uruchomienia aplikacji w systemie Windows.
# # # Ustawienia i aktualizacja

*   `chmod +x update.sh; ./update.sh`
* `setup/setup.bat`: Główny skrypt dla początkowych ustawień jednokrotnego czasu * * środowiska.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat`: Uruchom to z folderu projektu, aby * * uzyskać najnowszy kod i zależności * *.
- Uruchomienie aplikacji
* `start_aura.bat`: Podstawowy skrypt, aby * * rozpocząć usługę dyktowania * *.
# # # Core & Helper Scripts
* `aura_engine.py`: Podstawowa usługa Python (zazwyczaj uruchamiana przez jeden ze skryptów powyżej).
* `get_suggestions.py`: Skrypt pomocniczy dla specyficznych funkcji.

</details>


# # Cechy kluczowe i kompatybilność systemu operacyjnego

<details>
<summary>Legend for OS Compatibility</summary>

Legenda dotycząca kompatybilności systemu operacyjnego:   
* Hamilton * * Linux * * (np. Arch, Ubuntu)   
* Addison * * MacOS * *   
* Hamilton * * Windows * *   
* Adresat * * Android * * * (dla cech specyficznych dla komórki)   

---

</details>


# # # * * Core Speech-to-Text (Aura) Engine * *
Nasz główny silnik do rozpoznawania mowy offline i przetwarzania dźwięku.

    
<details>
<summary>Aura- Core</summary>
* * Aura- Core / * * Simpson  
├─ `aura_engine.py` (główna usługa Python orcheposting Aura)
├┬ * * Live Hot- Reload * * (Konfiguracja i mapy)
│├ * * Bezpieczne prywatne ładowanie mapy (Integrity- First) * * KLASYFIKACJA   
││ * * * Workflow * * Wczytuje archiwa ZIP chronione hasłem.   
│├ * * Przetwarzanie tekstu i korekta / * * Zgrupowane według języka (np. `de-DE`, `en-US`,...)   
│├ 1. `normalize_punctuation.py` (Standaryzuje interpunkcję po transkrypcji)
│├ 2. * * Inteligentna korekta wstępna * * (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules-pllang.md))
││ * * * Dynamiczne wykonanie skryptu: * * Zasady mogą uruchamiać własne skrypty Pythona (`on_match_exec`) do wykonywania zaawansowanych działań, takich jak wywołania API, plik I / O lub generowanie odpowiedzi dynamicznych.   
││ * * * Cascading Execution: * * Zasady są przetwarzane kolejno, a ich skutki są * * skumulowane * *. Późniejsze zasady mają zastosowanie do tekstu zmodyfikowanego przez wcześniejsze zasady.
││ * * * Najwyższe kryterium Priority Stop: * * Jeśli reguła osiąga * * Full Match * * (^... $), cały rurociąg przetwarzania dla tego symbolu natychmiast zatrzymuje się. Mechanizm ten ma kluczowe znaczenie dla wdrażania niezawodnych poleceń głosowych.   
│├ 3. `correct_text_by_languagetool.py` (Integrates LanguageTool for grammar / style correction)
│├ * * 4. Hierarchiczny RegEx- Rule- Engine z Ollama AI Fallback
││ * * * Deterministic Control: * * Używa RegEx- Rule- Engine do precyzyjnego, priorytetowego polecenia i sterowania tekstem.   
│├ * * Vector- Search Plugin * * (Lazy loading): Włącza semantyczne wyszukiwanie łącząc lokalne osadzenia wektorowe z warstwą Ollama / LLM
││ * * * Ollama AI (Local LLM) Fallback: * * Służy jako opcjonalny, niskopriorytetowy sprawdzian dla * * kreatywnych odpowiedzi, Q & A, i zaawansowanych Fuzzy Matching * * gdy nie jest określona reguła met.  
││ * * * Status: * * Lokalna integracja LLM.
│└ 5. * * Inteligentna korekta post- * * (`FuzzyMap`) * * * - Rafinowanie post- LT * * Refinezja   
││ * Stosowane po LanguageTool w celu skorygowania specyficznych wyjść LT. Follows the same strict cascading priority logics as the Pre- Correction layer.  
││ * * * Dynamiczne wykonanie skryptu: * * Zasady mogą uruchamiać własne skrypty Pythona ([on_match_exec](../docs/advanced-scripting-pllang.md)), aby wykonywać zaawansowane działania, takie jak wywołania API, plik I / O lub generować odpowiedzi dynamiczne.   
││ * * * Fuzzy Fallback * * * * FUZY SUPLIarity Check * * (kontrolowany przez próg, np. 85%) działa jako najniższa warstwa błędu priorytetowego. Jest on wykonywany tylko wtedy, gdy cała poprzednia reguła determinaristic / cascading nie uda się znaleźć dopasowania (current _ rule _ match is False), optymalizując wydajność poprzez unikanie powolnych, rozmytych kontroli w miarę możliwości.   
├┬ * * Model Management / * *   
│├─ `prioritize_model.py` (Optymalizuje model załadunku / rozładunku w zależności od zastosowania)
│└─ `setup_initial_model.py` (Konfiguracja modelu po raz pierwszy)
├─ * * Adaptive VAD Timeout * * Significations   
├─ * * Adaptive Hotkey (Start / Stop)
├─ * * Instant Language Switching * * (Experimental via model preloading)
├─ * * Orchestracja przepływu powietrza * * (automatyzacja przepływu pracy oparta na DAG) 🐧 🍏 🪟
│   Wymagane Docker · Interfejs: `http://localhost:8081`
├─ * * Trino State Engine * 🐧 🍏 🪟
└─  Wymagane Docker · Admin UI: `http://localhost:8084`

  
├┬ * * LanguageTool Server Management / * *   
│├─ `start_languagetool_server.py` (Inicjuje lokalny serwer LanguageTool)
│└─ `stop_languagetool_server.py` (Wyłącza serwer LanguageTool) 🐧 🍏 
├─ `monitor_mic.sh` (np. do stosowania z zestawem słuchawkowym bez użycia klawiatury i monitora)
# # # * * Model & Zarządzanie pakietami * *   
Narzędzia do solidnego obchodzenia się z dużymi modelami językowym.  

* * ModelManagement / * * Simpson  
├─ * * Solidny model * * (GitHub Release chunks)
├─ `split_and_hash.py` (Użyteczność dla właścicieli repo do podziału dużych plików i generowania kwot kontrolnych)
└─ `download_all_packages.py` (Narzędzie dla użytkowników końcowych do pobierania, weryfikacji i ponownego składania plików wieloczęściowych)

</details>


<details>
<summary>Rozwój i wdrażanie Helpers</summary>
*   
Skrypty dotyczące konfiguracji środowiska, testowania i wykonywania usług.   

* Wskazówka: glogg umożliwia korzystanie z wyrażeń regularnych w poszukiwaniu ciekawych zdarzeń w plikach dziennika. *   
Proszę zaznaczyć pole wyboru podczas instalacji, aby powiązać je z plikami log-.   
https: / / glogg.bonnefon.org /   
    
* Wskazówka: Po zdefiniowaniu wzorców regex, uruchom `python3 tools/map_tagger.py`, aby automatycznie wygenerować przykłady przeszukiwania dla narzędzi CLI. Szczegóły znajdują się w [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools-pllang.md). *

To może podwójne kliknięcie
`log/aura_engine.log`
    
* * DevHelpers / * *   
├┬ * * Wirtualne zarządzanie środowiskiem / * *   
│├ `scripts/restart_venv_and_run-server.sh` (Linux / macOS)
│└ `scripts/restart_venv_and_run-server.ahk` (Windows)
├┬ * * System- wide Dictation Integration / * *   
│├ Vosk- System- Integracja słuchaczy
│├ `scripts/monitor_mic.sh` (monitorowanie mikrofonu specyficznego dla Linuksa)   
│└ `scripts/type_watcher.ahk` (AutoHotkey słucha rozpoznanego tekstu i wypisuje go system- wide)   
└─ * * CI / CD Automation / * *   
    └─ Rozszerzone ćwiczenia GitHub (Instalacja, testowanie, wdrażanie dokumentów)

</details>

<details>
<summary>Experimental Features</summary>
    *   
Funkcje obecnie opracowywane lub w projekcie status.  

* * ExperimentalFeatures / * *   
├─ * * ENTER _ after _ DICTATION _ REGEX * * Przykład zasady aktywacji "(ExampleAplicationThatNotExist124; Pi, Twoja osobista AI)"   
├┬Plugins  
│* * Live Lazy- Reload * * * (*)
(* Zmiany aktywacji / dezaktywacji wtyczki oraz ich konfiguracje są stosowane w następnym procesie przetwarzania bez ponownego uruchomienia usługi. *)   
│ ├ * * git commands * * (Voice control for send git commands)
│ ├ * * wannweil * * (Mapa lokalizacji Germany-Wannweil)
│ ├ * * Wtyczka Poker (Draft) * * (Kontrola głosowa dla aplikacji pokerowych)
│ └ * * 0 A.D. Plugin (Draft) * * (Voice Control for 0 A.D. game)
├─ * * Wyjście dźwiękowe przy starcie lub zakończeniu sesji * * (Opis oczekujący)
├─ * * Speech Output for Visual Imparial * * (Opis oczekujący)
└─ * * SL5 Aura Android Prototyp * * (Nie w pełni offline jeszcze)

---

* (Uwaga: Specyficzne dystrybucje Linuksa, takie jak Arch (ARL) lub Ubuntu (UBT) są objęte ogólnym symbolem symbolu Linux. Szczegółowe rozróżnienia mogą być objęte przewodnikami instalacyjnymi.) *
</details>

<details>
<summary>Click aby zobaczyć polecenie używane do wygenerowania tego skryptu list</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A graficzny przegląd architektury </summary>
# # # Graficzny przegląd architektury:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Używane modele </summary>
Używane modele:

Zalecenie: stosować modele z Mirror https: / / github.com / sl5net / SL5-aura- service / releases / tag / v0.2.0.1 (prawdopodobnie szybciej)

Te zapięte modele muszą być zapisane w folderze `models/`

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
## Wspieraj Projekt
Jeśli uważasz to narzędzie za przydatne, rozważ proszę kupienie nam kawy! Twoje wsparcie pomaga w finansowaniu przyszłych ulepszeń.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)
