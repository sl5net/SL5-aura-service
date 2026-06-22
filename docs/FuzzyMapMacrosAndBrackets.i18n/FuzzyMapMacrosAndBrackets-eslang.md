# Macros de mapas difusos y lógica de corchetes

Aura admite la agrupación de múltiples reglas de preprocesamiento en archivos `FUZZY_MAP_pre.py` para ejecutarlas secuencialmente como una canalización cohesiva una vez que se activa una "Regla de inicio". Este documento describe la filosofía de diseño, la sintaxis y el flujo de ejecución de esta característica.

## Principios básicos de diseño

1. **Redundancia cero**: las reglas dentro de un grupo siguen siendo tuplas estándar de Python:
`('texto_reemplazo', r'patrón_regex', umbral, banderas_y_opciones)`
2. **Doble usabilidad**: las reglas individuales dentro de un grupo son reglas independientes completamente funcionales. Si el grupo no se activa, se evalúan normalmente en el bucle principal.
3. **Marcador de fin pasivo**: el final de un grupo se define mediante una entrada de regla pasiva que nunca coincide por sí sola. Actúa simplemente como un marcador de límites para el analizador.
4. **Reserva híbrida (agregar cuando no coincide)**: cuando un grupo está activo, cada regla interna debe contribuir a la salida. Si la expresión regular de una regla interna coincide con el texto, se produce la sustitución normal. Si no coincide, el texto de reemplazo se agrega al texto actual con un espacio.

---

## Sintaxis y estructura

Un grupo de macros se define envolviendo una serie de reglas estándar entre una **Regla de inicio** y una **Regla de finalización** en `FUZZY_MAP_pre.py`.

### 1. La regla de inicio
La regla de inicio es una regla estándar que activa la macro cuando coincide. Incluye una clave `'group_start'` en su diccionario de opciones:
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. Reglas internas
Las reglas internas son reglas estándar colocadas secuencialmente después de la regla de inicio. No requieren ningún metadato especial:
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. La regla final (marcador pasivo)
La regla final tiene un reemplazo `Ninguno`, un patrón vacío y una clave ``group_end'' en su diccionario de opciones:
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## Ejemplo concreto

Aquí hay un caso de prueba práctico definido en un archivo `FUZZY_MAP_pre.py`:

```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```

### Escenarios de flujo de ejecución:

* **Escenario A (Macro activada)**:
* Entrada: `"iniciar sandbox mit apfel"`
* Flujo esperado:
1. La regla de inicio coincide con `"start sandbox"` y la reemplaza con `"Sandbox:"` -> texto actual: `"Sandbox: mit apfel"`.
2. Se activa el grupo `'sandbox_test'`.
3. Ejecutamos las reglas internas de forma recursiva en `"Sandbox: mit apfel"`:
- La regla interna 1 coincide con `"apfel"` y se reemplaza con `"birne"` -> texto actual: `"Sandbox: mit birne"`.
- La regla interna 2 no coincide con `"banane"`. Dado que el grupo está activo, vuelve a agregar `"banane"` -> Texto actual: `"Sandbox: mit birne banane"`.
4. LanguageTool devuelve y corrige el texto final `"Sandbox: mit birne banane"`.
* Salida: `"Sandbox: mit Birne Banane"`

* **Escenario B (Macro no activada - Doble usabilidad)**:
* Entrada: `"ein apfel und eine kirsche"`
* Flujo esperado:
1. La regla de salida no coincide. El grupo `'sandbox_test'` permanece inactivo.
2. El ciclo continúa con la siguiente regla.
3. **Regla interna 1**: Coincide con `"apfel"` y lo reemplaza con `"birne"` -> Texto actual: `"ein birne und eine kirsche"`.
4. **Regla interior 2**: No coincide. Dado que el grupo no se activó, la regla se comporta como una regla independiente normal y **no se agrega nada**.
5. Se ignora la regla final.
* Salida: `"ein birne und eine kirsche"`

---

## Detalles técnicos (bajo el capó)

* **Recursión aislada**: cuando se activa un grupo, el motor invoca recursivamente `process_text_in_background` con `custom_rules=[inner_rule]`. Esto permite que cada regla interna se ejecute dentro de un paso de canalización completo y sincrónico.
* **Protección de rendimiento y estabilidad**:
* **Omisión de secuencia**: las ejecuciones recursivas internas omiten la cola de secuencia `chunk_id` para evitar interbloqueos y retrasos en la ejecución.
* **Supresión de E/S y TTS**: las ejecuciones recursivas suprimen la escritura de archivos intermedia y las salidas de voz TTS, lo que garantiza que solo se escriba y pronuncie el texto estabilizado final.
* **Protección de estabilidad**: las ejecuciones recursivas se interrumpen estrictamente después de una iteración para evitar bucles de estabilidad infinitos durante las anexaciones de respaldo.
* **Terminación segura**: la verificación de estabilidad se basa estrictamente en el recuento máximo de iteraciones (`MAX_ITERATION_FOR_SAFETY`) para evitar bucles infinitos, evitando la limitación basada en el tiempo que podría cancelar prematuramente ejecuciones de macros legítimas y más lentas.
__CODE_BLOCK_4__