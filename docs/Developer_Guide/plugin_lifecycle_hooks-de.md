# Plugin Lifecycle Hooks (Lebenszyklus-Funktionen)

Aura SL5 unterstützt sogenannte Lifecycle-Hooks. Diese ermöglichen es Plugins (Maps), automatisch speziellen Code auszuführen, wenn sich ihr Status ändert.

## Der `on_reload()` Hook

Die Funktion `on_reload()` ist eine optionale Funktion, die du in jeder Plugin-Datei (`.py`) definieren kannst.

### Verhalten
*   **Auslöser:** Diese Funktion wird **unmittelbar ausgeführt, nachdem** das Modul erfolgreich per Hot-Reload neu geladen wurde (also nach einer Dateiänderung und dem darauffolgenden Sprach-Trigger).
*   **Kontext:** Sie läuft im normalen Programmfluss der Anwendung.
*   **Geltungsbereich:** Sie wird **NICHT** beim initialen Start (Kaltstart) des Systems ausgeführt. Sie dient ausschließlich Szenarien, in denen eine Karte *während der Laufzeit* bearbeitet und neu geladen wurde.

### Anwendungsfälle
*   **Sicherheit:** Automatisches Wieder-Verschlüsseln oder Packen (Zippen) von sensiblen Dateien, nachdem man sie bearbeitet hat.
*   **Status-Management:** Zurücksetzen von globalen Zählern, Variablen oder das Leeren spezifischer Caches.
*   **Validierung:** Prüfen, ob eine Konfigurationsdatei nach der Änderung noch gültig ist.

### Technische Details & Sicherheit
*   **Fehler-Toleranz:** Der Aufruf ist in einen `try/except`-Block gekapselt. Wenn deine `on_reload`-Funktion abstürzt (z. B. durch eine Division durch Null), wird ein Fehler geloggt (`❌ Error executing on_reload...`), aber **Aura stürzt nicht ab**.
*   **Performance:** Die Funktion läuft synchron im Hauptprozess. Vermeide langwierige Aufgaben (wie große Downloads oder Sleep-Timer) direkt in dieser Funktion, da sie die Sprachverarbeitung kurzzeitig blockieren würden. Für schwere Aufgaben sollte ein eigener Thread gestartet werden.

### Code-Beispiel

```python
# config/maps/plugins/mein_plugin/de-DE/meine_karte.py

def execute(data):
    # Normale Logik für den Sprachbefehl
    pass

# --- LIFECYCLE HOOK ---
def on_reload():
    """
    Wird automatisch aufgerufen, wenn diese Datei geändert
    und von Aura neu geladen wurde.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("🔄 Plugin wurde aktualisiert! Führe Aufräumarbeiten durch...")
    
    # Beispiel: Prüfen, ob Hilfsdateien existieren
    # check_dependencies()
