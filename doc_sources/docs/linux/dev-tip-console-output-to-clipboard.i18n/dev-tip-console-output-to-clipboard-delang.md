# Entwicklertipp: Konsolenausgabe automatisch in die Zwischenablage kopieren

**Kategorie:** Linux/Shell-Produktivität  
**Plattform:** Linux (zsh + Konsole/KDE)

---

## Das Problem

Wenn Sie mit KI-Assistenten arbeiten, müssen Sie häufig Terminalausgaben kopieren und in den Chat einfügen. Dies bedeutet normalerweise:
1. Befehl ausführen
2. Wählen Sie den Ausgang mit der Maus aus
3. Kopieren
4. Wechseln Sie zum Browser
5. Einfügen

Das sind zu viele Schritte.

---

## Die Lösung: Automatische Erfassung über „preexec“ / „precmd“.

Fügen Sie dies zu Ihrer „~/.zshrc“ hinzu:

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}


precmd() {
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        cleaned=$(cat ~/t.txt \
            | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | sed "s|$HOME|~|g" \
            | sed 's/[^[:print:]]//g' \
            | grep -v '^$')
        if [ -n "$cleaned" ]; then
            echo "$cleaned" | xclip -selection clipboard
            echo "[📋 In Zwischenablage kopiert]"
        fi
    fi
}

```

Dann neu laden:
```bash
source ~/.zshrc
```

### Ergebnis

Nach jedem Befehl befindet sich die Ausgabe automatisch in Ihrer Zwischenablage – bereit zum Einfügen in Ihren KI-Chat mit **Strg+V**.

Die Ausgabe wird außerdem immer als Referenz in „~/t.txt“ gespeichert.

---

## Wie es funktioniert

| Teil | Was es tut |
|------|-------------|
| `preexec()` | Wird vor jedem Befehl ausgeführt und leitet die Ausgabe an „~/t.txt“ | weiter
| `precmd()` | Wird nach jedem Befehl ausgeführt, stellt stdout wieder her und kopiert in die Zwischenablage |
| `tee ~/t.txt` | Speichert die Ausgabe in einer Datei und zeigt sie weiterhin im Terminal | an
| `sed '...'' | Entfernt KDE-Konsole-Titel-Escape-Sequenzen (`]2;...` `]1;`) |
| `xclip` | Kopiert die bereinigte Ausgabe in die Zwischenablage |

---

## Anforderungen

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ Was man NICHT tun sollte

Verwenden Sie **nicht** „fc -ln -1 |“. bash`, um den letzten Befehl erneut auszuführen:

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

Dadurch wird jeder Befehl nach Abschluss erneut ausgeführt, was zerstörerische Nebenwirkungen haben kann – zum Beispiel das Überschreiben von Dateien, das erneute Ausführen von „git commit“, das erneute Ausführen von „sed -i“ usw.

Der obige „preexec“/„precmd“-Ansatz erfasst die Ausgabe **während** der Ausführung – sicher und zuverlässig.