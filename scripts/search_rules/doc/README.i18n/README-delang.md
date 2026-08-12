# Gewünschte Logik

# Alt+F und Alt+G

## **Logik**

Basierend auf der Beschreibung und der Analogie zu **Alt+F** sollte die Logik für **Alt+G** folgendermaßen aussehen:

### **1. Wechsel von Volltext → DITTO (`Alt+G`)**

- **Aktion**:
- Die aktuelle Suchanfrage („CURRENT_QUERY“) wird unter „SAVED_QUERY“ gespeichert.
- Suchfeld ist **geleert**.
- „DITTO_STATE“ ist auf „1“ gesetzt.
- GUI wird neu geladen

### **2. Im DITTO-Modus**

- **Bei jeder Eingabe (Tastendruck)**:
- Der DITTO-Modus wird **automatisch verlassen** (`DITTO_STATE="0"`).
- GUI wird neu geladen
- Suchfeld bleibt **leer** (keine Wiederherstellung von „SAVED_QUERY“).

### **3. Wechsel von DITTO → Volltext (erneut „Alt+G“)**

- **Aktion**:
- „DITTO_STATE“ ist auf „0“ gesetzt.
- GUI wird neu geladen
- „SAVED_QUERY“ wurde **wiederhergestellt**.


---


### **Alt+F Logik**

- **Wechsel vom Volltext → 1/Dateimodus**: