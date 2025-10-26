# Einrichten von Pre-Push-Git-Hooks und Python-Tools unter Linux

Dieses Projekt verwendet einen Pre-Push-Git-Hook, um „requirements.txt“ automatisch aus Ihren Python-Skripten zu aktualisieren.  
Um diesen Workflow nutzen zu können, muss das Tool „pipreqs“ installiert und für Git verfügbar sein.

## Empfohlen: Installieren Sie pipreqs mit pipx

1. **Pipx installieren (falls noch nicht installiert):**
   ```bash
   sudo pacman -S python-pipx
   ```

2. **Pipreqs mit pipx installieren:**
   ```bash
   pipx install pipreqs
   ```

3. **Überprüfen Sie, ob pipreqs funktioniert:**
   ```bash
   pipreqs --version
   ```

## Alternative: Verwenden Sie eine virtuelle Python-Umgebung

Wenn Sie eine virtuelle Umgebung für Ihr Projekt bevorzugen oder verwenden:

1. **Erstellen und aktivieren Sie eine virtuelle Umgebung:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Installieren Sie pipreqs innerhalb der virtuellen Umgebung:**
   ```bash
   pip install pipreqs
   ```

3. **Bearbeiten Sie den Git-Hook**, um pipreqs unter Verwendung des vollständigen Pfads aufzurufen:
   ```bash
   .venv/bin/pipreqs "$TMPDIR" --force
   ```

## Warum nicht eine einfache Pip-Installation verwenden?

Moderne Linux-Distributionen schränken systemweite Pip-Installationen ein, um zu verhindern, dass Betriebssystempakete beschädigt werden.  
**Verwenden Sie NICHT** global „sudo pip install pipreqs“ oder „pip install pipreqs“.

## Fehlerbehebung

- Wenn Sie „pipreqs: Befehl nicht gefunden“ sehen, stellen Sie sicher, dass Sie es mit pipx installiert haben und dass sich „~/.local/bin“ in Ihrem „$PATH“ befindet.
- Sie können Ihren Pfad überprüfen mit:
  ```bash
  echo $PATH
  ```

## Brauchen Sie Hilfe?

Eröffnen Sie ein Issue oder fragen Sie in der Projektdiskussion nach!