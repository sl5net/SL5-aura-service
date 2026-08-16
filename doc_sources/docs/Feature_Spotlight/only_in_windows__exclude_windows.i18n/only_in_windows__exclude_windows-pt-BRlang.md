# Atributos de regra: `only_in_windows` e `exclude_windows`

Esses dois atributos controlam **em quais janelas ativas uma regra pode ser acionada**.
Eles são definidos dentro do ditado `options` de uma regra e aceitam uma **lista de padrões regex**
que são comparados com o título da janela ativa atual (`_active_window_title`).

---

## `apenas_no_windows`

A regra é acionada **somente se** o título da janela ativa corresponder a **pelo menos um** dos padrões fornecidos.
Todas as outras janelas são ignoradas.

**Caso de uso:** Restringir uma regra a um aplicativo específico.


> A regra será acionada **somente** quando Firefox ou Chromium for a janela ativa.

---

## `exclude_windows`

A regra é acionada **a menos** que o título da janela ativa corresponda a **pelo menos um** dos padrões fornecidos.
As janelas correspondentes são ignoradas.

**Caso de uso:** Desative uma regra para aplicativos específicos.

Exemplos

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



A correspondência **não diferencia maiúsculas de minúsculas** e usa **expressões regulares** do Python.

---

## Resumo

| Atributo | Dispara quando... |
|-------------------|-------------------------------------------|
| `only_in_windows` | título da janela **corresponde** a um dos padrões |
| `excluir_windows` | título da janela **NÃO corresponde a** nenhum padrão |

---

## Veja também

- `scripts/py/func/process_text_in_background.py` — linhas ~1866 e ~1908
- `scripts/py/func/get_active_window_title.py` — como o título da janela é recuperado