# Atributo de regla: `execute_only` (Experimental, 7.7.'26 martes)

El atributo `execute_only` es una opción de configuración experimental diseñada para reglas que solo activan scripts externos sin modificar ni reemplazar el texto de entrada.

## Descripción general
- **Tipo:** `bool` (por ejemplo, `Verdadero` o `Falso`)
- **Caso de uso principal:** Normalmente se utiliza en combinación con `on_match_exec` para ejecutar scripts externos.

## Cómo funciona y comportamiento actual
- **Optimización de velocidad:** (solo algunos milisegundos) Omite las rutinas de posprocesamiento y reemplazo de texto, acelerando la ejecución inmediata de la acción desencadenada.
- **Sin exclusión/efecto secundario de exclusión:** Establecer `execute_only` en `True` **no** impide que otras reglas coincidentes evalúen el mismo texto de entrada.
- **Detener el flujo:** Si necesita evitar que reglas posteriores procesen el mismo texto de entrada, actualmente debe finalizar el flujo de ejecución manualmente (por ejemplo, lanzando una excepción al final del script activado o del controlador de conjunto de reglas).

## Configuración de ejemplo

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'command_flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```