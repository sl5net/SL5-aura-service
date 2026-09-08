# Solução de problemas do CopyQ macOS: GUI invisível e configuração manual de teclas de atalho

Este guia aborda problemas comuns encontrados no macOS (especificamente em dispositivos Apple Silicon série M) onde a interface gráfica (GUI) CopyQ não aparece ou atalhos globais (como F10) precisam ser reatribuídos sem acessar a GUI.

---

## 1. Solução de problemas da GUI invisível

No macOS, o CopyQ pode ser executado corretamente em segundo plano, permanecendo visualmente oculto por dois motivos principais:
- **Coordenadas da janela fora da tela**: Após alterações na resolução ou desconexão de um monitor externo, o CopyQ pode reter coordenadas fora da área de exibição visível.
- **Obstrução do entalhe da barra de menus**: em modelos de MacBook com entalhe para câmera, o macOS oculta automaticamente o excesso de ícones da barra de menus atrás do entalhe quando a bandeja está cheia.

### Solução: Redefinir geometria e forçar exibição

Execute os seguintes comandos no terminal para limpar as coordenadas fora da tela e trazer a janela para o primeiro plano:

```bash
copyq config geometry ""
copyq show
```

Se a janela ainda não aparecer, alterne seu estado via CLI:

```bash
copyq toggle
```

---

## 2. Alterando manualmente as teclas de atalho usando CudaText

Quando um atalho global (como `F10`) é reivindicado ou interceptado por outro aplicativo, o atalho pode ser editado diretamente no arquivo de configuração usando CudaText sem abrir a GUI do CopyQ.

### Etapa 1: Encerre o processo CopyQ

CopyQ deve ser interrompido antes de editar o arquivo de configuração para evitar que ele substitua suas alterações após o encerramento:

```bash
copyq exit
```

### Etapa 2: Abra a configuração no CudaText

No macOS, os atalhos de comando do CopyQ são armazenados em `copyq-commands.ini`.

Abra o arquivo em CudaText:

__CODE_BLOCO_3__

*Nota: Se o arquivo não existir em `Application Support`, abra o local de fallback do XDG:*

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

### Etapa 3: reatribuir o atalho

1- No CudaText, pressione `Cmd + F` para abrir a barra de pesquisa.
2- Procure por `F10` ou `GlobalShortcut=F10`.
3- Substitua `F10` por um atalho disponível (por exemplo, `F9` ou `Ctrl+F10` ou `Meta+F10`).
4- Salve o arquivo (`Cmd + S`) e feche o CudaText (`Cmd + Q`).

### Etapa 4: reinicie o CopyQ

Inicie o CopyQ novamente para carregar a configuração atualizada do atalho:

__CODE_BLOCO_5__

O novo atalho global estará agora ativo.

(atualizado: 8.9.'26 08:01 Ter)