## Atributos de reglas avanzadas

Además de los campos estándar, las reglas se pueden mejorar con opciones especiales:

### `only_in_windows` (Filtro de título de ventana)
A pesar de su nombre, este atributo es **independiente del sistema operativo**. Filtra reglas según el título de la ventana actualmente activa.

* **Función:** La regla solo se procesa si el título de la ventana activa coincide con uno de los patrones proporcionados (Regex).
*   **Ejemplo:**
    ```python
    (
        '|', 
        r'\b(pipe|symbol)\b', 
        75, 
        {'only_in_windows': ['Terminal', 'Console', 'iTerm']}
    ),
    ```
*En este caso, el reemplazo solo ocurre si el usuario está trabajando dentro de una ventana de terminal.*

### `on_match_exec` (Ejecución de script)
Permite activar scripts Python externos cuando coincide una regla.

* **Sintaxis:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
* **Caso de uso:** Ideal para acciones complejas como llamadas API, tareas del sistema de archivos o generación de contenido dinámico.