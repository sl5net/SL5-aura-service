# Ações de regras avançadas: execução de scripts Python

Este documento descreve como estender a funcionalidade de regras simples de substituição de texto executando scripts Python personalizados. Esse recurso poderoso permite criar respostas dinâmicas, interagir com arquivos, chamar APIs externas e implementar lógica complexa diretamente em seu fluxo de trabalho de reconhecimento de fala.

## O conceito central: `on_match_exec`

Em vez de apenas substituir o texto, agora você pode instruir uma regra para executar um ou mais scripts Python quando seu padrão corresponder. Isso é feito adicionando uma chave `on_match_exec` ao dicionário de opções da regra.

A principal tarefa do script é receber informações sobre a correspondência, realizar uma ação e retornar uma string final que será usada como novo texto.

### Estrutura de regras

Uma regra com uma ação de script é semelhante a esta:

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**Pontos-chave:**
- O valor `on_match_exec` deve ser uma **lista**.
- Os scripts estão localizados no mesmo diretório do arquivo de mapa, por isso `CONFIG_DIR / 'script_name.py'` é a forma recomendada para definir o caminho.

---

## Criando um script executável

Para que o sistema utilize seu script, ele deve seguir duas regras simples:
1. Deve ser um arquivo Python válido (por exemplo, `my_script.py`).
2. Deve conter uma função chamada `execute(match_data)`.

### A função `execute(match_data)`

Este é o ponto de entrada padrão para todos os scripts executáveis. O sistema chamará automaticamente esta função quando a regra corresponder.

- **`match_data` (dict):** Um dicionário contendo todo o contexto sobre a partida.
- **Valor de retorno (str):** A função **deve** retornar uma string. Esta string se tornará o novo texto processado.

### O dicionário `match_data`

Este dicionário é a ponte entre a aplicação principal e o seu script. Ele contém as seguintes chaves:

* `'original_text'` (str): A string de texto completa *antes* de qualquer substituição da regra atual ser aplicada.
* `'text_after_replacement'` (str): O texto *após* a string de substituição básica da regra ter sido aplicada, mas *antes* de seu script ser chamado. (Se a substituição for `None`, será o mesmo que `original_text`).
* `'regex_match_obj'` (re.Match): O objeto oficial de correspondência de regex do Python. Isso é extremamente poderoso para acessar **grupos de captura**. Você pode usar `match_obj.group(1)`, `match_obj.group(2)`, etc.
* `'rule_options'` (dict): O dicionário completo de opções para a regra que acionou o script.

---

## Exemplos

### Exemplo 1: Obtendo a hora atual (resposta dinâmica)

Este script retorna uma saudação personalizada com base na hora do dia.

**1. A regra (no seu arquivo de mapa):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. O script (`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**Uso:**
> **Entrada:** "que horas são"
> **Resultado:** "Boa tarde! Atualmente são 14h30."

### Exemplo 2: Calculadora Simples (Usando Grupos de Captura)

Este script usa grupos de captura da regex para realizar um cálculo.

**1. A regra (no seu arquivo de mapa):**
__CODE_BLOCO_3__

**2. O script (`calculator.py`):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```
**Uso:**
> **Entrada:** "calcular 55 mais 10"
> **Saída:** "O resultado é 65."

### Exemplo 3: lista de compras persistente (E/S de arquivo)

Este exemplo mostra como um script pode lidar com vários comandos (adicionar, mostrar) inspecionando o texto original do usuário e como pode persistir dados gravando em um arquivo.

**1. As regras (no seu arquivo de mapa):**
__CODE_BLOCO_5__

**2. O script (`shopping_list.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**Uso:**
> **Entrada 1:** "adicionar leite à lista de compras"
> **Resultado 1:** "Ok, adicionei 'leite' à lista de compras."
>
> **Entrada 2:** "mostrar a lista de compras"
> **Resultado 2:** "Na lista você tem: leite."

---

## Melhores práticas

- **Um trabalho por script:** Mantenha os scripts focados em uma única tarefa (por exemplo, `calculator.py` apenas calcula).
- **Tratamento de erros:** Sempre envolva a lógica do seu script em um bloco `try...except` para evitar que ele trave todo o aplicativo. Retorne uma mensagem de erro amigável do bloco `except`.
- **Bibliotecas Externas:** Você pode usar bibliotecas externas (como `requests` ou `wikipedia-api`), mas você deve garantir que elas estejam instaladas em seu ambiente Python (`pip install <library-name>`).
- **Segurança:** Esteja ciente de que esse recurso pode executar qualquer código Python. Use apenas scripts de fontes confiáveis.