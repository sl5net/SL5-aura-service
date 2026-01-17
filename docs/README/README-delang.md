# Systemweite Offline-Sprache zu Befehlen oder Text, steckbares System

**⚠️ Systemanforderungen und Kompatibilität**

* **Windows:** ✅ Vollständig unterstützt (verwendet AutoHotkey/PowerShell).
* **macOS:** ✅ Vollständig unterstützt (verwendet AppleScript).
* **Linux (X11/Xorg):** ✅ Vollständig unterstützt. Empfohlen für beste Erfahrung.
* **Linux (Wayland):** ⚠️ **Begrenzt / Experimentell.**
* *Globale Hotkeys und automatische Eingabe funktionieren aus Sicherheitsgründen im Allgemeinen nicht auf Wayland.*
* *Bitte wechseln Sie beim Anmelden zu einer **X11-Sitzung** (z. B. „Plasma (X11)“ oder „Ubuntu auf Xorg“), um alle Funktionen nutzen zu können.*


Willkommen beim SL5 Aura Service! Dieses Dokument bietet einen schnellen Überblick über unsere wichtigsten Funktionen und deren Betriebssystemkompatibilität.

Aura ist nicht nur eine Transkriptorin; Es handelt sich um eine leistungsstarke Offline-Verarbeitungs-Engine, die Ihre Stimme in präzise Aktionen und Texte umwandelt.

Es handelt sich um einen vollständigen **Offline-Sprachassistenten**, der auf **Vosk** (für Speech-to-Text) und **LanguageTool** (für Grammatik/Stil) basiert und jetzt über einen optionalen **Local LLM (Ollama) Fallback** für kreative Antworten und erweitertes Fuzzy-Matching verfügt. Es ist für die ultimative Anpassung durch ein steckbares Regelsystem und eine dynamische Skript-Engine konzipiert.

  
Übersetzungen: Dieses Dokument existiert auch in [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs).

Hinweis: Bei vielen Texten handelt es sich um maschinell erstellte Übersetzungen der englischen Originaldokumentation, die lediglich der allgemeinen Orientierung dienen. Im Falle von Unstimmigkeiten oder Unklarheiten ist stets die englische Version maßgebend. Wir freuen uns über die Hilfe der Community, um diese Übersetzung zu verbessern!

___

