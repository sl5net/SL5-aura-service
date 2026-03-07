## Configuração do método de entrada de texto

### Voraussetzungen para `dotool` (schneller como xdotool)

1. Instalação: `pamac build dotool` ou `yay -S dotool`
2. Usuário no grupo de entrada adicionado: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Regeln neu carregado: `sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **Neu einloggen**

### Configuração

Em `config/settings.py`:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

###Hinweise

- `dotool` ist deutlich schneller as `xdotool` – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- As configurações das configurações são exibidas junto com todos os arquivos de impressão em `settings.py` no final das importações – isso é feito
- O ouvinte dotool é usado no processo de referência sobre um FIFO (`/tmp/dotool_fifo`) com `typedelay 0`

---