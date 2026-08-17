# Rozwiązywanie problemów z dźwiękiem (Linux)

## Problem: Espeak / Fallback milczy
Jeśli dźwięk zastępczy (espeak) nie jest słyszalny, prawdopodobnie został wyciszony w systemowym mikserze dźwięku (np. PulseAudio lub PipeWire).

### „Sztuczka z długimi strunami”, aby wyłączyć wyciszenie
Krótkie fragmenty audio często znikają zbyt szybko z interfejsu GUI miksera, aby można je było wyłączyć ręcznie. Aby to naprawić, wymuś długi strumień audio:

__KOD_BLOKU_0__