# Lógica deseada

# Alt+F y Alt+G

## **Lógica**

Según la descripción y la analogía con **Alt+F**, la lógica para **Alt+G** debería verse así:

### **1. Cambiando de Texto completo → DITTO (`Alt+G`)**

- **Acción**:
- La consulta de búsqueda actual (`CURRENT_QUERY`) se guarda en `SAVED_QUERY`.
- El campo de búsqueda está **limpio**.
- `DITTO_STATE` está establecido en `"1"`.
- recargas GUI

### **2. En modo ÍDITO**

- **En cualquier entrada (pulsación de tecla)**:
- El modo DITTO se **sale automáticamente** (`DITTO_STATE="0"`).
- recargas GUI
- El campo de búsqueda permanece **vacío** (no se restaura `SAVED_QUERY`).

### **3. Cambiando de DITTO → Texto completo (`Alt+G` nuevamente)**

- **Acción**:
- `DITTO_STATE` está establecido en `"0"`.
- recargas GUI
- `SAVED_QUERY` está **restaurado**.


---


### **Lógica Alt+F**

- **Cambiar de Texto completo → 1/Modo Archivo**: