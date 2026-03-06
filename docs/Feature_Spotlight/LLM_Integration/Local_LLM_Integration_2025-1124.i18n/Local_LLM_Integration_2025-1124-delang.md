# 🧠 SL5 Aura Hybrid-Modus: Lokale LLM-Integration

**Status:** Experimentell / Stabil
**Technologie:** Ollama (Llama 3.2) + Python-Unterprozess
**Datenschutz:** 100 % offline

## Das Konzept: „Architekt & Praktikant“

Traditionell basiert Aura auf deterministischen Regeln (RegEx) – schnell, präzise und vorhersehbar. Das ist der **„Architekt“**. Manchmal möchte der Benutzer jedoch etwas „Unscharfes“ oder Kreatives fragen, wie zum Beispiel *„Erzähl mir einen Witz“* oder *„Diesen Text zusammenfassen“*.

Hier kommt das **Local LLM Plugin** ins Spiel (der **„Intern“**):
1. **Aura (RegEx)** überprüft zunächst alle strengen Befehle („Lichter einschalten“, „App öffnen“).
2. Wenn nichts mit **AND**/ **OR** einem bestimmten Auslösewort (z. B. „Aura ...“) übereinstimmt, wird die Fallback-Regel aktiviert.
3. Der Text wird an ein lokales KI-Modell (Ollama) gesendet.
4. Die Antwort wird bereinigt und über TTS oder Texteingabe ausgegeben.

---

## 🛠 Voraussetzungen

Das Plugin erfordert eine laufende Instanz von [Ollama](https://ollama.com/), die lokal auf dem Computer ausgeführt wird.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 Struktur und Ladereihenfolge

Das Plugin wird absichtlich im Ordner „z_fallback_llm“ abgelegt.
Da Aura Plugins **alphabetisch** lädt, stellt diese Benennung sicher, dass die LLM-Regel **zuletzt** geladen wird. Es dient als „Sicherheitsnetz“ für unerkannte Befehle.

**Pfad:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. Die Karte (`FUZZY_MAP_pre.py`)

Wir verwenden einen **Highscore (100)** und ein Triggerwort, um Aura zu zwingen, die Kontrolle an das Drehbuch zu übergeben.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. Der Handler (`ask_ollama.py`)

Dieses Skript kommuniziert mit der Ollama-CLI.
**Wichtig:** Es enthält eine Funktion „clean_text_for_typing“. Rohe LLM-Ausgaben enthalten häufig Emojis (😂, 🚀) oder Sonderzeichen, die Tools wie „xdotool“ oder ältere TTS-Systeme zum Absturz bringen können.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ Anpassungsoptionen

### Den Auslöser ändern
Ändern Sie den RegEx in „FUZZY_MAP_pre.py“, wenn Sie „Aura“ nicht als Aktivierungswort verwenden möchten.
* Beispiel für ein echtes Catch-All (alles, was Aura nicht weiß): `r'^(.*)$'' (Achtung: Passen Sie die Punktzahl an!)

### Das Modell austauschen
Sie können das Modell in „ask_ollama.py“ problemlos austauschen (z. B. zu „mistral“ für komplexere Logik, obwohl dafür mehr RAM erforderlich ist).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### Systemaufforderung (Persona)
Sie können Aura eine Persönlichkeit verleihen, indem Sie die „system_instruction“ anpassen:
> „Du bist ein sarkastischer Assistent aus einem Science-Fiction-Film.“

---

## ⚠️ Bekannte Einschränkungen

1. **Latenz:** Die allererste Anfrage nach dem Booten kann 1–3 Sekunden dauern, während das Modell in den RAM geladen wird. Nachfolgende Anfragen erfolgen schneller.
2. **Konflikte:** Wenn RegEx zu breit ist („.*“) und keine ordnungsgemäße Ordnerstruktur aufweist, kann es sein, dass es Standardbefehle verschluckt. Die alphabetische Reihenfolge („z_...“) ist wichtig.
3. **Hardware:** Benötigt ca. 2 GB freier RAM für Llama 3.2.