# 🧠 SL5 Aura: Większa integracja offline LLM

**Stan:** Produktybereit
**Silnik:** Ollama (Lama 3.2 3B)
**Opóźnienie:** Sofort (<0,1 s przy trafieniu w pamięć podręczną) / ~20 s (generowanie przez procesor)

## 1. Filozofia „Architekt & Praktikant”.
Aura nutzt ein Hybrid-Modell, um **Präzision** i **Flexibilität** zu vereinen:
* **Der Architekt (RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle („Browser öffnen”, „Lauter”).
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. Wird nur aktiv, wenn keine strikte Regel greift.

---

## 2. Architektura wydajności

Um ein lokales LLM auf normalen CPUs (ohne GPU) nutzbar zu machen, setzen wir auf eine **3-Stufen-Strategie**:

### Krok 1: Der „Instant Modus” (Schlagworte)
* **Trigger:** Wörter wie „Instant”, „Schnell”, „Sofort”.
* **Logik:** Umgeht das LLM komplett. Vergleicht Schlagworte der Eingabe direkt mit der SQLite-Datenbank.
* **Latenz:** **< 0,05 s**

### Stufe 2: Inteligentna pamięć podręczna (SQLite)
* **Logik:** Jeder Prompt wird gehasht (SHA256). Vor jeder Anfrage i Ollama wird die `llm_cache.db` geprüft.
* **Funkcja „Aktywna odmiana”:** Auch bei einem Cache-Treffer generiert das System manchmal (20% szansy) proaktywnie *neue* Antwort-Variante. Miejsce: ~5 Varianten pro Frage für mehr Lebendigkeit.
* **Funkcja „Semantic Hashing”:** Bei langen fragen (>50 Zeichen) extrahiert das LLM zuerst Keywords (np. „installation anleitung”) i hasht diese. Więc werden "Wie installiere ich es?" i „Installationshilfe bitte” są również identyfikowane.
* **Latenz:** **~0,1 s**

### Stufe 3: Die API-Generierung (awaria)
* **Logika:** Wenn kein Cache istnieję, rufen wir die Ollama API (`http://localhost:11434/api/generate`).
* **Optymalizacja:**
* **Twarde limity:** `num_predict=60` zwingt das Modell, nach ca. 40 Wörtern zu stoppen.
* **Input Rurociąg:** Große Texte (README) werden über STDIN übergeben, um Argumenten-Limits des Betriebssystems zu umgehen.
* **Latenz:** **~15–25 s** (wyłączony procesor)

---

## 3. Uziemienie systemu (antyhalucynacja)

Generische LLMs tworzy często GUI (przyciski, menu). Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**:

1. **Keine GUI:** Aura jest dostępna w trybie Headless CLI.
2. **Keine Config-Files:** Logik to reiner Python-Code, taki jak `.json`/`.xml`.
3. **Wyzwalacz:** Zewnętrzny steuerung erfolgt über Dateisystem-Events (`touch /tmp/sl5_record.trigger`), nicht über API.
4. **Instalacja:** Prawdziwe 10-20 minut na pobranie modelu 4 GB (verhindert false Versprechen).

---

## 4. Most schowka Die (bezpieczeństwo systemu Linux)

Hintergrunddienste (systemd) können aus Sicherheitsgründen oft nicht auf die Zwischenablage (X11/Wayland) zugreifen.
* **Lösung:** Skript in der User-Session (`clipboard_bridge.sh`) spiegelt den Inhalt in eine RAM-Disk-Datei (`/tmp/aura_clipboard.txt`).
* **Aura:** Liest diese Datei und umgeht więc alle Rechte-Probleme.

---

## 5. Selbst-Lernen (ogrzewanie pamięci podręcznej)

Wir nutzen das Skript `warm_up_cache.py`:
1. Jest to plik `README.md` des Projekts.
2. Es beauftragt das LLM, sich wahrscheinliche User-Fragen auszudenken.
3. Es stellt diese Fragen an Aura, um die Datenbank automatisch zu befüllen.