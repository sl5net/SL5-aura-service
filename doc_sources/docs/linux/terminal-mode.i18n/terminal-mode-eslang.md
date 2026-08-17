# Modo terminal (exclusión de idioma)

El modo terminal es un estado de configuración en el que no se instalan ni configuran paquetes de idiomas específicos para las unidades de procesamiento de voz/texto.

## Cómo habilitar
Durante la configuración inicial o el script de selección de idioma, cuando se le solicite el **Idioma principal**, ingrese:
-`n`
- `ninguno`
- `0`

## Efectos
- **EXCLUDE_LANGUAGES** está configurado en "todos".
- No se descargarán ni inicializarán modelos de idiomas específicos (como los modelos Whisper o Vosk).
- El sistema funciona en modo "Solo terminal", útil para entornos con poco disco o cuando solo se requieren las herramientas CLI principales sin soporte de voz localizada.

## Variables de entorno
Cuando está activo, se generan las siguientes exportaciones:
__CODE_BLOCK_0__