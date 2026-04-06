[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Computer Vision으로 구동되는 시각적 자동화 프레임워크
**볼 수 있으면 자동화할 수 있습니다.**

SikuliX는 이제 원래 제작자 [**RaiMan**](https://github.com/RaiMan)의 완전한 동의를 받아 [**oculix-org**](https://github.com/oculix-org)에서 적극적으로 유지 관리됩니다.

## SikuliX 란 무엇입니까?
SikuliX는 **컴퓨터 비전**([OpenCV](https://opencv.org/) 기반)을 사용하여 **Windows**, **macOS** 및 **Linux**에서 화면에 보이는 모든 것을 식별하고 상호 작용합니다.

**이미지 인식**을 통해 GUI 요소를 찾은 다음 시뮬레이션된 마우스 및 키보드 동작으로 이를 구동합니다. 소스 코드, DOM 또는 내부 API에 대한 액세스가 필요하지 않습니다.

## 아우라 플러그인
이 플러그인을 사용하면 SikuliX IDE에 초점이 맞춰진 동안 SikuliX 명령을 음성으로 지시할 수 있습니다.

| 음성 명령(드) | 출력 |
|---|---|
| "클릭" | `클릭("image.png")` |
| "도펠클릭" | `doubleClick("image.png")` |
| "rechtsklick" | `rightClick("image.png")` |
| "warte" | `기다려("image.png", 10)` |

명령은 SikuliX 창(`sikulixide`, `SikuliX`, `Sikuli`)에 초점이 맞춰진 경우에만 활성화됩니다.

## 자원
- [Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
- [SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)