# 🧠 SL5 Aura: Erweiterte Offline-LLM-Integration

**Status:** Produktionsbereit
**Motor:** Ollama (Llama 3.2 3B)
**Latenz:** Sofort (<0,1 s bei Cache-Treffer) / ~20 s (Generierung auf CPU)

## 1. Die „Architekt & Praktikant“-Philosophie
Aura arbeitet mit einem Hybridmodell, um **Präzision** und **Flexibilität** in Einklang zu bringen:
* **The Architect (RegEx/Python):** Deterministische, sofortige Ausführung für Systembefehle (z. B. „Browser öffnen“, „Lautstärke erhöhen“).
* **Der Praktikant (Local LLM):** Behandelt Fuzzy-Abfragen, Zusammenfassungen und Allgemeinwissen. Es wird nur ausgelöst, wenn keine strengen Regelübereinstimmungen oder bestimmte Schlüsselwörter verwendet werden.

---

## 2. Leistungsarchitektur

Um ein lokales LLM auf Standard-CPUs ohne GPU-Beschleunigung nutzbar zu machen, haben wir eine **3-Layer-Performance-Strategie** implementiert:

### Ebene 1: Der „Instant-Modus“ (Schlüsselwörter)
* **Auslöser:** Wörter wie „Instant“, „Schnell“, „Sofort“.
* **Logik:** Umgeht das LLM vollständig. Es vergleicht Benutzereingabeschlüsselwörter mit der lokalen SQLite-Datenbank unter Verwendung von Set-Schnittpunkten.
* **Latenz:** **< 0,05 s**

### Schicht 2: Der Smart Cache (SQLite)
* **Logik:** Jede Eingabeaufforderung wird gehasht (SHA256). Bevor wir Ollama fragen, überprüfen wir „llm_cache.db“.
* **Funktion „Aktive Variation“:** Selbst wenn ein Cache-Treffer vorliegt, generiert das System manchmal (20 % Chance) eine *neue* Variante, um verschiedene Formulierungen für dieselbe Frage zu lernen. Im Idealfall speichern wir ca. 5 Varianten pro Frage.
* **Funktion „Semantisches Hashing“:** Bei langen Fragen (>50 Zeichen) verwenden wir das LLM, um zuerst Schlüsselwörter zu extrahieren (z. B. „Installationsanleitung“) und diese anstelle des gesamten Satzes zu hashen. Dies entspricht „Wie installiere ich?“ mit „Installationsanleitung bitte“.
* **Latenz:** **~0,1 s**

### Schicht 3: Die API-Generierung (Fallback)
* **Logik:** Wenn kein Cache vorhanden ist, rufen wir die Ollama-API auf („http://localhost:11434/api/generate“).
* **Optimierung:**
* **Harte Grenzen:** „num_predict=60“ zwingt das Modell, nach ca. 40 Wörtern anzuhalten.
* **Eingabe-Piping:** Große Texte (README) werden über STDIN übergeben, um Beschränkungen der Betriebssystemargumente zu vermeiden.
* **Latenz:** **~15-25s** (CPU-abhängig)

---

## 3. Systemerdung (Anti-Halluzination)

Generische LLMs neigen dazu, GUI-Elemente (Schaltflächen, Menüs) zu erfinden. Wir fügen in jede Systemaufforderung ein striktes **`AURA_TECH_PROFILE`** ein:

1. **Keine GUI:** Aura ist ein Headless-CLI-Dienst.
2. **Keine Konfigurationsdateien:** Logik ist Python-Code, nicht `.json`/`.xml`.
3. **Trigger:** Die externe Steuerung funktioniert über die Dateierstellung („touch /tmp/sl5_record.trigger“), nicht über APIs.
4. **Installation:** Dauert aufgrund des Downloads des 4-GB-Modells 10 bis 20 Minuten (verhindert die Lüge „In 3 Sekunden installiert“).

---

## 4. Die Clipboard Bridge (Linux-Sicherheit)

Hintergrunddienste (systemd) können aufgrund der Sicherheitsisolation nicht direkt auf die X11/Wayland-Zwischenablage zugreifen.
* **Lösung:** Ein Benutzersitzungsskript („clipboard_bridge.sh“) spiegelt den Inhalt der Zwischenablage in eine RAM-Disk-Datei („/tmp/aura_clipboard.txt“).
* **Aura:** Liest diese Datei unter Umgehung aller Berechtigungsprobleme.

---

## 5. Selbstlernen (Cache-Erwärmung)

Wir stellen ein „warm_up_cache.py“-Skript zur Verfügung.
1. Es liest das Projekt „README.md“.
2. Es fordert den LLM auf, wahrscheinliche Benutzerfragen zum Projekt zu erfinden.
3. Es simuliert diese Fragen gegen Aura, um die Datenbank vorab zu füllen.