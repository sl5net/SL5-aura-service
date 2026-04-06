[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Framework automatyzacji wizualnej oparty na technologii Computer Vision
**Jeśli to widzisz, możesz to zautomatyzować.**

SikuliX jest obecnie aktywnie utrzymywany pod [**oculix-org**](https://github.com/oculix-org), za pełną zgodą jego pierwotnego twórcy [**RaiMan**](https://github.com/RaiMan).

## Czym jest SikuliX
SikuliX wykorzystuje **wizję komputerową** (obsługiwaną przez [OpenCV](https://opencv.org/)) do identyfikacji i interakcji ze wszystkim, co jest widoczne na ekranie — w **Windows**, **macOS** i **Linux**.

Lokalizuje elementy GUI poprzez **rozpoznawanie obrazu**, a następnie steruje nimi za pomocą symulowanych działań myszy i klawiatury. Nie jest wymagany dostęp do kodu źródłowego, DOM ani wewnętrznych API.

## Wtyczka Aura
Ta wtyczka umożliwia dyktowanie poleceń SikuliX za pomocą głosu, gdy aktywne jest środowisko SikuliX IDE.

| Polecenie głosowe (de) | Wyjście |
|---|---|
| "kliknij" | `click("image.png")` |
| "doppelklick" | `doubleClick("image.png")` |
| "rechtsklick" | `rightClick("image.png")` |
| "warte" | `wait("image.png", 10)` |

Polecenia są aktywne tylko wtedy, gdy aktywne jest okno SikuliX („sikulixide”, „SikuliX”, „Sikuli”).

## Zasoby
-[Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
-[SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)