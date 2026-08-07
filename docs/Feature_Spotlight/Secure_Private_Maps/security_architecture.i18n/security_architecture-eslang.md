# Arquitectura de Seguridad: Protección de Datos Privados (7.8.'26 13:22 Vie)

El código fuente de `service_api.py` implementa una arquitectura de seguridad de triple capa mutuamente independiente para proteger los datos privados.

## Descripción general

| Capa | Mecanismo | Componente | Objetivo de protección |
|-------|-----------|-----------|-----------------|
| 1 | Middleware de regla de subrayado | `servicio_api.py` | Bloquear el acceso a caminos ocultos |
| 2 | Autenticación de clave API | `servicio_api.py` | Control de acceso para puntos finales |
| 3 | Enmascaramiento de privacidad y aislamiento de caché | `service_api.py`, `aura_cache.py` | Ofuscación de datos y separación de caché |

---

## Capa 1: Middleware de reglas de subrayado

Cualquier solicitud a rutas o carpetas con un guión bajo inicial (como `_privat`) está bloqueada por el middleware con **HTTP 403 Prohibido**.

**Mensaje de error:**
```
Access to hidden folders (starting with '_') is forbidden.
```

Esta regla opera a nivel de ruta/enrutamiento e impide cualquier acceso a directorios marcados como privados.

---

## Capa 2: Autenticación de clave API

Todos los puntos finales de API están protegidos por "Depends (verify_api_key)".

Las solicitudes sin un encabezado "X-API-Key" válido se rechazan inmediatamente antes de alcanzar cualquier lógica empresarial.

---

## Capa 3: Enmascaramiento de privacidad y aislamiento de caché

### Enmascaramiento
A través de la API, "unmasked = False" es el valor predeterminado. Por lo tanto, los datos confidenciales en las respuestas de la API se enmascaran automáticamente.

### Aislamiento de caché
El hash `cache_id` en `aura_cache.py` está separado por el título de la ventana activa (`_active_window_title`).

**Consecuencia:** Las entradas de caché creadas en la terminal local no se pueden leer a través de la API porque poseen un hash `cache_id` diferente.

---

## Resumen

Por lo tanto, sus datos confidenciales en `_privat` están protegidos en los tres niveles de idioma y ruta contra el acceso API no autorizado:

1. **Nivel de ruta**: el acceso a las carpetas `_` está bloqueado
2. **Nivel de autenticación**: solo se concede acceso a claves API válidas
3. **Nivel de datos**: el enmascaramiento y el aislamiento de la caché evitan la filtración de datos