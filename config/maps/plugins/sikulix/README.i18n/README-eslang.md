[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Marco de automatización visual impulsado por visión por computadora
**Si puedes verlo, puedes automatizarlo.**

SikuliX ahora se mantiene activamente bajo [**oculix-org**](https://github.com/oculix-org), con el pleno acuerdo de su creador original [**RaiMan**](https://github.com/RaiMan).

## ¿Qué es SikuliX?
SikuliX utiliza **visión por computadora** (con tecnología [OpenCV](https://opencv.org/)) para identificar e interactuar con cualquier cosa visible en su pantalla, en **Windows**, **macOS** y **Linux**.

Localiza elementos de la GUI mediante **reconocimiento de imágenes** y luego los controla con acciones simuladas de mouse y teclado. No se requiere acceso al código fuente, DOM o API internas.

## Complemento Aura
Este complemento le permite dictar comandos de SikuliX por voz mientras el IDE de SikuliX está enfocado.

| Comando de voz (de) | Salida |
|---|---|
| "hacer clic" | `hacer clic("imagen.png")` |
| "doppelklick" | `doble clic("imagen.png")` |
| "rechtsklick" | `clic derecho("imagen.png")` |
| "warte" | `espera("imagen.png", 10)` |

Los comandos solo están activos cuando una ventana de SikuliX (`sikulixide`, `SikuliX`, `Sikuli`) está enfocada.

## Recursos
-[Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
-[SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)