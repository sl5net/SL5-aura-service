# Kaskadierende Regelausführung und Priorität Mechanismen

Todos los detalles notwendigen, um das komplex Zusammenspiel von Priorität, Modus y Fallback zu erklären.

---

# Kaskadierende Regelausführung und Priorität Mechanismen

Unser Regelsystem basa auf einer strikten, sequenziellen Verarbeitung, bei der the Position einer Regel in der Liste `fuzzy_map_pre` ihre Priorität bestimmt (Modul-Lade-Reihenfolge > Zeilennummer).

De acuerdo con el principio de **Kaskadierenden Regelausführung** (`default_mode_is_all = True`), todas las reglas pasadas cambian cuando se cambia, y se cumple una orden de parada específica.

## 1. Die Hohe Priorität: Der Deterministische Durchlauf

Die Verarbeitung comenzó con el Durchlauf der Regeln in der geladenen Reihenfolge. Hierbei gibt es dos Typen von Anwendungen, die die Priorität festlegen:

### A. Absolutos Stopp-Kriterium (Höchste Priorität)
Die Regel mit der höchsten Priorität, die einen **vollständigen Match** (von `^` bis `$`) auf das Token erzielt, wird angewendet und beendet die gesamte Verarbeitung für dieses Token sofort (**First Match Wins**). Dies stellt sicher, dass die spezifischste und deterministischste Regel Vorrang hat.

### B. Kumulación (Transformationsreihenfolge)
Cuando se selecciona un código, si no se activa Match (`^...$`), se cambiará el error. Die Verarbeitung geht jedoch zur nächsten Regel über. Da jede Regel auf dem **bereits modificazierten** Text arbeitet, ist die Listenreihenfolge entscheidend für die **Kaskadierung** der Transformationen.

## 2. La menor prioridad: el respaldo difuso

Der Einsatz der Fuzzy-Logik (puntuación de 0 a 100) es diferente al respaldo, un tippfehler im Rohtext zu korrigieren.

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** activiert, wenn der gesamte deterministische Durchlauf (Punkt 1) **keine einzige Regel** angewendet hat. Esta reglamentación determinista es muy tradicional, ya que establece la nueva bandera y **bloquea** el respaldo difuso para el token activo.

## 3. La validación externa (LanguageTool)

Nach Abschluss aller Regel-basierten Ersetzungen wird eine zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um stilistische oder grammatikalische Fehler zu beheben.

Esta herramienta no tendrá ningún efecto excesivo, cuando el nivel de ajuste de los parámetros de regulación más estrictos en el ajuste de los textos modificados se supere (`LT_SKIP_RATIO_THRESHOLD`). Dies stellt sicher, dass LT nicht auf Texte angewendet wird, die durch unsere Kaskade bereits so starr transformiert wurden, dass die Korrektur durch LT fehleranfällig wäre.