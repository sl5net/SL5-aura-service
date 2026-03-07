# Matemáticos Famosos – Guia de Correção STT

## O problema

Sistemas de reconhecimento de fala (STT), como o Vosk, muitas vezes ouvem ou escrevem incorretamente nomes de matemáticos famosos.
Isto é especialmente comum com nomes alemães que contêm caracteres especiais (ß, ü, ä, ö)
ou nomes emprestados de outras línguas.

## Erros comuns de STT

| Saída falada/STT | Ortografia Correta | Notas |
|---|---|---|
| gaus, gauss | Gauß | Matemático alemão, ß frequentemente desaparecido |
| lubrificador, lubrificador | Euler | Suíço, nome soa como "oiler" em alemão |
| leibnitz, lipnitz | Leibniz | z no final, erro ortográfico comum |
| Riman, Riemann | Riemann | double-n muitas vezes perdido |
| Hilberto | Hilberto | geralmente correto, apenas letras maiúsculas |
| cantor | Cantor | geralmente correto, apenas letras maiúsculas |
| poincaré, poincaré | Poincaré | sotaque muitas vezes faltando |
| noether, noeter | Noéter | trema muitas vezes perdido |

## Exemplo de regras

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## Por que Pré-LanguageTool?

Essas correções deveriam acontecer em `FUZZY_MAP_pre.py` (antes do LanguageTool),
porque o LanguageTool pode "corrigir" um nome com erro ortográfico em uma palavra errada diferente.
Melhor consertar primeiro e depois deixar o LanguageTool verificar a gramática.

## Teste

Depois de adicionar uma regra, teste com o console do Aura:
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
Esperado: `Euler hat die Formel e hoch i pi plus eins gleich null bewiesen`