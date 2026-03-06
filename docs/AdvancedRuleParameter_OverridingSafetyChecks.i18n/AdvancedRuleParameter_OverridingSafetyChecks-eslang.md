# Documentación del motor de reglas de aura SL5

## Parámetro de regla avanzada: anulación de comprobaciones de seguridad

En algunos escenarios (por ejemplo, comandos internos altamente confiables o entradas simples y de alta confianza), los usuarios pueden querer forzar la ejecución de pasos de posprocesamiento (como "fuzzyRules"), incluso si la confianza del sistema en el reconocimiento de voz inicial es baja.

De forma predeterminada, SL5 Aura emplea una barandilla de seguridad: si los cambios en las entradas son altos (`LT_SKIP_RATIO_THRESHOLD`), las herramientas de posprocesamiento se omiten para evitar correcciones/alucinaciones poco confiables y por razones de rendimiento.


Para deshabilitar esta verificación de seguridad para una regla específica, agregue el identificador al parámetro `skip_list`:

__CODE_BLOCK_0__