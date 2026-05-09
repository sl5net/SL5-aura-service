# Workflow-Benachrichtigungen (Audio-Benachrichtigungen)

Um die Produktivität zu verbessern, können Sie einen lokalen Git-Alias konfigurieren, der Ihren Code pusht und Sie automatisch (per Stimme oder Ton) benachrichtigt, sobald der GitHub Actions-Workflow abgeschlossen ist. Dies verhindert „GitHub-Watching-Müdigkeit“ und ermöglicht es Ihnen, sich auf andere Aufgaben zu konzentrieren.

### Voraussetzungen

Sie benötigen die **GitHub CLI** und eine Text-to-Speech-Engine oder einen Soundplayer, die auf Ihrem System installiert sind.

**Für Manjaro / Arch Linux:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### Aufstellen

Führen Sie den folgenden Befehl in Ihrem Terminal aus, um einen globalen Git-Alias namens „pushsound“ zu erstellen:

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### Nutzung

Anstelle von „git push“ führen Sie einfach Folgendes aus:
```bash
git pushsound
```
Ihr Terminal wartet, bis der Workflow abgeschlossen ist, und meldet dann: *"Alle Github-Workflows sind abgeschlossen"*.

---

### Anpassung und Alternativen

Abhängig von Ihren Vorlieben möchten Sie möglicherweise einen anderen Aliasnamen oder eine andere Benachrichtigungsmethode verwenden.

#### 1. Empfohlene Aliasnamen
Wenn „pushsound“ zu lang zum Eingeben ist, ziehen Sie diese Alternativen in Betracht:
* „git pw“ (Push & Watch) – **Empfohlen wegen der Geschwindigkeit.**
* `git sync` (Impliziert Drücken und Warten auf das „grüne Licht“)
* `git palert` (Push-Alarm)

#### 2. Benachrichtigungsstile
Sie können den Teil „espeak-ng“ gegen andere Arten von Warnungen austauschen:

* **Desktop-Benachrichtigung:**
`... && notify-send „GitHub Action“ „Workflow Finished!“`
* **Systemton (Glocke):**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **Kombination (Ton + Stimme):**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Fertig"`

#### 3. Fortgeschritten: Teamsichere Version
Wenn mehrere Entwickler gleichzeitig auf dasselbe Repository pushen, verfolgt der Standardbefehl möglicherweise die falsche Ausführung. Verwenden Sie diese „Branch-Safe“-Version, um nur Ihren eigenen aktuellen Zweig zu überwachen:

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'
```

### Fehlerbehebung
* **„Keine Läufe gefunden“:** Wir schließen „sleep 3“ ein, da GitHub einen Moment braucht, um den Push zu registrieren und den Workflow zu starten. Wenn Sie eine sehr langsame Verbindung haben, müssen Sie diese möglicherweise auf „Sleep 5“ erhöhen.
* **Terminal-Signaltöne:** Wenn „espeak-ng“ nicht funktioniert, stellen Sie sicher, dass Ihr Audio nicht stummgeschaltet ist und das Paket korrekt installiert ist.