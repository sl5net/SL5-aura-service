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
# Erstellen Sie die virtuelle Umgebung namens "vosk-tts"
python -m venv vosk-tts

# Aktivieren Sie die Umgebung. Dies müssen Sie immer tun, wenn Sie an diesem Projekt arbeiten.
source vosk-tts/bin/activate
```
Nach der Aktivierung sollte Ihr Terminal-Prompt `(vosk-tts)` anzeigen.

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

1.  Erstellen Sie eine neue Datei in Ihrem Projektverzeichnis:
    ```bash
    nano dictation_service.py
    ```

2.  Kopieren Sie den folgenden Code vollständig in die Datei:

    ```python
    # Datei: ~/projects/py/STT/dictation_service.py
    import vosk
    import sys
    import sounddevice as sd
    import queue
    import json
    import pyperclip
    import subprocess
    import time
    from pathlib import Path

    # --- Konfiguration ---
    SCRIPT_DIR = Path(__file__).resolve().parent
    MODEL_NAME = "vosk-model-de-0.21"
    MODEL_PATH = SCRIPT_DIR / MODEL_NAME
    TRIGGER_FILE = Path("/tmp/vosk_trigger") # Unsere "Signal"-Datei

    NOTIFY_SEND_PATH = "/usr/bin/notify-send"
    XDOTOOL_PATH = "/usr/bin/xdotool"
    SAMPLE_RATE = 16000

    # --- Hilfsfunktionen ---
    def notify(summary, body=""):
        try:
            subprocess.run([NOTIFY_SEND_PATH, summary, body, "-t", "2000"], check=True)
        except Exception:
            print(f"NOTIFY: {summary} - {body}")

    def transcribe_audio():
        q = queue.Queue()
        def audio_callback(indata, frames, time, status):
            q.put(bytes(indata))

        try:
            with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                                   dtype='int16', channels=1, callback=audio_callback):
                while True:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        break
            result = json.loads(recognizer.Result())
            return result.get('text', '')
        except Exception as e:
            print(f"Fehler bei der Transkription: {e}")
            return ""

    # --- Hauptlogik des Dienstes ---
    print("--- Vosk Diktier-Dienst ---")
    if not MODEL_PATH.exists():
        print(f"FATALER FEHLER: Modell nicht gefunden unter {MODEL_PATH}")
        sys.exit(1)

    print(f"Lade Modell '{MODEL_NAME}'... Dies kann einige Sekunden dauern.")
    try:
        model = vosk.Model(str(MODEL_PATH))
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Modell erfolgreich geladen. Dienst wartet auf Signal.")
        notify("Vosk Dienst Bereit", "Hotkey ist nun aktiv.")
    except Exception as e:
        print(f"FATALER FEHLER: Modell konnte nicht geladen werden. {e}")
        sys.exit(1)

    while True:
        try:
            if TRIGGER_FILE.exists():
                print("Signal erkannt! Starte Transkription.")
                notify("Vosk Hört zu...", "Jetzt sprechen.")
                TRIGGER_FILE.unlink()

                recognized_text = transcribe_audio()

                if recognized_text:
                    print(f"Transkribiert: '{recognized_text}'")
                    subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", recognized_text])
                    pyperclip.copy(recognized_text)
                else:
                    notify("Vosk Diktat", "Kein Text erkannt.")
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDienst durch Benutzer beendet.")
            break
        except Exception as e:
            print(f"Fehler im Haupt-Loop: {e}")
            notify("Vosk Dienst Fehler", str(e))
    ```

3.  Speichern und schließen Sie die Datei (mit `nano`: `Ctrl+X`, dann `Y`, dann `Enter`).

### Teil B: AutoKey für den Hotkey konfigurieren

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
    source vosk-tts/bin/activate
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
        /home/<DEIN_BENUTZERNAME>/projects/py/STT/vosk-tts/bin/python /home/<DEIN_BENUTZERNAME>/projects/py/STT/dictation_service.py
        ```
5.  Klicken Sie auf OK. Beim nächsten Anmelden startet der Dienst automatisch im Hintergrund.

Viel Erfolg
