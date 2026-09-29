> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# Protocolo de entrega: z_fallback_llm, la entrada CLI no produce un chiste

Estado: 29-09-2026

## 1- Tarea (comprendido, aún no confirmado por usted con "sí")

Estado real: La entrada CLI es exactamente "computer exactamente decir dos chistes". No aparece ninguna broma.

Estado de destino: La respuesta LLM aparece directamente en la consola, no en un archivo de registro.

No es parte de la tarea: reconstruir la tala, acortar o extender las líneas de registro, cambiar el comportamiento de caché. El bypass cache ("joke" en la entrada) es elegido deliberadamente de esta manera.

El seguidor debe coincidir primero con este entendimiento con usted y esperar a su “sí”.

## 2 Environment

Manjaro Linux, ZSH, función Branch/fallback-llm-lazy-install.

Ollama está disponible en http://localhost:11434 (Binary /usr/bin/ollama). Modelos disponibles: llama3.2:latest, qwen3:8b.

La prueba Ollama por curl con el modelo llama3.2, flujo:falso, num predijo:100 y las palabras de parada proporciona una respuesta válida ("¿Por qué el ordenador fue al médico?") ¡Porque tenía un virus! Ollama, nombre de modelo, palabras paradas y límite de token no son la causa. El impulso de prueba fue más corto que el impulso real de preguntar ollama.py (sin el papel del sistema, gradiente y aura sufijo).

Configuración:

```
config/settings_local.py
```

Key: PLUGINS ENABLED = {"z fallback llm": 1}. Access via DynamicSettings().PLUGINS ENABLED.get("z fallback llm", False).

Instalación de paquete existente:

```
scripts/py/func/ensure_package.py
```

## 3- secuencia de cadena (verificado de secciones de código)

Reglas:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

La regla 1 tiene prioridad 10 y requiere `{aura1}` más palabra modo (normal, lento, flujo, lento, preciso, minucioso). La regla 2 tiene prioridad 100 y requiere uno de los desencadenantes aura, aurora, laura, dora, era, hurra, prora o computadora, luego un espacio y cualquier texto. Ambas llaman a Ollama.py. Ambos excluyen ventanas como Firefox, Chrome, Brave y Element.

Diseño:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` toma el último grupo Regex como entrada y lo hace pequeño. Para "joke" en la entrada, se establece `bypass_cache = True`, se salta el cheque de caché. Esto es seguido por la solicitud Ollama con el modelo llama3.2. El tiempo es de 90 segundos. Los primeros retornos sin petición de Ollama están disponibles con entrada vacía ("nada escuchada"), con "olvidar todo", con `check_static_guardrails()` y con las palabras instantáneas "inmediatamente", "rápido", "instant".

CLI return:

```
scripts/py/service_api.py
```

La función lee el último archivo de salida y devuelve un dict con `status`, `result_text` y `input_text`. La línea de registro "API-CLI-Call: Terminado" reduce la entrada y el resultado a 20 caracteres. Esto es el acortamiento del tronco puro y no el acortamiento de datos.

## 4- Registro observado de la entrada CLI

En el registro sólo hay `reload_performed` y "API-CLI-Call: Terminado". Input="...computer accurate", Resultado="computer accurate". Cada línea de `execute()` falta (no "Input:", no "Cache BYPASS", no "Respuesta de AI sin censura").

Esto no prueba que `execute()` no funcionara porque:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

abre el FileHandler con `mode='w'`. El fichero ollama.log es sobrescrito por `utils` en cada importación. `log_debug` también escribe en stdout, es decir, en la consola del programa principal.

## 5 Open Questions (not used)

1- ¿`execute()` corre en absoluto al entrar en el CLI?
2- ¿Qué reglas coinciden, Regla 1, Regla 2 o Ninguno?
3- ¿El cliente de CLI obtiene el valor `result_text` en la consola?
4- ¿El archivo de salida contiene sólo la entrada o también una respuesta? Los primeros 20 caracteres de entrada y resultado son idénticos, más no es visible.
5- ¿Cuál es la llamada exacta CLI que utiliza para dejar el texto? Aún no se ha mencionado.

## 6- Hipótesis descartadas

1- La entrada no llega recortada, eso fue solo la reducción a 20 caracteres en el registro.
2- Ollama, las palabras vacías y num_predict no son la causa.
3- La caché está pasada por alto en "witz" y por lo tanto no es la causa.

## 7- Se encontraron errores fuera de la tarea (no cambiar nada sin una tarea)

1 archivo:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

Después de `if not raw_text:`, se establece `response = answer_for_all_fallback`. La siguiente línea lo sobrescribe con `clean_text_for_typing(raw_text)`. Con una respuesta Ollama vacía, la respuesta sigue vacía. Del mismo modo, `response.replace('sl5_config.py', ...)` y `response.replace(' sl5_record_trigger.py ', ...)` no tienen efecto porque el resultado no se asigna.

2 Archivo:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

Según `Overlay`, falta un `|`, se crea la variante `OverlayOrange`. Además, `_variants` no contiene la palabra "computer". Por lo tanto, la regla 1 no puede coincidir con "computer exactamente ...", la regla 2 puede.

3 Archivo:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` sobrescribe el registro en cada importación.

## 8- Próximos pasos (sólo después de tu sí)

Paso A: Solicite la llamada CLI de usted, sin una señal rápida.

Paso B: Encontrar el procesamiento de `result_text`:

```
tools/search.sh "result_text" .
```

Paso C: Compruebe la salida de la consola después de la entrada. Solicitar el texto completo de la consola principal del programa.

Paso D: Sólo entonces proponer cambios, sólo en formato anterior/después.

## 9- Reglas de trabajo que el sucesor debe cumplir

1- Comunicación en alemán. Código, comentarios, registros e identificadores en inglés solamente, incluso en bloques de código.
2- Ninguna declaración sobre el estado del sistema sin pruebas de su salida. No lo supongas, no reconstruyas.
3- Nueva tarea: describir primero el entendimiento, esperando su "sí".
4- No "No tengo acceso a tu repositorio".
5- Búsqueda de depósito sólo a través de herramientas/search.sh con las opciones -i, -E y -w.
6- Para los errores, obtener el rastreo completo primero.
7- Los comandos y caminos de archivo están cada uno en su propia línea, sin puntuación al final.
8- Número en el formato 1-, 2-, 3-.
9- El código cambia sólo como líneas modificadas en formato anterior/después, sin código de función circundante.
10- Sin código de pitón con indentación líder en bloques de código, en lugar de pequeñas funciones sin indentación.
11- No hay caminos absolutos, específicos para el usuario y ningún número de línea sin ruta de archivo.
12- Sin conjuntos de llenado, sin tono emocional, alrededor de 1400 caracteres por respuesta como objetivo.
13- Tratar acciones que ya has realizado como realizadas.
14- Cuando las salidas de copia no copian el signo rápido, de lo contrario se crea el código de salida 127.
15- Compromiso para encontrar fecha y hora: ./tools/find-nearest-commit.sh "2026-07-28 17:00"
