# 1-클릭 설치 프로그램(Zero-Setup)

한 번의 클릭으로 컴퓨터에서 **Aura**를 실행해 보세요. 프로그래밍 지식, 터미널 명령 또는 수동 Python 설정이 필요하지 않습니다.

---

## 전제 조건 없음

다음은 필요하지 **않습니다**:
- Python이 사전 설치되어 있음
- Git 또는 코드 저장소
- 명령줄 또는 터미널 경험

---

## 빠른 시작

### 방법 1: Web One-Liner(Linux/macOS에서 가장 빠르고 권장됨)
수동 파일 처리 시간을 최대 30초 절약하고 터미널에서 즉시 시작합니다.

**리눅스 및 macOS:**
#### 웹 원라이너 CodeBerg
```bash
curl -sSL https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
또는
#### 웹 원라이너 GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**윈도우(파워셸):**
#### 웹 원라이너 CodeBerg
# 테스트되지 않음 - Windows용 방법 2(독립형 바이너리)를 사용하세요.
```bash
irm https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
또는
#### 웹 원라이너 github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

방법 2: 독립 실행형 바이너리(Windows 및 데스크톱 클릭)

### 2.1 설치 프로그램 다운로드
[최신 GitHub 릴리스]에서 운영 체제와 일치하는 단일 설치 프로그램 파일을 다운로드하세요.

- **윈도우즈:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **리눅스:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **맥OS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. 설치 프로그램 실행

aura-installer-windows.exe.zip의 이름을 aura-installer-windows.exe로 바꿉니다.

다운로드한 파일을 두 번 클릭합니다. 설정 창이 나타나며 자동으로 환경을 준비합니다.

### 2.3. 받아쓰기 시작
완료되면 Aura는 바탕 화면 바로 가기를 만들고 즉시 듣기 시작합니다.

---

## 자동으로 어떻게 되나요?

설치 프로그램을 실행하면 Aura가 자동으로 다음을 수행합니다.
- 로컬, 개인 음성 인식 엔진을 구성합니다.
- 기본 음성 모델을 다운로드합니다.
- 필요한 모든 시스템 바로가기와 데스크탑 실행기를 설정합니다.

---

## 설치 세부 정보 및 요구 사항

- **설치 시간:** 약 2~3분.
- **필요한 디스크 공간:** 최소 ~1.5GB(선택한 언어 모델에 따라 최대 2.5GB).
- **설치 디렉터리:**
- **Linux 및 macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## 다음 단계

- **할머니 모드:** 규칙 파일에 한 단어를 입력하고 Aura가 자동으로 규칙을 생성하는 것을 지켜보세요.
- **Koans로 배우기:** [Getting Started](../GettingStarted.i18n/GettingStarted-kolang.md)의 단계별 개념을 살펴보세요.