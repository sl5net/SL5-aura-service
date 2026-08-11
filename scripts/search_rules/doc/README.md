# Desired Logic

# Alt+F and Alt+G

## **Logic**

Based on description and the analogy with **Alt+F**, the logic for **Alt+G** should look like this:

### **1. Switching from Full-Text → DITTO (`Alt+G`)**

- **Action**:
- Current search query (`CURRENT_QUERY`) is saved to `SAVED_QUERY`. 
- Search field is **cleared**. 
- `DITTO_STATE` is set to `"1"`.
- GUI reloads

### **2. In DITTO Mode**

- **On any input (keystroke)**:
- DITTO mode is **automatically exited** (`DITTO_STATE="0"`). 
- GUI reloads
- Search field remains **empty** (no restoration of `SAVED_QUERY`).

### **3. Switching from DITTO → Full-Text (`Alt+G` again)**

- **Action**:
- `DITTO_STATE` is set to `"0"`. 
- GUI reloads
- `SAVED_QUERY` is **restored**. (this step not works at the moment 11.8.'26 22:18 Tue)


---

## **Alt+F Works and Alt+G Doesn't at 11.8.'26 22:18 Tue**

Since **Alt+F** works correctly, we can adopt the **same logic** for **Alt+G**. 

### **Alt+F Logic (Works)**

- **Switching from Full-Text → 1/File Mode**:

