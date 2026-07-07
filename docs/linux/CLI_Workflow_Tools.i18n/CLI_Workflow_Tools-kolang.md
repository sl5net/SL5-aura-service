# CLI 워크플로 도구 설치 가이드

경로 탐색기 플러그인의 일부 작업은 외부 명령줄 유틸리티를 사용하여 퍼지 검색을 수행하고, 파일을 나열하고, 클립보드를 조작합니다. 이러한 도구가 없으면 시스템 콘솔에 경고가 표시됩니다.

다음은 지원되는 각 운영 체제에 대한 설치 지침입니다.

## 필수 유틸리티

* **`fzf`**: 범용 명령줄 퍼지 파인더.
* **`find`** (또는 `fd`): 표준 파일 검색 유틸리티.
* **클립보드 도구**: 출력을 시스템 클립보드로 직접 파이프하는 데 사용됩니다.
* **Linux:** `xclip`(X11 환경 필요).
* **macOS:** `pbcopy`(사전 설치됨).
* **Windows:** `clip`(사전 설치됨).
* **`file`**: 전체 터미널 미리보기에 대한 파일 형식을 결정합니다.

---

## 설치 지침

### 1. 리눅스(아치/만자로)
시스템이 Manjaro에서 실행되므로 'pacman'을 사용하여 필요한 패키지를 설치할 수 있습니다.

```bash
sudo pacman -S fzf findutils xclip file
```

### 2. 리눅스(데비안/우분투/민트)
Debian 기반 시스템에서는 'apt'를 사용하세요.

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. 맥OS
[Homebrew](https://brew.sh/) 패키지 관리자를 사용하여 누락된 도구를 설치하십시오.

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. 윈도우
Windows를 사용하는 경우 [Scoop](https://scoop.sh/) 또는 [Winget](https://github.com/microsoft/winget-cli)를 통해 `fzf`를 설치하는 것이 좋습니다.

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
__CODE_BLOCK_4__