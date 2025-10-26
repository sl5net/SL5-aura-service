# Erweiterte Regelaktionen: Ausführen von Python-Skripten

In diesem Dokument wird beschrieben, wie Sie die Funktionalität einfacher Textersetzungsregeln durch die Ausführung benutzerdefinierter Python-Skripte erweitern können. Mit dieser leistungsstarken Funktion können Sie dynamische Antworten erstellen, mit Dateien interagieren, externe APIs aufrufen und komplexe Logik direkt in Ihren Spracherkennungs-Workflow implementieren.

## Das Kernkonzept: „on_match_exec“.

Anstatt nur Text zu ersetzen, können Sie jetzt eine Regel anweisen, ein oder mehrere Python-Skripte auszuführen, wenn ihr Muster übereinstimmt. Dies erfolgt durch Hinzufügen eines „on_match_exec“-Schlüssels zum Optionswörterbuch der Regel.

Die Hauptaufgabe des Skripts besteht darin, Informationen über die Übereinstimmung zu empfangen, eine Aktion auszuführen und eine endgültige Zeichenfolge zurückzugeben, die als neuer Text verwendet wird.

### Regelstruktur

Eine Regel mit einer Skriptaktion sieht folgendermaßen aus:

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**Wichtige Punkte:**
– Der „on_match_exec“-Wert muss eine **Liste** sein.
- Skripte befinden sich im selben Verzeichnis wie die Map-Datei, weshalb `CONFIG_DIR / 'script_name.py'` die empfohlene Methode zur Definition des Pfades ist.

---

## Erstellen eines ausführbaren Skripts

Damit das System Ihr Skript verwenden kann, muss es zwei einfache Regeln befolgen:
1. Es muss eine gültige Python-Datei sein (z. B. „my_script.py“).
2. Es muss eine Funktion namens „execute(match_data)“ enthalten.

### Die Funktion „execute(match_data)“.

Dies ist der Standard-Einstiegspunkt für alle ausführbaren Skripte. Das System ruft diese Funktion automatisch auf, wenn die Regel übereinstimmt.

- **`match_data` (dict):** Ein Wörterbuch, das den gesamten Kontext zum Match enthält.
- **Rückgabewert (str):** Die Funktion **muss** einen String zurückgeben. Diese Zeichenfolge wird zum neuen verarbeiteten Text.

### Das `match_data`-Wörterbuch

Dieses Wörterbuch ist die Brücke zwischen der Hauptanwendung und Ihrem Skript. Es enthält die folgenden Schlüssel:

* „original_text“ (str): Die vollständige Textzeichenfolge *bevor* eine Ersetzung aus der aktuellen Regel angewendet wurde.
* „text_after_replacement“ (str): Der Text *nach* der grundlegenden Ersetzungszeichenfolge der Regel angewendet wurde, aber *bevor* Ihr Skript aufgerufen wurde. (Wenn die Ersetzung „None“ lautet, ist dies dasselbe wie „original_text“).
* „regex_match_obj“ (re.Match): Das offizielle Python-Regex-Match-Objekt. Dies ist äußerst leistungsstark für den Zugriff auf **Erfassungsgruppen**. Sie können „match_obj.group(1)“, „match_obj.group(2)“ usw. verwenden.
* „rule_options“ (dict): Das vollständige Optionswörterbuch für die Regel, die das Skript ausgelöst hat.

---

## Beispiele

### Beispiel 1: Aktuelle Uhrzeit abrufen (dynamische Antwort)

Dieses Skript gibt eine personalisierte Begrüßung basierend auf der Tageszeit zurück.

**1. Die Regel (in Ihrer Kartendatei):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. Das Skript (`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**Verwendung:**
> **Eingabe:** „Wie spät ist es?“
> **Ausgabe:** „Guten Tag! Es ist derzeit 14:30.“

### Beispiel 2: Einfacher Rechner (mit Capture-Gruppen)

Dieses Skript verwendet Capture-Gruppen aus dem regulären Ausdruck, um eine Berechnung durchzuführen.

**1. Die Regel (in Ihrer Kartendatei):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2. Das Skript (`calculator.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**Verwendung:**
> **Eingabe:** „55 plus 10 berechnen“
> **Ausgabe:** „Das Ergebnis ist 65.“

### Beispiel 3: Persistente Einkaufsliste (Datei-I/O)

Dieses Beispiel zeigt, wie ein Skript mehrere Befehle (Hinzufügen, Anzeigen) verarbeiten kann, indem es den Originaltext des Benutzers überprüft, und wie es Daten beibehalten kann, indem es in eine Datei schreibt.

**1. Die Regeln (in Ihrer Kartendatei):**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2. Das Skript (`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**Verwendung:**
> **Eingabe 1:** „Milch zur Einkaufsliste hinzufügen“
> **Ausgabe 1:** „Okay, ich habe ‚Milch‘ zur Einkaufsliste hinzugefügt.“
>
> **Eingabe 2:** „Einkaufsliste anzeigen“
> **Ausgabe 2:** „Auf der Liste steht: Milch.“

---

## Best Practices

- **Ein Job pro Skript:** Skripte konzentrieren sich auf eine einzelne Aufgabe (z. B. berechnet „calculator.py“ nur).
- **Fehlerbehandlung:** Schließen Sie die Logik Ihres Skripts immer in einen „try...exclusive“-Block ein, um zu verhindern, dass die gesamte Anwendung abstürzt. Gibt eine benutzerfreundliche Fehlermeldung aus dem „Exception“-Block zurück.
- **Externe Bibliotheken:** Sie können externe Bibliotheken (wie „requests“ oder „wikipedia-api“) verwenden, müssen jedoch sicherstellen, dass diese in Ihrer Python-Umgebung installiert sind („pip install <library-name>“).
- **Sicherheit:** Beachten Sie, dass diese Funktion jeden Python-Code ausführen kann. Verwenden Sie nur Skripte aus vertrauenswürdigen Quellen.