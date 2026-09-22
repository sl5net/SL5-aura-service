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
> 당신의 목소리가 정확히 무엇을 하는지 정의하세요 — 한 단어로부터
> 전체 Python 스크립트로. 클라우드 없음. 데이터가 당신의 기기를 떠나지 않음.  
> 터미널, 브라우저 또는 백그라운드 서비스로 실행되며 — Linux, macOS 및 Windows에서 가능합니다.

| 👵 초보 | 🎓 학습자 | 🧑‍💻 개발자 |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-kolang.md#the-oma-modus-beginner-shortcut) : 단어만 쓰면, Aura가 나머지를 처리합니다 | 코안으로 배우기 — 한 번에 한 개념씩 | 전체 Python 스크립팅, 플러그인, API 호출 |
| 🗄️ 상태 관리 | Trino + Airflow 오케스트레이션, fzf, CopyQ, 음성/터미널 명령, 브라우저 UI |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **테스트당 ~2.87 J** (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · 클라우드 컴퓨팅 없음

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **전체 테스트 스위트:** 94개의 테스트, LanguageTool로 800개 이상의 맵에서 실행, 웜 0.07초 / 콜드 0.46초 · 클라우드 컴퓨팅 없음

<details>
<summary>빠른 시작</summary>

## 빠른 시작

### 옵션 A: 원클릭 및 웹 설치 프로그램 (Recommended)

Linux, macOS 및 Windows용 한 줄 명령어 또는 독립 실행형 설치 프로그램:
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-kolang.md)**

---

## 옵션 B: 수동 설치 (개발자 / Git)

