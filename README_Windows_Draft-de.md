# Systemweites Diktier-Tool mit Vosk für Windows

Dieses Projekt realisiert eine leistungsstarke, systemweite Diktierfunktion für Windows. Nach der Einrichtung kannst du eine Hotkey-Tastenkombination in jedem beliebigen Textfeld (Browser, Editor, Chat usw.) drücken, um sofort mit dem Diktieren zu beginnen. Der gesprochene Text wird dann automatisch für dich hingeschrieben.

Dieses Tutorial adaptiert das ursprüngliche Linux-Konzept für Windows und verwendet dafür native Tools sowie die beliebte Automatisierungssoftware **AutoHotkey**.

## Merkmale

*   **Systemweit:** Funktioniert in jeder Anwendung, die Texteingaben akzeptiert.
*   **Hohe Genauigkeit:** Nutzt große, präzise Offline-Sprachmodelle von Vosk.
*   **Schnelle Reaktionszeit:** Dank eines persistenten Hintergrunddienstes gibt es keine Ladeverzögerung beim Aktivieren des Hotkeys.
*   **Offline & Privat:** Die gesamte Spracherkennung findet lokal auf deinem Computer statt. Es werden keine Daten in die Cloud gesendet.
*   **Anpassbar:** Wechsle einfach zu anderen Sprachen (z. B. Deutsch), indem du das Vosk-Modell austauschst.
*   **Open Source:** Basiert vollständig auf kostenlosen Open-Source-Tools.

---

## Installationsanleitung

Diese Anleitung führt dich Schritt für Schritt durch den gesamten Einrichtungsprozess.

### Schritt 1: System-Abhängigkeiten installieren

Zuerst installieren wir die notwendige Software. Es wird empfohlen, direkt von den offiziellen Webseiten zu installieren.

