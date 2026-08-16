Planeado no funcionar en este momento sin una contraseña en carpetas en algún lugar. Los archivos de contraseña deben comenzar con un punto "."


# Flujo de trabajo de cierre automático y documentación integrada

## Concepto
SL5 Aura monitorea automáticamente las carpetas que comienzan con `_` (por ejemplo, `_my_application`). Cuando se detectan cambios, Aura comprime automáticamente la carpeta en un archivo zip.

**Restricción crítica:**
El sistema de monitoreo y "Recarga en Caliente" de Aura escucha específicamente los cambios en **archivos Python válidos**. Una simple actualización de un archivo de texto (`.txt`) **no** activará el proceso de compresión automática.

## El patrón "Documentos integrados"
Para incluir instrucciones para destinatarios no técnicos (por ejemplo, Recursos Humanos, Clientes) y al mismo tiempo garantizar que Aura detecte el cambio y actualice el zip, utilizamos un **Python Docstring File**.

Este archivo es técnicamente un script Python válido (que satisface el analizador de Aura) pero aparece visualmente como un documento de texto estándar para el usuario.

### Implementación
Cree un archivo llamado `README_AUTOZIP.py` dentro de su carpeta monitoreada.

**Guía de estilo:**
1. Utilice `# Documentación` como primera línea (en lugar de un nombre de script técnico) para dar la bienvenida.
2. Utilice una cadena de documentación de comillas triples (""""`) para el contenido.
3. No se requiere ningún otro código.

### Código de ejemplo

__CODE_BLOCK_0__