## Guía para desarrolladores: expresiones regulares avanzadas de mapas difusos

El sistema Fuzzy Mapping utiliza expresiones regulares estándar de Python, lo que permite potentes patrones de coincidencia y exclusión, particularmente a través de **Negative Lookaheads (`(?!...)`)**.

### Uso de búsquedas anticipadas negativas para la inclusión en la lista blanca

Este patrón le permite definir una regla que se aplica a **todo EXCEPTO** una lista específica de palabras o frases. Esto es especialmente útil en combinación con el patrón `empty_all` para crear conjuntos de reglas restringidas y acumulativas.

| Gol | Regla de ejemplo (`FUZZY_MAP`) | Explicación |
| :--- | :--- | :--- |
| **Aplicar a todas excepto una palabra** | `('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regla aplicará un reemplazo (u lógica de omisión, aquí `''`) a **cualquier texto** que *no* sea exactamente "Haus". `(?!Haus)` es la anticipación negativa, lo que garantiza que el texto no comience con "Haus". |
| **Aplicar a todas excepto a varias palabras** | `('', r'^(?!Schach|Matt|malo|Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regla se aplica a **todo** que no comience con "Schach", "Matt", "bad" o "Haus". Utilice la canalización OR (`|`) dentro del grupo de búsqueda anticipada `(?!...)` para incluir en la lista blanca varios términos. |

***

### Uso de anticipaciones positivas para reglas restringidas

El enfoque estándar utiliza búsquedas positivas o grupos de captura simples para restringir una regla a *solo* una lista específica de palabras.

| Gol | Regla de ejemplo (`FUZZY_MAP`) | Explicación |
| :--- | :--- | :--- |
| **Aplicar sólo a una lista específica** | `('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE})` | Esta regla sólo se aplica si el texto comienza con una de las palabras enumeradas (Schach, Matt, bad o Haus). Luego, el texto coincidente se reemplaza por el objetivo ("Schachmatt") según el umbral. |