1.  **Python für Windows:**
    *   Gehe zur [offiziellen Python-Webseite](https://www.python.org/downloads/windows/).
    *   Lade den neuesten Python 3-Installer herunter.
    *   Führe das Installationsprogramm aus. **WICHTIG:** Im ersten Installationsbildschirm musst du unbedingt das Kästchen **"Add Python to PATH"** aktivieren. Dies ist entscheidend, damit die Befehle später funktionieren. Klicke dann auf "Install Now".

2.  **Git für Windows (Optional, aber empfohlen):**
    *   Gehe zur [Git für Windows Webseite](https://git-scm.com/download/win).
    *   Lade den Installer herunter und führe ihn aus. Die Standardeinstellungen sind in der Regel ausreichend.

3.  **AutoHotkey:**
    *   Gehe zur [offiziellen AutoHotkey Webseite](https://www.autohotkey.com/).
    *   Lade die neueste Version (v2.0 wird empfohlen) herunter und installiere sie.

### Schritt 2: Projektverzeichnis einrichten

Wir erstellen ein eigenes Verzeichnis für unser Projekt.

1.  Öffne den **Datei-Explorer**.
2.  Navigiere zu deinem Benutzerordner (z. B. `C:\Benutzer\DeinBenutzername`).
3.  Erstelle eine neue Ordnerstruktur: `projekte\py\STT`. Der endgültige Pfad sollte so aussehen: `C:\Benutzer\DeinBenutzername\projekte\py\STT`.
4.  Öffne eine **Eingabeaufforderung**, indem du in die Adressleiste des Datei-Explorers (während du im `STT`-Ordner bist) `cmd` eingibst und Enter drückst.

### Schritt 3: Virtuelle Python-Umgebung erstellen

Eine virtuelle Umgebung isoliert die Python-Pakete dieses Projekts von deinem restlichen System. Führe in der soeben geöffneten Eingabeaufforderung folgende Befehle aus:

```cmd
:: Erstellt die virtuelle Umgebung mit dem Namen "vosk-env"
python -m venv vosk-env

:: Aktiviert die Umgebung. Dies musst du jedes Mal tun, wenn du an diesem Projekt arbeitest.
.\vosk-env\Scripts\activate
```
Nach der Aktivierung sollte sich deine Eingabeaufforderung ändern und `(vosk-env)` am Anfang anzeigen.

### Schritt 4: Python-Pakete installieren

Installiere nun die benötigten Python-Bibliotheken mit `pip`. Wir fügen `pyautogui` hinzu, eine Bibliothek, die es Python unter Windows ermöglicht, die Tastatur zu steuern.

```cmd
pip install vosk sounddevice pyperclip pyautogui
```

### Schritt 5: Vosk-Sprachmodell herunterladen

Für eine hohe Genauigkeit in Englisch verwenden wir das `vosk-model-en-us-0.22-lgraph`-Modell.

1.  Lade das Modell über diesen Link herunter: [vosk-model-en-us-0.22-lgraph.zip](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) (128 MB).
2.  Öffne die heruntergeladene `.zip`-Datei.
3.  Entpacke den darin enthaltenen Ordner (`vosk-model-en-us-0.22-lgraph`) in dein Projektverzeichnis (`C:\Benutzer\DeinBenutzername\projekte\py\STT`).

---

## Konfiguration

Das System besteht aus zwei Skripten: dem Python-Hintergrunddienst und dem AutoHotkey-Auslöser.

### Teil A: Das Python-Hintergrundskript

Dieses Skript läuft im Hintergrund, hält das Sprachmodell im Speicher und wartet auf ein Signal.

1.  Erstelle in deinem Projektordner eine neue Datei namens `dictation_service.py`.
2.  Kopiere den folgenden Code vollständig in die Datei.

    ```python
    # Datei: C:\Benutzer\DeinBenutzername\projekte\py\STT\dictation_service.py
    import vosk
    import sys
    import sounddevice as sd
    import queue
    import json
    import pyperclip
    import time
    import tempfile
    import pyautogui
    from pathlib import Path

    # --- Konfiguration ---
    SCRIPT_DIR = Path(__file__).resolve().parent
    MODEL_NAME = "vosk-model-en-us-0.22-lgraph" # Englisches Modell
    MODEL_PATH = SCRIPT_DIR / MODEL_NAME
    # Nutze das temporäre Verzeichnis des Systems für die Trigger-Datei
    TRIGGER_FILE = Path(tempfile.gettempdir()) / "vosk_trigger"
    SAMPLE_RATE = 16000

    # --- Hilfsfunktionen ---
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
        print(f"FATALER FEHLER: Modell nicht unter {MODEL_PATH} gefunden.")
        sys.exit(1)

    print(f"Lade Modell '{MODEL_NAME}'... Dies kann einige Sekunden dauern.")
    try:
        model = vosk.Model(str(MODEL_PATH))
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Modell erfolgreich geladen. Dienst wartet auf einen Auslöser.")
    except Exception as e:
        print(f"FATALER FEHLER: Modell konnte nicht geladen werden. {e}")
        sys.exit(1)

    while True:
        try:
            if TRIGGER_FILE.exists():
                print("Auslöser erkannt! Starte Transkription.")
                TRIGGER_FILE.unlink() # Datei löschen, um den Auslöser zurückzusetzen

                recognized_text = transcribe_audio()

                if recognized_text:
                    print(f"Transkribiert: '{recognized_text}'")
                    # Nutze pyautogui, um den Text automatisch zu tippen
                    pyautogui.typewrite(recognized_text)
                    pyperclip.copy(recognized_text) # Auch in die Zwischenablage kopieren
                else:
                    print("Kein Text erkannt.")
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDienst durch Benutzer beendet.")
            break
        except Exception as e:
            print(f"Ein Fehler in der Hauptschleife ist aufgetreten: {e}")
    ```

### Teil B: Das AutoHotkey-Skript

Dieses Skript erstellt den globalen Hotkey, der dem Python-Dienst das Signal gibt.

1.  In deinem Projektordner (`C:\Benutzer\DeinBenutzername\projekte\py\STT`), rechtsklicke, gehe zu **Neu** und wähle **AutoHotkey Script**.
2.  Nenne die Datei `vosk_trigger.ahk`.
3.  Rechtsklicke die neue Datei und wähle **Edit script**.
4.  Lösche den vorhandenen Text und füge den folgenden Code ein. Dieser legt den Hotkey auf **`Strg` + `Alt` + `D`** fest.

    ```autohotkey
    ; Vosk Diktier-Auslöser für Windows
    ; Hotkey: Strg+Alt+D

    ^!d::
    {
        ; Erzeugt eine leere Datei im Temp-Verzeichnis, um das Python-Skript zu signalisieren
        FileAppend, "", A_Temp . "\vosk_trigger"
        ; Zeigt eine Benachrichtigung an, dass die Aufnahme läuft
        TrayTip, "Vosk hört zu...", "Sprich jetzt.", 1
    }
    return
    ```
5.  Speichere und schließe die Datei.

---

## Verwendung

1.  **Den Dienst starten (einmal pro Sitzung):**
    *   Öffne eine Eingabeaufforderung, navigiere zu deinem Projektverzeichnis und aktiviere die Umgebung wie in Schritt 2 und 3 gezeigt.
    *   Führe den Python-Dienst aus:
        ```cmd
        cd C:\Benutzer\DeinBenutzername\projekte\py\STT
        .\vosk-env\Scripts\activate
        python dictation_service.py
        ```
    *   **WICHTIG:** Lass dieses Fenster der Eingabeaufforderung geöffnet! Du kannst es minimieren. Solange es offen ist, läuft der Dienst.

2.  **Das Hotkey-Skript starten:**
    *   Navigiere zu deinem Projektordner im Datei-Explorer.
    *   Doppelklicke auf das Skript `vosk_trigger.ahk`. Du wirst ein grünes "H"-Symbol in deinem System-Tray (im Infobereich der Taskleiste, unten rechts) sehen.

3.  **Diktieren:**
    *   Klicke in ein beliebiges Textfeld.
    *   Drücke deinen Hotkey (`Strg+Alt+D`).
    *   Eine Benachrichtigung "Vosk hört zu..." erscheint.
    *   Sprich einen Satz. Mache eine kurze Pause, wenn du fertig bist.
    *   Der erkannte Text wird automatisch für dich getippt.

---

## Optional: Alles automatisch beim Systemstart laden

Um die Skripte nicht jedes Mal manuell starten zu müssen, kannst du sie zum Autostart-Ordner von Windows hinzufügen.

1.  **Einen Starter für den Python-Dienst erstellen:**
    *   Erstelle in deinem Projektordner eine neue Textdatei. Nenne sie `launch_vosk_service.bat`.
    *   Bearbeite die Datei und füge den folgenden Befehl ein. **Ersetze `DeinBenutzername` durch deinen tatsächlichen Windows-Benutzernamen.**
        ```batch
        @echo off
        start "Vosk Service" /B "C:\Benutzer\DeinBenutzername\projekte\py\STT\vosk-env\Scripts\python.exe" "C:\Benutzer\DeinBenutzername\projekte\py\STT\dictation_service.py"
        ```
    *   Speichere die Datei. Dieses Skript startet den Python-Dienst im Hintergrund, ohne ein sichtbares Konsolenfenster zu hinterlassen.

2.  **Verknüpfungen zum Autostart-Ordner hinzufügen:**
    *   Drücke `Win` + `R`, um den "Ausführen"-Dialog zu öffnen.
    *   Gib `shell:startup` ein und drücke Enter. Dein persönlicher Autostart-Ordner wird geöffnet.
    *   Gehe zurück zu deinem Projektordner (`C:\Benutzer\DeinBenutzername\projekte\py\STT`).
    *   Rechtsklicke `launch_vosk_service.bat` und wähle **Kopieren**. Gehe zum Autostart-Ordner und mache einen Rechtsklick -> **Verknüpfung einfügen**.
    *   Rechtsklicke `vosk_trigger.ahk` und wähle **Kopieren**. Gehe zum Autostart-Ordner und mache einen Rechtsklick -> **Verknüpfung einfügen**.

Jetzt werden sowohl der Hintergrunddienst als auch das Hotkey-Skript bei jeder Anmeldung an Windows automatisch gestartet. Viel Spaß mit deinem neuen Diktier-Tool
