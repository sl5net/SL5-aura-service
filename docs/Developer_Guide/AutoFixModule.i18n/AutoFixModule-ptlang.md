# Módulo de correção automática (modo de entrada rápida de regras)

## O que faz

Quando você digita uma palavra simples (sem aspas ou sintaxe Python) em um arquivo de mapa
como `FUZZY_MAP_pre.py`, o sistema o converte automaticamente em uma regra válida.

Esta é a maneira mais rápida de criar novas regras — não há necessidade de lembrar o formato.

## Exemplo

Você digita isso em `FUZZY_MAP_pre.py`:

```
oma
```

O módulo de correção automática detecta um `NameError` (palavra simples, Python não válido)
e transforma o arquivo automaticamente em:

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

Agora edite a regra para o que você realmente precisa:

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

##Como funciona

O módulo `scripts/py/func/auto_fix_module.py` é acionado automaticamente
quando o Aura detecta um `NameError` ao carregar um arquivo de mapa.

Então:
1. Adiciona o cabeçalho do caminho do arquivo correto
2. Adiciona `import re` se estiver faltando
3. Adiciona a definição de lista `FUZZY_MAP_pre = [`
4. Converte palavras simples em tuplas `('word', 'word'),`
5. Fecha a lista com `]`

## Regras e Limites

- Funciona apenas em arquivos menores que **1 KB** (limite de segurança)
- Aplica-se apenas a: `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCTUATION_MAP.py`
- O arquivo deve estar em uma pasta de idioma válida (por exemplo, `de-DE/`)
- Funciona com várias palavras ao mesmo tempo (por exemplo, de uma lista telefônica)

## Problemas conhecidos (não totalmente testados)

> ⚠️ Este módulo é funcional, mas não foi testado exaustivamente. Os seguintes casos podem não funcionar corretamente:

- **Números** – `5` ou `6` não são identificadores Python válidos, a correção automática pode não lidar com eles
- **Caracteres especiais** – palavras com `-`, `.`, tremas não podem acionar um `NameError`
- **Entradas com várias palavras** – `thomas mueller` (com espaço) causa `SyntaxError` e não `NameError`, então a correção automática pode não ser acionada
- **Valores separados por vírgula** – `drei, vier` pode ser inserido como está sem se tornar uma tupla adequada

Se a correção automática não for acionada, adicione a regra manualmente:
__CODE_BLOCO_3__

## O comentário `# too<-from`

Este comentário é adicionado automaticamente como um lembrete da direção da regra:

```python
('replacement', 'input word'),
```

Significado: **saída** (também) ← **entrada** (de). A substituição vem primeiro.

Para `PUNCTUATION_MAP.py` a direção é invertida: `# from->too`

## Entrada em massa de uma lista

Você pode colar várias palavras de uma vez:

__CODE_BLOCO_5__

Cada palavra simples se torna sua própria regra:

```
too <- from
```

Em seguida, edite cada substituição conforme necessário.

## Arquivo: `scripts/py/func/auto_fix_module.py`