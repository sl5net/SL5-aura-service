# Guia de regras FUZZY_MAP

## Formato da regra

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| Posição | Nome | Descrição |
|---|---|---|
| 1 | substituição | O texto de saída após a regra corresponder |
| 2 | padrão | Regex ou string difusa para correspondência |
| 3 | limiar | Ignorado para regras de regex. Usado para correspondência difusa (0–100) |
| 4 | bandeiras | `{'flags': re.IGNORECASE}` para não diferenciar maiúsculas de minúsculas, `0` para diferenciar maiúsculas de minúsculas |

## Lógica de pipeline

- As regras são processadas **de cima para baixo**
- **Todas** as regras correspondentes são aplicadas (cumulativas)
- Um **fullmatch** (`^...$`) interrompe o pipeline imediatamente
- As regras anteriores têm prioridade sobre as regras posteriores

## Padrões Comuns

### Corresponder a uma única palavra (limite da palavra)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### Combine múltiplas variantes
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – interrompe o pipeline
__CODE_BLOCO_3__
⚠️ Isso combina com **tudo**. O pipeline para aqui. As regras anteriores ainda têm prioridade.

### Corresponde ao início da entrada
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```

### Corresponde à frase exata
__CODE_BLOCO_5__

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
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

## Sua primeira regra - passo a passo

1. Abra `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Adicione sua regra dentro de `FUZZY_MAP_pre = [...]`
3. Salvar – Aura recarrega automaticamente, não é necessário reiniciar
4. Dite sua frase-gatilho e observe-a disparar


## Estrutura de arquivo recomendada

Coloque suas regras **antes** de longos blocos de comentários:
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
```

**Por quê?** O Auto-Fix do Aura verifica apenas o primeiro ~1KB de um arquivo.
Se suas regras aparecerem após um cabeçalho longo, o Auto-Fix não poderá localizá-las ou repará-las.
O comentário do caminho na linha 1 também é recomendado — ajuda os humanos a identificar rapidamente o arquivo.