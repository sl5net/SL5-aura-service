# Systemweites Diktier-Tool mit Vosk für Manjaro Linux

Dieses Projekt implementiert eine leistungsstarke, systemweite Diktierfunktion für Manjaro Linux (und andere Linux-Distributionen mit geringfügigen Anpassungen). Nach der Einrichtung können Sie in jedem beliebigen Textfeld (Browser, Editor, Chat etc.) eine Tastenkombination (Hotkey) drücken, um sofort mit dem Diktieren zu beginnen. Der gesprochene Text wird automatisch eingefügt.

Das System ist so konzipiert, dass es eine hohe Genauigkeit (durch große Sprachmodelle) mit einer sofortigen Reaktionszeit (durch eine Hintergrund-Dienst-Architektur) kombiniert.

## Features

*   **Systemweit:** Funktioniert in jeder Anwendung, die Texteingaben akzeptiert.
*   **Hohe Genauigkeit:** Verwendet große, präzise Offline-Sprachmodelle von Vosk.
*   **Schnelle Reaktion:** Dank eines permanenten Hintergrund-Dienstes gibt es keine Ladeverzögerung beim Aktivieren des Hotkeys.
*   **Offline & Privat:** Die gesamte Spracherkennung findet lokal auf Ihrem Computer statt. Es werden keine Daten an die Cloud gesendet.
*   **Anpassbar:** Leicht auf andere Sprachen (z.B. Englisch) umstellbar durch Austausch des Vosk-Modells.
*   **Open Source:** Basiert ausschließlich auf freien und quelloffenen Werkzeugen.

---

## Installationsanleitung

Diese Anleitung führt Sie Schritt für Schritt durch die gesamte Einrichtung.

### Schritt 1: Systemabhängigkeiten installieren

Zuerst installieren wir alle notwendigen Programme und Bibliotheken über den Manjaro-Paketmanager `pacman`.

Öffnen Sie ein Terminal und führen Sie den folgenden Befehl aus:

```bash
sudo pacman -Syu python git portaudio ffmpeg xclip xdotool libnotify autokey unzip
```

*   `python`: Die Programmiersprache, die wir verwenden.
*   `git`: Zur Verwaltung von Quellcode (Best Practice).
*   `portaudio`: Eine Audio-Bibliothek, die von `sounddevice` benötigt wird.
*   `ffmpeg`: Zum Konvertieren von Audioformaten (optional, aber nützlich).
*   `xclip`, `xdotool`: Werkzeuge zur Steuerung von Maus, Tastatur und Zwischenablage.
*   `libnotify`: Ermöglicht das Senden von Desktop-Benachrichtigungen.
*   `autokey`: Die Automatisierungssoftware für unseren Hotkey.
*   `unzip`: Zum Entpacken der Sprachmodelle.

### Schritt 2: Projektverzeichnis einrichten

Wir erstellen ein Verzeichnis für unser Projekt.

```bash
# Erstellen Sie das Verzeichnis und wechseln Sie hinein
mkdir -p ~/projects/py/STT
cd ~/projects/py/STT
```

### Schritt 3: Python Virtuelle Umgebung erstellen

Eine virtuelle Umgebung ist entscheidend, um die Python-Pakete für dieses Projekt von Ihrem System zu isolieren.

```bash
# Erstellen Sie die virtuelle Umgebung namens ".venv"
python -m venv .venv

# Aktivieren Sie die Umgebung. Dies müssen Sie immer tun, wenn Sie an diesem Projekt arbeiten.
source .venv/bin/activate
```
Nach der Aktivierung sollte Ihr Terminal-Prompt `(.venv)` anzeigen.

### Schritt 4: Python-Pakete installieren

Installieren Sie nun die benötigten Python-Bibliotheken mit `pip`.

```bash
pip install vosk sounddevice pyperclip
```

### Schritt 5: Vosk-Sprachmodell herunterladen

Für eine hohe Genauigkeit in Deutsch verwenden wir das Modell `vosk-model-de-0.21`.

