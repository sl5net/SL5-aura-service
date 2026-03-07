# dotool – Instalação e configuração (baseado em Manjaro/Arch)

## Visão geral
`dotool` é um utilitário de simulação de entrada de baixo nível. Ao contrário do `xdotool`, ele interage diretamente com o kernel Linux via `uinput`, tornando-o compatível com **X11 e Wayland**.

---

## Instalação (Manjaro/Arco)

### 1. Instale o pacote
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. Permissões e regras do udev
Para permitir que `dotool` simule entradas sem privilégios de root, seu usuário deve fazer parte do grupo `input` e uma regra do udev deve estar ativa:

1. **Adicionar usuário ao grupo:** `sudo gpasswd -a $USER input`
2. **Criar regra do udev:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Recarregue as regras do udev:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Importante:** Você deve **sair e fazer login novamente** para que as alterações do grupo entrem em vigor.

---

## Configuração do projeto (`config/settings.py`)

__CODE_BLOCO_3__

---

## Implementação de script

### Otimização de desempenho (FIFO)
Iniciar uma nova instância `dotool` para cada palavra é lento (latência de aproximadamente 100 ms). Para obter digitação "instantânea", o script usa um processo persistente em segundo plano lendo um canal FIFO.

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

### A função de digitação
__CODE_BLOCO_5__

---

## Solução de problemas e notas
- **Caracteres ausentes:** Se caracteres especiais (como tremas) forem ignorados, aumente `dotool_typedelay` para 5 ou 10.
- **Compatibilidade de aplicativos:** Alguns aplicativos (Electron, navegadores) podem exigir um atraso maior para registrar a entrada rápida corretamente.
- **Suporte Wayland:** `dotool` é o backend necessário para Wayland, pois `xdotool` não o suporta.
- **Fallback automático:** O script volta automaticamente para `xdotool` se `dotool` não estiver instalado ou configurado corretamente.