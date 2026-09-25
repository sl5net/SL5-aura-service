> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# 1 클릭 설치자 (Zero-Setup)

Get **Aura ** 한 번의 클릭으로 기계에서 실행. 프로그래밍 지식, 터미널 명령, 또는 수동 Python 설정이 필요하지 않습니다.

---

## Zero 필수품

** 필요:
- Python 사전 설치
- Git 또는 코드 저장소
- 명령행 또는 터미널 경험

---

## 빠른 시작

## 방법 1: 웹 원라인러 (빠른 & Linux / macOS용 권장)
수동 파일 취급의 ~30 초를 저장하고 맨끝에서 즉각 시작하십시오:

**리눅스 및 macOS:**
### 웹 원라인 코드Berg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
또는
### 웹 원라인 GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**윈도우 (PowerShell):**
#### 웹 원라이너 코드버그

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
또는
#### 웹 원라이너 깃허브
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

방법 2: 독립 실행형 바이너리 (Windows 및 데스크톱 클릭)

### 2.1 설치 프로그램 다운로드
사용 중인 운영체제에 맞는 단일 설치 파일을 [최신 GitHub 릴리스]에서 다운로드하세요:

- **윈도우:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **리눅스:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. 설치 프로그램 실행

aura-installer-windows.exe.zip의 이름을 aura-installer-windows.exe로 변경하세요

다운로드한 파일을 더블 클릭하십시오. 설치 창이 나타나고 자동으로 환경을 준비합니다.

### 2.3. 받아쓰기 시작
완료되면 Aura는 바탕화면 바로가기를 생성하고 즉시 듣기를 시작합니다.

---

## 자동으로 일어나는 일은 무엇인가요?

설치 관리자를 실행하면 Aura가 자동으로:
- 로컬 사설 음성 인식 엔진을 구성합니다.
- 기본 음성 모델을 다운로드합니다.
- 필요한 모든 시스템 바로가기와 데스크톱 실행 아이콘을 설정합니다.

---

## 설치 세부 정보 및 요구 사항

- **설치 소요 시간:** 약 2~3분.
- **필요 디스크 공간:** 최소 약 1.5GB (선택한 언어 모델에 따라 최대 2.5GB).
- **설치 디렉토리:**
  - **리눅스 & macOS:** `~/opt/sl5-aura-service`
  - **윈도우:** `%LOCALAPPDATA%\sl5-aura-service`

---

## 다음 단계

- **할머니-모드:** 규칙 파일에 단어 하나를 입력하면 오라가 자동으로 규칙을 생성합니다.
- **코안과 함께 배우기:** [Getting Started](../GettingStarted.i18n/GettingStarted-kolang.md)에서 단계별 개념을 탐구하세요.
