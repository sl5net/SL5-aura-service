# Ejecutando 0 A.D. con Aura Voice Control en sistemas con poca RAM (Linux Mint)

Esta guía documenta la configuración y optimización de la memoria para ejecutar el control de voz **sl5net Aura** junto con **0 A.D.** en hardware Linux Mint heredado o con memoria limitada.

## Hardware de destino y perfil del sistema
- **Dispositivo**: Lenovo ThinkPad T520 (portátil)
- **CPU**: Intel Core i7-2620M (doble núcleo a 2,70 GHz - 3,40 GHz)
- **Memoria**: 5,67 GiB de RAM
- **Swap**: intercambio efectivo de 4 GiB
- **Sistema operativo**: Linux Mint 21.3 Virginia (64 bits)
- **Entorno de escritorio**: Cinnamon 6.0.5 (servidor de pantalla X11)
- **Objetivo de la aplicación**: 0 d.C. (Ascendente del Imperio)

## Gestión y arquitectura de la memoria
En sistemas con ≤ 6 GiB de RAM, ejecutar un entorno de escritorio pesado, un juego de estrategia en tiempo real en 3D (0 A.D.) y reconocimiento de voz simultáneamente requiere una protección estricta de la memoria:

1. **Prioridad del modelo de voz Vosk**:
- Utiliza `vosk-model-small-de` (o idioma equivalente) para un uso reducido de memoria (~300-500 MB).
- Se prioriza la retención del modelo Vosk para garantizar la capacidad de respuesta de los comandos en tiempo real durante el juego.

2. **Desalojo automático de LanguageTool**:
- El proceso Java de LanguageTool puede consumir ~1,34 GiB RSS.
- Cuando la RAM disponible cae por debajo de `CRITICAL_THRESHOLD_MB` (2.0 GiB), `model_manager` de Aura finaliza inmediatamente LanguageTool para liberar ~1.3 GiB de RAM para el juego.
- Un tiempo de reutilización de 5 minutos (`set_language_tool_cooldown`) evita que LanguageTool se reinicie y destruya la memoria durante el juego activo.

## Comandos de verificación
Para inspeccionar la memoria del sistema y los estados de proceso:
__CODE_BLOCK_0__