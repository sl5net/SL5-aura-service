# CopyQ macOS 문제 해결: 보이지 않는 GUI 및 수동 단축키 구성

이 가이드에서는 CopyQ 그래픽 인터페이스(GUI)가 표시되지 않거나 GUI에 액세스하지 않고 전역 단축키(예: F10)를 다시 할당해야 하는 macOS(특히 Apple Silicon M 시리즈 장치)에서 발생하는 일반적인 문제를 다룹니다.

---

## 1. 보이지 않는 GUI 문제 해결

macOS에서 CopyQ는 다음 두 가지 주요 이유로 시각적으로 숨겨진 상태로 백그라운드에서 제대로 실행될 수 있습니다.
- **오프스크린 창 좌표**: 해상도가 변경되거나 외부 모니터 연결이 끊어진 후 CopyQ는 보이는 디스플레이 영역 외부의 좌표를 유지할 수 있습니다.
- **메뉴 막대 노치 방해**: 카메라 노치가 있는 MacBook 모델에서 macOS는 트레이가 가득 차면 자동으로 노치 뒤에 과도한 메뉴 막대 아이콘을 숨깁니다.

### 해결 방법: 형상 재설정 및 힘 표시

화면 밖의 좌표를 지우고 창을 전경으로 가져오려면 터미널에서 다음 명령을 실행하십시오.

```bash
copyq config geometry ""
copyq show
```

창이 여전히 표시되지 않으면 CLI를 통해 상태를 전환하세요.

```bash
copyq toggle
```

---

## 2. CudaText를 사용하여 수동으로 단축키 변경하기

전역 단축키(예: 'F10')가 다른 애플리케이션에 의해 요청되거나 가로채는 경우 CopyQ GUI를 열지 않고도 CudaText를 사용하여 구성 파일에서 단축키를 직접 편집할 수 있습니다.

### 1단계: CopyQ 프로세스 종료

종료 시 변경 사항을 덮어쓰지 않도록 구성 파일을 편집하기 전에 CopyQ를 중지해야 합니다.

```bash
copyq exit
```

### 2단계: CudaText에서 구성 열기

macOS에서 CopyQ 명령 단축키는 `copyq-commands.ini`에 저장됩니다.

CudaText에서 파일을 엽니다.

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

*참고: `Application Support`에 파일이 없으면 XDG 대체 위치를 엽니다.*

```bash
cudatext "$HOME/.config/copyq/copyq-commands.ini"
```

### 3단계: 바로가기 재지정

1- CudaText에서 `Cmd + F`를 눌러 검색창을 엽니다.
2- 'F10' 또는 'GlobalShortcut=F10'을 검색하세요.
3- 'F10'을 사용 가능한 단축키(예: 'F9', 'Ctrl+F10' 또는 'Meta+F10')로 바꿉니다.
4- 파일을 저장하고(`Cmd + S`) CudaText를 닫습니다(`Cmd + Q`).

### 4단계: CopyQ 다시 시작

업데이트된 바로가기 구성을 로드하려면 CopyQ를 다시 시작하세요.

```bash
open -a CopyQ
```

이제 새로운 전역 바로가기가 활성화됩니다.

(업데이트 : 8.9.'26 08:01 화)