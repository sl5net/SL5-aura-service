# Solución de problemas de audio (Linux)

## Problema: Hablar/Retroceso está en silencio
Si el audio de reserva (espeak) no es audible, es probable que esté silenciado en el mezclador de sonido del sistema (por ejemplo, PulseAudio o PipeWire).

### El "truco de la cuerda larga" para activar el silencio
Los fragmentos de audio cortos a menudo desaparecen demasiado rápido de la GUI del mezclador como para reactivarlos manualmente. Para solucionar este problema, fuerce una transmisión de audio larga:

__CODE_BLOCK_0__