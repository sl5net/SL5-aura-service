# 🧠 SL5 Aura Hybrid-Modus: Lokale LLM- und Zwischenablage-Integration

**Status:** Stabil
**Technologie:** Ollama (Llama 3.2) + File Bridge-Architektur
**Datenschutz:** 100 % offline

## Das Konzept: „Architekt & Praktikant“

Traditionell basiert Aura auf deterministischen Regeln (RegEx) – schnell und präzise. Das ist der **„Architekt“**.
Das **Local LLM Plugin** fungiert als **„Intern“**: Es verarbeitet Fuzzy-Anfragen, fasst Texte zusammen und beantwortet allgemeine Fragen.

## 🛠 Architektur: Die Clipboard Bridge

Aufgrund von Sicherheitsbeschränkungen in Linux (Wayland/X11) können Hintergrundprozesse (wie Aura) oft nicht direkt auf die Zwischenablage zugreifen. Wir haben dies mit einer **Brückenarchitektur** gelöst:

1. **Der Anbieter (Benutzersitzung):** Ein kleines Shell-Skript („clipboard_bridge.sh“) wird in der Sitzung des Benutzers ausgeführt. Es überwacht die Zwischenablage und spiegelt ihren Inhalt in eine temporäre Datei („/tmp/aura_clipboard.txt“).
2. **Der Verbraucher (Aura):** Das Python-Plugin liest diese Datei. Da der Dateizugriff universell ist, werden Berechtigungsprobleme umgangen.

---

## 🚀 Einrichtungsanleitung

### 1. Ollama installieren
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. Richten Sie das Bridge-Skript ein
Erstellen Sie „~/clipboard_bridge.sh“ und machen Sie es ausführbar:

```bash
#!/bin/bash
# Mirrors clipboard to a file in RAM
FILE="/tmp/aura_clipboard.txt"
while true; do
    if command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    else
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    fi
    sleep 1.5
done
```

**Wichtig:** Fügen Sie dieses Skript zu Ihrem System-Autostart hinzu!

### 3. Plugin-Logik (`ask_ollama.py`)

Das Skript befindet sich in `config/maps/plugins/z_fallback_llm/de-DE/`.
* **Auslöser:** Erkennt Wörter wie „Computer“, „Aura“, „Zwischenablage“, „Zusammenfassung“.
* **Speicher:** Behält eine „conversation_history.json“, um sich den Kontext zu merken (z. B. „Was habe ich gerade gefragt?“).
* **Prompt Engineering:** Priorisiert aktuelle Daten aus der Zwischenablage gegenüber historischen Konversationskontexten, um Halluzinationen vorzubeugen.

---

## 📝 Anwendungsbeispiele

1. **Text zusammenfassen:**
* *Aktion:* Kopieren Sie einen langen E-Mail- oder Website-Text (Strg+C).
* *Sprachbefehl:* „Computer, fassen Sie den Text in der Zwischenablage zusammen.“

2. **Übersetzung/Analyse:**
* *Aktion:* Kopieren Sie ein Code-Snippet.
* *Sprachbefehl:* „Computer, was macht der Code in der Zwischenablage?“

3. **Allgemeiner Chat:**
* *Sprachbefehl:* „Computer, erzähl mir einen Witz über Programmierer.“

4. **Speicher zurücksetzen:**
* *Sprachbefehl:* „Computer, vergiss alles.“ (Löscht den JSON-Verlauf).
  