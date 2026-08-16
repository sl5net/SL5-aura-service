planejado não funcionar no momento sem uma senha em pastas em algum lugar. os arquivos de senha precisam começar com um ponto "."


# Fluxo de trabalho de compactação automática e documentação incorporada

## Conceito
SL5 Aura monitora automaticamente pastas começando com `_` (por exemplo, `_my_application`). Quando alterações são detectadas, o Aura compacta automaticamente a pasta em um arquivo zip.

**Restrição crítica:**
O sistema de monitoramento e "Hot-Reload" do Aura escuta especificamente alterações em **arquivos Python válidos**. Uma simples atualização de arquivo de texto (`.txt`) **não** acionará o processo de compactação automática.

## O padrão "Documentos incorporados"
Para incluir instruções para destinatários não técnicos (por exemplo, RH, Clientes) e garantir que o Aura detecte a alteração e atualize o zip, usamos um **Arquivo Python Docstring**.

Este arquivo é tecnicamente um script Python válido (satisfazendo o analisador do Aura), mas aparece visualmente como um documento de texto padrão para o usuário.

### Implementação
Crie um arquivo chamado `README_AUTOZIP.py` dentro da sua pasta monitorada.

**Guia de estilo:**
1. Use `# Documentation` como primeira linha (em vez de um nome de script técnico) para ser acolhedor.
2. Use uma Docstring de aspas triplas (`"""`) para o conteúdo.
3. Nenhum outro código é necessário.

### Código de exemplo

__CODE_BLOCK_0__