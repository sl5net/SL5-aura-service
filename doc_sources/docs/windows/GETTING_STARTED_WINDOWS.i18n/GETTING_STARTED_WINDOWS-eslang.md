# Primeros pasos en Windows

## Paso 1: ejecutar la instalación
Haga doble clic en `setup/windows11_setup_with_ahk_copyq.bat`.
- Haga clic derecho → "Ejecutar como administrador" si se le solicita.
- El script instala Python, AutoHotkey v2, CopyQ y descarga los modelos de voz (~4 GB).
- Esto tarda aproximadamente entre 8 y 10 minutos.

## Paso 2: Iniciar Aura
Haga doble clic en `start_aura.bat` en la carpeta del proyecto.
Deberías escuchar un sonido de inicio: Aura está lista.

**¿No pasó nada?** Consulta el registro:
registro\aura_engine.log

## Paso 3: Configura tu tecla de acceso rápido
La configuración instala CopyQ automáticamente. Para activar el dictado:
1. Abra CopyQ → Comandos → Agregar comando
2. Establezca el comando en:
cmd /c eco. > C:\tmp\sl5_record.trigger
3. Asigne un acceso directo global (por ejemplo, `F9`)

## Paso 4: Primer dictado
1. Haga clic en cualquier campo de texto
2. Presione su tecla de acceso rápido y espere la notificación "Escuchando..."
3. Di "Hola mundo"
4. Presione la tecla de acceso rápido nuevamente: aparece el texto.

## Paso 5: buscar comandos de voz
Diga: **"Búsqueda de aura"**: se abre una ventana con todas las reglas disponibles.

## Solución de problemas
| Síntoma | Arreglar |
|---|---|
| Sin sonido de inicio | Marque `log\aura_engine.log` |
| La tecla de acceso rápido no hace nada | Compruebe si se ha creado `C:\tmp\sl5_record.trigger` |
| Texto no escrito | Compruebe si `type_watcher.ahk` se está ejecutando en el Administrador de tareas |
| Fallo al inicio | Ejecute la configuración nuevamente como Administrador |

> Solución de problemas completa: [TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-eslang.md)