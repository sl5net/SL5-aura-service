# Almacenamiento en caché de resultados avanzado (consciente del estado)

## Descripción general
Aura presenta un caché de resultados persistente y contextual diseñado para eliminar el procesamiento redundante. Cuando se reconoce un comando de voz y coincide con una regla, Aura verifica si se ha generado exactamente el mismo resultado antes en las mismas circunstancias. Si se encuentra una coincidencia, Aura omite operaciones costosas como **verificaciones gramaticales de LanguageTool** o **generación de Ollama LLM**, entregando el resultado con una latencia cercana a cero.

## Características clave
- **Context-Aware:** El caché es específico del título de la ventana activa. Un comando dicho en "LibreOffice" puede tener un resultado en caché diferente al del mismo comando en "Terminal".
- **Autorreparación (Invalidación automática):** El caché caduca automáticamente si modifica el archivo de reglas subyacente (mapa `.py`).
- **Privacidad primero:** Todos los resultados almacenados en caché se almacenan en una base de datos SQLite local (`data/_aura_result_cache.db`).
- **Mantenimiento cero:** Para la mayoría de los usuarios, esto funciona completamente en segundo plano sin configuración.

## Cómo funciona
El sistema genera un `cache_id` único basado en tres variables:
1. **El resultado de la regla:** El texto generado por el mapa.
2. **El idioma:** El código de idioma activo actual (por ejemplo, `de-DE`).
3. **La ventana activa:** El título de la ventana actualmente enfocada.

### Lógica de validez
El caché garantiza que nunca reciba información "obsoleta". Utiliza dos tipos de comprobaciones de validez:

| Tipo | Nombre | Lógica | Caso de uso |
| :--- | :--- | :--- | :--- |
| **Tipo 0** | **Sincronización automática de archivos** | Utiliza la hora de modificación (`mtime`) del archivo de mapa. | **Estándar.** Si editas tu Sandbox o Mapa, todas las entradas de caché asociadas se invalidan instantáneamente. |
| **Tipo 1** | **Marca de tiempo manual** | Utiliza una "marca de tiempo" fija proporcionada en los atributos de la regla. | **Desarrollador.** Codifique una versión/marca de tiempo para forzar o mantener un estado de resultado específico. |

## Ejemplos de configuración de reglas

Puede controlar el comportamiento del almacenamiento en caché directamente dentro de sus archivos `FUZZY_MAP_pre.py` o `FUZZY_MAP.py`.

### 1. Comportamiento predeterminado (almacenamiento en caché automático)
De forma predeterminada, el almacenamiento en caché está habilitado y utiliza la hora de modificación del archivo.
```python
# No extra attributes needed. 
# If this file is saved, the cache for this rule refreshes.
('Bold', r'^make it bold$', 100)
```

### 2. Deshabilitar la caché
Si un comando produce datos dinámicos (como la hora actual o un chiste aleatorio), debes desactivar el caché.
```python
('Current Time', r'^what time is it$', 100, {
    'cache': False 
})
```

### 3. Marca de tiempo manual (versiones fijas)
Si desea que el caché persista independientemente de las ediciones del archivo (a menos que cambie la versión), use una marca de tiempo manual.
```python
('Stable Command', r'^run complex task$', 100, {
    'timestamp': '2026-05-09-v1'
})
```

## Impacto en el rendimiento
- **Cache Miss:** Procesamiento estándar (0,05 s - 5,0 s según el uso de LLM).
- **Caché Hit:** Procesamiento instantáneo.

Este mecanismo consiste en que los comandos o los errores tipográficos corregidos se devuelven instantáneamente sin forzar la CPU.