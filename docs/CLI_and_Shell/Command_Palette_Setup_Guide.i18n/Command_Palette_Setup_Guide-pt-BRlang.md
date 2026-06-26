# Paleta de comandos e guia de pesquisa de mapas

Este guia explica como configurar e usar a **Paleta de Comandos** independente de local e em todo o sistema para SL5 Aura. Ele permite que você pesquise suas regras de mapa de forma interativa, veja visualizações de execução ao vivo do cache SQLite local e digite instantaneamente a saída selecionada em seu cursor ativo.

## Pré-requisitos

Certifique-se de que os seguintes serviços e ferramentas em segundo plano estejam instalados e ativos:
1. **`fzf`** (Localizador Difuso)
2. **CopyQ** (Clipboard Manager, usado para orquestração global de teclas de atalho)
3. **`type_watcher.sh`** (daemon de digitação em segundo plano do Aura)

---

## Configuração de atalho global do CopyQ

Para iniciar a Paleta de Comandos instantaneamente a partir de qualquer janela ativa (por exemplo, seu navegador ou editor de texto), configure uma tecla de atalho global no CopyQ:

1. Abra **CopyQ** e pressione `F6` (ou vá para **Comandos** / **Befehle**).
2. Clique em **Adicionar** (Hinzufügen) e nomeie-o como `Aura Command Palette`.
3. Defina o **Atalho Global** desejado (por exemplo, `Meta+S` ou `Ctrl+Alt+S`).
4. Defina **Type** como `Command` (Befehl).
5. Cole o seguinte código JavaScript na caixa de comando:

__CODE_BLOCK_0__