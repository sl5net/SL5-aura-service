# Paleta de comandos y guía de búsqueda de mapas

Esta guía explica cómo configurar y utilizar la **Paleta de comandos** independiente de la ubicación en todo el sistema para SL5 Aura. Le permite buscar a través de sus reglas de mapas de forma interactiva, ver vistas previas de ejecución en vivo desde el caché SQLite local y escribir instantáneamente la salida seleccionada en su cursor activo.

## Requisitos previos

Asegúrese de que los siguientes servicios y herramientas en segundo plano estén instalados y activos:
1. **`fzf`** (Buscador difuso)
2. **CopyQ** (Administrador del portapapeles, utilizado para la orquestación global de teclas de acceso rápido)
3. **`type_watcher.sh`** (Demonio de escritura de fondo de aura)

---

## Configuración de acceso directo global de CopyQ

Para iniciar la paleta de comandos instantáneamente desde cualquier ventana activa (por ejemplo, su navegador o editor de texto), configure una tecla de acceso rápido global en CopyQ:

1. Abra **CopyQ** y presione `F6` (o vaya a **Comandos** / **Befehle**).
2. Haga clic en **Agregar** (Hinzufügen) y asígnele el nombre "Aura Command Palette".
3. Configure el **Atajo global** que desee (por ejemplo, `Meta+S` o `Ctrl+Alt+S`).
4. Establezca **Tipo** en "Comando" (Befehl).
5. Pegue el siguiente código JavaScript en el cuadro de comando:

__CODE_BLOCK_0__