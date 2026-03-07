## Guia do desenvolvedor: Expressões regulares avançadas de mapa difuso

O sistema Fuzzy Mapping utiliza expressões regulares padrão do Python, permitindo padrões poderosos de correspondência e exclusão, especialmente por meio de **Negative Lookaheads (`(?!...)`)**.

### Usando Lookaheads Negativos para Lista Branca

Este padrão permite definir uma regra que se aplica a **tudo, EXCETO** uma lista específica de palavras ou frases. Isso é especialmente útil em combinação com o padrão `empty_all` para construir conjuntos de regras restritos e cumulativos.

| Meta | Exemplo de regra (`FUZZY_MAP`) | Explicação |
| :--- | :--- | :--- |
| **Aplicar a todos, exceto uma palavra** | `('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regra aplicará uma substituição (ou lógica de salto, aqui `''`) a **qualquer texto** que *não* seja exatamente "Haus". `(?!Haus)` é o Lookahead Negativo, garantindo que o texto não comece com "Haus". |
| **Aplicar a todos, exceto palavras múltiplas** | `('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regra se aplica a **tudo** que não comece com "Schach", "Matt", "bad" ou "Haus". Use o canal OR (`|`) dentro do grupo lookahead `(?!...)` para colocar vários termos na lista de permissões. |

***

### Usando Lookaheads Positivos para Regras Restritas

A abordagem padrão usa Lookaheads Positivos ou grupos de captura simples para restringir uma regra a *apenas* uma lista específica de palavras.

| Meta | Exemplo de regra (`FUZZY_MAP`) | Explicação |
| :--- | :--- | :--- |
| **Inscreva-se apenas em uma lista específica** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regra só se aplica se o texto começar com uma das palavras listadas (Schach, Matt, bad ou Haus). O texto correspondente é então substituído pelo alvo (`Schachmatt`) com base no limite. |