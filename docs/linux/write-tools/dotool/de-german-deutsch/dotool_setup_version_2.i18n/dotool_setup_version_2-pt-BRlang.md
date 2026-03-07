### Parte 1: Documentação Alemã

# dotool – Instalação e configuração (Manjaro / Arch-basiert)

## Foi dotool?
`dotool` é um trabalho para simulação de teste. A comunicação do `xdotool` é feita diretamente com o Kernel via `uinput` e funciona no universo de **X11 e Wayland**.

---

## Instalação (Manjaro/Arco)

### 1. Instalação do pacote
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. Conjuntos de Berechtigungen
Damit `dotool` ohne Root-Rechte tippen darf, muss dein User in the Gruppe `input` e um udev-Regel ativo sein:

1. **Usuário do Grupo:** `sudo gpasswd -a $USER input`
2. **udev-Regel:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Regeln neu laden:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Wichtig:** Danach einmal **aus- und neu einloggen**, damit die Gruppenrechte aktiv werden.

---

## Configuração no projeto (`config/settings.py`)

__CODE_BLOCO_3__

---

## Implementação no Skript

### Processo Persistente (FIFO)
Um dos Overhead durch ständiges Neuerstellen des virtullen Keyboards zu vermeiden, nutzt das Skript eine Pipe (FIFO). Dadurch reagiert `dotool` verzögerungsfrei.

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

### Die Eingabe-Funktion
__CODE_BLOCO_5__

---

## Hinweise & Fehlerbehebung
- **Fehlende Zeichen:** Quando umlaute foi lançado, use `dotool_typedelay` em 5 ou 10.
- **Fallback:** O `dotool` não foi configurado corretamente, o sistema é automaticamente adicionado ao `xdotool`.
- **Wayland-Support:** No Wayland o `dotool` é executado automaticamente e o `xdotool` não funciona.