# 1-Klick-Installer (Zero-Setup)

Bringen Sie **Aura** mit einem einzigen Klick auf Ihrem Computer zum Laufen. Keine Programmierkenntnisse, Terminalbefehle oder manuelle Python-Einrichtung erforderlich.

---

## Null Voraussetzungen

Sie brauchen **nicht**:
- Python vorinstalliert
- Git- oder Code-Repositorys
- Erfahrung mit der Befehlszeile oder dem Terminal

---

## Schnellstart

### Methode 1: Web One-Liner (am schnellsten und empfohlen für Linux/MacOS)
Spart ca. 30 Sekunden manuelle Dateiverwaltung und startet sofort in Ihrem Terminal:

**Linux und macOS:**
#### Web One-Liner CodeBerg
```bash
curl -sSL https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
oder
#### Web One-Liner GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Web One-Liner CodeBerg
# nicht getestet – bitte verwenden Sie Methode 2 (eigenständige Binärdatei) für Windows
```bash
irm https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
oder
#### Web One-Liner Github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Methode 2: Eigenständige Binärdatei (Windows- und Desktop-Klick)

### 2.1 Laden Sie das Installationsprogramm herunter
Laden Sie die einzelne Installationsdatei passend zu Ihrem Betriebssystem von der [neuesten GitHub-Version] herunter:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Führen Sie das Installationsprogramm aus

Benennen Sie aura-installer-windows.exe.zip in aura-installer-windows.exe um

Doppelklicken Sie auf die heruntergeladene Datei. Ein Setup-Fenster erscheint und bereitet die Umgebung automatisch vor.

### 2.3. Beginnen Sie mit dem Diktieren
Sobald der Vorgang abgeschlossen ist, erstellt Aura eine Desktop-Verknüpfung und beginnt sofort mit dem Zuhören.

---

## Was passiert automatisch?

Wenn Sie das Installationsprogramm ausführen, führt Aura automatisch Folgendes aus:
– Konfiguriert die lokale, private Spracherkennungs-Engine.
- Lädt die Standard-Sprachmodelle herunter.
- Richtet alle notwendigen Systemverknüpfungen und Desktop-Startprogramme ein.

---

## Installationsdetails und Anforderungen

- **Installationsdauer:** Ungefähr 2–3 Minuten.
- **Erforderlicher Speicherplatz:** Mindestens ~1,5 GB (bis zu 2,5 GB abhängig von den ausgewählten Sprachmodellen).
- **Installationsverzeichnis:**
- **Linux & macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Nächste Schritte

- **Oma-Modus:** Geben Sie ein einzelnes Wort in Ihre Regeldatei ein und beobachten Sie, wie Aura automatisch Regeln erstellt.
- **Lernen mit Koans:** Entdecken Sie Schritt-für-Schritt-Konzepte in [Getting Started](../GettingStarted.i18n/GettingStarted-delang.md).