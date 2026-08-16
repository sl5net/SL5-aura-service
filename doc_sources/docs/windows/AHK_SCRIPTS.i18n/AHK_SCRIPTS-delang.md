### Markdown-Dokumentation (`docs/AHK_SCRIPTS.md`)

# AutoHotkey-Infrastruktur für SL5-Aura-Service

Da Windows Dateisperren und System-Hotkeys anders handhabt als Linux, verwendet dieses Projekt eine Reihe von AutoHotkey-Skripten (v2), um die Lücke zwischen der Python STT-Engine und der Windows-Benutzeroberfläche zu schließen.

## Übersicht über Skripte

### 1. `trigger-hotkeys.ahk`
* **Zweck:** Die Hauptbenutzeroberfläche zur Steuerung des Dienstes.
* **Hauptmerkmale:**
* Fängt **F10** und **F11** ab, um das Diktat zu starten/stoppen.
* Verwendet einen „Tastatur-Hook“, um das Standardverhalten des Windows-Systems zu überschreiben (z. B. F10 aktiviert die Menüleiste).
* **Bereitstellung:** Entwickelt für die Registrierung über den Windows-Taskplaner mit „Höchsten Berechtigungen“, sodass Hotkeys auch dann erfasst werden können, wenn der Benutzer in einer Anwendung auf Administratorebene arbeitet.

### 2. `type_watcher.ahk`
* **Zweck:** Fungiert als „Consumer“ in der STT-Pipeline.
* **Hauptmerkmale:**
* Überwacht ein temporäres Verzeichnis für eingehende „.txt“-Dateien, die von der Python-Engine generiert werden.
* **Zustandsmaschine (Zombie-Map):** Implementiert eine speicherbasierte Karte, um sicherzustellen, dass jede Datei genau einmal eingegeben wird. Dies verhindert „doppelte Eingaben“, die durch redundante Windows-Dateisystemereignisse (hinzugefügt/geändert) verursacht werden.
* **Sicheres Tippen:** Verwendet „SendText“, um sicherzustellen, dass Sonderzeichen in jedem aktiven Editor korrekt verarbeitet werden.
* **Zuverlässige Bereinigung:** Verwaltet das Löschen von Dateien mit einer Wiederholungslogik, um Windows-Dateizugriffssperren zu verarbeiten.

### 3. `scripts/ahk/sync_editor.ahk`
* **Zweck:** Gewährleistet eine nahtlose Synchronisierung zwischen der Festplatte und dem Texteditor (z. B. Notepad++).
* **Hauptmerkmale:**
* **Save-on-Demand:** Kann von Python ausgelöst werden, um ein „Strg+S“ im Editor zu erzwingen, bevor die Engine die Datei liest.
* **Dialog-Automator:** Erkennt und bestätigt automatisch Neuladedialoge „Datei von einem anderen Programm geändert“ und sorgt so für ein flüssiges Echtzeit-Update-Erlebnis.
* **Visuelles Feedback:** Bietet kurzlebige Benachrichtigungsfelder, um den Benutzer darüber zu informieren, dass Korrekturen angewendet werden.

### 4. `scripts/notification_watcher.ahk`
* **Zweck:** Bietet UI-Feedback für Hintergrundprozesse.
* **Hauptmerkmale:**
* Überwacht bestimmte Statusdateien oder Ereignisse, um dem Benutzer Benachrichtigungen anzuzeigen.
* Entkoppelt die Logik der „Berechnung“ einer Nachricht (Python) von deren „Anzeige“ (AHK), um sicherzustellen, dass die Haupt-STT-Engine nicht durch UI-Interaktionen blockiert wird.


---

### Nicht-Administrator-Fallback
Wenn die Anwendung ohne Administratorrechte ausgeführt wird:
- **Funktionalität:** Der Dienst bleibt voll funktionsfähig.
- **Hotkey-Einschränkungen:** Systemreservierte Tasten wie **F10** können weiterhin das Windows-Menü auslösen. In diesem Fall wird empfohlen, die Hotkeys auf Nicht-Systemtasten umzustellen (z. B. „F9“ oder „Einfügen“).
- **Aufgabenplaner:** Wenn die Aufgabe „AuraDictation_Hotkeys“ während einer Admin-Installation erstellt wurde, wird das Skript selbst für einen Standardbenutzer mit hohen Berechtigungen ausgeführt. Wenn nicht, startet „start_dictation.bat“ stillschweigend eine lokale Instanz auf Benutzerebene.

---

### 3. Warum „nervige Meldungen“ erscheinen und wie man sie im AHK-Code stoppt
Um sicherzustellen, dass das Skript selbst niemals den Nutzer mit Popups stört, füge diese „Silent-Flags“ oben in deine `.ahk` Dateien ein:

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. Strategie für die Hotkeys (F10 Alternative)
Da F10 ohne Admin-Rechte unter Windows fast unmöglich sauber abzufangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Zusammenfassung der Verbesserungen:
1. **Batch-Datei:** Nutzt `start "" /b`, um das schwarze Fenster zu vermeiden, und prüft vorher, ob der Admin-Task schon läuft.
2. **Transparenz:** Die Doku erklärt nun offen: „Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10“.
3. **AHK-Skript:** Nutzt `#SingleInstance Force`, um den „Eine ältere Instanz läuft“-Dialog zu unterdrücken.

Damit wirkt die Software viel professioneller („Smooth“), da sie im Hintergrund startet, ohne dass der Nutzer mit technischen Details oder Bestätigungsfenstern konfrontiert wird.
  
  
---

### Warum diese Dokumentation wichtig ist:
Indem Sie die **„Zombie Map“** und die **„Task Scheduler/Admin“**-Anforderung dokumentieren, erklären Sie anderen Entwicklern (und Ihrem zukünftigen Ich), warum der Code komplexer ist als ein einfaches Linux-Skript. Es verwandelt „seltsame Problemumgehungen“ in „technische Lösungen für Windows-Einschränkungen“.

(s,29.1.'26 11:02 Do)