# Kaskadierende Regelausführung und Mechanismen

Alle notwendigen Details, um das komplexe Zusammenspiel von Priorität, Modus und Fallback zu erklären.

---

# Kaskadierende Regelausführung und Mechanismen

Unser Regelsystem basiert auf einer strengen, sequenziellen Verarbeitung, bei der die Position einer Regel in der Liste `fuzzy_map_pre` ihre Priorität bestimmt (Modul-Lade-Reihenfolge > Zeilennummer).

Dies folgt dem Prinzip der **Kaskadierenden Regelausführung** (`default_mode_is_all = True`), wobei alle Regeln passend nacheinander angewendet werden, bis ein spezifisches Stopp-Kriterium erfüllt ist.

## 1. Die Hohe Priorität: Der deterministische Durchlauf

Die Verarbeitung beginnt mit dem Durchlauf der Regeln in der geladenen Reihenfolge. Hier gibt es zwei Typen von Anwendungen, die die Priorität festlegen:

### A. Absolutes Stopp-Kriterium (Höchste Priorität)
Die Regel mit der höchsten Priorität erzielt, die einen **vollständigen Match** (von `^` bis `$`) auf das Token, wird angewendet und beendet die gesamte Verarbeitung für dieses Token sofort (**First Match Wins**). Dies stellt sicher, dass die spezifischste und deterministischste Regel Vorrang hat.

### B. Kumulation (Transformationsreihenfolge)
Wenn eine Regel zutrifft, aber kein vollständiger Match (`^...$`) erzielt wird, wird die Ersetzung angewendet. Die Verarbeitung geht jedoch zur nächsten Regel über. Da jede Regel auf dem **bereits modifizierten** Text arbeitet, ist die Listenreihenfolge entscheidend für die **Kaskadierung** der Transformationen.

## 2. Die niedrige Priorität: Der Fuzzy-Fallback

Der Einsatz der Fuzzy-Logik (Ähnlichkeitsscore 0–100) dient ausschließlich als Fallback, um Tippfehler im Rohtext zu korrigieren.

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** aktiviert, wenn der gesamte deterministische Durchlauf (Punkt 1) **keine einzige Regel** hat. Jede erfolgreiche deterministische Regelanwendung setzt die notwendige Flagge und **blockiert** damit den Fuzzy-Fallback für das aktuelle Token.

## 3. Die externe Validierung (LanguageTool)

Nach Abschluss aller regelbasierten Übersetzungen wird eine Prüfung durch LanguageTool (LT) durchgeführt, um stilistische oder grammatikalische Fehler zu beheben.

Dieses Tool wird jedoch übersprungen, wenn die Anzahl der durchgeführten Regel-Ersetzungen im Verhältnis zur ursprünglichen Textlänge einen Schwellenwert übersteigt (`LT_SKIP_RATIO_THRESHOLD`). Dies stellt sicher, dass LT nicht auf Texte angewendet wird, die durch unsere Kaskade bereits so stark transformiert wurden, dass die Korrektur durch LT fehleranfällig wäre.