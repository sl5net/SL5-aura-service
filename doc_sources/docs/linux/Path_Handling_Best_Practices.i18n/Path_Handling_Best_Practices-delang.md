# Home-Verzeichnis und plattformübergreifende Pfadverwaltung

Aura ist für die Ausführung auf mehreren Betriebssystemen konzipiert. Um sicherzustellen, dass Dateisystem-Navigationsbefehle unabhängig davon funktionieren, ob Sie Linux, macOS oder Windows verwenden, werden Pfadzeichenfolgen dynamisch analysiert, bevor sie in den aktiven Fuzzy-Maps registriert werden.

---

## Pfadnormalisierungslogik (`FUZZY_MAP_pre.py`)

Die dynamische Pfadzuordnungslogik basiert auf den folgenden Standardpraktiken:

### 1. Tilde-Reduktion (POSIX)
Auf POSIX-kompatiblen Systemen (Linux und macOS) werden absolute Pfade, die mit dem Home-Verzeichnis des Benutzers übereinstimmen (z. B. „/home/Benutzername/“), beim Start in relative Pfade „~“ konvertiert. Dadurch werden die Zeichenfolgenlängen kürzer und die generierten Regeln können zwischen verschiedenen Benutzern auf demselben Betriebssystem übertragen werden:

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. Absolute Pfaderhaltung (Windows)
Windows wertet das Zeichen „~“ in Standard-Eingabeaufforderungs- („cmd.exe“) oder PowerShell-Umgebungen nicht zuverlässig aus. Wenn das Plugin daher eine Windows-Umgebung erkennt (`sys.platform == 'win32'`), behält es den vollständig qualifizierten absoluten Pfad (z. B. `C:\Benutzer\Benutzername\...`) bei, um sicherzustellen, dass die Befehlsausführung nicht fehlschlägt.

### 3. Schrägstrich-Normalisierung (`as_posix()`)
Aura verwendet intern Schrägstriche im POSIX-Stil (`/`) für Konfigurationszuordnungen. Das Skript normalisiert alle betriebssystemabhängigen Pfadtrennzeichen, indem es die Methode „pathlib.Path.as_posix()“ von Python verwendet, die Backslashes („\“) in Windows-Umgebungen automatisch bereinigt.