[![SL5 Aura (v0.16.1): HowTo crash SL5 Aura? -  seeh Hierarchical and Recursive Rule Engine](https://img.youtube.com/vi/d98ml86u68g/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)
(https://www.youtube.com/watch?v=BZCHonTqwUw oder https://skipvids.com/?v=BZCHonTqwUw)

## Hauptmerkmale

* **Offline und privat:** 100 % lokal. Keine Daten verlassen jemals Ihren Computer.
* **Dynamic Scripting Engine:** Gehen Sie über das Ersetzen von Text hinaus. Regeln können benutzerdefinierte Python-Skripte („on_match_exec“) ausführen, um erweiterte Aktionen wie das Aufrufen von APIs (z. B. Wikipedia durchsuchen), die Interaktion mit Dateien (z. B. das Verwalten einer Aufgabenliste) oder das Generieren dynamischer Inhalte (z. B. eine kontextbezogene E-Mail-Begrüßung) durchzuführen.
* **High-Control Transformation Engine:** Implementiert eine konfigurationsgesteuerte, hochgradig anpassbare Verarbeitungspipeline. Regelpriorität, Befehlserkennung und Texttransformationen werden ausschließlich durch die Reihenfolge der Regeln in den Fuzzy Maps bestimmt und erfordern **Konfiguration, keine Codierung**.
* **Konservative RAM-Nutzung:** Verwaltet den Speicher intelligent und lädt Modelle nur dann vor, wenn genügend freier RAM verfügbar ist, um sicherzustellen, dass andere Anwendungen (wie Ihre PC-Spiele) immer Vorrang haben.
* **Plattformübergreifend:** Funktioniert unter Linux, macOS und Windows.
* **Vollautomatisch:** Verwaltet seinen eigenen LanguageTool-Server (Sie können aber auch einen externen verwenden).
* **Blitzschnell:** Intelligentes Caching sorgt für sofortige „Listening…“-Benachrichtigungen und schnelle Verarbeitung.

## Dokumentation

Eine vollständige technische Referenz, einschließlich aller Module und Skripte, finden Sie auf unserer offiziellen Dokumentationsseite. Es wird automatisch generiert und ist immer aktuell.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### Build-Status
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**Lesen Sie dies in anderen Sprachen:**

[🇬🇧 English](README.md) | [🇸🇦 العربية](./README-arlang.md) | [🇩🇪 Deutsch](./README-delang.md) | [🇪🇸 Español](./README-eslang.md) | [🇫🇷 Français](./README-frlang.md) | [🇮🇳 हिन्दी](./README-hilang.md) | [🇯🇵 日本語](./README-jalang.md) | [🇰🇷 한국어](./README-kolang.md) | [🇵🇱 Polski](./README-pllang.md) | [🇵🇹 Português](./README-ptlang.md) | [🇧🇷 Português Brasil](./README-pt-BRlang.md) | [🇨🇳 简体中文](./README-zh-CNlang.md)

---







## Installation

Die Einrichtung ist ein zweistufiger Prozess:
1. Laden Sie die letzte Version oder den Master herunter (https://github.com/sl5net/Vosk-System-Listener/archive/master.zip) oder klonen Sie dieses Repository auf Ihren Computer.
2. Führen Sie das einmalige Setup-Skript für Ihr Betriebssystem aus.

Die Setup-Skripte kümmern sich um alles: Systemabhängigkeiten, Python-Umgebung und das Herunterladen der erforderlichen Modelle und Tools (~4 GB) direkt von unseren GitHub-Releases für maximale Geschwindigkeit.


#### Für Linux, macOS und Windows (mit optionalem Sprachausschluss)

Um Speicherplatz und Bandbreite zu sparen, können Sie beim Setup bestimmte Sprachmodelle („de“, „en“) oder alle optionalen Modelle („all“) ausschließen. **Kernkomponenten (LanguageTool, lid.176) sind immer enthalten.**

Öffnen Sie ein Terminal im Stammverzeichnis des Projekts und führen Sie das Skript für Ihr System aus:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

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

# Or (recommend) - Start des BAT: 
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
setup\windows11_setup.bat

# Exclude specific language models (saves space):
# Exclude English:
setup\windows11_setup.bat -Exclude "en"

# Exclude German and English:
setup\windows11_setup.bat -Exclude "de,en"
```


---

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

1. **Starten Sie den Hauptdienst:** Führen Sie „start_dictation_v2.0.bat“ aus. oder starten Sie von „.venv“ aus den Dienst mit „python3“.

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

---


## Erweiterte Konfiguration (optional)

Sie können das Verhalten der Anwendung anpassen, indem Sie eine lokale Einstellungsdatei erstellen.

1. Navigieren Sie zum Verzeichnis „config/“.
2. Erstellen Sie eine Kopie von „config/settings_local.py_Example.txt“ und benennen Sie sie in „config/settings_local.py“ um.
3. Bearbeiten Sie „config/settings_local.py“ (es überschreibt alle Einstellungen aus der Hauptdatei „config/settings.py“).

Diese Datei „config/settings_local.py“ wird (möglicherweise) von Git ignoriert, sodass Ihre persönlichen Änderungen (möglicherweise) nicht durch Updates überschrieben werden.

### Plug-in-Struktur und Logik

Die Modularität des Systems ermöglicht eine robuste Erweiterung über das Plugins/-Verzeichnis.

Die Verarbeitungs-Engine hält sich strikt an eine **hierarchische Prioritätskette**:

1. **Ladereihenfolge der Module (hohe Priorität):** Regeln, die aus Kernsprachpaketen (de-DE, en-US) geladen werden, haben Vorrang vor Regeln, die aus dem Verzeichnis „plugins/“ geladen werden (die in alphabetischer Reihenfolge zuletzt geladen werden).
  
2. **Reihenfolge in der Datei (Mikropriorität):** Innerhalb einer bestimmten Kartendatei (FUZZY_MAP_pre.py) werden Regeln streng nach **Zeilennummer** (von oben nach unten) verarbeitet.
  

Diese Architektur stellt sicher, dass Kernsystemregeln geschützt sind, während projektspezifische oder kontextbezogene Regeln (wie die für CodeIgniter oder Spielsteuerungen) einfach über Plug-Ins als Erweiterungen mit niedriger Priorität hinzugefügt werden können.
## Wichtige Skripte für Windows-Benutzer

Hier finden Sie eine Liste der wichtigsten Skripte zum Einrichten, Aktualisieren und Ausführen der Anwendung auf einem Windows-System.

### Einrichtung und Aktualisierung
* „setup/setup.bat“: Das Hauptskript für die **erste einmalige Einrichtung** der Umgebung.
*

* `update.bat`: Durchsuchen Sie diese aus dem Projektordner **holen Sie sich den neuesten Code und die neuesten Abhängigkeiten**.

### Ausführen der Anwendung
* „start_dictation_v2.0.bat“: Ein primäres Skript zum **Starten des Diktierdienstes**.

### Kern- und Hilfsskripte
* „aura_engine.py“: Der Kern-Python-Dienst (normalerweise von einem der oben genannten Skripte gestartet).
* „get_suggestions.py“: Ein Hilfsskript für bestimmte Funktionen.




## 🚀 Hauptfunktionen und Betriebssystemkompatibilität

Legende zur Betriebssystemkompatibilität:  
* 🐧 **Linux** (z. B. Arch, Ubuntu)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (für mobilspezifische Funktionen)  

---

### **Kern-Speech-to-Text-Engine (Aura)**
Unsere primäre Engine für Offline-Spracherkennung und Audioverarbeitung.

  
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Haupt-Python-Dienst, der Aura orchestriert) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Konfiguration & Karten) 🐧 🍏 🪟  
│├ **Sicheres Laden privater Karten (Integrity-First)** 🔒 🐧 🍏 🪟  
││ * **Workflow:** Lädt passwortgeschützte ZIP-Archive.   
│├ **Textverarbeitung und -korrektur/** Gruppiert nach Sprache (z. B. „de-DE“, „en-US“, ...)   
│├ 1. `normalize_punctuation.py` (Standardisiert die Zeichensetzung nach der Transkription) 🐧 🍏 🪟  
│├ 2. **Intelligente Vorkorrektur** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules-delang.md)) 🐧 🍏 🪟  
││ * **Dynamische Skriptausführung:** Regeln können benutzerdefinierte Python-Skripte (on_match_exec) auslösen, um erweiterte Aktionen wie API-Aufrufe, Datei-E/A auszuführen oder dynamische Antworten zu generieren.  
││ * **Kaskadierende Ausführung:** Regeln werden nacheinander verarbeitet und ihre Auswirkungen sind **kumulativ**. Spätere Regeln gelten für Text, der durch frühere Regeln geändert wurde.  
││ * **Stoppkriterium mit höchster Priorität:** Wenn eine Regel eine **Vollständige Übereinstimmung** (^...$) erreicht, stoppt die gesamte Verarbeitungspipeline für dieses Token sofort. Dieser Mechanismus ist für die Implementierung zuverlässiger Sprachbefehle von entscheidender Bedeutung.  
│├ 3. `correct_text_by_lingualtool.py` (Integriert LanguageTool zur Grammatik-/Stilkorrektur) 🐧 🍏 🪟  
│├ **4. Hierarchische RegEx-Regel-Engine mit Ollama AI Fallback** 🐧 🍏 🪟  
││ * **Deterministische Steuerung:** Verwendet RegEx-Rule-Engine für präzise Befehls- und Textsteuerung mit hoher Priorität.  
││ * **Ollama AI (Local LLM) Fallback:** Dient als optionale Prüfung mit niedriger Priorität für **kreative Antworten, Fragen und Antworten und erweitertes Fuzzy-Matching**, wenn keine deterministische Regel erfüllt ist.  
││ * **Status:** Lokale LLM-Integration.
│└ 5. **Intelligente Nachkorrektur** („FuzzyMap“)** – Post-LT-Verfeinerung** 🐧 🍏 🪟
││ * Wird nach LanguageTool angewendet, um LT-spezifische Ausgaben zu korrigieren. Folgt der gleichen strengen kaskadierenden Prioritätslogik wie die Vorkorrekturschicht.  
││ * **Dynamische Skriptausführung:** Regeln können benutzerdefinierte Python-Skripte ([on_match_exec](docs/advanced-scripting-delang.md)) auslösen, um erweiterte Aktionen wie API-Aufrufe, Datei-E/A auszuführen oder dynamische Antworten zu generieren.  
││ * **Fuzzy-Fallback:** Die **Fuzzy-Ähnlichkeitsprüfung** (gesteuert durch einen Schwellenwert, z. B. 85 %) fungiert als Fehlerkorrekturebene mit der niedrigsten Priorität. Es wird nur ausgeführt, wenn bei der gesamten vorherigen Ausführung der deterministischen/kaskadierenden Regel keine Übereinstimmung gefunden werden konnte (current_rule_matched ist False). Dadurch wird die Leistung optimiert, indem nach Möglichkeit langsame Fuzzy-Prüfungen vermieden werden.  
├┬ **Modellverwaltung/**   
│├─ `prioritize_model.py` (Optimiert das Laden/Entladen von Modellen basierend auf der Nutzung) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Konfiguriert die erstmalige Modelleinrichtung) 🐧 🍏 🪟  
├─ **Adaptives VAD-Timeout** 🐧 🍏 🪟  
├─ **Adaptiver Hotkey (Start/Stopp)** 🐧 🍏 🪟  
└─ **Sofortige Sprachumschaltung** (Experimentell über Modell-Vorladen) 🐧 🍏   

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_lingualtool_server.py` (Initialisiert den lokalen LanguageTool-Server) 🐧 🍏 🪟  
│└─ `stop_lingualtool_server.py` (fährt den LanguageTool-Server herunter) 🐧 🍏
├─ `monitor_mic.sh` (z. B. zur Verwendung mit Headset ohne Verwendung von Tastatur und Monitor) 🐧 🍏 🪟  

### **Modell- und Paketverwaltung**  
Tools für den robusten Umgang mit großen Sprachmodellen.  

**ModelManagement/** 🐧 🍏 🪟  
├─ **Robust Model Downloader** (GitHub-Release-Chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Dienstprogramm für Repo-Besitzer zum Teilen großer Dateien und Generieren von Prüfsummen) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool für Endbenutzer zum Herunterladen, Überprüfen und erneuten Zusammensetzen mehrteiliger Dateien) 🐧 🍏 🪟  


### **Entwicklungs- und Bereitstellungshelfer**  
Skripte zum Einrichten, Testen und Ausführen von Diensten.  

*Tipp: Mit glogg können Sie reguläre Ausdrücke verwenden, um in Ihren Protokolldateien nach interessanten Ereignissen zu suchen.*   
Bitte aktivieren Sie das Kontrollkästchen bei der Installation, um eine Verknüpfung mit Protokolldateien herzustellen.    
https://translate.google.com/translate?hl=en&sl=en&tl=de&u=https://glogg.bonnefon.org/     
  
*Tipp: Nachdem Sie Ihre Regex-Muster definiert haben, führen Sie „python3 tools/map_tagger.py“ aus, um automatisch durchsuchbare Beispiele für die CLI-Tools zu generieren. Weitere Informationen finden Sie unter [Map Maintenance Tools](docs/Developer_Guide/Map_Maintenance_Tools-delang.md).*

Dann vielleicht Double Click
`log/aura_engine.log`
  
  
**DevHelpers/**  
├┬ **Virtuelle Umgebungsverwaltung/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Systemweite Diktierintegration/**  
│├ Vosk-System-Listener-Integration 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux-spezifische Mikrofonüberwachung) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey wartet auf erkannten Text und gibt ihn systemweit ein) 🪟  
└─ **CI/CD-Automatisierung/**  
└─ Erweiterte GitHub-Workflows (Installation, Tests, Bereitstellung von Dokumenten) 🐧 🍏 🪟 *(Läuft auf GitHub-Aktionen)*  

### **Kommende/experimentelle Funktionen**  
Funktionen, die sich derzeit in der Entwicklung oder im Entwurfsstatus befinden.  

**Experimentelle Funktionen/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Beispiel-Aktivierungsregel „(ExampleAplicationThatNotExist|Pi, Ihre persönliche KI)“ 🐧  
├┬Plugins  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Änderungen an der Plugin-Aktivierung/Deaktivierung und deren Konfigurationen werden beim nächsten Verarbeitungslauf ohne Neustart des Dienstes übernommen.*)  
│ ├ **Git-Befehle** (Sprachsteuerung zum Senden von Git-Befehlen) 🐧 🍏 🪟  
│ ├ **wannweil** (Karte für Standort Deutschland-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker-Plugin (Entwurf)** (Sprachsteuerung für Pokeranwendungen) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Entwurf)** (Sprachsteuerung für 0 A.D.-Spiel) 🐧   
├─ **Tonausgabe beim Starten oder Beenden einer Sitzung** (Beschreibung steht noch aus) 🐧   
├─ **Sprachausgabe für Sehbehinderte** (Beschreibung steht noch aus) 🐧 🍏 🪟  
└─ **SL5 Aura Android Prototyp** (Noch nicht vollständig offline) 📱  

---

*(Hinweis: Bestimmte Linux-Distributionen wie Arch (ARL) oder Ubuntu (UBT) werden durch das allgemeine Linux-Symbol 🐧 abgedeckt. Detaillierte Unterscheidungen werden möglicherweise in Installationshandbüchern behandelt.)*









<Details>
<summary>Klicken Sie hier, um den Befehl anzuzeigen, der zum Generieren dieser Skriptliste verwendet wurde</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>


### Schauen Sie sich etwas grafisch an, um zu sehen, was sich dahinter verbirgt:

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# Gebrauchte Modelle:

Empfehlung: Modelle von Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 verwenden (wahrscheinlich schneller)

Diese komprimierten Modelle müssen im Ordner „models/“ gespeichert werden

`mv vosk-model-*.zip models/`


| Modell | Größe | Wortfehlerrate/Geschwindigkeit | Notizen | Lizenz |
| -------------------------------------------------------------------------------------- | ---- | ----------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5,69 (Librispeech Test-Clean)<br/>6,05 (Tedlium)<br/>29,78 (Callcenter) | Präzises generisches US-englisches Modell | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9,83 (Tuda-de-Test)<br/>24,00 (Podcast)<br/>12,82 (CV-Test)<br/>12,42 (mls)<br/>33,26 (mtedx) | Großes deutsches Modell für Telefonie und Server | Apache 2.0 |

Diese Tabelle bietet einen Überblick über verschiedene Vosk-Modelle, einschließlich ihrer Größe, Wortfehlerrate oder -geschwindigkeit, Anmerkungen und Lizenzinformationen.


- **Vosk-Modelle:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**Lizenz von LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Unterstützen Sie das Projekt
Wenn Sie dieses Tool nützlich finden, denken Sie bitte darüber nach, uns einen Kaffee zu spenden! Ihre Unterstützung trägt dazu bei, zukünftige Verbesserungen voranzutreiben.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)



IgnorePkg = linux66-nvidia-575xx nvidia-575xx-utils lib32-nvidia-575xx-utils

nvidia-575xx-settings mhwd-nvidia-575xx