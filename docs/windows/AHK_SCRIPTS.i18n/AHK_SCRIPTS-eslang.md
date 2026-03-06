### Documentación de rebajas (`docs/AHK_SCRIPTS.md`)

# Infraestructura AutoHotkey para SL5-Aura-Service

Debido a que Windows maneja los bloqueos de archivos y las teclas de acceso rápido del sistema de manera diferente que Linux, este proyecto utiliza un conjunto de scripts AutoHotkey (v2) para cerrar la brecha entre el motor Python STT y la interfaz de usuario de Windows.

## Descripción general de los scripts

### 1. `trigger-hotkeys.ahk`
* **Propósito:** La interfaz de usuario principal para controlar el servicio.
* **Características clave:**
* Intercepta **F10** y **F11** para iniciar/detener el dictado.
* Utiliza un `Keyboard Hook` para anular el comportamiento predeterminado del sistema Windows (por ejemplo, F10 activa la barra de menú).
* **Implementación:** Diseñado para registrarse a través del Programador de tareas de Windows con "Privilegios más altos" para que pueda capturar teclas de acceso rápido incluso cuando el usuario esté trabajando en una aplicación de nivel de administrador.

### 2. `type_watcher.ahk`
* **Propósito:** Actúa como el "Consumidor" en el canal STT.
* **Características clave:**
* Observa un directorio temporal en busca de archivos `.txt` entrantes generados por el motor Python.
* **State Machine (Zombie Map):** Implementa un mapa basado en memoria para garantizar que cada archivo se escriba exactamente una vez. Esto evita la "doble escritura" causada por eventos redundantes del sistema de archivos de Windows (agregados/modificados).
* **Escritura segura:** Utiliza `SendText` para garantizar que los caracteres especiales se manejen correctamente en cualquier editor activo.
* **Limpieza confiable:** Administra la eliminación de archivos con una lógica de reintento para manejar los bloqueos de acceso a archivos de Windows.

### 3. `scripts/ahk/sync_editor.ahk`
* **Propósito:** Garantiza una sincronización perfecta entre el disco y el editor de texto (por ejemplo, Notepad++).
* **Características clave:**
* **Guardar bajo demanda:** Python puede activarlo para forzar `Ctrl+S` en el editor antes de que el motor lea el archivo.
* **Dialog Automator:** Detecta y confirma automáticamente los cuadros de diálogo de recarga de "Archivo modificado por otro programa", creando una experiencia de actualización fluida en tiempo real.
* **Comentarios visuales:** Proporciona cuadros de notificación de corta duración para informar al usuario que se están aplicando correcciones.

### 4. `scripts/notification_watcher.ahk`
* **Propósito:** Proporciona comentarios de la interfaz de usuario para procesos en segundo plano.
* **Características clave:**
* Supervisa archivos de estado o eventos específicos para mostrar notificaciones al usuario.
* Desacopla la lógica de "calcular" un mensaje (Python) de "mostrarlo" (AHK), asegurando que el motor STT principal no esté bloqueado por interacciones de UI.


---

### Reserva no administrativa
Si la aplicación se ejecuta sin privilegios de administrador:
- **Funcionalidad:** El servicio sigue siendo totalmente funcional.
- **Limitaciones de las teclas de acceso rápido:** Las teclas reservadas por el sistema como **F10** aún pueden activar el menú de Windows. En este caso, se recomienda cambiar las teclas de acceso rápido por teclas que no sean del sistema (por ejemplo, `F9` o `Insertar`).
- **Programador de tareas:** Si la tarea "AuraDictation_Hotkeys" se creó durante una instalación de administrador, el script se ejecutará con altos privilegios incluso para un usuario estándar. De lo contrario, `start_dictation.bat` iniciará una instancia local a nivel de usuario de forma silenciosa.

---

### 3. Warum "nervige Meldungen" erscheinen und wie man sie im AHK-Code stoppt
Para garantizar que el script no tenga ningún valor de Nutzer con ventanas emergentes, coloque estas "banderas silenciosas" en una fecha `.ahk`:

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. Estrategia para las teclas de acceso rápido (alternativa F10)
Con F10 sin la función de administrador en Windows para desbloquear rápidamente, puede probar en `trigger-hotkeys.ahk` una pequeña cantidad:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Zusammenfassung der Verbesserungen:
1. **Batch-Datei:** Nutzt `start "" /b`, um das schwarze Fenster zu vermeiden, und prüft vorher, ob der Admin-Task schon läuft.
2. **Transparenz:** Die Doku erklärt nun offen: "¿Kein Admin? Kein Problem, nimm einfach eine andere Taste als F10".
3. **AHK-Skript:** En el cuadro de diálogo `#SingleInstance Force`, aparece el cuadro de diálogo "Se está ejecutando una instancia anterior".

Damit wirkt die Software viel professional ("Smooth"), da sie im Hintergrund startet, ohne dass der Nutzer mit technischen Details oder Bestätigungsfenstern konfrontiert wird.
  
  
---

### Por qué esta documentación es importante:
Al documentar el requisito **"Zombie Map"** y **"Task Scheduler/Admin"**, explicas a otros desarrolladores (y a ti mismo en el futuro) por qué el código es más complejo que un simple script de Linux. Convierte "soluciones extrañas" en "soluciones diseñadas para las limitaciones de Windows".

(s,29.1.'26 11:02 jueves)