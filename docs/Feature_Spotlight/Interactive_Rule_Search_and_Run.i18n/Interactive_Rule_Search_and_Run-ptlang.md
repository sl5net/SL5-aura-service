# Pesquisa e execução de regras interativas

Este destaque destaca o sistema interativo de busca e execução de regras, unindo comandos vocais, navegação ao vivo e execução instantânea.

## Recursos principais
[1] **Pesquisa ao vivo de painel duplo (`fzf`):** O painel esquerdo filtra arquivos de regras; o painel direito exibe a visualização do contexto da linha via `preview_rule.py`.
[2] **Execuções instantâneas (`Enter` / `Ctrl+R`):** Executa o comando de destino extraído instantaneamente via `run_palette_command.py` em segundo plano.
[3] **Edição direta (`Ctrl+E`):** Inicia o editor (CudaText com `@line`, Kate/VS Code com `--line`) diretamente na linha de destino.
[4] **Tecla de atalho da janela flutuante:** Vinculada a `Super+S` para um fluxo de trabalho rápido e integrado ao desktop.
[5] **Ativado por comando de voz:** Vários comandos de voz pré-configuram padrões de pesquisa em `search_rules.sh` para pesquisas rápidas e direcionadas.

## Suporte multiplataforma
- **Linux Bash (`run_rule.sh` / `search_rules.sh`):** Implementação completa com rastreamento de histórico e operações da área de transferência (`Ctrl+X` / `Ctrl+A`).
- **Windows PowerShell (`search_rules.ps1`):** Ferramenta complementar que fornece recursos leves de pesquisa de terminal.

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)