1. 다운로드 또는 복제 이 저장소
2. OS의 설정 스크립트를 실행 (`setup/` 폴더 참조):
- 리눅스 (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh`
- 리눅스 (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
- 리눅스 (openSUSE): `bash setup/suse_setup.sh`
- 리눅스 (NixOS): `nix-shell setup/shell.nix` 다음 `bash setup/nixos_setup.sh`
===> ⚠️ 실험 - 저자, 피드백 환영에 의해 테스트! XSPACE인실
- macOS: `bash setup/macos_setup.sh`
- 윈도우: `setup/windows11_setup_with_ahk_copyq.bat`
3. 아우라 시작: `./scripts/restart_venv_and_run-server.sh`
4. 단축키를 누르고 말하기 — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-kolang.md)**

---

### 제거
SL5 Aura 배경 서비스, autostart 항목 및 가상 환경을 제거하려면 :
- **리눅스 / macOS:** `bash setup/uninstall.sh`
- **Windows(PowerShell):** `powershell -File setup/uninstall.ps1`
* (`config/maps/`의 사용자 정의 규칙은 `--purge`를 지정하지 않는 한 기본적으로 안전합니다).*

---


**⚠️ 시스템 요구 사항 및 호환성**

***Windows:** ✅ 완전 지원(AutoHotkey/PowerShell 사용).
* ** macOS:** ✅ 완전 지원 (AppleScript 사용).
* ** 리눅스 (X11/Xorg):** ✅ 완전 지원.
* **Linux (Wayland) : ** ✅ 완전 지원 (KDE Plasma 6 / Wayland 테스트).
* **Linux (CachyOS / Arch 기반 롤링 릴리스) : ** ✅ 완전 지원.
glibc 2.43 호환성 때문에 mimalloc (`sudo pacman -S mimalloc`)가 필요합니다.
* **Linux (NixOS):** N Experimental - 아직 테스트되지 않은 커뮤니티 기여 설정.
당신이 그것을 시도하면, 당신의 발견과 문제 또는 PR을 열어! XSPACE인실  
* **리눅스 (Manjaro):** 새로운 : 시스템 전체 단축키는 fzf-like, 키보드 구동 인터페이스를 열고 바탕 화면의 어디에서나 Aura 명령을 실행할 수 있습니다. (일반적으로 활성 창에서 분리 됨). 이 단축키 구동 발사기는 현재 리눅스 (Manjaro); 다른 배포에서 구현 및 테스트되었지만 설정이 필요합니다. [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-kolang.md) XSPACE인실  


    
SL5 Aura는**Vosk**(오라마)에 내장된 완전성**(오라마)과 **LanguageTool**(오라마/스타일용)로 구성되어 있습니다. 플러그 가능한 규칙 시스템과 동적 스크립트 엔진을 통해 궁극적 인 사용자 정의를 위해 설계된 정확한 행동과 텍스트로 목소리를 변환합니다.
    
번역: 이 문서는 [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n)에서도 존재합니다.


참고 : 많은 텍스트는 원래 영어 문서의 기계 생성 된 번역이며 일반적인지도에만 사용됩니다. discrepancies 또는 ambiguities의 경우, 영어 버전은 항상 준비합니다. 우리는이 번역을 개선하기 위해 커뮤니티에서 도움을 환영합니다!

</details>

<details>
<summary>Demo</summary>

### COIN 터미널 데모

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **팁:** 더 나은 터미널 경험을 위해 [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-kolang.md)를 참조하십시오.

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(단일 링크: [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>Key 기능</summary>

## 키 기능

* ** 오프라인 및 개인 : ** 100 % 로컬. 아무 자료도 당신의 기계를 떠난다.
* **Dynamic 스크립트 엔진: ** 텍스트 교체를 넘어갑니다. 규칙은 API를 호출하는 것과 같은 고급 작업을 수행하기 위해 사용자 정의 파이썬 스크립트 (`on_match_exec`)를 실행할 수 있습니다 (예를 들어, 파일과 상호 작용 (예를 들어, to-do 목록을 관리), 또는 동적 콘텐츠 생성 (예를들면, 컨텍스트 인식 이메일 인사).
* **Context-Aware Rules:** 특정 응용 프로그램에 규칙을 제한합니다. `only_in_windows`를 사용하여 특정 창 제목 (예 : "Terminal", "VS Code"또는 "Browser")이 활성화되면 규칙 만 트리거를 보장 할 수 있습니다. Cross-platform(리눅스, 윈도우, macOS)를 사용합니다.
* **높은 제어 변환 엔진: ** 구성 구동, 높은 customizable 처리 파이프라인을 구현합니다. 규칙 우선, 명령 감지 및 텍스트 변환은 퓨지 맵의 규칙의 순차적 순서에 의해 순으로 결정됩니다 ** 구성, 코딩하지 않는 **.
* ** 보존 RAM 사용:** 지능적으로 메모리를 관리, 충분한 무료 RAM을 사용할 수 있다면 사전 로드 모델, 다른 응용 프로그램을 보장 (당신의 PC 게임과 같은) 항상 우선.
* ** 크로스 플랫폼: ** Linux, macOS 및 Windows에서 작동합니다.
***Fully Automated:** 자신의 LanguageTool 서버를 관리 (하지만 외부를 사용할 수도 있습니다).
* ** 빠른 검색 : ** 지능형 캐싱은 즉각적인 "듣기 ..." 알림 및 빠른 처리를 보장합니다.
* ** Trino를 통한 Dynamic State Management: ** Interface-aware 구성 엔진
`speech`, `terminal` 및 `web`에 대한 설정 분리 -없이 하나를 변경
다른 사람에 영향을 미치는. 실시간 **Admin Dashboard** (포트 8084)를 포함합니다.
</details>

<details>
<summary> 는 지원 통합 </summary>
  
    
## 🔌 바로 사용 가능한 통합

SL5-Aura는 **100개 이상의 미리 구성된 플러그인**을 갖춘 방대한 생태계를 제공합니다. 다음은 몇 가지 하이라이트입니다:

### OculiX/SikuliX IDE 음성 제어
SL5-Aura는 **OculiX** 및 **SikuliX IDE**의 일류 음성 지원을 제공합니다. 이 통합은 자동화 코드를 "speak"할 수 있습니다.

***Voice-to-Snippet:** "click", "wait", 또는 "find all", 및 서비스는 즉시 올바른 파이썬 코드를 입력합니다 (예 : `click("image.png")`) IDE.
* **Window-Aware:** 플러그인은 컨텍스트 감지; OculiX/SikuliX 창이 집중될 때만 활성화합니다.
* **Smart English Support:** 비정상적인 악센트(e.g., German-English phonetics)에 특별한 초점과 `en-US`에 최적화되어 글로벌 커뮤니티의 높은 인식 정확도를 보장합니다.
* ** 예외:** 쉽게 편집 `FUZZY_MAP_pre.py` 형식을 사용합니다.

> ** 서버:** OculiX 팀의 커뮤니티 플러그인으로 인정 ([Issue #204](https://github.com/oculix-org/Oculix/issues/204) 참조).

### 리브레오피스 IDE 음성 제어

### 0 A.D. 음성 제어

---

</details>


<details>
XHTML태그2X문서화XHTML태그3X

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## 문서

모든 모듈과 스크립트를 포함한 완전한 기술 참조를 원하신다면, 공식 문서 페이지를 방문해 주세요. 이 문서는 자동으로 생성되며 항상 최신 상태로 유지됩니다.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

### 기능 스포트라이트
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-kolang.md) - Dual-pane `fzf` 규칙 검색, 라이브 컨텍스트 미리보기, `Enter`/`Ctrl+R`를 통해 즉시 명령 실행, `Ctrl+E`를 통해 편집기 통합. Global Hotkey (`Super+S`) 및 음성 명령을 통해 여러 개의 전용 검색 환경이 사전 구성되었습니다.

## 빌드 상태

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

더 많은 언어:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-kolang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-kolang.md) | [🇪🇸 Español](../README.i18n/README-eslang-kolang.md) | [🇫🇷 Français](../README.i18n/README-frlang-kolang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-kolang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-kolang.md) | [🇰🇷 한국어](../README.i18n/README-kolang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-kolang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-kolang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-kolang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-kolang.md)

---

<details>
<summary>설치</summary>

## 설치

### 😀 빠른 설치 모드없이 (Manjaro/Arch 비디오)
가득 차있는 6 분 체제 과정을 보십시오:
***다운로드:** ~3분
***Setup & First Start:** ~3분 (Welcome Wizard 포함)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


설정은 두 단계 과정입니다:
1. 최신 릴리스 또는 마스터 다운로드 ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) 또는 복제본이 컴퓨터에 저장소.
2. 운영 체제의 한 번 설정 스크립트를 실행합니다.

설정 스크립트는 모든 것을 처리합니다: 시스템 의존성, Python 환경, 그리고 필요한 모델과 도구를 다운로드 (~4GB)는 GitHub 릴리스에서 최고 속도.


Linux, macOS 및 Windows용 ####(옵션 언어 제외)

디스크 공간 및 대역폭을 저장하려면 특정 언어 모델 (`de`, `en`) 또는 설정 중 모든 옵션 모델 (`all`)을 제외 할 수 있습니다. ** 코어 구성 요소 (LanguageTool, lid.176)은 항상 포함되어 있습니다. **

프로젝트의 루트 디렉토리에 터미널을 열고 시스템에 대한 스크립트를 실행:

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
2. ** `windows11_setup_with_ahk_copyq.bat` **에서 더블 클릭.
*이 스크립트는 Administrator 특권에 대해 자동으로 프롬프트합니다.*
* Core System, Language Models, **AutoHotkey v2**, **CopyQ**를 설치합니다.*
3. 설치가 완료되면 **Aura Dictation**가 자동으로 시작됩니다.

> **주의:** Python 또는 Git beforehand를 설치할 필요가 없습니다. 스크립트는 모든 것을 처리합니다.

---

#### 고급/주문 임명
클라이언트 도구 (AHK/CopyQ)를 설치하지 않거나 특정 언어를 제외하고 디스크 공간을 저장하려면 명령 줄을 통해 핵심 스크립트를 실행할 수 있습니다.

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
<summary>Usage</summary>

## 사용법

##1. 서비스 시작

Linux 및 macOS의 ####
단일 스크립트는 모든 것을 처리합니다. 그것은 주요 인용 서비스 및 파일 watcher를 자동으로 배경에서 시작합니다.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

Windows에서 ####
서비스 시작은 ** 2단계 수동 프로세스**:

1. ** 메인 서비스 시작:** `start_aura.bat` 실행. 또는 `.venv`에서 시작 `python3`

##2. 단축키

dictation을 트리거하려면 특정 파일을 생성하는 글로벌 단축키가 필요합니다. 크로스 플랫폼 도구 [CopyQ](https://github.com/hluk/CopyQ)를 적극 추천합니다.

### 우리의 추천: CopyQ

CopyQ의 새로운 명령을 글로벌 단축키로 만듭니다.

** 리눅스 / macOS에 대한 권한: **
```bash
touch /tmp/sl5_record.trigger
```

**[CopyQ](https://github.com/hluk/CopyQ)를 사용할 때 Windows 용 COMmand : **
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


**[AutoHotkey](https://AutoHotkey.com)를 사용할 때 Windows 용 COMmand : **
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


##3. 수정 시작!
텍스트 필드를 클릭하면 단축키를 누르고 "Listening..." 알림이 나타납니다. 분명히 말하고, 일시 중지. 올바른 텍스트는 당신을 위해 입력됩니다.

</details>

---


<details>
(선택) <summary>Advanced 윤곽 </summary>

## (선택) 진보된 윤곽

로컬 설정 파일을 작성하여 응용 프로그램의 행동을 사용자 정의 할 수 있습니다.

1. `config/` 디렉토리로 이동합니다.
2. `config/settings_local.py_Example.txt`의 복사본을 만들고 `config/settings_local.py`로 이름을 변경하십시오.
3. `config/settings_local.py`를 편집하십시오 (주요 `config/settings.py` 파일에서 어떤 조정든지 overrides).

이 `config/settings_local.py` 파일은 기본적으로 Git에 의해 무시됩니다, 그래서 귀하의 개인 변경은 업데이트에 의해 과잉되지 않습니다.

### 플러그인 구조 및 논리

시스템의 모듈성은 플러그인 / 디렉토리를 통해 강력한 확장을 허용합니다.

가공 엔진은 **Hierarchical Priority Chain**에 엄격히 준수합니다.

1. ** 모듈로드 주문 (고 우선) : ** 핵심 언어 팩 (de-DE, en-US)에서 로드된 규칙은 플러그인/ 디렉토리 (마지막 알파벳으로 로드되는)에서 로드된 규칙에 대한 우선 순위를 취합니다.
    
2. **In-File Order (Micro Priority): ** 주어진 맵 파일 내 (FUZZY MAP pre.py), 규칙은 **라인 번호** (top-to-bottom)에 의해 엄격히 처리됩니다.
    

이 아키텍처는 핵심 시스템 규칙이 보호되고, 프로젝트 별 또는 컨텍스트 인식 규칙 (CodeIgniter 또는 게임 컨트롤과 같은)은 플러그 인을 통해 낮은 선명도 확장으로 쉽게 추가 할 수 있습니다.

</details>

<details>
Windows Users</summary>에 대한 <summary>Key 스크립트






## 윈도우 사용자용 주요 스크립트

다음은 Windows 시스템에서 애플리케이션을 설정, 업데이트 및 실행하는 데 가장 중요한 스크립트 목록입니다.

### 설치 및 업데이트

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: 환경의 **초기 일회성 설정**을 위한 주요 스크립트.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : 프로젝트 폴더에서 실행하여 **최신 코드와 종속성을 가져오세요**.

### 애플리케이션 실행
*   `start_aura.bat`: 받아쓰기 서비스를 **시작하는** 기본 스크립트입니다.

### 핵심 및 보조 스크립트
*   `aura_engine.py`: 코어 Python 서비스(보통 위 스크립트 중 하나에 의해 시작됨).
*   `get_suggestions.py`: 특정 기능을 위한 도우미 스크립트.

</details>



## 🚀 주요 기능 및 운영 체제 호환성

<details>
OS 호환성을 위한 전설

OS 호환성 전설:  
*   🐧 **리눅스** (예: 아치, 우분투)
    *   🍏 **macOS**  
*   🪟 **윈도우즈**  
*   📱 **안드로이드** (모바일 전용 기능용)

---

</details>



##**Core Speech-to-Text (Aura) 엔진**
오프라인 음성 인식 및 오디오 처리를위한 주요 엔진.

    
<details>
<summary>Aura-Core</summary>
  
**Aura-Core/** A EA  
├─ `aura_engine.py` (주요 파이썬 서비스 오케스트라)  
├┬ **Live Hot-Reload** (Config & Maps) EA EA  
│├ **Secure 개인지도 로딩 (Integrity-First)** └ 李俊億  
││ * ** 워크플로우:** 비밀번호 보호 ZIP 아카이브를로드합니다. XSPACE인실  
│├ ** 텍스트 처리 및 수정 ** 언어에 의해 그룹화 (예 : `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (표준화) 진동 포스트 지연  
│├ 2.**Intelligent Pre-Correction** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-kolang.md)) 李俊億  
││ ***Dynamic 스크립트 실행:** 규칙은 API 호출, 파일 I/O와 같은 고급 작업을 수행하기 위해 Python 스크립트 (`on_match_exec`)를 트리거하거나 동적 응답을 생성합니다. XSPACE인실  
││ * **Cascading 실행:** 규칙은 순차적으로 처리되고 그들의 효력은 **cumulative **입니다. 나중에 규칙은 이전 규칙에 의해 수정 된 텍스트에 적용됩니다.  
││ * **Highest Priority Stop Criterion:** 규칙이 **Full Match** (^...$)를 달성하면 토큰의 전체 처리 파이프라인이 즉시 중지됩니다. 이 메커니즘은 신뢰할 수있는 음성 명령을 구현하는 데 중요합니다. XSPACE인실  
│├ 3. `correct_text_by_languagetool.py` (문자 / 스타일 보정을위한 언어 도구) 李俊億  
│├ **4. Ollama AI Fallback을 가진 Hierarchical RegEx-Rule-Engine ** 李俊億  
││ ***Deterministic Control:** 정확한, 높은-priority 명령 및 텍스트 제어를 위한 RegEx-Rule-Engine을 사용합니다. XSPACE인실  
│├ **Vector-Search 플러그인** (라지 로딩): Ollama/LLM fallback layer 李俊億  
││ * **올라마 AI (Local LLM) Fallback:** 옵션으로 봉사, **creative Answer, Q&A 및 고급 Fuzzy Matching** deterministic Rule이 충족되지 않을 때.  
││ ***Status:** 로컬 LLM 통합.  
│└ 5.**Intelligent Post-Correction** (`FuzzyMap`)**– Post-LT Refinement** 李俊億  
││ * LT-specific 산출을 수정하기 위하여 LanguageTool 후에 적용해. Pre-Correction layer.  와 동일한 엄격한 캐스케이드 우선 논리를 따릅니다.  
││ ***Dynamic 스크립트 실행:** 규칙은 API 호출, 파일 I/O와 같은 고급 작업을 수행하기 위해 Python 스크립트 ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-kolang.md))를 트리거하거나 동적 응답을 생성합니다. XSPACE인실  
││ * **Fuzzy Fallback:** **Fuzzy similarity Check** (계값에 의해 제어, 예를 들어, 85 %)는 가장 낮은 우선 오류 방지 층 역할을합니다. 전신 결정/캐스케이드 규칙이 일치 (current rule  matching is False)를 발견하지 못하는 경우에만 실행됩니다, 가능한 한 느슨한 체크를 피하여 성능 최적화. XSPACE인실  
├┬ ** 모델 관리 **   
│├─ `prioritize_model.py` (사용에 근거를 둔 모형 선적/unloading를 낙관하십시오) 李俊億  
│└─ `setup_initial_model.py` (최초 모델 설정 구성) 李俊億  
├─ ** Adaptive VAD Timeout**   EA  
├─ ** Adaptive Hotkey (Start/Stop)** 李俊億  
├─ ** Instant Language Switching** (모델 사전 로드를 통해 실험) 李俊億
├─ **Airflow Orchestration** (DAG 기반 워크플로우 자동화) 🐧 🍏 🪟  
│   고정 도커 · UI : `http://localhost:8081` 李俊億
├─ **Trino State Engine** (문자/terminal/web 당 인터페이스) 🐧 🍏 🪟  
└─  Requires Docker · Admin UI : `http://localhost:8084` 李俊億
  
