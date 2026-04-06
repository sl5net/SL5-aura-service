[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Estrutura de automação visual desenvolvida por visão computacional
**Se você pode ver, você pode automatizá-lo.**

SikuliX agora é mantido ativamente sob [**oculix-org**](https://github.com/oculix-org), com o acordo total de seu criador original, [**RaiMan**](https://github.com/RaiMan).

## O que é SikuliX
SikuliX usa **visão computacional** (com tecnologia [OpenCV](https://opencv.org/)) para identificar e interagir com qualquer coisa visível em sua tela — em **Windows**, **macOS** e **Linux**.

Ele localiza elementos da GUI por meio de **reconhecimento de imagem** e, em seguida, os direciona com ações simuladas de mouse e teclado. Não é necessário acesso ao código-fonte, DOM ou APIs internas.

## Plug-in Aura
Este plugin permite ditar comandos do SikuliX por voz enquanto o IDE do SikuliX está em foco.

| Comando de voz (de) | Saída |
|---|---|
| "clique" | `clique("imagem.png")` |
| "doppelklick" | `doubleClick("imagem.png")` |
| "rechtsklick" | `rightClick("imagem.png")` |
| "warte" | `espera("imagem.png", 10)` |

Os comandos só ficam ativos quando uma janela do SikuliX (`sikulixide`, `SikuliX`, `Sikuli`) está em foco.

## Recursos
-[Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
-[SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)