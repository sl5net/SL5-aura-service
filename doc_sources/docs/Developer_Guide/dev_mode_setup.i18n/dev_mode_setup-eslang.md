# Guía de configuración DEV_MODE

## El problema

Como somos compatibles con Weyland, utilizamos `threading.Lock` para iniciar sesión.

Ahora (21.3.'26 sábado) las reglas para el registro han cambiado. En Manjaro no hubo problemas.

Cuando `DEV_MODE = 1` está activo, Aura produce cientos de entradas de registro por segundo
de múltiples hilos. Esto puede causar que `SafeStreamToLogger` se bloquee, haciendo
Aura suspendida después del primer dictado.

## La solución: utilice el filtro LOG_ONLY

Al desarrollar con `DEV_MODE = 1`, **debes** también configurar un filtro de registro en:
`config/filters/settings_local_log_filter.py`

### Filtro de trabajo mínimo para DEV_MODE:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## Una línea para settings_local.py
Agregue este comentario como recordatorio junto a su configuración DEV_MODE:
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## Causa raíz (ya que somos compatibles con Weyland)
`SafeStreamToLogger` utiliza un `threading.Lock` para proteger las escrituras estándar.
Bajo una carga de registro alta (DEV_MODE), la contención de bloqueo provoca interbloqueos en los sistemas
con programación de subprocesos agresiva (por ejemplo, CachyOS con kernels/glibc más nuevos).