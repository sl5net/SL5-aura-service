# Interaktive Regelsuche und -ausführung

In diesem Spotlight wird das interaktive Regelsuch- und Ausführungssystem hervorgehoben, das Sprachbefehle, Live-Navigation und sofortige Ausführung verbindet.

## Kernfunktionen
[1] **Dual-Pane Live Search (`fzf`):** Linker Bereich filtert Regeldateien; Im rechten Bereich wird die Zeilenkontextvorschau über „preview_rule.py“ angezeigt.
[2] **Sofortige Ausführungen („Enter“ / „Strg+R“):** Führt den extrahierten Zielbefehl sofort über „run_palette_command.py“ im Hintergrund aus.
[3] **Direkte Bearbeitung (`Strg+E`):** Startet den Editor (CudaText mit `@line`, Kate/VS Code mit `--line`) direkt an der Zielzeile.
[4] **Floating Window Hotkey:** An „Super+S“ gebunden für einen schnellen, in den Desktop integrierten Arbeitsablauf.
[5] **Sprachbefehlsgesteuert:** Zahlreiche Sprachbefehle konfigurieren Suchmuster in „search_rules.sh“ für schnelle, gezielte Suchvorgänge vor.

## Plattformübergreifende Unterstützung
- **Linux Bash (`run_rule.sh` / `search_rules.sh`):** Voll ausgestattete Implementierung mit Verlaufsverfolgung und Zwischenablageoperationen (`Strg+X` / `Strg+A`).
- **Windows PowerShell (`search_rules.ps1`):** Begleittool mit einfachen Terminalsuchfunktionen.

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)