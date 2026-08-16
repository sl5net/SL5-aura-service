# 🧠 SL5 Aura: Erweiterte Offline-LLM-Integration

**Status:** Produktionsbereit
**Motor:** Ollama (Llama 3.2 3B)
**Latenz:** Sofort (<0,1s bei Cache Hit) / ~20s (Generierung auf CPU)

## 1. Die „Architekt & Praktikant“ Philosophie
Aura nutzt ein Hybrid-Modell, um **Präzision** und **Flexibilität** zu vereinen:
* **Der Architekt (RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle ("Browser öffnen", "Lauter").
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. Wird nur aktiv, wenn keine Regel greift.

---

## 2. Performance-Architektur

Um ein lokales LLM auf normalen CPUs (ohne GPU) nutzbar zu machen, setzen wir auf eine **3-Stufen-Strategie**:

### Stufe 1: Der „Instant Modus“ (Schlagworte)
* **Trigger:** Wörter wie „Instant“, „Schnell“, „Sofort“.
* **Logik:** Umgeht das LLM komplett. Vergleicht Schlagworte der Eingabe direkt mit der SQLite-Datenbank.
* **Latenz:** **< 0,05s**

### Stufe 2: Der Intelligente Cache (SQLite)
* **Logik:** Jeder Prompt wird gehasht (SHA256). Vor jeder Anfrage an Ollama wird die `llm_cache.db` geprüft.
* **Feature "Active Variation":** Auch bei einem Cache-Treffer generiert das System manchmal (20% Chance) proaktiv eine *neue* Antwort-Variante. Ziel: ~5 Varianten pro Frage für mehr Lebendigkeit.
* **Feature „Semantic Hashing“:** Bei langen Fragen (>50 Zeichen) führt das LLM zuerst Keywords (z.B. „Installationsanleitung“) aus und hasht diese. So werden „Wie installiere ich es?“ und „Installationshilfe bitte“ als identisch erkannt.
* **Latenz:** **~0,1s**

### Stufe 3: Die API-Generierung (Fallback)
* **Logik:** Wenn kein Cache vorhanden ist, rufen wir die Ollama API auf (`http://localhost:11434/api/generate`).
* **Optimierung:**
* **Hard Limits:** `num_predict=60` ändert das Modell, nach ca. 40 Wörtern zu stoppen.
* **Input Piping:** Große Texte (README) werden über STDIN übergeben, um Argumenten-Limits des Betriebssystems zu umgehen.
* **Latenz:** **~15-25s** (abhängig von CPU)

---

## 3. Systemerdung (Anti-Halluzination)

Generische LLMs finden sich oft in GUIs (Buttons, Menüs). Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**:

1. **Keine GUI:** Aura ist ein Headless CLI-Dienst.
2. **Keine Konfigurationsdateien:** Logik ist reiner Python-Code, kein `.json`/`.xml`.
3. **Trigger:** Externe Steuerung erfolgt über Dateisystem-Events (`touch /tmp/sl5_record.trigger`), nicht über APIs.
4. **Installation:** Dauert real 10-20 Min wegen 4GB Modelldownloads (verhindert falsches Versprechen).

---

## 4. Die Clipboard Bridge (Linux-Sicherheit)

Hintergrunddienste (systemd) können aus Sicherheitsgründen oft nicht auf die Zwischenablage (X11/Wayland) zugreifen.
* **Lösung:** Ein Skript in der User-Session (`clipboard_bridge.sh`) spiegelt den Inhalt in einer RAM-Disk-Datei (`/tmp/aura_clipboard.txt`) wider.
* **Aura:** Liest diese Datei und umgeht so alle Rechte-Probleme.

---

## 5. Selbst-Lernen (Cache Warming)

Wir nutzen das Skript `warm_up_cache.py`:
1. Es liegt die `README.md` des Projekts.
2. Es ist das LLM, sich wahrscheinlich User-Fragen auszudenken.
3. Diese Fragen stellen eine Aura dar, um die Datenbank automatisch zu füllen.