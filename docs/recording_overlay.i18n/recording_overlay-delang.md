# Aufnahme-Overlay (Bildschirmanzeige)

Das Aufnahme-Overlay bietet eine sofortige, plattformübergreifende visuelle Anzeige des Diktatstatus. Es funktioniert unabhängig von Desktop-Benachrichtigungs-Daemons und „Bitte nicht stören“-Filtern und zeigt den Status direkt auf dem Hauptbildschirm an.

## Visuelle Beispiele

| Unten links (`bl`) | Oben-Rechts (`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *Passt in dunkle Panels und Systemablagen* | *Hoher Kontrast gegenüber hellen oder komplexen Fenstern* |

## Staaten

- **Aufnahme (`🔴`)**: Ein leuchtend roter Kreis mit hervorgehobener Umrandung („#e62222“ auf „#181818“) signalisiert eine aktive Audioaufnahme.
- **Leerlauf**:
- „Ausgeblendet“ (Standard): Das Fenster wird vollständig ausgeblendet, wodurch Platz auf dem Desktop für die normale Interaktion frei wird.
- „Fünfeck“: Zeigt im Ruhemodus ein dezentes geometrisches Fünfeck-Symbol („⬟“) an.

## Konfiguration

Einstellungen werden in „config/settings.py“ verwaltet:

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

## Architektur

- Erstellt unter Verwendung der Python-Standardbibliothek („tkinter“) und erfordert keine externen C-Abhängigkeiten.
– Wird in einem Hintergrund-Daemon-Thread mit Thread-sicherer Warteschlangen-Ereignisbehandlung ausgeführt.
- Erkennt dynamisch den primären Monitor in Umgebungen mit mehreren Displays.

(s, 10.9.26 14:41 Do)