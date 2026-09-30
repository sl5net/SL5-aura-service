> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 오라 – 당신의 목소리. 당신의 규칙.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% 오프라인, 프라이버시 중심 음성 비서 프레임워크.  
> 단어 하나에서 당신의 목소리가 정확히 무엇을 하는지 정의하세요  
> 전체 Python 스크립트로. 클라우드 없음. 데이터가 머신을 벗어나지 않습니다.  
> 터미널, 브라우저 또는 백그라운드 서비스로 실행됨 — Linux, macOS 및 Windows에서.

| 👵 초보자 | 🎓 학습자 | 🧑‍💻 개발자 |
|---|---|---|
| [grandma-mode](../docs/GettingStarted-kolang.md#the-oma-modus-beginner-shortcut) : 단어만 쓰면, Aura가 나머지를 처리합니다 | 코안으로 배우기 — 한 번에 한 개념씩 | 전체 Python 스크립팅, 플러그인, API 호출 |
| 🗄️ 상태 관리 | Trino + Airflow 오케스트레이션, fzf, CopyQ, 음성/터미널 명령, 브라우저 UI |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **테스트당 약 2.87 J** (39개의 테스트, LanguageTool 없이, 800개 이상의 맵에서 @ 0.07초 웜 / 0.36초 콜드 🌿 [Eco-CI](https://metrics.green-coding.io/index.html)로 측정) · 클라우드 컴퓨팅 없음

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **전체 테스트 스위트:** 94개의 테스트, LanguageTool로 >800개의 지도에서 실행, 0.07초 웜 / 0.46초 콜드 · 클라우드 컴퓨팅 없음

<details>
<summary>빠른 시작</summary>

## 빠른 시작

### 옵션 A: 원클릭 & 웹 설치 프로그램 (추천)

Linux, macOS 및 Windows용 원라이너 명령어 또는 독립 실행 설치 프로그램:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller-kolang.md)**

---

## 옵션 B: 수동 설치 (개발자 / Git)

1. 다운로드 또는 복제 이 저장소
2. OS의 설정 스크립트를 실행 (`setup/` 폴더 참조):
   - 리눅스 (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - 리눅스 (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - 리눅스 (openSUSE): `bash setup/suse_setup.sh`
   - 리눅스 (NixOS): `nix-shell setup/shell.nix` 다음 `bash setup/nixos_setup.sh`
   ===> ︎️ 실험 - 저자, 피드백 환영에 의해 테스트!   
   - 맥 OS: `bash setup/macos_setup.sh`
   - 윈도우: `setup/windows11_setup_with_ahk_copyq.bat`
3. 시작 Aura: `./scripts/restart_venv_and_run-server.sh`
4. 단축키를 누르고 말하기 — **[full guide →](../docs/GettingStarted-kolang.md) * *

---

### 제거
SL5 Aura 배경 서비스, autostart 항목 및 가상 환경을 제거하려면 :
- ** 리눅스 / macOS:** `bash setup/uninstall.sh`
- **윈도우(PowerShell):** `powershell -File setup/uninstall.ps1`
* (`config/maps/`의 사용자 정의 규칙은 `--purge`를 지정하지 않는 한 기본적으로 안전합니다). *

---


시스템 요구 사항 및 호환성 * *

*   **Windows:** ✅ 완전 지원 (AutoHotkey/PowerShell 사용).
*   ** macOS:** ✅ 완전 지원 (AppleScript 사용).
*   ** 리눅스 (X11/Xorg):** ✅ 완전 지원.
*   **Linux (Wayland) :** ✅ 완전 지원 (KDE Plasma 6 / Wayland 테스트).
*   **Linux (CachyOS / Arch 기반 롤링 릴리스) : ** ✅ 완전 지원.
    glibc 2.43 호환성 때문에 mimalloc (`sudo pacman -S mimalloc`)가 필요합니다.
*   **Linux (NixOS):**   Experimental — 커뮤니티 기여 설정, 아직 테스트되지 않았습니다.
    당신이 그것을 시도하면, 당신의 발견과 문제 또는 PR을 열어!    
*   **리눅스 (Manjaro):** 새로운 : 시스템 전체 단축키는 fzf-like, 키보드 구동 인터페이스를 열고 바탕 화면의 어디에서나 Aura 명령을 실행할 수 있습니다. (일반적으로 활성 창에서 분리 됨). 이 단축키 구동 발사기는 현재 Linux (Manjaro);에서 구현 및 테스트됩니다. 다른 배포는 작동하지만 설정이 필요합니다. [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s-kolang.md)에 대해서    


    
SL5 Aura는**Vosk**(오라마)에 내장된 완전성**(오라마)과 **LanguageTool**(오라마/스타일용)로 구성되어 있습니다. 플러그 가능한 규칙 시스템과 동적 스크립트 엔진을 통해 궁극적 인 사용자 정의를 위해 설계된 정확한 행동과 텍스트로 목소리를 변환합니다.
    
번역: 이 문서는 [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n)에서도 존재합니다.


참고 : 많은 텍스트는 원래 영어 문서의 기계 생성 된 번역이며 일반적인지도에만 사용됩니다. discrepancies 또는 ambiguities의 경우, 영어 버전은 항상 준비합니다. 우리는이 번역을 개선하기 위해 커뮤니티에서 도움을 환영합니다!

</details>

<details>
<summary>계정 만들기</summary>

### 📺 터미널 데모

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **팁:** 더 나은 터미널 경험을 위해 [Zsh Integration](../docs/linux/zsh-integration-kolang.md)를 참조하세요.

### 🎥 비디오 튜토리얼
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(대체 링크: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>주요 특징</summary>

## 키 기능

*   ** 오프라인 및 개인 : ** 100 % 로컬. 아무 자료도 당신의 기계를 떠난다.
*   **Dynamic 스크립트 엔진: ** 텍스트 교체를 넘어갑니다. 규칙은 API를 호출하는 것과 같은 고급 작업을 수행하기 위해 사용자 정의 파이썬 스크립트 (`on_match_exec`)를 실행할 수 있습니다 (예를 들어, 파일과 상호 작용 (예를 들어, to-do 목록을 관리), 또는 동적 콘텐츠 생성 (예를들면, 컨텍스트 인식 이메일 인사).
*   **Context-Aware Rules:** 특정 애플리케이션에 대한 규칙을 제한합니다. `only_in_windows`를 사용하여 특정 창 제목 (예 : "Terminal", "VS Code"또는 "Browser")이 활성화되면 규칙 만 트리거를 보장 할 수 있습니다. Cross-platform(리눅스, 윈도우, macOS)를 사용합니다.
*  **높은 제어 변환 엔진: ** 구성 구동, 높은 customizable 처리 파이프라인을 구현합니다. 규칙 우선, 명령 감지 및 텍스트 변환은 퓨지 맵의 규칙의 순차적 순서에 의해 순으로 결정됩니다 ** 구성, 코딩하지 않는 **.
*   ** 보존 RAM 사용 : ** 지능적으로 메모리를 관리, 충분한 무료 RAM을 사용할 수 있다면 사전 로드 모델, 다른 응용 프로그램을 보장 (당신의 PC 게임과 같은) 항상 우선.
*   ** 크로스 플랫폼: ** Linux, macOS 및 Windows에서 작동합니다.
*   **Fully Automated:** 자신의 LanguageTool 서버를 관리 (하지만 외부를 사용할 수도 있습니다).
*   ** 빠른 검색 : ** 지능형 캐싱은 즉각적인 "듣기 ..." 알림 및 빠른 처리를 보장합니다.
*   ** Trino를 통한 Dynamic State Management: ** Interface-aware 구성 엔진
    `speech`, `terminal` 및 `web`에 대한 설정 분리 -없이 하나를 변경
    다른 사람. 실시간 **Admin Dashboard** (포트 8084)를 포함합니다.
</details>

<details>
<summary>Ready-to-use 통합</summary>
    
## 🔌 바로 사용할 수 있는 통합

SL5-Aura는 **100개 이상의 미리 구성된 플러그인**을 갖춘 방대한 생태계를 제공합니다. 다음은 몇 가지 하이라이트입니다:

OculiX / SikuliX IDE 음성 제어
SL5-Aura는 **OculiX** 및 **SikuliX IDE**의 일류 음성 지원을 제공합니다. 이 통합은 자동화 코드를 "speak"할 수 있습니다.

*   **Voice-to-Snippet: ** "click", "wait", 또는 "find all", 및 서비스는 즉시 올바른 파이썬 코드를 입력합니다 (예 : `click("image.png")`) IDE.
*   **Window-Aware:** 플러그인은 컨텍스트 감지; OculiX/SikuliX 창이 집중될 때만 활성화합니다.
*   **Smart English Support:** 비정상적인 악센트(e.g., German-English phonetics)에 특별한 초점과 `en-US`에 최적화되어 글로벌 커뮤니티의 높은 인식 정확도를 보장합니다.
*   ** 예외:** 쉽게 편집 `FUZZY_MAP_pre.py` 형식을 사용합니다.

> ** 서버:** OculiX 팀의 커뮤니티 플러그인으로 인정 ([Issue #204](https://github.com/oculix-org/Oculix/issues/204) 참조).

### LibreOffice IDE 음성 제어

### 0 A.D. 음성 제어

---

</details>


<details>
<summary>문서화</summary>

## 문서

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=ko)

모든 모듈과 스크립트를 포함한 완전한 기술 참조를 위해, 공식 문서 페이지를 방문하십시오. 이 문서는 자동으로 생성되며 항상 최신 상태로 유지됩니다.

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

### 기능 하이라이트
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run-kolang.md) — 이중 창 `fzf` 규칙 검색, 실시간 컨텍스트 미리보기, `Enter`/`Ctrl+R`를 통한 즉시 명령 실행, 그리고 `Ctrl+E`를 통한 편집기 통합. 전역 단축키(`Super+S`)와 음성 명령으로 미리 구성된 여러 전용 검색 환경이 지원됩니다.

### 빌드 상태

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

👉 **다른 언어로 읽기:**

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

---

<details>
<summary>설치</summary>

## 설치

### 😀 빠른 설치 모드없이 (Manjaro/Arch 비디오)
가득 차있는 6 분 체제 과정을 보십시오:
* ** 다운로드: ~3 분
* ** 설정 및 첫 시작:** ~3 분 (웰컴 마법사 포함)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


설정은 두 단계 과정입니다:
1.  최신 릴리스 또는 마스터 다운로드 ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) 또는 컴퓨터에 저장소 복제.
2.  운영 체제의 한 번 설정 스크립트를 실행합니다.

설정 스크립트는 모든 것을 처리합니다: 시스템 의존성, Python 환경, 그리고 필요한 모델과 도구를 다운로드 (~4GB)는 GitHub 릴리스에서 최고 속도.


#### 리눅스, macOS 및 윈도우용 (선택적 언어 제외 포함)

디스크 공간과 대역폭을 절약하기 위해 설치 과정에서 특정 언어 모델(`de`, `en`)이나 모든 선택적 모델(`all`)을 제외할 수 있습니다. **핵심 구성 요소(LanguageTool, lid.176)는 항상 포함됩니다.**

프로젝트의 루트 디렉터리에서 터미널을 열고 시스템에 맞는 스크립트를 실행하세요:

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

Windows를 위한 ####
관리자 권한으로 설정 스크립트를 실행합니다.

** 읽기 및 실행 도구, 예를 들어, [CopyQ](https://github.com/hluk/CopyQ) 또는 [AutoHotkey v2](https://www.autohotkey.com/)**. 이것은 text-typing watcher에 필요합니다.

설치는 완전히 자동화되고 약 걸립니다 ** 8-10 분 ** 신선한 시스템에 2 개의 모델을 사용할 때.

1. `setup` 폴더로 이동합니다.
2. **`windows11_setup_with_ahk_copyq.bat`**에서 더블 클릭.
   * *이 스크립트는 Administrator 특권에 자동으로 표시됩니다. *
   * *Core System, Language Models, **AutoHotkey v2**, **CopyQ**를 설치합니다. *
3. 설치가 완료되면 **Aura Dictation**가 자동으로 시작됩니다.

> **주의:** Python 또는 Git를 미리 설치할 필요가 없습니다. 스크립트는 모든 것을 처리합니다.

---

#### 고급 / 맞춤 설치
클라이언트 도구(AHK/CopyQ)를 설치하지 않거나 특정 언어를 제외하여 디스크 공간을 절약하고 싶다면 명령줄을 통해 핵심 스크립트를 실행할 수 있습니다:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>사용법</summary>

## 사용법

### 1. 서비스를 시작합니다

#### 리눅스 및 macOS에서
하나의 스크립트가 모든 것을 처리합니다. 메인 받아쓰기 서비스와 파일 감시자를 자동으로 백그라운드에서 시작합니다.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### 윈도우에서
서비스 시작은 **두 단계의 수동 과정**입니다:

1.  **주요 서비스 시작:** `start_aura.bat`를 실행하거나 `.venv`에서 `python3`로 서비스를 시작합니다

### 2. 단축키 설정

음성 입력을 트리거하려면 특정 파일을 생성하는 전역 단축키가 필요합니다. 우리는 크로스 플랫폼 도구 [CopyQ](https://github.com/hluk/CopyQ)를 강력히 추천합니다.

#### 저희 추천: CopyQ

글로벌 단축키로 CopyQ에 새 명령을 만드세요.

**리눅스/macOS용 명령어:**
```bash
touch /tmp/sl5_record.trigger
```

**[CopyQ](https://github.com/hluk/CopyQ)를 사용할 때 Windows용 명령어:**
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**[AutoHotkey](https://AutoHotkey.com)를 사용할 때 Windows용 명령:**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 script
#SingleInstance Force ; Ensures only one instance of the script runs

;===================================================================
; Hotkey to trigger Aura
; Press Ctrl + Alt + T to write the trigger file.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger activated!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3. 받아쓰기를 시작하세요!
텍스트 필드 아무 곳이나 클릭하고 단축키를 누르면 '듣는 중...' 알림이 표시됩니다. 명확하게 말한 후 잠시 멈추세요. 수정된 텍스트가 입력됩니다.

</details>

---


<details>
<summary>고급 설정(선택 사항)</summary>

## (선택) 진보된 윤곽

로컬 설정 파일을 작성하여 응용 프로그램의 행동을 사용자 정의 할 수 있습니다.

1.  `config/` 디렉토리로 이동합니다.
2.  `config/settings_local.py_Example.txt`의 복사본을 만들고 `config/settings_local.py`로 이름을 변경합니다.
3.  `config/settings_local.py`를 편집하십시오 (주요 `config/settings.py` 파일에서 어떤 설정을 overrides).

이 `config/settings_local.py` 파일은 기본적으로 Git에 의해 무시됩니다, 그래서 귀하의 개인 변경은 업데이트에 의해 과잉되지 않습니다.

플러그 인 구조 및 논리

시스템의 모듈성은 플러그인 / 지시를 통해 강력한 확장을 허용합니다.

가공 엔진은 **Hierarchical Priority Chain ***에 엄격히 준수합니다.

1. **Module 선적 순서 (높은 우선권): ** 핵심 언어 팩 (de-DE, en-US)에서 로드된 규칙은 플러그인/디렉토리 (마지막 알파벳으로 로드되는)에서 로드된 규칙에 대한 우선 순위를 취합니다.
    
2. **In-File Order (Micro Priority): ** 주어진 맵 파일 내 (FUZZY MAP pre.py), 규칙은 ** 라인 번호** (top-to-bottom)에 의해 엄격히 처리됩니다.
    

이 아키텍처는 핵심 시스템 규칙이 보호되고, 프로젝트 별 또는 컨텍스트 인식 규칙 (CodeIgniter 또는 게임 컨트롤과 같은)은 플러그 인을 통해 낮은 선명도 확장으로 쉽게 추가 할 수 있습니다.

</details>

<details>
<summary>Windows 사용자용 키 스크립트</summary>






## 윈도우 사용자용 주요 스크립트

다음은 Windows 시스템에서 애플리케이션을 설정, 업데이트 및 실행하는 데 가장 중요한 스크립트 목록입니다.

### 설치 및 업데이트

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: 환경의 **초기 일회성 설정**을 위한 주요 스크립트입니다.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : 최신 코드와 종속성을 **가져오기 위해** 프로젝트 폴더에서 이것을 실행하세요.

### 애플리케이션 실행
*   `start_aura.bat`: 받아쓰기 서비스를 **시작하는** 기본 스크립트입니다.

### 핵심 및 도우미 스크립트
*   `aura_engine.py`: 핵심 Python 서비스(일반적으로 위 스크립트 중 하나에 의해 시작됨).
*   `get_suggestions.py`: 특정 기능을 위한 도우미 스크립트입니다.

</details>



## 🚀 주요 기능 및 운영 체제 호환성

<details>
<summary>OS 호환성 범례</summary>

운영 체제 호환성에 대한 범례:  
*   🐧 **리눅스** (예: 아치, 우분투)  
    *   🍏 **macOS**  
*   🪟 **윈도우**  
*   📱 **안드로이드** (모바일 특정 기능용)  

---

</details>



###**Core Speech-to-Text (Aura) 엔진* *
    오프라인 음성 인식 및 오디오 처리를위한 주요 엔진.

    
<details>
<summary>Aura 핵심</summary>

** 아우라 코어 / ** 🐧 🍏 🪟  
├─ `aura_engine.py` (주요 파이썬 서비스 오케스트라 아우라) 🐧 🍏 🪟  
├┬ **리브 핫로드 ** (Config & Maps) 🐧 🍏 🪟  
│├ **Secure 개인지도 로딩 (Integrity-First)** 🔒  🐧 🍏 🪟  
││ * ** 워크플로우:** 비밀번호 보호 ZIP 아카이브를로드합니다.   
│├ ** 텍스트 처리 및 수정 ** 언어에 의해 그룹화 (예 : `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (표준화 후문) 🐧 🍏 🪟  
│├ 2. **Intelligent Pre-Correction** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules-kolang.md)) 🐧 🍏 🪟  
││ * **Dynamic Script Execution: 규칙은 API 호출, 파일 I/O와 같은 고급 작업을 수행하기 위해 사용자 정의 파이썬 스크립트 (`on_match_exec`)를 트리거하거나 동적 응답을 생성합니다.  
││ * **Cascading 실행:** 규칙은 순차적으로 처리되고 그들의 효력은 **cumulative **입니다. 나중에 규칙은 이전 규칙에 의해 수정 된 텍스트에 적용됩니다.  
││ * **Highest Priority Stop Criterion:** 규칙이 **Full Match** (^...$)를 달성하면 토큰의 전체 처리 파이프라인이 즉시 중지됩니다. 이 메커니즘은 신뢰할 수있는 음성 명령을 구현하는 데 중요합니다.  
│├ 3. `correct_text_by_languagetool.py` (문자 / 스타일 보정을위한 언어 도구 통합) 🐧 🍏 🪟  
│├ **4. Ollama AI Fallback * *를 가진 Hierarchical RegEx 규칙 엔진 🐧 🍏 🪟  
││ * **Deterministic Control:** 정확한, 높은-priority 명령 및 텍스트 컨트롤을 위한 RegEx Rule Engine을 사용합니다.  
│├ *Vector-Search Plugin** (라지 로딩): Ollama/LLM fallback layer와 로컬 Vector embeddings를 연결하여 Semantic Search를 활성화 🐧  
││ * **올라마 AI (Local LLM) Fallback:** **creative Answer, Q&A 및 고급 Fuzzy Matching**에 대한 선택적, 낮은 선명도 검사로 제공.  
││ * **Status:** 로컬 LLM 통합.
│└ 5. **Intelligent Post-Correction** (`FuzzyMap`)**– Post-LT Refinement * * * 🐧 🍏 🪟  
││ * LanguageTool가 LT-specific output을 수정한 후 적용됨. 동일한 엄격한 캐스케이드 우선 논리를 pre-correction 층으로 따릅니다.  
││ * *Dynamic Script Execution: 규칙은 API 호출, 파일 I/O와 같은 고급 작업을 수행하기 위해 사용자 정의 파이썬 스크립트 ([on_match_exec](../docs/advanced-scripting-kolang.md))를 트리거하거나 동적 응답을 생성합니다.  
││ * **Fuzzy Fallback: ** **Fuzzy similarity Check** (계값에 의해 제어, 예를 들어, 85 %)는 가장 낮은 우선 오류 방지 층 역할을합니다. 전신 결정/카스케이프 규칙이 일치할 수 없는 경우만 실행됩니다. (현재 규칙은 false입니다), 가능한 한 느슨한 체크를 피함으로써 성능 최적화.  
├┬ **모델 관리/**   
│├─ `prioritize_model.py` (사용에 따라 모델로드 /로드 최적화) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (최초 모델 설정 구성) 🐧 🍏 🪟  
├─ ** 적합한 VAD 타임아웃 * * 🐧 🍏 🪟  
├─ **Adaptive Hotkey (시작 / 정지) ** 🐧 🍏 🪟  
├─ ** 즉시 언어 전환 ** (모델 사전 로드를 통해 실험) 🐧 🍏         
├─ **Airflow Orchestration** (DAG 기반 워크플로우 자동화) 🐧 🍏 🪟
│   도커 · UI 필요: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino State Engine** (문자/terminal/web 당 인터페이스) 🐧 🍏 🪟
└─  Docker · Admin UI가 필요합니다. `http://localhost:8084` 🐧 🍏 🪟  

**시스템/**   
├┬ **LanguageTool 서버 관리/**   
│├─ `start_languagetool_server.py` (지역 언어 도구 서버 통합) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (LanguageTool 서버를 중단) 🐧 🍏 
├─ `monitor_mic.sh` (사용 키보드 및 모니터없이 헤드셋과 함께 사용) 🐧 🍏 🪟  

### **모델 및 패키지 관리**  
    대형 언어 모델을 안정적으로 다루기 위한 도구.  

**모델관리/** 🐧 🍏 🪟  
├─ **견고한 모델 다운로더** (GitHub 릴리스 청크) 🐧 🍏 🪟  
├─ `split_and_hash.py` (큰 파일을 분할하고 체크섬을 생성하기 위한 저장소 소유자용 유틸리티) 🐧 🍏 🪟  
└─ `download_all_packages.py` (최종 사용자가 멀티파트 파일을 다운로드, 확인 및 재조립하기 위한 도구) 🐧 🍏 🪟  

</details>


<details>
<summary>개발 및 배포 도우미</summary>

### **개발 및 배포 지원 * *  
    환경 설정, 테스트 및 서비스 실행에 대한 스크립트.  

*Tip: glogg는 로그 파일에서 흥미로운 이벤트를 검색하려면 정규 표현식을 사용할 수 있습니다. *     
로그 파일에 연결할 때 체크 박스를 확인하십시오.    
https://glogg.bonnefon.org/ - 한국어     
    
팁 : regex 패턴을 정의 한 후, `python3 tools/map_tagger.py`를 실행하여 CLI 도구에 대한 검색 가능한 예를 자동으로 생성합니다. 자세한 내용은 [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools-kolang.md) 참조. *

그런 다음 두 번 클릭
`log/aura_engine.log`
    
**DevHelpers / **  
├┬ **가상 환경 관리/**  
│├ `scripts/restart_venv_and_run-server.sh` (리눅스/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (윈도우) 🪟  
├┬ **시스템 전체 Dictation 통합/* *  
│├ Vosk 시스템 인라이브 통합 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (리눅스 특정 마이크 모니터링) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey는 인식 된 텍스트를 듣고 시스템 전체를 입력합니다) 🪟  
└─ **CI/CD 자동화/**  
    └─ 확장된 GitHub Workflows (설치, 테스트, 문서 배포) 李俊億  

</details>

<details>
<summary>실험 기능</summary>
    
###**실행 / 실험 기능 * *  
    현재 개발중인 기능 또는 초안 상태.  

** 실험 기능/**  
├─ **ENTER AFTER DICTATION REGEX ** 예제 활성화 규칙 "(ExampleAplicationThatNotExist|Pi, 개인 AI)" 🐧  
├┬플러그인  
│**Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Changes to Plugin Activation/deactivation, and their configurations, service restart.*없이 다음 처리 실행에 적용됩니다.)  
│ ├ **git commands* (git 명령어를 보내는 음성 제어) 🐧 🍏 🪟  
│ ├ ** Wannweil** (위치 독일-Wannweil 지도) 🐧 🍏 🪟  
│ ├ **Poker 플러그인 (Draft) ** (포커 애플리케이션의 음성 제어) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (0 A.D. 게임용 마우스 컨트롤) 🐧   
├─ ** 세션 시작 또는 종료시 출력 ** (Description pending) 🐧   
├─ **Speech는 Visually Impaired에 대한 출력** (Description pending) 🐧 🍏 🪟  
└─ *SL5 Aura Android Prototype** (전체 오프라인 없음) 📱  

---

* (주: Arch (ARL) 또는 Ubuntu (UBT)와 같은 특정 Linux 배포는 일반 Linux 李俊億 상세 구분은 설치 안내서에 포함될 수 있습니다. *
</details>

<details>
<summary>이 스크립트 목록을 생성하기 위해 사용되는 명령을 보려면</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>건축의 그래픽 개요</summary>

### 아키텍처의 그래픽 개요:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>사용된 모델</summary>

사용된 모형:

추천: 거울에서 모델 사용 https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (가장 빠른)

이 zipped 모델은 `models/` 폴더에 저장되어야 합니다.

`mv vosk-model-*.zip models/`


| 모델 | 크기 | 단어 오류율/속도 | 주 | 라이센스 |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter) | 정확한 일반 미국 영어 모델 | 아파치 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G | 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (ml)<br/>33.26 (mtedx) | 텔레폰 및 서버를위한 큰 독일어 모델 | 아파치 2.0 |

이 테이블은 크기, 단어 오류율 또는 속도, 노트 및 라이센스 정보를 포함하여 다른 Vosk 모델의 개요를 제공합니다.


- ** Vosk 모델:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- ** 언어 도구:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

** 언어 도구의 장점 :** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

프로젝트 지원
이 도구를 유용한 경우, 우리를 구입하시기 바랍니다 커피! 당신의 지원은 연료 미래 개선을 돕습니다.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

