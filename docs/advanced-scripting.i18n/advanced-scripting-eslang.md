# Acciones de reglas avanzadas: ejecución de scripts de Python

Este documento describe cómo ampliar la funcionalidad de reglas simples de reemplazo de texto mediante la ejecución de scripts Python personalizados. Esta poderosa característica le permite crear respuestas dinámicas, interactuar con archivos, llamar a API externas e implementar lógica compleja directamente dentro de su flujo de trabajo de reconocimiento de voz.

## El concepto central: `on_match_exec`

En lugar de simplemente reemplazar texto, ahora puede indicarle a una regla que ejecute uno o más scripts de Python cuando su patrón coincida. Esto se hace agregando una clave `on_match_exec` al diccionario de opciones de la regla.

El trabajo principal del script es recibir información sobre la coincidencia, realizar una acción y devolver una cadena final que se utilizará como nuevo texto.

### Estructura de reglas

Una regla con una acción de script tiene este aspecto:

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
**Puntos clave:**
- El valor `on_match_exec` debe ser una **lista**.
- Los scripts se encuentran en el mismo directorio que el archivo de mapa, por lo que `CONFIG_DIR / 'script_name.py'` es la forma recomendada de definir la ruta.

---

## Creando un script ejecutable

Para que el sistema utilice su script, debe seguir dos reglas simples:
1. Debe ser un archivo Python válido (por ejemplo, `my_script.py`).
2. Debe contener una función denominada `ejecutar (match_data)`.

### La función `ejecutar(match_data)`

Este es el punto de entrada estándar para todos los scripts ejecutables. El sistema llamará automáticamente a esta función cuando la regla coincida.

- **`match_data` (dict):** Un diccionario que contiene todo el contexto sobre la coincidencia.
- **Valor de retorno (cadena):** La función **debe** devolver una cadena. Esta cadena se convertirá en el nuevo texto procesado.

### El diccionario `match_data`

Este diccionario es el puente entre la aplicación principal y su script. Contiene las siguientes claves:

* `'original_text'` (cadena): La cadena de texto completo *antes* de aplicar cualquier reemplazo de la regla actual.
* `'text_after_replacement'` (cadena): El texto *después* de que se aplicó la cadena de reemplazo básica de la regla, pero *antes* de que se llamara su script. (Si el reemplazo es `Ninguno`, será lo mismo que `original_text`).
* `'regex_match_obj'` (re.Match): El objeto oficial de coincidencia de expresiones regulares de Python. Esto es extremadamente poderoso para acceder a **grupos de captura**. Puede utilizar `match_obj.group(1)`, `match_obj.group(2)`, etc.
* `'rule_options'` (dict): El diccionario de opciones completo para la regla que activó el script.

---

## Ejemplos

### Ejemplo 1: Obtener la hora actual (respuesta dinámica)

Este script devuelve un saludo personalizado según la hora del día.

**1. La regla (en su archivo de mapa):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. El script (`get_current_time.py`):**
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
> **Entrada:** "qué hora es"
> **Salida:** "¡Buenas tardes! Actualmente son las 14:30".

### Ejemplo 2: Calculadora simple (usando grupos de captura)

Este script utiliza grupos de captura de la expresión regular para realizar un cálculo.

**1. La regla (en su archivo de mapa):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2. El script (`calculadora.py`):**
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
> **Entrada:** "calcular 55 más 10"
> **Salida:** "El resultado es 65."

### Ejemplo 3: Lista de compras persistente (E/S de archivos)

Este ejemplo muestra cómo un script puede manejar múltiples comandos (agregar, mostrar) inspeccionando el texto original del usuario y cómo puede conservar datos escribiendo en un archivo.

**1. Las reglas (en su archivo de mapa):**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2. El guión (`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**Uso:**
> **Entrada 1:** "agregar leche a la lista de compras"
> **Salida 1:** "Está bien, agregué 'leche' a la lista de compras".
>
> **Entrada 2:** "mostrar la lista de compras"
> **Salida 2:** "En la lista tienes: leche."

---

## Mejores prácticas

- **Un trabajo por script:** Mantenga los scripts enfocados en una sola tarea (por ejemplo, `calculator.py` solo calcula).
- **Manejo de errores:** Siempre incluya la lógica de su script en un bloque `try...except` para evitar que bloquee toda la aplicación. Devuelve un mensaje de error fácil de usar del bloque "excepto".
- **Bibliotecas externas:** Puede utilizar bibliotecas externas (como `solicitudes` o `wikipedia-api`), pero debe asegurarse de que estén instaladas en su entorno Python (`pip install <nombre-biblioteca>`).
- **Seguridad:** Tenga en cuenta que esta función puede ejecutar cualquier código Python. Utilice únicamente scripts de fuentes confiables.