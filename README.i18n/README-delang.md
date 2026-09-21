<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Deine Stimme. Deine Regeln.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100 % offline, datenschutzorientiertes Sprachassistenten-Framework.  
> Definieren Sie genau, was Ihre Stimme tut — von einem einzelnen Wort
> zu vollständigen Python-Skripten. Keine Cloud. Keine Daten verlassen Ihr Gerät.
> Läuft im Terminal, im Browser oder als Hintergrunddienst — auf Linux, macOS und Windows.| 👵 Anfänger | 🎓 Lernender | 🧑u200d💻 Entwickler |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-delang.md#the-oma-modus-beginner-shortcut): Schreiben Sie einfach ein Wort, Aura erledigt den Rest | Lernen Sie mit Koans – ein Konzept nach dem anderen | Vollständige Python-Skripterstellung, Plugins, API-Aufrufe |
| 🗄️ Staatsverwaltung | Trino + Airflow-Orchestrierung, fzf, CopyQ, Sprach-/Terminalbefehle, Browser-Benutzeroberflächen |[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** pro Test (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · keine Cloud-Berechnung

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Vollständige Testreihe:** 94 Tests mit LanguageTool über >800 Karten @ 0,07s warm / 0,46s kalt · keine Cloud-Berechnung

<details>
<summary>Schnellstart</summary>## Schnellstart### Option A: 1-Klick & Web Installer (Recommended)

Einzeiliger Befehl oder eigenständiges Installationsprogramm für Linux, macOS und Windows:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-delang.md)**

---### Option B: Manuelle Installation (Developers / Git)

1. Laden Sie dieses Repository herunter oder klonen Sie es
2. Führen Sie das Setup-Skript für Ihr Betriebssystem (see `setup/` folder) aus:
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix`, dann `bash setup/nixos_setup.sh`
===> ⚠️ Experimentell – von Autoren nicht getestet, Feedback willkommen!   
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Starten Sie Aura: `./scripts/restart_venv_and_run-server.sh`
4. Drücken Sie Ihren Hotkey und sprechen Sie – **[full guide →](../docs/GettingStarted.i18n/GettingStarted-delang.md)**

---### Deinstallation
So entfernen Sie SL5 Aura-Hintergrunddienste, Autostart-Einträge und virtuelle Umgebungen:
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


**⚠️ Systemanforderungen und Kompatibilität**

* **Windows:** ✅ Vollständige Unterstützung von (uses AutoHotkey/PowerShell).
* **macOS:** ✅ Vollständige Unterstützung von (uses AppleScript).
* **Linux (X11/Xorg):** ✅ Vollständig unterstützt.
* **Linux (Wayland):** ✅ Vollständige Unterstützung von (tested on KDE Plasma 6 / Wayland).
* **Linux (CachyOS / Arch-based rolling release):** ✅ Vollständig unterstützt.
Erfordert mimalloc (`sudo pacman -S mimalloc`) aufgrund der Glibc 2.43-Kompatibilität.
* **Linux (NixOS):** 🧪 Experimentell – von der Community bereitgestelltes Setup, noch nicht getestet.
Wenn Sie es versuchen, eröffnen Sie bitte eine Ausgabe oder PR mit Ihren Ergebnissen!    
* **Linux (Manjaro):** Neu: Ein systemweiter Hotkey öffnet eine fzf-ähnliche, tastaturgesteuerte Oberfläche, sodass Sie Aura-Befehle von überall auf dem Desktop ausführen können (completely decoupled from the active window). Dieser Hotkey-gesteuerte Launcher wird derzeit unter Linux (Manjaro) implementiert und getestet; Andere Distributionen funktionieren möglicherweise, erfordern jedoch das Setup. Siehe in 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-delang.md)   


  
SL5 Aura ist ein vollständiger **Offline-Sprachassistent**, der auf **Vosk** (for Speech-to-Text) und **LanguageTool** Es wandelt Ihre Stimme in präzise Aktionen und Texte um und ist durch ein steckbares Regelsystem und eine dynamische Skript-Engine für die ultimative Anpassung konzipiert.
  
Übersetzungen: Dieses Dokument existiert auch in [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Hinweis: Bei vielen Texten handelt es sich um maschinell erstellte Übersetzungen der englischen Originaldokumentation, die lediglich der allgemeinen Orientierung dienen. Bei Unstimmigkeiten oder Unklarheiten ist immer die englische Version maßgebend. Wir freuen uns über die Hilfe der Community, um diese Übersetzung zu verbessern!

</details>

<details>
<summary>Demo</summary>### 📺 Terminal-Demo

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Tipp:** Für ein besseres Terminalerlebnis siehe [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-delang.md).### 🎥 Videoanleitung
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: XMDLINK1X)*

</details>

<details>
<summary>Hauptmerkmale</summary>## Hauptmerkmale

* **Offline und privat:** 100 % lokal. Keine Daten verlassen jemals Ihren Computer.
* **Dynamic Scripting Engine:** Gehen Sie über das Ersetzen von Text hinaus. Regeln können benutzerdefinierte Python-Skripte (`on_match_exec`) ausführen, um erweiterte Aktionen wie das Aufrufen von APIs (e.g., search Wikipedia), die Interaktion mit Dateien (e.g., manage a to-do list) oder das Generieren dynamischer Inhalte (e.g., a context-aware email greeting) durchzuführen.
* **Kontextsensitive Regeln:** Regeln auf bestimmte Anwendungen beschränken. Mit „only_in_windows“ können Sie sicherstellen, dass eine Regel nur dann ausgelöst wird, wenn ein bestimmter Fenstertitel (e.g., "Terminal", "VS Code" or "Browser") aktiv ist. Dies funktioniert plattformübergreifend mit (Linux, Windows, macOS).
* **High-Control Transformation Engine:** Implementiert eine konfigurationsgesteuerte, hochgradig anpassbare Verarbeitungspipeline. Regelpriorität, Befehlserkennung und Texttransformationen werden ausschließlich durch die Reihenfolge der Regeln in den Fuzzy Maps bestimmt und erfordern **Konfiguration, keine Codierung**.
* **Konservative RAM-Nutzung:** Verwaltet den Speicher intelligent und lädt Modelle nur dann vor, wenn genügend freier RAM verfügbar ist, um sicherzustellen, dass andere Anwendungen immer Vorrang haben.
* **Plattformübergreifend:** Funktioniert unter Linux, macOS und Windows.
* **Vollautomatisch:** Verwaltet seinen eigenen LanguageTool-Server (but you can also use an external one).
* **Blitzschnell:** Intelligentes Caching sorgt für sofortige „Listening…“-Benachrichtigungen und schnelle Verarbeitung.
* **Dynamisches Zustandsmanagement über Trino:** Schnittstellenbewusste Konfigurations-Engine
trennt die Einstellungen für „Sprache“, „Terminal“ und „Web“ – ändern Sie eine ohne
die anderen beeinflussen. Enthält ein Echtzeit-Admin-Dashboard mit (port 8084).
</details>

<details>
<summary> 🔌 Gebrauchsfertige Integrationen</summary>
  ## 🔌 Gebrauchsfertige Integrationen

SL5-Aura verfügt über ein riesiges Ökosystem von über **100+ vorkonfigurierten Plugins**. Hier einige Highlights:### OculiX / SikuliX IDE-Sprachsteuerung
SL5-Aura bietet erstklassige Sprachunterstützung für **OculiX** und **SikuliX IDE**. Diese Integration ermöglicht es Ihnen, Ihren Automatisierungscode zu „sprechen“.

* **Voice-to-Snippet:** Sagen Sie „Klicken“, „Warten“ oder „Alle finden“, und der Dienst gibt sofort den richtigen Python-Code ((e.g., `click("image.png")`) in die IDE ein.
* **Window-Aware:** Das Plugin ist kontextsensitiv; Es wird nur aktiviert, wenn das OculiX/SikuliX-Fenster fokussiert ist.
* **Intelligente Englischunterstützung:** Optimiert für „en-US“ mit besonderem Fokus auf nicht-muttersprachliche Akzente (e.g., German-English phonetics), um eine hohe Erkennungsgenauigkeit für die globale Community zu gewährleisten.
* **Erweiterbar:** Verwendet das einfach zu bearbeitende Format „FUZZY_MAP_pre.py“.

> **Status:** Vom OculiX-Team (see XMDLINK0X) als Community-Plugin anerkannt.### LibreOffice IDE-Sprachsteuerung### 0 A.D. Sprachsteuerung

---

</details>


<details>
<summary>Dokumentation</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)## Dokumentation

Eine vollständige technische Referenz, einschließlich aller Module und Skripte, finden Sie auf unserer offiziellen Dokumentationsseite. Es wird automatisch generiert und ist immer aktuell.

👉[**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)### Funktions-Highlights
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-delang.md) — Dual-Pane-`fzf`-Regelsuche, Live-Kontextvorschauen, sofortige Befehlsausführung über `Enter`/`Ctrl+R` und Editor-Integration über `Ctrl+E`. Unterstützt durch eine globale Tastenkombination (`Super+S`) und mehrere dedizierte Suchumgebungen, die über Sprachbefehle vorkonfiguriert sind.### Build-Status

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

👉 **Lies dies in anderen Sprachen:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-delang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang.md) | [🇪🇸 Español](../README.i18n/README-eslang-delang.md) | [🇫🇷 Français](../README.i18n/README-frlang-delang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-delang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-delang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-delang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-delang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-delang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-delang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-delang.md)

---

<details>
<summary>Installation</summary>## Installation### 🎥 Schnelle Installation ohne Moderation (Manjaro/Arch Video)
Sehen Sie sich den vollständigen 6-minütigen Einrichtungsprozess an:
* **Download:** ~3 Minuten
* **Einrichtung & erster Start:** ~3 Minuten (including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


Die Einrichtung ist ein zweistufiger Prozess:
1. Laden Sie die neueste Version oder den Master von ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) herunter oder klonen Sie dieses Repository auf Ihren Computer.
2. Führen Sie das einmalige Einrichtungsskript für Ihr Betriebssystem aus.

Die Setup-Skripte kümmern sich um alles: Systemabhängigkeiten, Python-Umgebung und das Herunterladen der notwendigen Modelle und Werkzeuge (~4GB) direkt von unseren GitHub-Releases für maximale Geschwindigkeit.#### Für Linux, macOS und Windows (with Optional Language Exclusion)

Um Speicherplatz und Bandbreite zu sparen, können Sie während der Einrichtung bestimmte Sprachmodelle (`de`, `en`) oder alle optionalen Modelle (`all`) ausschließen. **Kernkomponenten (LanguageTool, lid.176) sind immer enthalten.**

Öffnen Sie ein Terminal im Stammverzeichnis des Projekts und führen Sie das Skript für Ihr System aus:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Beispiele:
# Alles installieren (Default):
# bash setup/manjaro_arch_setup.sh

# Deutsche Modelle ausschließen:
# bash setup/manjaro_arch_setup.shexclude=de

# Alle VOSK-Sprachmodelle ausschließen:
# bash setup/manjaro_arch_setup.shexclude=all

# Für Windows in einer Admin-Powershell-Sitzung

setup/windows11_setup.ps1 -Exclude [OPTION]

# Beispiele:
# Alles installieren (Default):
# setup/windows11_setup.ps1

# Englische Modelle ausschließen:
# setup/windows11_setup.ps1 -Exclude „en“

# Deutsche und englische Modelle ausschließen:
# setup/windows11_setup.ps1 -Exclude „de,en“

# Oder (recommend) – Führen Sie die BAT-Datei aus:
windows11_setup.bat -Exclude „en“
__CODE_BLOCK_1__#### Für Windows
Führen Sie das Setup-Skript mit Administratorrechten aus.

**Installieren Sie ein Werkzeug zum Lesen und Ausführen, z. B. [CopyQ](https://github.com/hluk/CopyQ) oder [AutoHotkey v2](https://www.autohotkey.com/)**. Dies wird für den Text-Überwachungsleser benötigt.

Die Installation ist vollständig automatisiert und dauert etwa **8-10 Minuten**, wenn auf einem frischen System 2 Modelle verwendet werden.

1. Navigiere zum `setup`-Ordner.
2. Doppelklicken Sie auf **`windows11_setup_with_ahk_copyq.bat`**.
   * *Das Skript wird automatisch nach Administratorrechten fragen.*
* *Es installiert das Kernsystem, Sprachmodelle, **AutoHotkey v2** und **CopyQ**.*
3. Sobald die Installation abgeschlossen ist, wird **Aura Dictation** automatisch gestartet.

> **Hinweis:** Sie müssen Python oder Git nicht vorher installieren; das Skript übernimmt alles.

---#### Erweiterte / benutzerdefinierte Installation
Wenn Sie die Client-Tools (AHK/CopyQ) nicht installieren möchten oder durch den Ausschluss bestimmter Sprachen Speicherplatz sparen möchten, können Sie das Kernskript über die Befehlszeile ausführen:

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
<summary>Usage</summary>## Verwendung### 1. Starten Sie die Dienste#### Auf Linux & macOS
Ein einzelnes Skript erledigt alles. Es startet den Hauptdiktatdienst und den Dateiüberwacher automatisch im Hintergrund.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```#### Unter Windows
Das Starten des Dienstes ist ein **zweistufiger manueller Prozess**:

1. **Starten Sie den Hauptdienst:** Führen Sie „start_aura.bat“ aus. oder starten Sie von „.venv“ aus den Dienst mit „python3“.### 2. Konfigurieren Sie Ihre Tastenkombination

Um die Diktierfunktion auszulösen, benötigen Sie eine globale Tastenkombination, die eine bestimmte Datei erstellt. Wir empfehlen dringend das plattformübergreifende Werkzeug [CopyQ](https://github.com/hluk/CopyQ).#### Unsere Empfehlung: CopyQ

Erstellen Sie in CopyQ einen neuen Befehl mit einer globalen Verknüpfung.

**Befehl für Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Befehl für Windows bei Verwendung von [CopyQ](https://github.com/hluk/CopyQ):**
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


**Befehl für Windows bei Verwendung von [AutoHotkey](https://AutoHotkey.com):**
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
```### 3. Beginne mit dem Diktieren!
Klicken Sie in ein beliebiges Textfeld, drücken Sie Ihre Tastenkombination, und eine „Zuhören...“-Benachrichtigung wird angezeigt. Sprechen Sie deutlich, und machen Sie dann eine Pause. Der korrigierte Text wird für Sie eingegeben.

</details>

---


<details>
<summary>Erweiterte Konfiguration (Optional)</summary>## Erweiterte Konfiguration (Optional)

Sie können das Verhalten der Anwendung anpassen, indem Sie eine lokale Einstellungsdatei erstellen.

1. Navigieren Sie zum Verzeichnis „config/“.
2. Erstellen Sie eine Kopie von „config/settings_local.py_Example.txt“ und benennen Sie sie in „config/settings_local.py“ um.
3. Bearbeiten Sie „config/settings_local.py“ (it overrides any setting from the main `config/settings.py` file).

Diese Datei „config/settings_local.py“ wird von Git standardmäßig ignoriert, sodass Ihre persönlichen Änderungen nicht durch Updates überschrieben werden.### Plug-in-Struktur und Logik

Die Modularität des Systems ermöglicht eine robuste Erweiterung über das Verzeichnis plugins/.

Die Verarbeitungseinheit hält sich strikt an eine **Hierarchische Prioritätskette**:

1. **Modul-Lade-Reihenfolge (High Priority):** Regeln, die aus den Kern-Sprachpaketen (de-DE, en-US) geladen werden, haben Vorrang vor Regeln, die aus dem Plugins/-Verzeichnis (which load last alphabetically) geladen werden.
    
2. **In-Datei-Reihenfolge (Micro Priority):** Innerhalb jeder beliebigen Karten-Datei (FUZZY_MAP_pre.py) werden Regeln strikt nach **Zeilennummer** (top-to-bottom) verarbeitet.
    

Diese Architektur stellt sicher, dass zentrale Systemregeln geschützt sind, während projektspezifische oder kontextbewusste Regeln (like those for CodeIgniter or game controls) leicht als niedrig priorisierte Erweiterungen über Plug-ins hinzugefügt werden können.

</details>

<details>
<summary>Key-Skripte für Windows-Benutzer</summary>## Wichtige Skripte für Windows-Benutzer

Hier finden Sie eine Liste der wichtigsten Skripte zum Einrichten, Aktualisieren und Ausführen der Anwendung auf einem Windows-System.### Einrichtung & Aktualisierung

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: Das Hauptskript für die **erste einmalige Einrichtung** der Umgebung.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Führe powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"` aus

*   `update.bat` : Führe dies aus dem Projektordner aus, um **den neuesten Code und die Abhängigkeiten zu erhalten**.### Ausführen der Anwendung
* „start_aura.bat“: Ein primäres Skript zum **Starten des Diktierdienstes**.### Kern- & Hilfsskripte
*   `aura_engine.py`: Der Kern-Python-Dienst (usually started by one of the scripts above).
*   `get_suggestions.py`: Ein Hilfsskript für bestimmte Funktionen.

</details>## 🚀 Hauptfunktionen und Betriebssystemkompatibilität

<details>
<summary>Legende für Betriebssystemkompatibilität</summary>

Legende zur Betriebssystemkompatibilität:  
* 🐧 **Linux** (e.g., Arch, Ubuntu)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (for mobile-specific features)  

---

</details>### **Kern-Speech-to-Text-(Aura)-Engine**
Unsere primäre Engine für Offline-Spracherkennung und Audioverarbeitung.

  
<details>
<summary>Aura-Core</summary>
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Main Python service orchestrating Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config & Maps) 🐧 🍏 🪟  
│├ **Sicheres Laden privater Karten mit (Integrity-First)** 🔒 🐧 🍏 🪟  
││ * **Workflow:** Lädt passwortgeschützte ZIP-Archive.   
│├ **Textverarbeitung und -korrektur/** Gruppiert nach Sprache ( e.g. `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardizes punctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **Intelligente Vorkorrektur** (`FuzzyMap Pre` - XMDLINK0X) 🐧 🍏 🪟  
││ * **Dynamische Skriptausführung:** Regeln können benutzerdefinierte Python-Skripte (`on_match_exec`) auslösen, um erweiterte Aktionen wie API-Aufrufe, Datei-E/A auszuführen oder dynamische Antworten zu generieren.  
││ * **Kaskadierende Ausführung:** Regeln werden nacheinander verarbeitet und ihre Auswirkungen sind **kumulativ**. Spätere Regeln gelten für Text, der durch frühere Regeln geändert wurde.  
││ * **Stoppkriterium mit höchster Priorität:** Wenn eine Regel eine **Vollständige Übereinstimmung** (^...$) erreicht, wird die gesamte Verarbeitungspipeline für dieses Token sofort gestoppt. Dieser Mechanismus ist für die Implementierung zuverlässiger Sprachbefehle von entscheidender Bedeutung.  
│├ 3. `correct_text_by_lingualtool.py` (Integrates LanguageTool for grammar/style correction) 🐧 🍏 🪟  
│├ **4. Hierarchische RegEx-Regel-Engine mit Ollama AI Fallback** 🐧 🍏 🪟  
││ * **Deterministische Steuerung:** Verwendet RegEx-Rule-Engine für präzise Befehls- und Textsteuerung mit hoher Priorität.  
│├ **Plugin für die Vektorsuche**
││ * **Ollama AI (Local LLM) Fallback:** Dient als optionale Prüfung mit niedriger Priorität für **kreative Antworten, Fragen und Antworten und erweitertes Fuzzy Matching**, wenn keine deterministische Regel erfüllt ist.  
││ * **Status:** Lokale LLM-Integration.
│└ 5. **Intelligente Nachkorrektur** (`FuzzyMap`)**– Post-LT-Verfeinerung** 🐧 🍏 🪟  
││ * Wird nach LanguageTool angewendet, um LT-spezifische Ausgaben zu korrigieren. Folgt der gleichen strengen kaskadierenden Prioritätslogik wie die Vorkorrekturschicht.  
││ * **Dynamische Skriptausführung:** Regeln können benutzerdefinierte Python-Skripte (XMDLINK1X) auslösen, um erweiterte Aktionen wie API-Aufrufe, Datei-E/A auszuführen oder dynamische Antworten zu generieren.  
││ * **Fuzzy-Fallback:** Die **Fuzzy-Ähnlichkeitsprüfung** (controlled by a threshold, e.g., 85%) fungiert als Fehlerkorrekturebene mit der niedrigsten Priorität. Es wird nur ausgeführt, wenn die gesamte vorhergehende Ausführung der deterministischen/kaskadierenden Regel keine Übereinstimmung mit (current_rule_matched is False) gefunden hat. Dadurch wird die Leistung optimiert, indem nach Möglichkeit langsame Fuzzy-Prüfungen vermieden werden.  
├┬ **Modellverwaltung/**   
│├─ `prioritize_model.py` (Optimizes model loading/unloading based on usage) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configures the first-time model setup) 🐧 🍏 🪟  
├─ **Adaptives VAD-Timeout** 🐧 🍏 🪟  
├─ **Adaptiver Hotkey (Start/Stop)** 🐧 🍏 🪟  
├─ **Sofortige Sprachumschaltung** (Experimental via model preloading) 🐧 🍏   
├─ **Airflow Orchestration** (DAG-based workflow automation) 🐧 🍏 🪟
│ Erfordert Docker · Benutzeroberfläche: „http://localhost:8081“ 🐧 🍏 🪟  
├─ **Trino State Engine** (Interface-aware config per speech/terminal/web) 🐧 🍏 🪟
└─ Erfordert Docker · Admin-Benutzeroberfläche: „http://localhost:8084“ 🐧 🍏 🪟  

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_lingualtool_server.py` (Initializes the local LanguageTool server) 🐧 🍏 🪟  
│└─ `stop_lingualtool_server.py` (Shuts down the LanguageTool server) 🐧 🍏
├─ `monitor_mic.sh` (e.g. for use with Headset without use keyboard and Monitor) 🐧 🍏 🪟  ### **Modell- und Paketverwaltung**  
Tools für den robusten Umgang mit großen Sprachmodellen.  

**ModelManagement/** 🐧 🍏 🪟  
├─ **Robuster Modell-Downloader** (GitHub Release chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utility for repo owners to split large files and generate checksums) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool for end-users to download, verify, and reassemble multi-part files) 🐧 🍏 🪟  

</details>


<details>
<summary>Entwicklungs- und Bereitstellungshelfer</summary>### **Entwicklungs- & Bereitstellungshelfer**  
Skripte für die Einrichtung der Umgebung, Tests und Dienstausführung.

*Tipp: Glogg ermöglicht es Ihnen, reguläre Ausdrücke zu verwenden, um interessante Ereignisse in Ihren Protokolldateien zu suchen.*
Bitte aktivieren Sie das Kontrollkästchen während der Installation, um eine Verknüpfung mit Protokolldateien herzustellen.   
https://www.translatetheweb.com/?from=en&to=de&a=https://glogg.bonnefon.org/     
    
*Tipp: Nachdem Sie Ihre Regex-Muster definiert haben, führen Sie `python3 tools/map_tagger.py` aus, um automatisch durchsuchbare Beispiele für die CLI-Tools zu erstellen. Siehe [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-delang.md) für Details.*

Dann vielleicht doppelklicken
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ **Verwaltung virtueller Umgebungen/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Systemweite Diktat-Integration/**  
│├ Vosk-System-Listener-Integration 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux-specific microphone monitoring) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey listens for recognized text and types it out system-wide) 🪟  
└─ **CI/CD-Automatisierung/**  
    └─ Erweiterte GitHub-Workflows (Installation, testing, docs deployment) 🐧 🍏 🪟 *(Runs on GitHub Actions)*  

</details>

<details>
<summary>Experimentelle Funktionen</summary>
    ### **Kommende / Experimentelle Funktionen**  
Funktionen, die sich derzeit in der Entwicklung oder im Entwurfsstatus befinden.  

**ExperimentelleFunktionen/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Beispiel für eine Aktivierungsregel "(ExampleAplicationThatNotExist|Pi, your personal AI)" 🐧  
├┬Plugins  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)  
│ ├ **git Befehle** (Voice control for send git commands) 🐧 🍏 🪟  
│ ├ **wannweil** (Map for Location Germany-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Voice control for poker applications) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Voice control for 0 A.D. game) 🐧   
├─ **Ton-Ausgabe beim Starten oder Beenden einer Sitzung** (Description pending) 🐧   
├─ **Sprachausgabe für Sehbehinderte** (Description pending) 🐧 🍏 🪟  
└─ **SL5 Aura Android-Prototyp** (Not fully offline yet) 📱  

---

*(Note: Specific Linux distributions like Arch (ARL) oder Ubuntu (UBT) werden durch das allgemeine Linux 🐧 Symbol abgedeckt. Detaillierte Unterschiede könnten in Installationshandbüchern behandelt werden.)*
</details>

<details>
<summary>Klicken Sie hier, um den Befehl zu sehen, der verwendet wurde, um diese Skriptliste zu erstellen</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A grafische Übersicht der Architektur</summary>### Ein grafischer Überblick über die Architektur:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Gebrauchte Modelle</summary>## Verwendete Modelle:

Empfehlung: Verwenden Sie Modelle von Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probably faster)

Diese gezippten Modelle müssen im Ordner `models/` gespeichert werden

`mv vosk-model-*.zip models/`| Modell | Größe | Wortfehlerrate/Geschwindigkeit | Notizen | Lizenz |
| -------------------------------------------------------------------------------------- | ---- | ----------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter) | Präzises generisches US-englisches Modell | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 Großes deutsches Modell für Telefonie und Server | Apache 2.0 |Diese Tabelle bietet einen Überblick über verschiedene Vosk-Modelle, einschließlich ihrer Größe, Wortfehlerrate oder -geschwindigkeit, Anmerkungen und Lizenzinformationen.


- **Vosk-Modelle:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**Lizenz von LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>## Unterstützen Sie das Projekt
Wenn Sie dieses Tool nützlich finden, denken Sie bitte darüber nach, uns einen Kaffee zu spenden! Ihre Unterstützung trägt dazu bei, zukünftige Verbesserungen voranzutreiben.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)