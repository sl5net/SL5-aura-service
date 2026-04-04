# Manejo de audio de sesión y alternancia de voz

Aura implementa un bucle de procesamiento de audio basado en sesiones. Los comandos de voz para la gestión del estado sólo están activos dentro de una sesión de grabación establecida.

## Configuración
El comportamiento interno de la sesión está controlado por:
`ENABLE_WAKE_WORD = Verdadero/Falso` (en `config/settings.py`)

## Lógica operativa
A diferencia de un oyente en segundo plano persistente, el motor STT de Aura (Vosk) solo procesa audio cuando una sesión de grabación se ha activado externamente (por ejemplo, mediante una tecla de acceso rápido).

### La alternancia durante la sesión ("Teleskop")
Cuando `ENABLE_WAKE_WORD` se establece en **Verdadero**:
1. **Activador:** El usuario inicia una sesión manualmente.
2. **Alternar:** Al decir "Teleskop" durante la sesión se alterna entre los estados **ACTIVO** y **SUSPENDIDO**.
3. **Comportamiento:** Esto permite al usuario "pausar" y "reanudar" el procesamiento de texto mediante comandos de voz sin finalizar la transmisión de audio.

### Privacidad y eficiencia
Cuando `ENABLE_WAKE_WORD` está configurado en **Falso** (predeterminado):
- **Supresión de STT:** Mientras está en estado suspendido, las llamadas a `AcceptWaveform` y `PartialResult` se omiten por completo.
- **Privacidad:** No se analizan datos de audio a menos que el sistema esté en un estado activo explícito.
- **Administración de recursos:** el uso de la CPU se minimiza al omitir el análisis de la red neuronal durante la suspensión.

## Latencia y rendimiento
- **Reanudación instantánea:** debido a que `RawInputStream` permanece abierto durante toda la sesión, cambiar de SUSPENDIDO a ACTIVO tiene **0 ms de latencia adicional**.
- **Tiempo de bucle:** El bucle de procesamiento opera en un intervalo de ~100 ms (`q.get(timeout=0.1)`), lo que garantiza tiempos de respuesta casi instantáneos.