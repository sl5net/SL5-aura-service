# Erweitertes Ergebnis-Caching (statusbewusst)

## Übersicht
Aura verfügt über einen dauerhaften, kontextsensitiven Ergebniscache, der darauf ausgelegt ist, redundante Verarbeitung zu vermeiden. Wenn ein Sprachbefehl erkannt wird und einer Regel entspricht, prüft Aura, ob unter denselben Umständen zuvor genau dasselbe Ergebnis generiert wurde. Wenn eine Übereinstimmung gefunden wird, umgeht Aura teure Vorgänge wie **LanguageTool-Grammatikprüfungen** oder **Ollama-LLM-Generierung** und liefert das Ergebnis nahezu ohne Latenz.

## Hauptmerkmale
- **Kontextbewusst:** Der Cache ist spezifisch für den Titel des aktiven Fensters. Ein in „LibreOffice“ gesagter Befehl kann ein anderes zwischengespeichertes Ergebnis haben als der gleiche Befehl in „Terminal“.
- **Selbstheilung (automatische Invalidierung):** Der Cache läuft automatisch ab, wenn Sie die zugrunde liegende Regeldatei (`.py`-Karte) ändern.
- **Datenschutz geht vor:** Alle zwischengespeicherten Ergebnisse werden in einer lokalen SQLite-Datenbank („data/_aura_result_cache.db“) gespeichert.
- **Kein Wartungsaufwand:** Für die meisten Benutzer funktioniert dies vollständig im Hintergrund ohne Konfiguration.

## Wie es funktioniert
Das System generiert eine eindeutige „cache_id“ basierend auf drei Variablen:
1. **Die Regelausgabe:** Der von der Karte generierte Text.
2. **Die Sprache:** Der aktuell aktive Sprachcode (z. B. „de-DE“).
3. **Das aktive Fenster:** Der Titel des aktuell fokussierten Fensters.

### Gültigkeitslogik
Der Cache stellt sicher, dass Sie niemals „veraltete“ Informationen erhalten. Es werden zwei Arten von Gültigkeitsprüfungen verwendet:

| Geben Sie | ein Name | Logik | Anwendungsfall |
| :--- | :--- | :--- | :--- |
| **Typ 0** | **Automatische Dateisynchronisierung** | Verwendet die Änderungszeit („mtime“) der Kartendatei. | **Standard.** Wenn Sie Ihre Sandbox oder Karte bearbeiten, werden alle zugehörigen Cache-Einträge sofort ungültig. |
| **Typ 1** | **Manueller Zeitstempel** | Verwendet einen festen „Zeitstempel“, der in den Regelattributen bereitgestellt wird. | **Entwickler.** Codieren Sie eine Version/einen Zeitstempel fest, um einen bestimmten Ergebnisstatus zu erzwingen oder beizubehalten. |

## Beispiele für die Regelkonfiguration

Sie können das Caching-Verhalten direkt in Ihren Dateien „FUZZY_MAP_pre.py“ oder „FUZZY_MAP.py“ steuern.

### 1. Standardverhalten (automatisches Caching)
Standardmäßig ist das Caching aktiviert und verwendet die Änderungszeit der Datei.
```python
# No extra attributes needed. 
# If this file is saved, the cache for this rule refreshes.
('Bold', r'^make it bold$', 100)
```

### 2. Cache deaktivieren
Wenn ein Befehl dynamische Daten erzeugt (wie die aktuelle Uhrzeit oder einen zufälligen Witz), sollten Sie den Cache deaktivieren.
```python
('Current Time', r'^what time is it$', 100, {
    'cache': False 
})
```

### 3. Manueller Zeitstempel (feste Versionierung)
Wenn Sie möchten, dass der Cache unabhängig von Dateiänderungen bestehen bleibt (es sei denn, Sie ändern die Version), verwenden Sie einen manuellen Zeitstempel.
```python
('Stable Command', r'^run complex task$', 100, {
    'timestamp': '2026-05-09-v1'
})
```

## Auswirkungen auf die Leistung
- **Cache-Fehler:** Standardverarbeitung (0,05 s – 5,0 s, abhängig von der LLM-Nutzung).
- **Cache-Treffer:** Sofortige Verarbeitung.

Durch diesen Mechanismus werden Befehle oder korrigierte Tippfehler sofort zurückgegeben, ohne die CPU zu belasten.