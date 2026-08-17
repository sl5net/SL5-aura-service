# Zip automático seguro e documentação incorporada

## Conceito
SL5 Aura monitora pastas privadas começando com `_` (por exemplo, `_my_confidential_data`).
Quando alterações são detectadas, o Aura cria um arquivo zip **criptografado** automaticamente.

## Pré-requisito crítico: chave de criptografia
**A criptografia é obrigatória.** O processo de compactação automática exige estritamente que um arquivo de senha esteja presente na hierarquia de diretórios (pastas atuais ou pai).

* **Requisito de arquivo:** O arquivo de senha deve começar com um ponto `.` (por exemplo, `.archive_pass`, `.secret`).
* **Comportamento:** Se nenhum arquivo ponto com senha for encontrado, o processo zip será **bloqueado**. Essa proteção contra falhas garante que nenhum dado não criptografado seja empacotado.

## O padrão "Documentos incorporados"
Como o sistema de recarga a quente do Aura escuta **arquivos Python válidos**, atualizar um simples leia-me `.txt` não acionará um re-zip.

Para incluir instruções para os destinatários (por exemplo, "Como descompactar") e ao mesmo tempo garantir que o gatilho seja acionado, use um **Arquivo Python Docstring**.

### Implementação
Crie um arquivo chamado `README_AUTOZIP.py` dentro da sua pasta monitorada.

__CODE_BLOCK_0__