```bash
# Laden Sie das Modell herunter (1.9 GB)
wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip

# Entpacken Sie das Modell
unzip vosk-model-de-0.21.zip
```
Nach dem Entpacken haben Sie einen Ordner namens `vosk-model-de-0.21` in Ihrem Projektverzeichnis.

---

## Konfiguration

Das System besteht aus zwei Skripten: dem Hintergrund-Dienst und dem AutoKey-Trigger.

### Teil A: Das Hintergrund-Dienst-Skript

Dieses Skript läuft permanent, hält das Sprachmodell im Speicher und wartet auf ein Signal vom Hotkey.

    ```bash
    nano dictation_service.py
    ```

### Teil B 1 : AutoKey ist nicht nötig für den Hotkey 

    
i got this to work thank you! i'm using it right now!

i suggest the that you mention in the docs that auto key isn't needed. A person can set up a hot key in whatever operating system or desktop they're using. i first tried installing auto key with yay and it had to install about seven or eight dependencies so i prefer not to use it and i have removed it.

In xfce, I've added control alt V as the hot key


### Teil B 2 : AutoKey für den Hotkey konfigurieren

1.  Starten Sie **AutoKey** aus Ihrem Anwendungsmenü.
2.  Klicken Sie auf **File -> New -> Script**.
3.  Geben Sie dem Skript einen Namen, z.B. `Vosk Trigger`.
4.  Löschen Sie den gesamten Beispiel-Code im rechten Fenster.
5.  Fügen Sie diese **eine Zeile** Code ein:
    ```python
    system.exec_command('touch /tmp/vosk_trigger')
    ```
6.  Klicken Sie oben auf den Button **"Set"** neben "Hotkey".
7.  Drücken Sie die gewünschte Tastenkombination, z.B. **`Ctrl` + `Alt` + `D`**. Klicken Sie OK.
8.  Klicken Sie auf das **Speichern-Symbol** (Diskette), um das Skript zu sichern.

---

## Benutzung

1.  **Dienst starten (einmal pro Computersitzung):**
    Öffnen Sie ein Terminal und führen Sie aus:
    ```bash
    cd ~/projects/py/STT
    source .venv/bin/activate
    python dictation_service.py
    ```
    **WICHTIG:** Lassen Sie dieses Terminalfenster geöffnet! Solange es offen ist, läuft Ihr Diktier-Dienst.

2.  **Diktieren:**
    *   Klicken Sie in ein beliebiges Textfeld in einer beliebigen Anwendung.
    *   Drücken Sie Ihren Hotkey (`Ctrl+Alt+D`).
    *   Eine Benachrichtigung "Vosk Hört zu..." erscheint sofort.
    *   Sprechen Sie einen Satz. Machen Sie eine kurze Pause, wenn Sie fertig sind.
    *   Der erkannte Text wird automatisch an der Cursor-Position eingefügt.

---

## Optional: Dienst automatisch starten

Damit Sie den Dienst nicht jedes Mal manuell starten müssen, können Sie ihn zum Autostart hinzufügen.

1.  Suchen Sie in Ihrem Anwendungsmenü nach "Sitzung und Startverhalten" (Session and Startup).
2.  Gehen Sie zum Reiter "Anwendungs-Autostart".
3.  Klicken Sie auf "Hinzufügen".
4.  Füllen Sie die Felder aus:
    *   **Name:** `Vosk Diktier-Dienst`
    *   **Beschreibung:** `Startet den Hintergrunddienst für die Spracherkennung`
    *   **Befehl:** Kopieren Sie hier den **vollständigen Pfad** zum Skript. Ersetzen Sie `<DEIN_BENUTZERNAME>` durch Ihren tatsächlichen Benutzernamen.
        ```
        /home/<DEIN_BENUTZERNAME>/projects/py/STT/.venv/bin/python /home/<DEIN_BENUTZERNAME>/projects/py/STT/dictation_service.py
        ```
5.  Klicken Sie auf OK. Beim nächsten Anmelden startet der Dienst automatisch im Hintergrund.

Viel Erfolg
