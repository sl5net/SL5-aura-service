# Guia de regras FUZZY_MAP

## Formato da regra

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| Posição | Nome | Descrição |
|---|---|---|
| 1 | substituição | O texto de saída após a regra corresponder |
| 2 | padrão | Regex ou string difusa para correspondência |
| 3 | limiar | Para regras regex: ignorado. Para regras difusas: pontuação mínima de correspondência (0–100) |
| 4 | opções | Dicionário opcional (veja "Referência de opções" abaixo). Use `0` ou omita os padrões |
### Substituições brutas
Por padrão (`False`), as strings de substituição são processadas pelo `re.sub()` do Python, que suporta o uso de referências anteriores de regex como `\1` ou `\2` para inserir grupos capturados (por exemplo: `(r'\1', r'(\d)\s+(?=\d)', 95)`).
Se a sua substituição for uma string multilinha ou contém barras invertidas sem escape (como modelos de código ou caminhos) e deve ser preservada exatamente como está, habilite `'raw_replacement': True` no dicionário de opções:
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### Opções configuráveis pelo usuário disponíveis:

* **`command_flags`** (inteiro): Flags Regex usados durante a compilação do padrão.
*Exemplo:* `{'command_flags': re.IGNORECASE}`
* **`raw_replacement`** (booleano): Quando `True`, o texto de substituição é tratado como uma string literal pura e ignorado pela análise de barra invertida `re.sub` do Python. Crucial para prompts multilinhas ou strings com barras invertidas sem escape (`\`).
*Exemplo:* `{'raw_replacement': True}`
* **`cache`** (booleano): Alterna o cache de resultados do AURA. Defina como `False` para regras que geram resultados dinâmicos (por exemplo, horário atual, piadas aleatórias) para garantir que sejam avaliadas de forma atualizada em cada partida.
*Exemplo:* `{'cache': False}`
* **`skip_list`** (lista de strings): Especifica módulos de pipeline de pós-processamento a serem ignorados quando esta regra corresponder.
*Exemplo:* `{'skip_list': ['LanguageTool']}` (ignora a verificação gramatical)
* **`only_in_windows`** (string/regex): Restringe a regra para ser acionada apenas se o título da janela ativa corresponder a esse padrão.
*Exemplo:* `{'only_in_windows': 'google ai studio'}`
* **`exclude_windows`** (string/regex): Impede que a regra seja acionada se o título da janela ativa corresponder a esse padrão.
*Exemplo:* `{'exclude_windows': 'Terminal'}`
* **`on_match_exec`** (lista de objetos Path/string): Caminhos para scripts/plugins que devem ser executados quando esta regra corresponder (muito usado por regras catch-all e fallback).
*Exemplo:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Lógica de pipeline
- As regras são processadas **de cima para baixo**


## Lógica de pipeline

- As regras são processadas **de cima para baixo**
- **Todas** as regras correspondentes são aplicadas (cumulativas)
- Um **fullmatch** (`^...$`) interrompe o pipeline imediatamente
- As regras anteriores têm prioridade sobre as regras posteriores

## Padrões Comuns

### Corresponder a uma única palavra (limite da palavra)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### Combine múltiplas variantes
__CODE_BLOCO_3__

### Fullmatch – interrompe o pipeline
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```
⚠️ Isso combina com **tudo**. O pipeline para aqui. As regras anteriores ainda têm prioridade.

### Corresponde ao início da entrada
__CODE_BLOCO_5__

### Corresponde à frase exata
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```

## Locais de arquivos

| Arquivo | Fase | Descrição |
|---|---|---|
| `FUZZY_MAP_pre.py` | Pré-IdiomaFerramenta | Aplicado antes da verificação ortográfica |
| `FUZZY_MAP.py` | Ferramenta Pós-Linguagem | Aplicado após verificação ortográfica |
| `PUNCTUATION_MAP.py` | Pré-IdiomaFerramenta | Regras de pontuação |

## Pontas

- Coloque regras **específicas** antes das regras **gerais**
- Use `^...$` fullmatch somente quando quiser interromper todo o processamento adicional
- `FUZZY_MAP_pre.py` é ideal para correções antes da verificação ortográfica
- Regras de teste com: `é sua entrada de teste` no console do Aura
- Os backups são criados automaticamente como `.peter_backup`

## Exemplos

```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

## Sua primeira regra - passo a passo

1. Abra `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Adicione sua regra dentro de `FUZZY_MAP_pre = [...]`
3. Salvar – Aura recarrega automaticamente, não é necessário reiniciar
4. Dite sua frase-gatilho e observe-a disparar


## Estrutura de arquivo recomendada

Coloque suas regras **antes** de longos blocos de comentários:
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
```

**Por quê?** O Auto-Fix do Aura verifica apenas o primeiro ~1KB de um arquivo.
Se suas regras aparecerem após um cabeçalho longo, o Auto-Fix não poderá localizá-las ou repará-las.
O comentário do caminho na linha 1 também é recomendado — ajuda os humanos a identificar rapidamente o arquivo.