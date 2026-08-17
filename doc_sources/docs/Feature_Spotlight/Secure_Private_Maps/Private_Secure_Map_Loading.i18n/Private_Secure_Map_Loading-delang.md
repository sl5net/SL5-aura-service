# FEATURE SPOTLIGHT: Sicheres Laden privater Karten und automatisches Packen

Dieses Dokument beschreibt die Architektur für die Verwaltung sensibler Karten-Plugins (z. B. Client-Daten, proprietäre Befehle) auf eine Weise, die **Live-Bearbeitung** ermöglicht und gleichzeitig **Best Practices für die Sicherheit** durchsetzt, um eine versehentliche Offenlegung von Git zu verhindern.

---

## 1. Das Konzept: „Matroschka“-Sicherheit

Um maximale Privatsphäre bei der Verwendung von Standardtools zu gewährleisten, verwendet Aura eine **Matroschka (Russische Puppe)**-Verschachtelungsstrategie für verschlüsselte Archive.

1. **Äußere Schicht:** Eine Standard-ZIP-Datei, verschlüsselt mit **AES-256** (über den Systembefehl „zip“).
* *Erscheinungsbild:* Enthält nur **eine** Datei mit dem Namen „aura_secure.blob“.
* *Vorteil:* Versteckt Dateinamen und Verzeichnisstruktur vor neugierigen Blicken.
2. **Innere Schicht (Der Blob):** Ein unverschlüsselter ZIP-Container innerhalb des Blobs.
* *Inhalt:* Die tatsächliche Verzeichnisstruktur und Python-Dateien.
3. **Arbeitsstatus:** Wenn die Sperre aufgehoben ist, werden Dateien in einen temporären Ordner extrahiert, dem ein Unterstrich vorangestellt ist (z. B. „_private“).
* *Sicherheit:* Dieser Ordner wird von „.gitignore“ strikt ignoriert.

---

## 2. Technischer Arbeitsablauf

### A. Das Sicherheitstor (Start-Up)
Bevor etwas entpackt wird, überprüft Aura „scripts/py/func/map_reloader.py“ auf bestimmte „.gitignore“-Regeln.
* **Regel 1:** `config/maps/**/.*` (Schützt Schlüsseldateien)
* **Regel 2:** `config/maps/**/_*` (Schützt Arbeitsverzeichnisse)
Fehlen diese, kommt es zum **Abbruch** des Systems.

### B. Auspacken (ausnahmegesteuert)
1. Der Benutzer erstellt eine Schlüsseldatei (z. B. „.auth_key.py“), die das Passwort (im Klartext oder als Kommentar) enthält.
2. Aura erkennt diese Datei und die entsprechende ZIP-Datei (z. B. „private.zip“).
3. Aura entschlüsselt die äußere ZIP-Datei mithilfe des Schlüssels.
4. Aura erkennt „aura_secure.blob“, extrahiert die innere Ebene und verschiebt die Dateien in das Arbeitsverzeichnis „_private“.

### C. Live-Bearbeitung und automatisches Packen (The Cycle)
Hier wird das System zur „Selbstheilung“:

1. **Bearbeiten:** Sie ändern eine Datei in „_private/“ und speichern sie.
2. **Auslöser:** Aura erkennt die Änderung und lädt das Modul neu.
3. **Lifecycle Hook:** Das Modul löst seine Funktion „on_reload()“ aus.
4. **SecurePacker:** Ein Skript („secure_packer.py“) im Stammverzeichnis des privaten Ordners führt Folgendes aus:
* Es erstellt die innere ZIP-Struktur (Struktur).
* Es wird in „.blob“ umbenannt.
* Es ruft den Systembefehl „zip“ auf, um es mit dem Passwort aus der „.key“-Datei in das äußere Archiv zu verschlüsseln.

**Ergebnis:** Ihre „private.zip“ ist immer mit Ihren neuesten Änderungen auf dem neuesten Stand, aber Git sieht nur die Änderung der binären ZIP-Datei.

---

## 3. Einrichtungsanleitung

### Schritt 1: Verzeichnisstruktur
Erstellen Sie eine Ordnerstruktur wie diese:
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### Schritt 2: Die Schlüsseldatei (`.auth_key.py`)
Muss mit einem Punkt beginnen.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### Schritt 3: Das Packer-Skript („secure_packer.py“)
Platzieren Sie dieses Skript in Ihrem privaten Kartenordner (bevor Sie es zunächst komprimieren). Es verwaltet die Verschlüsselungslogik. Stellen Sie sicher, dass Ihre Karten dieses Skript über den Hook „on_reload“ aufrufen.

### Schritt 4: Hook-Implementierung
Fügen Sie in Ihren Kartendateien („.py“) diesen Hook hinzu, um die Sicherung bei jedem Speichern auszulösen:

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Git-Status und Sicherheit

Bei ordnungsgemäßer Einrichtung zeigt „git status“ **nur** Folgendes an:
```text
modified:   config/maps/private/private_maps.zip
```
Der Ordner „_private_maps“ und die Datei „.auth_key.py“ werden niemals verfolgt.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# Entwicklerhandbuch: Plugin-Lebenszyklus-Hooks

Mit Aura SL5 können Plugins (Maps) spezifische „Hooks“ definieren, die automatisch ausgeführt werden, wenn sich der Status des Moduls ändert. Dies ist für erweiterte Arbeitsabläufe wie das **Secure Private Map**-System unerlässlich.

## Der „on_reload()“-Hook

Die Funktion „on_reload()“ ist eine optionale Funktion, die Sie in jedem Map-Modul definieren können.

### Verhalten
* **Auslöser:** Wird sofort ausgeführt, nachdem ein Modul erfolgreich **im laufenden Betrieb neu geladen wurde** (Dateiänderung + Sprachauslöser).
* **Kontext:** Wird im Hauptanwendungsthread ausgeführt.
* **Sicherheit:** Eingepackt in einen „try/exclusive“-Block. Fehler hier werden protokolliert, führen jedoch **nicht zum Absturz** der Anwendung.

### Nutzungsmuster: Die „Daisy Chain“
Bei komplexen Paketen (wie Private Maps) gibt es oft viele Unterdateien, aber nur ein zentrales Skript („secure_packer.py“) sollte die Logik übernehmen.

Mit dem Hook können Sie die Aufgabe nach oben delegieren:

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

### Best Practices
1. **Halten Sie es schnell:** Führen Sie keine langen Blockierungsaufgaben (wie große Downloads) im Haupt-Hook aus. Verwenden Sie bei Bedarf Fäden.
2. **Idempotenz:** Stellen Sie sicher, dass Ihr Hook mehrere Male ausgeführt werden kann, ohne dass etwas kaputt geht (z. B. nicht endlos an eine Datei anhängen, sondern sie stattdessen neu schreiben).