das **README sollte unbedingt aktualisiert werden**, da **Kern der Leistungsfähigkeit und der Erweiterbarkeit** im aktuellen Text noch nicht sichtbar ist.

Das aktuelle README beschreibt lediglich *was* passiert (z.B. "Intelligent Pre-Correction"), erklärt aber nicht *wie* es funktioniert (Priorität, Stopp-Kriterien, Kumulation), was für potenzielle Nutzer und Entwickler, die eigene Regeln schreiben möchten, extrem wichtig ist.

Hier sind die vorgeschlagenen Aktualisierungspunkte und wie sie in das bestehende README integriert werden könnten:

---

## 1. Ergänzung unter "Key Features"

Fügen Sie einen Punkt hinzu, der die **Kontrolle und Erweiterbarkeit** durch die Konfigurationslogik hervorhebt:

| Vorherige Features | Ergänzungsvorschlag |
| :--- | :--- |
| **Offline & Private:** 100% local. | **Konfigurationsgetriebene Logik:** Ermöglicht die Erweiterung und Anpassung der Textverarbeitung (wie Sprachbefehle oder Code-Konvertierungen) ausschließlich über **Regel-Konfigurationen** (Fuzzy Maps), ohne dass Programmierung erforderlich ist. |
| **Cross-Platform:** Works on Linux, macOS, and Windows. | |

## 2. Detaillierung der Textverarbeitung (Wichtigste Änderung)

Der Abschnitt unter `STT-Core/ -> Text Processing & Correction/` ist der Ort, um die Logik zu erklären. Wir können Punkt 2 und 4 detaillierter fassen:

| Alter Text | Neuer Textvorschlag |
| :--- | :--- |
| **2. Intelligent Pre-Correction** (`FuzzyMap Pre` - applied before LT for performance) 🐧 🍏 🪟 | **2. Intelligente Prä-Korrektur (Hohe Priorität):** (`FuzzyMap Pre`) Angewendet **vor** LanguageTool zur sofortigen Ersetzung und Kommandoerkennung. Hier bestimmt die **Reihenfolge der Regeln** (Modul > Zeile) die Priorität. Die Kaskade kann durch einen **Full Match (^...$)** sofort gestoppt werden, was eine zuverlässige Befehlssteuerung ermöglicht. |
| | **(Neu: Erklärung der Logik)** Die Regeln arbeiten kaskadierend/kumulativ, wobei jede Regel auf dem Ergebnis der vorherigen Regel aufbaut. |
| **4. Intelligent Post-Correction** (`FuzzyMap` - applied behind LT) 🐧 🍏 🪟 | **4. Intelligente Post-Korrektur (Niedrige Priorität):** (`FuzzyMap`) Angewendet **nach** LanguageTool, um LT-spezifische Ausgaben final anzupassen. Auch hier gilt die kaskadierende Prioritätslogik. |
| | **(Neu: Fuzzy & LT-Steuerung)** |
| | • **Fuzzy-Fallback:** Die Fuzzy-Ähnlichkeitslogik (z.B. 85%) dient ausschließlich als **Fallback** für Tippfehler im Rohtext und wird nur dann aktiviert, wenn im deterministischen Durchlauf **keine einzige Regel** angewendet wurde. |
| | • **LT-Überspringlogik:** LanguageTool wird übersprungen, wenn die Anzahl der durchgeführten Regel-Ersetzungen im Verhältnis zur Textlänge einen Schwellenwert (`LT_SKIP_RATIO_THRESHOLD`) übersteigt, um die Anwendung von LT auf stark transformierte Texte zu verhindern. |

## 3. Ergänzung unter "Advanced Configuration"

Hier kann die mächtige Rolle der Plug-in-Struktur und der Konfiguration hervorgehoben werden:

| Alter Text | Ergänzungsvorschlag |
| :--- | :--- |
| **Advanced Configuration (Optional)** ... This `settings_local.py` file is (maybe) ignored by Git... | **Advanced Configuration (Optional)** ... |
| | **Plug-in Struktur und Priorität:** Die Logik ist so aufgebaut, dass Plug-ins (im Ordner `plugins/`) die niedrigste Priorität haben (alphabetische Sortierung), wodurch sie die Kern-Sprachregeln erweitern oder überschreiben können, ohne diese zu beschädigen. Dies ermöglicht die einfache Integration von anwendungsspezifischen Regeln (z.B. für CodeIgniter oder Spiele-Kommandos). |

---

**Fazit:** Die Aktualisierung dieser drei Bereiche würde das README von einer reinen Funktionsliste in eine **Erklärung der architektonischen Leistungsfähigkeit** verwandeln, was den Wert des Systems – insbesondere die einfache Konfigurierbarkeit und die hohe Kontrolle über die Texttransformation – viel deutlicher macht.

(S,24.10.'25 12:11 Fri)
