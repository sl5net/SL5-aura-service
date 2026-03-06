# 🧠 SL5 Aura: Erweiterte 오프라인 LLM 통합

**상태:** 생산 개시
**엔진:** 올라마(Llama 3.2 3B)
**Latenz:** Sofort(<0.1초 캐시 적중) / ~20초(CPU 생성)

## 1. "Architekt & Praktikant" 철학 죽기
Aura nutzt ein Hybrid-Modell, 음 **Präzision** 및 **Flexibilität** zu vereinen:
* **Der Architekt(RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle("Browser öffnen", "Lauter").
* **Der Praktikant(Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. 활동을 시작하려면 Regel greift를 사용하세요.

---

## 2. 성능-건축

Um ein lokales LLM auf Normalen CPUs (ohne GPU) nutzbar zu machen, setzen wir auf eine **3-Stufen-Strategie**:

### Stufe 1: Der "Instant Modus"(Schlagworte)
* **트리거:** "Instant", "Schnell", "Sofort"를 선택하세요.
* **논리:** Umgeht das LLM komplett. Vergleicht Schlagworte der Eingabe direct mit der SQLite-Datenbank.
* **라텐츠:** **< 0.05초**

### Stufe 2: 지능적인 캐시(SQLite)
* **로직:** Jeder Prompt wird gehasht(SHA256). Anfrage와 Ollama는 `llm_cache.db`를 통해 확인할 수 있습니다.
* **"활성 변형" 기능:** Auch bei einem Cache-Treffer generiert das System manchmal (20% Chance) proaktiv eine *neue* Antwort-Variante. Ziel: ~5 Varianten pro Frage für mehr Lebendigkeit.
* **"의미론적 해싱" 기능:** Bei langen Fragen (>50 Zeichen) extrahiert das LLM zuerst 키워드(z.B. "installation anleitung") 및 해시 다이제. 그래서 "Wie installiere ich es?"라고 묻습니다. 그리고 "Installationshilfe bitte"는 동일합니다.
* **라텐츠:** **~0.1초**

### Stufe 3: Die API 생성(대체)
* **로직:** 캐시가 존재하는지 확인하고 Ollama API(`http://localhost:11434/api/generate`)를 사용하세요.
* **최적화:**
* **엄격한 제한:** `num_predict=60` zwingt das Modell, nach ca. 40 Wörtern zu stoppen.
* **입력 배관:** Große Texte(README) werden über STDIN übergeben, um Argumenten-Limits des Betriebssystems zu umgehen.
* **Latenz:** **~15-25s** (CPU에 따라 다름)

---

## 3. 시스템 접지(환각 방지)

Generische LLM은 종종 GUI(버튼, 메뉴)를 사용합니다. Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**:

1. **Keine GUI:** Aura는 Headless CLI 기반입니다.
2. **Keine 구성 파일:** Logik ist reiner Python-Code, kein `.json`/`.xml`.
3. **트리거:** Dateisystem-Events에 대한 외부 제어(`touch /tmp/sl5_record.trigger`), API에 적합하지 않습니다.
4. **설치:** Dauert real 10-20 Min wegen 4GB 모델 다운로드(verhindert falsche Versprechen).

---

## 4. 다이 클립보드 브리지(Linux 보안)

Hintergrunddienste (systemd) können aus Sicherheitsgründen oft nicht auf die Zwischenablage (X11/Wayland) zugreifen.
* **요성:** 사용자 세션(`clipboard_bridge.sh`)의 스크립트는 RAM 디스크 날짜(`/tmp/aura_clipboard.txt`)에 흡입됩니다.
* **Aura:** Liest diese Datei und umgeht so alle Rechte-Probleme.

---

## 5. Selbst-Lernen(캐시 워밍)

스크립트 `warm_up_cache.py`에 대해 알아보세요:
1. 가장 중요한 것은 프로젝트의 `README.md`입니다.
2. Es beauftragt das LLM, sich wahrscheinliche User-Fragen auszudenken.
3. Es stellt diese Fragen an Aura, um die Datenbank automatisch zu befüllen.