# Solución de problemas de CopyQ macOS: GUI invisible y configuración manual de teclas de acceso rápido

Esta guía aborda problemas comunes encontrados en macOS (específicamente dispositivos Apple Silicon serie M) donde la interfaz gráfica (GUI) CopyQ no aparece o es necesario reasignar accesos directos globales (como F10) sin acceder a la GUI.

---

## 1. Solución de problemas de la GUI invisible

En macOS, CopyQ puede ejecutarse correctamente en segundo plano y permanecer visualmente oculto por dos razones principales:
- **Coordenadas de ventana fuera de la pantalla**: después de cambios de resolución o desconectando un monitor externo, CopyQ puede retener coordenadas fuera del área de visualización visible.
- **Obstrucción de la muesca de la barra de menú**: en los modelos de MacBook con una muesca para la cámara, macOS oculta automáticamente el exceso de iconos de la barra de menú detrás de la muesca cuando la bandeja está llena.

### Solución: Restablecer visualización de geometría y fuerza

Ejecute los siguientes comandos en la terminal para borrar las coordenadas fuera de la pantalla y poner la ventana en primer plano:

```bash
copyq config geometry ""
copyq show
```

Si la ventana aún no aparece, cambie su estado mediante CLI:

```bash
copyq toggle
```

---

## 2. Cambiar manualmente las teclas de acceso rápido usando CudaText

Cuando otra aplicación reclama o intercepta un acceso directo global (como `F10`), el acceso directo se puede editar directamente en el archivo de configuración usando CudaText sin abrir la GUI de CopyQ.

### Paso 1: finalizar el proceso CopyQ

Se debe detener CopyQ antes de editar el archivo de configuración para evitar que sobrescriba sus cambios al finalizar:

```bash
copyq exit
```

### Paso 2: Abra la Configuración en CudaText

En macOS, los atajos de comandos de CopyQ se almacenan en `copyq-commands.ini`.

Abra el archivo en CudaText:

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

*Nota: Si el archivo no existe en "Soporte de aplicaciones", abra la ubicación alternativa de XDG:*

```bash
cudatext "$HOME/.config/copyq/copyq-commands.ini"
```

### Paso 3: reasignar el acceso directo

1- En CudaText, presione `Cmd + F` para abrir la barra de búsqueda.
2- Busque `F10` o `GlobalShortcut=F10`.
3- Reemplace `F10` con un acceso directo disponible (por ejemplo, `F9` o `Ctrl+F10` o `Meta+F10`).
4- Guarde el archivo (`Cmd + S`) y cierre CudaText (`Cmd + Q`).

### Paso 4: reiniciar CopyQ

Inicie CopyQ nuevamente para cargar la configuración de acceso directo actualizada:

```bash
open -a CopyQ
```

El nuevo acceso directo global ahora estará activo.