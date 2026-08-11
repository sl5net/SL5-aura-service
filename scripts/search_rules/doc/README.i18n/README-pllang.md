# Pożądana logika

# Alt+F i Alt+G

## **Logika**

Bazując na opisie i analogii z **Alt+F**, logika dla **Alt+G** powinna wyglądać następująco:

### **1. Przełączanie z pełnego tekstu → DITTO (`Alt+G`)**

- **Działanie**:
- Bieżące zapytanie („CURRENT_QUERY”) jest zapisywane w „SAVED_QUERY”.
- Pole wyszukiwania jest **wyczyszczone**.
- `DITTO_STATE` jest ustawione na `"1"`.
- Przeładowuje GUI

### **2. W trybie DITTO**

- **Na dowolnym wejściu (naciśnięcie klawisza)**:
- Tryb DITTO jest **automatycznie opuszczany** (`DITTO_STATE="0"`).
- Przeładowuje GUI
- Pole wyszukiwania pozostaje **puste** (nie ma możliwości przywrócenia `SAVED_QUERY`).

### **3. Przełączanie z DITTO → Pełny tekst (znowu „Alt+G”)**

- **Działanie**:
- `DITTO_STATE` jest ustawione na ``0''.
- Przeładowuje GUI
- `SAVED_QUERY` zostało **przywrócone**. (ten krok nie działa w tej chwili 11.8.'26 22:18 Wt)


---

## **Alt+F działa, a Alt+G nie działa o 11.8.'26 22:18 wtorek**

Ponieważ **Alt+F** działa poprawnie, możemy przyjąć **taką samą logikę** dla **Alt+G**.

### **Alt+F Logika (działa)**

- **Przełączanie z trybu pełnotekstowego → 1/pliku**: