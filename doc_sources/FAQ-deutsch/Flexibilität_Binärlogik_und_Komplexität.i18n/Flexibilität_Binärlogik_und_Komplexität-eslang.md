## Die Flexibilität des Regelwerks: Von Binärlogik zur Komplexität

La combinación de prioridades y lógica de verificación (clasificación secuencial, detención de partido completo, acumulación, retroceso difuso) incluye una flexibilidad combinada:

### 1. Einfache (Binäre) Steuerung durch höchste Priorität

Durante la posición, un **ajuste de prioridades alto con una parada completa del partido** puede configurar un mecanismo de cambio/interrupción (`Toggle`).

* **Beispiel:** Eine Regel ganz oben in `FUZZY_MAP_pre` kann einen bestimmten Eingabestring (z. B. ein einfaches Kommandowort) erkennen, sofort verarbeiten und damit die gesamte nachfolgende Kaskade für dieses Token blockieren. Dies ermöglicht die Konfiguration von einfachen Kommandos oder Zuständen, die nur dos Worte/Befehle zulassen.

### 2. Integración de complejos y frameworks

El tiempo que se utiliza para implementar la implementación del complejo, las modificaciones que se pueden realizar y las modificaciones específicas del marco (como CodeIgniter o otros) incluyen:

* **Kumulación:** Durch die Kumulation können mehrere Regeln sequenziell auf den Text angewendet werden, um beispielsweise die Benennungskonventionen oder Platzhalter eines Frameworks schrittweise in eine gewünschte Ausgabe zu überführen.
* **Complementos:** La lógica jerárquica entre `plugins/` está segura, ya sea para proyectos específicos o para marcos específicos (por ejemplo, para CodeIgniter) y también se pueden utilizar módulos separados. Este plug-in-regeln tiene una definición definida, sin prioridad alguna en el Kern-Sprachregeln, wodurch die Kernlogik unangetastet bleibt, aber das Verhalten gezielt erweitert werden kann.

**Fazit:** Ob es sich um die binäre Umschaltung von Steuerwörtern oder the Detaillierte Anpassung and die Konventionen eines komplexen Frameworks handelt – die Hierarchie der Prioritäten (Modul > Zeile) und die Steuerung durch das Stopp-Kriterium des Full Match bieten die nötige Kontrolle über den Verarbeitungsprozess.