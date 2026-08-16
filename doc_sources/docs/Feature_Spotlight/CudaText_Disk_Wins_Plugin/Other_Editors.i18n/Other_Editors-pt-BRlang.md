# Recarregar automaticamente em outros editores

Este documento descreve como configurar o recarregamento automático em dispositivos externos
alterações de arquivos em editores comuns — e por que isso muitas vezes **não é suficiente**
no modo Aura Oma.

---

##Kate (KDE)

### Configurar

1. **Configurações → Configurar Kate → Abrir/Salvar → Avançado**
2. Habilite:
- **"Recarregar arquivos automaticamente"**

### O que funciona

- Quando o buffer permanece **inalterado**, o Kate recarrega o arquivo imediatamente.
- Isto é suficiente para o modo de visualização puro.

### O que **não** funciona (e por que falha no modo Oma)

- Assim que você pressionar **uma única tecla** no buffer (mesmo que apenas uma
espaço ou pressionamento acidental de tecla), o buffer é considerado "modificado".
- A partir desse momento, Kate **sempre** pergunta sobre cada mudança externa:
> "O arquivo foi alterado externamente. Deseja recarregá-lo?"
- No Modo Oma, o usuário pode não estar no computador ou não ver o
diálogo — Aura continua escrevendo, mas o editor permanece na versão antiga.
- **Kate não tem configuração** que descarta silenciosamente alterações de buffer não salvas
a favor da versão em disco.

> **Resumindo:** Kate não é adequada para o Modo Oma assim que o usuário
> digita acidentalmente no editor.

---

## Código VS

### Configurar

Em `settings.json`:

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

### Limitações

- `autoSave` salva o buffer — ele sobrescreve as alterações do Aura com o
versão local, e não o contrário.
- Um prompt ainda aparece para alterações não salvas.
- Nenhuma opção para "disco sempre vence".

---

##Emacs

```elisp
(global-auto-revert-mode t)
```

### Limitações

- Recarrega automaticamente apenas quando o buffer não é alterado.
- Pergunta quando o buffer é modificado.

---

##Vim/Neovim

```vim
set autoread
au FocusGained,BufEnter,CursorHold * :checktime
```

### Limitações

- `autoread` só recarrega quando o buffer permanece inalterado.
- Não sobrescreve um buffer `modificado` automaticamente.

---

## CudaText (sem plugin)

Em `user.json`:

__CODE_BLOCO_3__

### Limitações

- Todos os valores de `ui_notif_confirm` (0–4) mostram alguma forma de prompt —
modal ou sem modal.
- Não há valor **no** que signifique: "Recarregue imediatamente, nunca pergunte."
- Portanto, o plugin `cuda_disk_wins` é necessário.

---

## Visão geral

| Editor | Recarga automática (inalterado) | Recarga automática (modificado) | Licença |
|--------|-------------|------------------------|---------|
| Kate | Sim | Sempre solicita | Código aberto |
| Código VS | Sim | Sempre solicita | Código aberto |
| Texto Sublime | Sim | Sempre solicita | Proprietário |
| Emacs | Sim | Sempre solicita | Código aberto |
| Vim | Sim | Sempre solicita | Código aberto |
| CudaText (sem plugin) | Sim | Sempre solicita | Código aberto |
| **CudaText + vitórias em disco** | Sim | **Sem aviso** | Código aberto |

---

## Por que nenhum editor pode fazer isso imediatamente

Descartar silenciosamente alterações não salvas é considerado uma grande perda de dados
bug** no desenvolvimento de software. Nenhum editor sério oferece uma configuração
"substituir meu buffer sem perguntar". Isso é correto e importante -
para trabalho normal de desenvolvedor.

No modo Aura Oma, entretanto, a prioridade é invertida: Aura é a fonte
da verdade, e o buffer do editor humano é secundário. Portanto um
intervenção explícita do plugin é necessária para impor esse comportamento para
este caso de uso específico.