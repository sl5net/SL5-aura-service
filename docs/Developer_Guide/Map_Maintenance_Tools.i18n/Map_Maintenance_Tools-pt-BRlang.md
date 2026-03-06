# Ferramentas de manutenção de mapas Regex

Para suportar a funcionalidade de pesquisa rápida (comando `s` / `search_rules.sh`), usamos um script auxiliar que anota automaticamente padrões regex com exemplos legíveis por humanos.

## Por que precisamos disso?
Nossos arquivos `FUZZY_MAP.py` contêm expressões regulares complexas. Para torná-los pesquisáveis por meio de fuzzy finders (fzf) sem a necessidade de entender o regex bruto, adicionamos comentários `# EXAMPLE:` acima dos padrões.

**Antes:**
```python
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

**Depois (gerado automaticamente):**
```python
# EXAMPLE: 1234-5678-9012-3456
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

## O script Tagger (`map_tagger.py`)

Fornecemos um script Python que verifica todos os arquivos `FUZZY_MAP.py` e `FUZZY_MAP_pre.py` e gera esses exemplos automaticamente.

### Instalação
O script requer a biblioteca `exrex` para gerar correspondências aleatórias para expressões regulares complexas.

```bash
pip install exrex
```

### Uso
Execute o script na raiz do projeto:

__CODE_BLOCO_3__

### Fluxo de trabalho
1. **Crie ou edite** um arquivo de mapa (por exemplo, adicionando novas regras).
2. **Execute** o script do tagger.
3. **Modo Interativo:**
- O script mostrará uma sugestão gerada.
- Pressione `ENTER` para aceitá-lo.
- Digite `s` para pular.
- Digite `sa` (pular todos) se quiser pular todos os padrões restantes que falharam na geração.
4. **Confirme** as alterações.

> **Nota:** O script ignora as tags `# EXAMPLE:` existentes, portanto é seguro executá-lo repetidamente.