# Entwickler-Handbuch: Plugin Lifecycle Hooks

Aura SL5 ermöglicht es Plugins (Maps), spezifische "Hooks" (Einhängepunkte) zu definieren, die automatisch ausgeführt werden, wenn sich der Status eines Moduls ändert. Dies ist essenziell für fortgeschrittene Workflows wie das **Secure Private Map** System.

## Der `on_reload()` Hook

Die Funktion `on_reload()` ist eine optionale Funktion, die du in jedem Map-Modul definieren kannst.

### Verhalten
*   **Auslöser:** Wird unmittelbar ausgeführt, nachdem ein Modul erfolgreich per **Hot-Reload** neu geladen wurde (Dateiänderung + Sprach-Trigger).
*   **Kontext:** Läuft innerhalb des Haupt-Anwendungs-Threads (Main Thread).
*   **Sicherheit:** Ist in einen `try/except`-Block gekapselt. Fehler, die hier auftreten, werden protokolliert, führen aber **nicht** zum Absturz der Anwendung.

### Verwendungsmuster: Die "Daisy Chain" (Delegation)
Bei komplexen Paketen (wie Private Maps) hast du oft viele Unterdateien, aber nur ein zentrales Skript (z. B. `secure_packer.py`), das die Logik (wie das Zippen) steuern soll.

Du kannst den Hook nutzen, um die Aufgabe "nach oben" zu delegieren:

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

### Best Practices (Bewährte Vorgehensweisen)
1.  **Halte es schnell:** Führe keine langwierigen, blockierenden Aufgaben (wie riesige Downloads) direkt im Hook aus. Nutze Threads, wenn nötig.
2.  **Idempotenz:** Stelle sicher, dass dein Hook mehrfach ausgeführt werden kann, ohne Schaden anzurichten (z. B. hänge Text nicht endlos an eine Datei an, sondern überschreibe sie oder prüfe vorher).
