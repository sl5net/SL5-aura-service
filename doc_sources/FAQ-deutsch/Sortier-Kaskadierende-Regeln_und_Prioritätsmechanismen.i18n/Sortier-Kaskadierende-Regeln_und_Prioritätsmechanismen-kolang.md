# Kaskadierende Regelausführung 및 우선 순위 메커니즘

Alle notwendigen Details, um das komplexe Zusammenspiel von Priorität, Modus und Fallback zu erklären.

---

# Kaskadierende Regelausführung 및 우선 순위 메커니즘

Regelsystem을 기본으로 실행하고 순차적으로 실행하면 가장 좋은 우선순위(Modul-Lade-Reihenfolge > Zeilennummer)에 따라 목록 `fuzzy_map_pre`에 위치 einer Regel이 배치됩니다.

Dies folgt dem Prinzip der **Kaskadierenden Regelausführung** (`default_mode_is_all = True`), wobei alle passenden Regeln nacheinander angewendet werden, bis ein spezifisches Stopp-Kriterium erfüllt ist.

## 1. 최우선 순위: Der Deterministische Durchlauf

Die Verarbeitung은 geladenen Reihenfolge에서 Durchlauf der Regeln과 함께 시작되었습니다. Hierbei gibt es zwei Typen von Anwendungen, die die Priorität festlegen:

### A. 절대 중지 기준(Höchste Priorität)
Die Regel mit der höchsten Priorität, die einen **vollständigen Match** (von `^` bis `$`) auf das Token erzielt, wird angewendet und beendet die gesamte Verarbeitung für dieses Token sofort (**첫 번째 매치 승리**). Dies stellt sicher, dass die spezifschste und determinististste Regel Vorrang hat.

### B. Kumulation(Transformationsreihenfolge)
Wenn eine Regel zutrifft, aber keinen vollständigen Match (`^...$`) erzielt, wird die Ersetzung angewendet. Die Verarbeitung geht jedoch zur nächsten Regel über. Da jede Regel auf dem **bereits modifizierten** Text arbeitet, ist die Listenreihenfolge entscheidend für die **Kaskadierung** der Transformationen.

## 2. 우선 순위: 퍼지 폴백(Der Fuzzy-Fallback)

Der Einsatz der Fuzzy-Logik(ähnlichkeitsscore 0–100) dient ausschließlich als Fallback, um Tippfehler im Rohtext zu korrigieren.

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** aktiviert, wenn der gesamte deterministische Durchlauf(Punkt 1) **keine einzige Regel** angewendet hat. Jede는 결정론적으로 플래그를 설정하고 **차단**하여 실제 토큰에 대한 퍼지 폴백을 설정했습니다.

## 3. 외부 유효성 검사(LanguageTool)

Nach Abschluss aller Regel-basierten Ersetzungen wird eine zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um stilistische oder grammatikalische Fehler zu beheben.

Dieses Tool wird jedoch übersprungen, wenn die Anzahl der durchgeführten Regel-Ersetzungen im Verhältnis zur ursprünglichen Textlänge einen Schwellenwert übersteigt (`LT_SKIP_RATIO_THRESHOLD`). Dies stellt sicher, dass LT nicht auf Texte angewendet wird, die durch unsere Kaskade bereits so stark Transformert wurden, dass die Korrektur durch LT fehleranfällig wäre.