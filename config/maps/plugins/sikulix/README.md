[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Visual Automation Framework powered by Computer Vision
**If you can see it, you can automate it.**

SikuliX is now actively maintained under [**oculix-org**](https://github.com/oculix-org), with the full agreement of its original creator [**RaiMan**](https://github.com/RaiMan).

## What is SikuliX
SikuliX uses **computer vision** (powered by [OpenCV](https://opencv.org/)) to identify and interact with anything visible on your screen — across **Windows**, **macOS** and **Linux**.

It locates GUI elements through **image recognition**, then drives them with simulated mouse and keyboard actions. No access to source code, DOM or internal APIs required.

## Aura Plugin
This plugin lets you dictate SikuliX commands by voice while the SikuliX IDE is in focus.

| Voice command (de) | Output |
|---|---|
| "klick" | `click("image.png")` |
| "doppelklick" | `doubleClick("image.png")` |
| "rechtsklick" | `rightClick("image.png")` |
| "warte" | `wait("image.png", 10)` |

Commands are only active when a SikuliX window (`sikulixide`, `SikuliX`, `Sikuli`) is focused.

## Resources
- [Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
- [SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)

