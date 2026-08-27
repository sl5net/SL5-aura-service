<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Deine Stimme. Ihre Regeln.

> 100 % Offline-Sprachassistenten-Framework, bei dem die Privatsphäre an erster Stelle steht.  
> Definieren Sie genau, was Ihre Stimme tut – mit einem einzigen Wort  
> zu vollständigen Python-Skripten. Keine Wolke. Keine Daten verlassen Ihren Computer.  
> Läuft im Terminal, Browser oder als Hintergrunddienst – unter Linux, macOS und Windows.

| 👵 Anfänger | 🎓 Lernender | 🧑u200d💻 Entwickler |
|---|---|---|


| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-delang.md#the-oma-modus-beginner-shortcut): Schreiben Sie einfach ein Wort, Aura erledigt den Rest | Lernen Sie mit Koans – ein Konzept nach dem anderen | Vollständige Python-Skripterstellung, Plugins, API-Aufrufe |
| 🗄️ Staatsverwaltung | Trino + Airflow-Orchestrierung, fzf, CopyQ, Sprach-/Terminalbefehle, Browser-Benutzeroberflächen |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)
⚡ **~2,87 J** pro Test (39 Tests auf >800 Karten bei 0,08 s warm / 0,35 s kalt 🌿 gemessen mit [Eco-CI](https://metrics.green-coding.io/index.html)) · kein Cloud-Computing


<Details>
<summary>Schnellstart</summary>

## Schnellstart
1. Laden Sie dieses Repository herunter oder klonen Sie es
2. Führen Sie das Setup-Skript für Ihr Betriebssystem aus (siehe Ordner „setup/“):
- Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
===> 🧩 [docs/LINUX_WAYLAND_dotool](../docs/LINUX_WAYLAND_dotool.i18n/LINUX_WAYLAND_dotool-delang.md) lesen
- Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix`, dann `bash setup/nixos_setup.sh`
===> ⚠️ Experimentell – von Autoren nicht getestet, Feedback willkommen!   
- macOS: `bash setup/macos_setup.sh`
- Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Starten Sie Aura: `./scripts/restart_venv_and_run-server.sh`
4. Drücken Sie Ihren Hotkey und sprechen Sie – **[full guide →](../docs/GettingStarted.i18n/GettingStarted-delang.md)**


**⚠️ Systemanforderungen und Kompatibilität**

* **Windows:** ✅ Vollständig unterstützt (verwendet AutoHotkey/PowerShell).
* **macOS:** ✅ Vollständig unterstützt (verwendet AppleScript).
* **Linux (X11/Xorg):** ✅ Vollständig unterstützt.
* **Linux (Wayland):** ✅ Vollständig unterstützt (getestet auf KDE Plasma 6 / Wayland).
* **Linux (CachyOS / Arch-basiertes Rolling Release):** ✅ Vollständig unterstützt.
Erfordert mimalloc („sudo pacman -S mimalloc“) aufgrund der Glibc 2.43-Kompatibilität.
* **Linux (NixOS):** 🧪 Experimentell – von der Community bereitgestelltes Setup, noch nicht getestet.
Wenn Sie es versuchen, eröffnen Sie bitte eine Ausgabe oder PR mit Ihren Ergebnissen!    
* **Linux (Manjaro):** Neu/experimentell: Ein systemweiter Hotkey öffnet eine fzf-ähnliche, tastaturgesteuerte Oberfläche, sodass Sie Aura-Befehle von überall auf dem Desktop ausführen können (völlig entkoppelt vom aktiven Fenster). Dieser Hotkey-gesteuerte Launcher wird derzeit unter Linux (Manjaro) implementiert und getestet. Andere Distributionen funktionieren möglicherweise, erfordern jedoch das Setup. Siehe in 👉 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-delang.md)   


  
SL5 Aura ist ein vollständiger **Offline-Sprachassistent**, der auf **Vosk** (für Speech-to-Text) und **LanguageTool** (für Grammatik/Stil) basiert und über einen optionalen **Local LLM (Ollama) Fallback** für kreative Antworten und erweitertes Fuzzy-Matching verfügt. Es wandelt Ihre Stimme in präzise Aktionen und Texte um und ist durch ein steckbares Regelsystem und eine dynamische Skript-Engine für die ultimative Anpassung konzipiert.
  
Übersetzungen: Dieses Dokument existiert auch in [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Hinweis: Bei vielen Texten handelt es sich um maschinell erstellte Übersetzungen der englischen Originaldokumentation, die lediglich der allgemeinen Orientierung dienen. Im Falle von Unstimmigkeiten oder Unklarheiten ist stets die englische Version maßgebend. Wir freuen uns über die Hilfe der Community, um diese Übersetzung zu verbessern!

</details>

<Details>
<summary>Demo</summary>

### 📺 Terminal-Demo

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Tipp:** Für ein besseres Terminalerlebnis siehe [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-delang.md).

### 🎥 Video-Tutorial
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternativer Link: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<Details>
<summary>Hauptfunktionen</summary>

## Hauptmerkmale

* **Offline und privat:** 100 % lokal. Keine Daten verlassen jemals Ihren Computer.
* **Dynamic Scripting Engine:** Gehen Sie über das Ersetzen von Text hinaus. Regeln können benutzerdefinierte Python-Skripte („on_match_exec“) ausführen, um erweiterte Aktionen wie das Aufrufen von APIs (z. B. Wikipedia durchsuchen), die Interaktion mit Dateien (z. B. eine Aufgabenliste verwalten) oder das Generieren dynamischer Inhalte (z. B. eine kontextbezogene E-Mail-Begrüßung) durchzuführen.
* **Kontextsensitive Regeln:** Regeln auf bestimmte Anwendungen beschränken. Mit „only_in_windows“ können Sie sicherstellen, dass eine Regel nur dann ausgelöst wird, wenn ein bestimmter Fenstertitel (z. B. „Terminal“, „VS-Code“ oder „Browser“) aktiv ist. Dies funktioniert plattformübergreifend (Linux, Windows, macOS).
* **High-Control Transformation Engine:** Implementiert eine konfigurationsgesteuerte, hochgradig anpassbare Verarbeitungspipeline. Regelpriorität, Befehlserkennung und Texttransformationen werden ausschließlich durch die Reihenfolge der Regeln in den Fuzzy Maps bestimmt und erfordern **Konfiguration, keine Codierung**.
* **Konservative RAM-Nutzung:** Verwaltet den Speicher intelligent und lädt Modelle nur dann vor, wenn genügend freier RAM verfügbar ist, sodass andere Anwendungen (z. B. Ihre PC-Spiele) immer Vorrang haben.
* **Plattformübergreifend:** Funktioniert unter Linux, macOS und Windows.
* **Vollautomatisch:** Verwaltet seinen eigenen LanguageTool-Server (Sie können aber auch einen externen verwenden).
* **Blitzschnell:** Intelligentes Caching sorgt für sofortige „Listening…“-Benachrichtigungen und schnelle Verarbeitung.
* **Dynamisches Zustandsmanagement über Trino:** Schnittstellenbewusste Konfigurations-Engine
trennt die Einstellungen für „Sprache“, „Terminal“ und „Web“ – ändern Sie eine ohne
die anderen beeinflussen. Enthält ein Echtzeit-Admin-Dashboard (Port 8084).
</details>

<Details>
<summary> 🔌 Einsatzbereite Integrationen</summary>
  
## 🔌 Gebrauchsfertige Integrationen

SL5-Aura verfügt über ein riesiges Ökosystem von über **100+ vorkonfigurierten Plugins**. Hier einige Highlights:

### OculiX / SikuliX IDE-Sprachsteuerung
SL5-Aura bietet erstklassige Sprachunterstützung für **OculiX** und **SikuliX IDE**. Diese Integration ermöglicht es Ihnen, Ihren Automatisierungscode zu „sprechen“.

* **Voice-to-Snippet:** Sagen Sie „Klick“, „Warten“ oder „Alle finden“, und der Dienst gibt sofort den richtigen Python-Code (z. B. „click("image.png")`) in die IDE ein.
* **Window-Aware:** Das Plugin ist kontextsensitiv; Es wird nur aktiviert, wenn das OculiX/SikuliX-Fenster fokussiert ist.
* **Intelligente Englischunterstützung:** Optimiert für „en-US“ mit besonderem Fokus auf nicht-muttersprachliche Akzente (z. B. Deutsch-Englisch-Phonetik), um eine hohe Erkennungsgenauigkeit für die globale Community zu gewährleisten.
* **Erweiterbar:** Verwendet das einfach zu bearbeitende Format „FUZZY_MAP_pre.py“.

> **Status:** Vom OculiX-Team als Community-Plugin anerkannt (siehe [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### LibreOffice IDE-Sprachsteuerung

### 0 n. Chr. Sprachsteuerung

---

</details>


<Details>
<summary>Dokumentation</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## Dokumentation

Eine vollständige technische Referenz, einschließlich aller Module und Skripte, finden Sie auf unserer offiziellen Dokumentationsseite. Es wird automatisch generiert und ist immer aktuell.

👉[**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### Feature-Spotlights
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-delang.md) – Doppelfenster-„fzf“-Regelsuche, Live-Kontextvorschau, sofortige Befehlsausführung über „Enter“/„Strg+R“ und Editor-Integration über „Strg+E“. Unterstützt durch einen globalen Hotkey („Super+S“) und mehrere dedizierte Suchumgebungen, die über Sprachbefehle vorkonfiguriert sind.

### Build-Status
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/29xiwIW1ZHQ )
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

👉 **Lesen Sie dies in anderen Sprachen:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-delang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang.md) | [🇪🇸 Español](../README.i18n/README-eslang-delang.md) | [🇫🇷 Français](../README.i18n/README-frlang-delang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-delang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-delang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-delang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-delang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-delang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-delang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-delang.md)

---

<Details>
<summary>Installation</summary>

## Installation

### 🎥 Schnelle Installation ohne Moderation (Manjaro/Arch Video)
Sehen Sie sich den gesamten 6-minütigen Einrichtungsprozess an:
* **Download:** ~3 Minuten
* **Einrichtung und erster Start:** ~3 Minuten (einschließlich Willkommensassistent)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


Die Einrichtung ist ein zweistufiger Prozess:
1. Laden Sie die neueste Version oder den neuesten Master herunter (https://github.com/sl5net/SL5-aura-service/archive/master.zip) oder klonen Sie dieses Repository auf Ihren Computer.
2. Führen Sie das einmalige Setup-Skript für Ihr Betriebssystem aus.

Die Setup-Skripte kümmern sich um alles: Systemabhängigkeiten, Python-Umgebung und das Herunterladen der erforderlichen Modelle und Tools (~4 GB) direkt von unseren GitHub-Releases für maximale Geschwindigkeit.


#### Für Linux, macOS und Windows (mit optionalem Sprachausschluss)

Um Speicherplatz und Bandbreite zu sparen, können Sie beim Setup bestimmte Sprachmodelle („de“, „en“) oder alle optionalen Modelle („all“) ausschließen. **Kernkomponenten (LanguageTool, lid.176) sind immer enthalten.**

Öffnen Sie ein Terminal im Stammverzeichnis des Projekts und führen Sie das Skript für Ihr System aus:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

`sudo pacman -S mimalloc`


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

#### Für Windows
Führen Sie das Setup-Skript mit Administratorrechten aus.

**Installieren Sie ein Tool zum Lesen und Ausführen, z. B. [CopyQ](https://github.com/hluk/CopyQ) oder [AutoHotkey v2](https://www.autohotkey.com/)**. Dies ist für den Texteingabe-Watcher erforderlich.

Die Installation erfolgt vollständig automatisiert und dauert etwa **8–10 Minuten**, wenn 2 Modelle auf einem neuen System verwendet werden.

1. Navigieren Sie zum Ordner „Setup“.
2. Doppelklicken Sie auf **`windows11_setup_with_ahk_copyq.bat`**.
* *Das Skript fordert automatisch zur Eingabe von Administratorrechten auf.*
* *Es installiert das Kernsystem, Sprachmodelle, **AutoHotkey v2** und **CopyQ**.*
3. Sobald die Installation abgeschlossen ist, wird **Aura Dictation** automatisch gestartet.

> **Hinweis:** Sie müssen Python oder Git nicht vorher installieren; Das Skript kümmert sich um alles.

---

#### Erweiterte / benutzerdefinierte Installation
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


<Details>
<summary>Nutzung</summary>

## Nutzung

### 1. Starten Sie die Dienste

#### Unter Linux und macOS
Ein einziges Skript erledigt alles. Es startet den Haupt-Diktierdienst und den Datei-Watcher automatisch im Hintergrund.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### Unter Windows
Das Starten des Dienstes ist ein **zweistufiger manueller Prozess**:

1. **Starten Sie den Hauptdienst:** Führen Sie „start_aura.bat“ aus. oder starten Sie von „.venv“ aus den Dienst mit „python3“.

### 2. Konfigurieren Sie Ihren Hotkey

Um das Diktat auszulösen, benötigen Sie einen globalen Hotkey, der eine bestimmte Datei erstellt. Wir empfehlen dringend das plattformübergreifende Tool [CopyQ](https://github.com/hluk/CopyQ).

#### Unsere Empfehlung: CopyQ

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
```


### 3. Beginnen Sie mit dem Diktieren!
Klicken Sie in ein beliebiges Textfeld, drücken Sie Ihren Hotkey und die Benachrichtigung „Zuhören…“ wird angezeigt. Sprechen Sie deutlich und machen Sie dann eine Pause. Der korrigierte Text wird für Sie getippt.

</details>

---


<Details>
<summary>Erweiterte Konfiguration (optional)</summary>

## Erweiterte Konfiguration (optional)

Sie können das Verhalten der Anwendung anpassen, indem Sie eine lokale Einstellungsdatei erstellen.

1. Navigieren Sie zum Verzeichnis „config/“.
2. Erstellen Sie eine Kopie von „config/settings_local.py_Example.txt“ und benennen Sie sie in „config/settings_local.py“ um.
3. Bearbeiten Sie „config/settings_local.py“ (es überschreibt alle Einstellungen aus der Hauptdatei „config/settings.py“).

Diese Datei „config/settings_local.py“ wird von Git standardmäßig ignoriert, sodass Ihre persönlichen Änderungen nicht durch Updates überschrieben werden.

### Plug-in-Struktur und Logik

Die Modularität des Systems ermöglicht eine robuste Erweiterung über das Plugins/-Verzeichnis.

Die Verarbeitungs-Engine hält sich strikt an eine **hierarchische Prioritätskette**:

1. **Ladereihenfolge der Module (hohe Priorität):** Regeln, die aus Kernsprachpaketen (de-DE, en-US) geladen werden, haben Vorrang vor Regeln, die aus dem Verzeichnis „plugins/“ geladen werden (die alphabetisch zuletzt geladen werden).
  
2. **Reihenfolge in der Datei (Mikropriorität):** Innerhalb einer bestimmten Kartendatei (FUZZY_MAP_pre.py) werden Regeln streng nach **Zeilennummer** (von oben nach unten) verarbeitet.


Diese Architektur stellt sicher, dass Kernsystemregeln geschützt sind, während projektspezifische oder kontextbezogene Regeln (wie die für CodeIgniter oder Spielsteuerungen) einfach über Plug-Ins als Erweiterungen mit niedriger Priorität hinzugefügt werden können.



<Details>
<summary>Schlüsselskripts für Windows-Benutzer</summary>








Hier finden Sie eine Liste der wichtigsten Skripte zum Einrichten, Aktualisieren und Ausführen der Anwendung auf einem Windows-System.





*






























































































https://translate.google.com/translate?hl=en&sl=en&tl=de&u=https://glogg.bonnefon.org/     