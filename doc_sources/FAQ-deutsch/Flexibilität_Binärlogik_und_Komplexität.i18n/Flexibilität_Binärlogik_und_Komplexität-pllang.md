## Die Flexibilität des Regelwerks: Von Binärlogik zur Komplexität

Die kombinierte Prioritäts- und Verarbeitungslogik (sekwencyjne sortowanie, pełne zatrzymanie dopasowania, kumulacja, fuzzy-fallback) umożliwia elastyczne dostosowanie:

### 1. Einfache (Binäre) Steuerung durch höchste Priorität

Durch die Positionierung einer **höchst priorisierten Regel mit einem Full Match Stopp** kann ein einfacher Ein-/Ausschalt-Mechanismus (`Toggle`) konfiguriert werden.

* **Beispiel:** Eine Regel ganz oben in `FUZZY_MAP_pre` kann einen bestimmten Eingabestring (z. B. einfaches Kommandowort) erkennen, sofort verarbeiten und damit die gesamte nachfolgende Kaskade für dieses Token blockieren. Dies ermöglicht die Konfiguration von einfachen Kommandos oder Zuständen, die nur zwei Worte/Befehle zulassen.

### 2. Komplexe Anpassungen i Framework-Integration

Gleichzeitig erlaubt der Aufbau die Implementierung von komplexen, kaskadierenden Modifikationen, die für spezifische Framework-Anforderungen (wie CodeIgniter oder ähnliche) notwendig sind:

* **Kumulacja:** Durch die Kumulation können mehrere Regeln sequenziell auf den Text angewendet werden, um beispielsweise die Benennungskonventionen oder Platzhalter eines Frameworks schrittweise in eine gewünschte Ausgabe zu überführen.
* **Wtyczki:** Die hierarchische Ladelogik über `plugins/` stellt sicher, dass projektspezifische oder frameworkspezifische Regeln (z. B. für CodeIgniter) jest również oddzielnym modułem hinzugefügt werden können. Diese Plug-in-Regeln haben eine definierte, aber niedrigere Priorität als die Kern-Sprachregeln, wodurch die Kernlogik unangetastet bleibt, aber das Verhalten gezielt erweitert werden kann.

**Fazit:** Ob es sich um die binäre Umschaltung von Steuerwörtern oder die szczegółylierte Anpassung an die Konventionen eines kompleksen Frameworks handelt – die Hierarchie der Prioritäten (Modul > Zeile) und die Steuerung durch das Stopp-Kriterium des Full Match bieten die nötige Kontrolle über den Verarbeitungsprozes.