# 🧠 SL5 Aura Hybrid-Modus: Lokale LLM-Integration

**Status:** Experimentell / Stable
**Technologie:** Ollama (Llama 3.2) + Python Subprocess
**Datenschutz:** 100% Offline

## Das Konzept: "Architekt & Praktikant"

Aura basiert traditionell auf deterministischen Regeln (RegEx) – schnell, präzise, vorhersagbar. Das ist der "Architekt". Doch manchmal will der Nutzer etwas "Unscharfes" (Fuzzy) fragen, wie *"Erzähl einen Witz"* oder *"Fasse diesen Text zusammen"*.

Hier kommt das **Local LLM Plugin** ins Spiel (der "Praktikant"):
1.  **Aura (RegEx)** prüft zuerst alle strikten Befehle ("Licht an", "App öffnen").
2.  Wenn nichts passt **UND**/**ODER** ein Trigger-Wort (z.B. "Aura ...") erkannt wird, greift die Fallback-Regel.
3.  Der Text wird an eine lokale KI (Ollama) gesendet.
4.  Die Antwort wird bereinigt und via TTS oder Text-Output ausgegeben.

---

## 🛠 Voraussetzungen

Das Plugin benötigt eine laufende Instanz von [Ollama](https://ollama.com/), die lokal auf dem Rechner läuft.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Modell laden (Llama 3.2 3B - nur ca. 2GB, sehr schnell)
ollama run llama3.2
```

---

## 📂 Struktur & Ladereihenfolge

Das Plugin liegt bewusst im Ordner `z_fallback_llm`.
Da Aura Plugins **alphabetisch** lädt, stellen wir so sicher, dass die LLM-Regel als **letztes** geladen wird. Sie dient als "Auffangnetz" (Safety Net).

**Pfad:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. Die Map (`FUZZY_MAP_pre.py`)

Wir nutzen einen **hohen Score (100)** und ein Trigger-Wort, um Aura zu zwingen, die Kontrolle abzugeben.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + beliebiger Text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. Der Handler (`ask_ollama.py`)

Dieses Skript kommuniziert mit der CLI von Ollama.
**Wichtig:** Es enthält eine `clean_text_for_typing` Funktion. Rohe LLM-Ausgaben enthalten oft Emojis (😂, 🚀), die Tools wie `xdotool` oder alte TTS-Systeme zum Absturz bringen können.

```python
# Auszug aus ask_ollama.py
def execute(match_data):
    # ... (Extraktion der Regex-Gruppe) ...
    
    # System-Prompt für kurze Antworten
    system_instruction = "Antworte auf Deutsch. Maximal 2 Sätze. Keine Emojis."
    
    # Subprocess Aufruf (blockiert kurzzeitig, Timeout beachten!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # WICHTIG: Bereinigung für Stabilität
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ Anpassungsmöglichkeiten

### Trigger ändern
Ändere die RegEx in `FUZZY_MAP_pre.py`, wenn du nicht "Aura" sagen willst.
*   Beispiel für Catch-All (alles, was Aura nicht kennt): `r'^(.*)$'`

### Modell wechseln
In `ask_ollama.py` kann das Modell einfach getauscht werden (z.B. zu `mistral` für komplexere Logik, benötigt aber mehr RAM).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### System Prompt (Persona)
Du kannst Aura eine Persönlichkeit geben, indem du `system_instruction` anpasst:
> "Du bist ein sarkastischer Assistent aus einem Sci-Fi Film."

---

## ⚠️ Bekannte Limitierungen

1.  **Latenz:** Der erste Aufruf kann 1-3 Sekunden dauern, da das Modell in den RAM geladen wird. Danach geht es schneller.
2.  **Konflikte:** Wenn die RegEx zu allgemein ist (`.*`), könnten Standard-Befehle verschluckt werden. Die alphabetische Sortierung (`z_...`) ist essenziell.
3.  **Hardware:** Benötigt ca. 2GB freien RAM für Llama 3.2.
