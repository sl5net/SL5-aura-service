# Lógica Desejada

# Alt+F e Alt+G

## **Lógica**

Com base na descrição e na analogia com **Alt+F**, a lógica para **Alt+G** deve ser semelhante a esta:

### **1. Mudando de Texto Completo → Idem (`Alt+G`)**

- **Ação**:
- A consulta de pesquisa atual (`CURRENT_QUERY`) é salva em `SAVED_QUERY`.
- O campo de pesquisa está **limpo**.
- `DITTO_STATE` está definido como `"1"`.
- Recarregamentos da GUI

### **2. No modo DITTO**

- **Em qualquer entrada (pressionamento de tecla)**:
- O modo DITTO é **saído automaticamente** (`DITTO_STATE="0"`).
- Recarregamentos da GUI
- O campo de pesquisa permanece **vazio** (sem restauração de `SAVED_QUERY`).

### **3. Mudando de DITTO → Texto Completo (`Alt+G` novamente)**

- **Ação**:
- `DITTO_STATE` está definido como `"0"`.
- Recarregamentos da GUI
- `SAVED_QUERY` é **restaurado**.


---


### **Lógica Alt+F**

- **Mudando de Texto Completo → 1/Modo Arquivo**: