# Entwicklerhandbuch: Generieren des Serviceanrufdiagramms

Dieses Dokument beschreibt die robuste, threadsichere Methode zum Generieren eines visuellen Aufrufdiagramms der lang laufenden „aura_engine.py“. Wir verwenden den Profiler „yappi“ (zur Multithreading-Unterstützung) und „gprof2dot“ zur Visualisierung.

### Voraussetzungen

Stellen Sie sicher, dass Sie die erforderlichen Tools global oder in Ihrer virtuellen Umgebung installiert haben:

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### Schritt 1: Ändern des Dienstes für die Profilerstellung

Das Skript „aura_engine.py“ muss geändert werden, um den „yappi“-Profiler manuell zu starten und die Profilierungsdaten bei einer Unterbrechung ordnungsgemäß zu speichern („Strg+C“).

**Wichtige Änderungen in „aura_engine.py“:**

1. **Importe und Signalhandler:** Importieren Sie „yappi“ und definieren Sie die Funktion „generate_graph_on_interrupt“ (wie zuvor implementiert), um „yappi.stop()“ und „stats.save(...)“ aufzurufen.
2. **Start/Stopp:** Fügen Sie „yappi.start()“ und „signal.signal(signal.SIGINT, ...)“ innerhalb des „if

### Schritt 2: Ausführen des Dienstes und Sammeln von Daten

Führen Sie das geänderte Skript direkt aus und lassen Sie es ausreichend Zeit (z. B. 10–20 Sekunden) Daten verarbeiten, um sicherzustellen, dass alle Kernfunktionen, einschließlich Thread-Funktionen (wie die LanguageTool-Korrektur), aufgerufen werden.

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

Drücken Sie einmal **Strg+C**, um den Signalhandler auszulösen. Dadurch wird der Profiler gestoppt und die Rohdaten gespeichert unter:

`\mathbf{yappi\_profile\_data.prof`

### Schritt 3: Generieren und Filtern des visuellen Diagramms

Wir verwenden „gprof2dot“, um die rohen „pstats“-Daten in das SVG-Format zu konvertieren. Da erweiterte Filteroptionen wie „--include“ und „--threshold“ von unserer spezifischen Umgebung möglicherweise nicht unterstützt werden, verwenden wir den grundlegenden **`--strip`**-Filter, um Pfadinformationen zu bereinigen und Systeminterna zu reduzieren.

**Führen Sie den Visualisierungsbefehl aus:**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### Schritt 4: Dokumentation (manueller Zuschnitt)

Die resultierende Datei „yappi_call_graph_stripped.svg“ (oder „.png“) ist zwar groß, enthält aber genau den gesamten Ausführungsablauf, einschließlich aller Threads.

Zu Dokumentationszwecken **schneiden Sie das Bild manuell zu**, um sich auf die zentrale Logik (die 10–20 Kernknoten und ihre Verbindungen) zu konzentrieren und ein fokussiertes und lesbares Aufrufdiagramm für die Repository-Dokumentation zu erstellen.

### Archivierung

Die geänderte Konfigurationsdatei und die endgültige Call Graph-Visualisierung sollten im Quellverzeichnis der Dokumentation archiviert werden:

| Artefakt | Standort |
| :--- | :--- |
| **Geänderte Servicedatei** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **Endgültiges zugeschnittenes Bild** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **Rohe Profildaten** | *(Optional: Sollte aus der endgültigen Repository-Dokumentation ausgeschlossen werden)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")