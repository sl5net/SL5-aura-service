# SL5 Dictation: Detaillierte Installationsanleitung für Windows

Diese Anleitung führt dich Schritt für Schritt durch den gesamten Einrichtungsprozess. Sie ist ausführlich, da bei der Installation auf einem frischen Windows-System einige Hürden zu nehmen sind.

### **Teil 1: Vorbereitung – Der zuverlässigste Weg (Offline-Modelle)**

Die Server für die Sprachmodelle sind oft langsam oder überlastet. Um Zeitouts und Fehler zu vermeiden, ist es **dringend empfohlen**, die großen Dateien vorab manuell herunterzuladen.

1.  **Gehe zu unserer GitHub Releases-Seite:**



    *   **[Hier alle benötigten Dateien herunterladen](https://github.com/sl5net/Vosk-System-Listener/releases/tag/v0.2.0.1)**

2.  **Lade diese Dateien herunter:**
    *   `vosk-model-en-us-0.22.zip` (~1.8 GB)
    *   `vosk-model-de-0.21.zip` (~1.9 GB)

3.  **WICHTIG:** Entpacke diese drei `.zip`-Dateien direkt im Hauptverzeichnis des Projekts (z.B. in `C:\Users\DeinName\stt\models`). 

### **Teil 2: Das Setup-Skript ausführen**

1.  **PowerShell als Administrator starten:**
    *   Öffne das Windows-Startmenü, tippe `PowerShell` ein.
    *   Klicke mit der **rechten Maustaste** auf "Windows PowerShell" und wähle **"Als Administrator ausführen"**. Ein blaues Fenster sollte erscheinen.

2.  **Skript-Ausführung erlauben (einmalig pro Sitzung):**
    *   Gib in der Admin-PowerShell folgenden Befehl ein und bestätige die Frage mit `J`:
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```

3.  **Zum richtigen Ordner navigieren:**
    *   Wechsle in das `setup`-Verzeichnis deines Projekts. Passe den Pfad bei Bedarf an:
    ```powershell
    cd C:\Users\neu\stt\setup
    ```

4.  **Setup-Skript starten:**
    *   Führe nun das Skript aus:
    ```powershell
    .\windows11_setup.ps1
    ```
    *   **Hinweis:** Das Skript muss eventuell **zweimal** ausgeführt werden. Wenn es anhält, weil Python gerade erst installiert wurde, schließe das Fenster, starte eine neue Admin-PowerShell und wiederhole die Schritte 2-4.

### **Teil 3: Manuelle Korrekturen nach dem Setup**

Nach dem erfolgreichen Setup müssen noch ein paar Dinge manuell erledigt werden, damit der Server startet.

1.  **Fehlende Ordner erstellen:**
    *   Unser Skript braucht zwei Ordner, die es (noch) nicht selbst erstellt. Erstelle diese manuell:
        *   Einen Ordner `log` im Hauptverzeichnis des Projekts (also in `C:\Users\neu\stt\log`).
        *   Einen Ordner `tmp` direkt auf deinem `C:` Laufwerk (also `C:\tmp`).

### **Teil 4: Der erste Start (Funktionstest)**

Jetzt sollte alles bereit sein.

1.  **Watcher starten:** Starte `type_watcher.ahk` und `notification_watcher.ahk` per Doppelklick.
2.  **Server starten:** Führe in der Git-Bash mit der aktiven `(.venv)`-Umgebung aus:
    ```bash
    python dictation_service.py
    ```
    Lass dieses Fenster offen. Es sollte nun fehlerfrei laufen.
3.  **Diktat auslösen:** Öffne eine **zweite Git-Bash** und tippe:
    ```bash
    touch C:/tmp/vosk_trigger
    ```
Eine "Listening..."-Notification sollte erscheinen und das Diktat funktionieren.