**시스템 유틸리티/**   
├┬ **LanguageTool 서버 관리/**   
│├─ `start_languagetool_server.py` (현지 언어 도구 서버) 李俊億
│└─ `stop_languagetool_server.py` (LanguageTool 서버를 중단) 🐧 🍏  
├─ `monitor_mic.sh` (e.g. 사용 키보드 및 모니터없이 헤드셋 사용) 李俊億

###**모델 및 패키지 관리**  
큰 언어 모델의 강력한 취급을위한 도구.  

** ModelManagement/**   EA  
├─ **Robust Model Downloader** (GitHub Release chunk) 李俊億  
├─ `split_and_hash.py` (큰 파일을 분할하고 체크섬을 생성하기 위해 재포 소유자를위한 필수) 李俊億  
└─ `download_all_packages.py` (다운로드, 확인 및 멀티 파트 파일을 재조정하는 최종 사용자를위한 도구) 宁波    

</details>


<details>
<summary>개발 및 배포 Helpers</summary>

###**개발 및 배포 도우미**  
환경 설정, 테스트 및 서비스 실행에 대한 스크립트. XSPACE인실  

*Tip: glogg는 로그 파일에서 흥미로운 이벤트를 검색하려면 정규 표현식을 사용할 수 있습니다.* XSPACE인실  
로그 파일과 연관될 때 체크 박스를 확인하십시오. XSPACE인실  
https://glogg.bonnefon.org/ - 한국어 XSPACE인실  
    
*Tip: regex 패턴을 정의한 후, `python3 tools/map_tagger.py`를 실행하여 CLI 도구에 대한 검색 가능한 예를 자동으로 생성합니다. 자세한 내용은 [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-kolang.md) 참조.*

그런 다음 두 번 클릭
`log/aura_engine.log`
    
**DevHelpers/**  
├┬ **가상 환경 관리/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS)  X  
│└ `scripts/restart_venv_and_run-server.ahk` (윈도우)    
├┬ **시스템 전체 Dictation 통합/**  
│├ Vosk-System-Listener 통합 🐧 EA  
│├ `scripts/monitor_mic.sh` (리눅스 특정 마이크 모니터링) 宁波  
│└ `scripts/type_watcher.ahk` (AutoHotkey는 인식 된 텍스트를 듣고 시스템 전체를 입력합니다)    
└─ **CI/CD 자동화/**  
    └─ 확장된 GitHub 워크플로우(Installation, Testing, docs deploy) 宁波     *(Runs on GitHub Action)*  

</details>

<details>
<summary> 실험 특징</summary>
  
    
###**실행 / 실험 기능**  
현재 개발중인 기능 또는 초안 상태.  

**ExperimentalFeatures/**  
├─ **ENTER AFTER DICTATION REGEX ** 예제 활성화 규칙 "(ExampleAplicationThatNotExist|Pi, Your personal AI)" 宁波  
├┬플러그인  
│**Live Lazy-Reload** (*) EA EA  
(*Changes to Plugin Activation/deactivation, and their configurations, service restart.*)  없이 다음 처리 실행에 적용됩니다.
│ ├ **git 명령어** (git 명령어를 보내는 음성제어) 李俊億
│ ├ ** Wannweil ** (위치 Germany-Wannweil의지도) 李俊億
│ ├ **Poker 플러그인 (Draft) ** (포커 애플리케이션의 음성 제어) 李俊億
│ └ **0 A.D. Plugin (Draft)** (0 A.D. 게임용 Voice 컨트롤)
├─ ** 세션 시작 또는 종료시 사운드 출력 ** (Description pending) 宁波   
├─ **Speech는 Visually Impaired에 대한 출력** (Description pending) 李俊億
└─ **SL5 Aura Android Prototype** (전체 오프라인 없음)

---

* (주: Arch (ARL) 또는 Ubuntu (UBT)와 같은 특정 Linux 배포는 일반 Linux 李俊億 상세 구분은 설치 안내서에 포함될 수 있습니다.)*
</details>

<details>
<summary>이 스크립트 목록</summary>를 생성하기 위해 사용되는 명령을 보려면

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
Architecture</summary>의 <summary>A 그래픽 개요

### 아키텍처의 그래픽 개요:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>사용된 모델</summary>

## 사용된 모델:

권장: Mirror의 모델 사용 https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (아마 더 빠름)

이 압축된 모델들은 `models/` 폴더에 저장되어야 합니다

`mv vosk-model-*.zip models/`


| 모델 | 크기 | 단어 오류율/속도 | 주 | 라이센스 |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter) | 정확한 일반 미국 영어 모델 | 아파치 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G | 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (ml)<br/>33.26 (mtedx) | 텔레폰 및 서버를위한 큰 독일어 모델 | 아파치 2.0 |

이 테이블은 크기, 단어 오류율 또는 속도, 노트 및 라이센스 정보를 포함하여 다른 Vosk 모델의 개요를 제공합니다.


- ** Vosk 모델:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- ** 언어 도구 :**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

** 언어 도구의 장점 :** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## 프로젝트 지원
이 도구를 유용한 경우, 우리를 구입하시기 바랍니다 커피! 당신의 지원은 연료 미래 개선을 돕습니다.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

