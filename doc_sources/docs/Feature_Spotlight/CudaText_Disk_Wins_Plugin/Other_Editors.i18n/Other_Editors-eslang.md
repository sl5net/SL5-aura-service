# Recarga automática en otros editores

Este documento describe cómo configurar la recarga automática en dispositivos externos.
cambios de archivos en editores comunes y por qué esto a menudo **no es suficiente**
en modo Aura Oma.

---

## Kate (KDE)

### Configuración

1. **Configuración → Configurar Kate → Abrir/Guardar → Avanzado**
2. Habilitar:
- **"Recargar archivos automáticamente"**

### ¿Qué funciona?

- Cuando el búfer **no cambia**, Kate recarga el archivo inmediatamente.
- Esto es suficiente para el modo de visualización pura.

### Qué **no** funciona (y por qué falla en el modo Oma)

- Tan pronto como presionas **una sola tecla** en el búfer (incluso solo una
espacio o pulsación accidental de una tecla), el buffer se considera "modificado".
- A partir de ese momento, Kate **siempre** pregunta ante cada cambio externo:
> "El archivo fue modificado externamente. ¿Quieres recargarlo?"
- En el modo Oma, es posible que el usuario no esté frente a la computadora o que no vea la
diálogo: Aura sigue escribiendo, pero el editor permanece en la versión anterior.
- **Kate no tiene ninguna configuración** que descarte silenciosamente los cambios de búfer no guardados
a favor de la versión en disco.

> **Conclusión:** Kate no es apta para el Modo Oma tan pronto como el usuario
> escribe accidentalmente en el editor.

---

## Código VS

### Configuración

En `configuración.json`:

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

### Limitaciones

- `autoSave` guarda el búfer; sobrescribe los cambios de Aura con el
versión local, no al revés.
- Todavía aparece un mensaje para los cambios no guardados.
- No hay opción para "el disco siempre gana".

---

## Emacs

```elisp
(global-auto-revert-mode t)
```

### Limitaciones

- Solo se recarga automáticamente cuando el buffer no cambia.
- Pregunta cuando se modifica el buffer.

---

## Vim / Neovim

```vim
set autoread
au FocusGained,BufEnter,CursorHold * :checktime
```

### Limitaciones

- `autoread` solo se recarga cuando el búfer no cambia.
- No sobrescribe automáticamente un buffer "modificado".

---

## CudaText (sin complemento)

En `usuario.json`:

```json
{
    "ui_notif": true,
    "ui_notif_confirm": 0
}
```

### Limitaciones

- Todos los valores de `ui_notif_confirm` (0–4) muestran algún tipo de aviso:
modal o sin modal.
- No hay **ningún** valor que signifique: "Recargar inmediatamente, nunca preguntar".
- Por lo tanto, se requiere el complemento `cuda_disk_wins`.

---

## Descripción general

| Redactor | Recarga automática (sin cambios) | Recarga automática (modificado) | Licencia |
|--------|-------------------------|------------------------|---------|
| Kate | Sí | Siempre indica | Código abierto |
| Código VS | Sí | Siempre indica | Código abierto |
| Texto sublime | Sí | Siempre indica | Propietario |
| Emacs | Sí | Siempre indica | Código abierto |
| Vim | Sí | Siempre indica | Código abierto |
| CudaText (sin complemento) | Sí | Siempre indica | Código abierto |
| **CudaText + Disco gana** | Sí | **Sin aviso** | Código abierto |

---

## Por qué ningún editor puede hacer esto de inmediato

Descartar silenciosamente los cambios no guardados se considera una **pérdida masiva de datos
error** en el desarrollo de software. Ningún editor serio ofrece una configuración
"sobrescribir mi buffer sin preguntar". Esto es correcto e importante.
para el trabajo normal de desarrollador.

En el modo Aura Oma, sin embargo, la prioridad se invierte: Aura es la fuente
de la verdad, y el buffer del editor humano es secundario. Por lo tanto un
Se necesita la intervención explícita del complemento para hacer cumplir este comportamiento para
este caso de uso específico.