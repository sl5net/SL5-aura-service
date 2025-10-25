# 시스템 전체 오프라인 음성에서 명령 또는 텍스트로 변환, 플러그형 시스템

# SL5 Aura 서비스 - 기능 및 IOS 호환성

SL5 Aura 서비스에 오신 것을 환영합니다! 이 문서에서는 주요 기능과 운영 체제 호환성에 대한 간략한 개요를 제공합니다.

Aura는 단순한 음성-텍스트 변환 그 이상입니다. 이를 통해 사용자 정의가 가능합니다.

Vosk 및 LanguageTool을 기반으로 구축된 완전한 오프라인 도우미입니다.

번역: 이 문서는 [other languages](https://github.com/sl5net/docs)에도 존재합니다.

참고: 많은 텍스트는 원래 영어 문서를 기계로 생성한 번역이며 일반적인 지침으로만 사용됩니다. 불일치나 모호성이 있는 경우에는 항상 영어 버전이 우선합니다. 이 번역을 개선하기 위한 커뮤니티의 도움을 환영합니다!


[![SL5 Aura (v0.7.0.2): A Deep Dive Under the Hood – Live Coding & Core Concepts](https://img.youtube.com/vi/tEijy8WRFCI/maxresdefault.jpg)](https://www.youtube.com/watch?v=tEijy8WRFCI)
( https://skipvids.com/?v=tEijy8WRFCI )

## 주요 기능

* **오프라인 및 비공개:** 100% 로컬. 어떤 데이터도 귀하의 컴퓨터를 떠나지 않습니다.
* **고도의 제어 변환 엔진:** 구성 중심의 고도로 사용자 정의 가능한 처리 파이프라인을 구현합니다. 규칙 우선순위, 명령 감지 및 텍스트 변환은 순전히 퍼지 맵의 규칙 순서에 따라 결정되며 **코딩이 아닌 구성**이 필요합니다.
* **보수적인 RAM 사용:** 메모리를 지능적으로 관리하고 여유 RAM이 충분한 경우에만 모델을 사전 로드하여 다른 애플리케이션(예: PC 게임)이 항상 우선순위를 갖도록 합니다.
* **크로스 플랫폼:** Linux, macOS, Windows에서 작동합니다.
* **완전 자동화:** 자체 LanguageTool 서버를 관리합니다(단, 외부 서버도 사용할 수 있음).
* **매우 빠른 속도:** 지능형 캐싱은 즉각적인 "듣기..." 알림과 빠른 처리를 보장합니다.

## 문서

모든 모듈과 스크립트를 포함한 전체 기술 참조를 보려면 공식 문서 페이지를 방문하세요. 자동으로 생성되며 항상 최신 상태를 유지합니다.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### 빌드 상태
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

---

## 설치

설정은 2단계 프로세스로 이루어집니다.
1. 이 저장소를 컴퓨터에 복제합니다.
2. 운영 체제에 대한 일회성 설정 스크립트를 실행합니다.

설정 스크립트는 시스템 종속성, Python 환경, 최대 속도를 위해 GitHub 릴리스에서 직접 필요한 모델 및 도구(~4GB) 다운로드 등 모든 것을 처리합니다.

#### Linux, macOS, Windows용
프로젝트의 루트 디렉터리에서 터미널을 열고 시스템에 대한 스크립트를 실행합니다.
```bash
# For Ubuntu/Debian, Manjaro/Arch, macOs  or other derivatives

bash setup/{your-os}_setup.sh

# For Windows in Admin-Powershell

setup/windows11_setup.ps1
```

#### 윈도우의 경우
관리자 권한 **"PowerShell로 실행"**으로 설정 스크립트를 실행합니다.

**읽기 및 실행을 위한 도구를 설치합니다. [CopyQ](https://github.com/hluk/CopyQ) 또는 [AutoHotkey v2](https://www.autohotkey.com/)**. 이는 텍스트 입력 감시자에게 필요합니다.

---

## 용법

### 1. 서비스 시작

#### Linux 및 macOS의 경우
단일 스크립트가 모든 것을 처리합니다. 기본 받아쓰기 서비스와 파일 감시자가 백그라운드에서 자동으로 시작됩니다.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### 윈도우즈의 경우
서비스 시작은 **2단계 수동 프로세스**로 이루어집니다.

1. **메인 서비스 시작:** `start_dictation_v2.0.bat`를 실행합니다. 또는 `python3`을 사용하여 `.venv`에서 서비스를 시작합니다.

### 2. 단축키 구성

받아쓰기를 실행하려면 특정 파일을 생성하는 전역 단축키가 필요합니다. 크로스 플랫폼 도구 [CopyQ](https://github.com/hluk/CopyQ)를 적극 권장합니다.

#### 우리의 추천: CopyQ

전역 단축키를 사용하여 CopyQ에서 새 명령을 만듭니다.

**Linux/macOS용 명령:**
```bash
touch /tmp/sl5_record.trigger
```

**[CopyQ](https://github.com/hluk/CopyQ) 사용 시 Windows용 명령:**
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


**[AutoHotkey](https://AutoHotkey.com) 사용 시 Windows용 명령:**
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


### 3. 받아쓰기를 시작하세요!
텍스트 필드를 클릭하고 단축키를 누르면 "듣기..." 알림이 나타납니다. 명확하게 말한 다음 잠시 멈추십시오. 수정된 텍스트가 자동으로 입력됩니다.

---


## 고급 구성(선택 사항)

로컬 설정 파일을 생성하여 애플리케이션의 동작을 사용자 정의할 수 있습니다.

1. `config/` 디렉토리로 이동합니다.
2. `settings_local.py_Example.txt`의 복사본을 만들고 이름을 `settings_local.py`로 바꿉니다.
3. `settings_local.py`를 편집하여 기본 `config/settings.py` 파일의 설정을 재정의합니다.

이 `settings_local.py` 파일은 Git에서 (아마도) 무시되므로 업데이트로 인해 개인적인 변경 사항이 (아마도) 덮어쓰여지지 않을 것입니다.

### 플러그인 구조 및 로직

시스템의 모듈성은 플러그인/ 디렉토리를 통한 강력한 확장을 허용합니다.

처리 엔진은 **계층적 우선순위 체인**을 엄격하게 준수합니다.

1. **모듈 로드 순서(높은 우선순위):** 핵심 언어 팩(de-DE, en-US)에서 로드된 규칙은 플러그인/ 디렉터리에서 로드된 규칙(마지막 알파벳순으로 로드됨)보다 우선합니다.
XSPACEbreakX
2. **파일 내 순서(마이크로 우선순위):** 지정된 맵 파일(FUZZY_MAP_pre.py) 내에서 규칙은 **라인 번호**(위에서 아래로)에 따라 엄격하게 처리됩니다.
XSPACEbreakX

이 아키텍처는 핵심 시스템 규칙이 보호되는 동시에 프로젝트별 또는 상황 인식 규칙(예: CodeIgniter 또는 게임 제어용 규칙)을 플러그인을 통해 우선순위가 낮은 확장으로 쉽게 추가할 수 있도록 보장합니다.
## Windows 사용자를 위한 주요 스크립트

다음은 Windows 시스템에서 애플리케이션을 설정, 업데이트 및 실행하는 데 가장 중요한 스크립트 목록입니다.

### 설정 및 업데이트
* `setup/setup.bat`: 환경의 **초기 일회성 설정**을 위한 기본 스크립트입니다.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `powershell 실행 -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` : 프로젝트 폴더에서 이를 실행합니다. **최신 코드와 종속성을 가져옵니다**.

### 애플리케이션 실행
* `start_dictation_v2.0.bat`: **받아쓰기 서비스를 시작**하는 기본 스크립트입니다.

### 핵심 및 도우미 스크립트
* `dictation_service.py`: 핵심 Python 서비스(일반적으로 위 스크립트 중 하나에 의해 시작됨).
* `get_suggestions.py`: 특정 기능을 위한 도우미 스크립트입니다.




## 🚀 주요 기능 및 OS 호환성

OS 호환성 범례:XSPACEbreakX
* 🐧 **Linux**(예: Arch, Ubuntu)XSPACEbreakX
* 🍏 **macOS**XSPACEbreakX
* 🪟 **윈도우**XSPACEbreakX
* 📱 **Android**(모바일 전용 기능용)XSPACEbreakX

---

### **핵심 음성-텍스트(Aura) 엔진**
오프라인 음성 인식 및 오디오 처리를 위한 기본 엔진입니다.

**Aura-Core/** 🐧 🍏 🪟XSPACEbreakX
├─ `dictation_service.py`(Aura를 조정하는 주요 Python 서비스) 🐧 🍏 🪟  
├┬ **라이브 핫 리로드**(구성 및 맵) 🐧 🍏 🪟XSPACEbreakX
│├ **텍스트 처리 및 수정/** 언어별로 그룹화됨(예: `de-DE`, `en-US`, ... ) XSPACEbreakX
│├ 1. `normalize_punkation.py` (구두점 표기 표준화) 🐧 🍏 🪟  
│├ 2. **지능형 사전 수정** (`FuzzyMap Pre` - **기본 명령 계층**) 🐧 🍏 🪟XSPACEbreakX
││ * **계단식 실행:** 규칙은 순차적으로 처리되며 해당 효과는 **누적**됩니다. 이후 규칙은 이전 규칙에 의해 수정된 텍스트에 적용됩니다.  
││ * **가장 높은 우선순위 중지 기준:** 규칙이 **완전 일치**(^...$)를 달성하면 해당 토큰에 대한 전체 처리 파이프라인이 즉시 중지됩니다. 이 메커니즘은 안정적인 음성 명령을 구현하는 데 중요합니다.  
│├ 3. `corright_text_by_언어tool.py` (문법/스타일 교정을 위한 LanguageTool 통합) 🐧 🍏 🪟  
│└ 4. **지능형 사후 수정**(`FuzzyMap`)**– LT 이후 개선** 🐧 🍏 🪟XSPACEbreakX
││ * LT 관련 출력을 수정하기 위해 LanguageTool 다음에 적용됩니다. 사전 수정 레이어와 동일한 엄격한 계단식 우선 순위 논리를 따릅니다.  
││ * **퍼지 폴백:** **퍼지 유사성 검사**(임계값(예: 85%)으로 제어됨)은 우선순위가 가장 낮은 오류 수정 레이어 역할을 합니다. 이전 결정적/계단식 규칙 실행 전체가 일치 항목을 찾지 못한 경우에만 실행되며(current_rule_matched는 False임) 가능할 때마다 느린 퍼지 검사를 피하여 성능을 최적화합니다.  
├┬ **모델 관리/** XSPACEbreakX
│├─ `prioritize_model.py` (사용에 따라 모델 로드/언로드 최적화) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (최초 모델 설정 구성) 🐧 🍏 🪟  
├─ **적응형 VAD 시간 초과** 🐧 🍏 🪟XSPACEbreakX
├─ **적응형 단축키(시작/중지)** 🐧 🍏 🪟XSPACEbreakX
└─ **즉각적인 언어 전환** (모델 사전 로드를 통한 실험) 🐧 🍏 XSPACEbreakX

**시스템 유틸리티/** XSPACEbreakX
├┬ **LanguageTool 서버 관리/** XSPACEbreakX
│├─ `start_언어tool_server.py`(로컬 LanguageTool 서버 초기화) 🐧 🍏 🪟  
│└─ `stop_언어tool_server.py` (LanguageTool 서버 종료) 🐧 🍏
├─ `monitor_mic.sh` (예: 키보드와 모니터를 사용하지 않고 헤드셋과 함께 사용) 🐧 🍏 🪟XSPACEbreakX

### **모델 및 패키지 관리**XSPACEbreakX
대규모 언어 모델을 강력하게 처리하기 위한 도구입니다.  

**모델 관리/** 🐧 🍏 🪟XSPACEbreakX
├─ **강력한 모델 다운로더**(GitHub 릴리스 청크) 🐧 🍏 🪟XSPACEbreakX
├─ `split_and_hash.py`(저장소 소유자가 대용량 파일을 분할하고 체크섬을 생성하는 유틸리티) 🐧 🍏 🪟  
└─ `download_all_packages.py`(최종 사용자가 여러 부분으로 구성된 파일을 다운로드, 확인 및 재조립할 수 있는 도구) 🐧 🍏 🪟  


### **개발 및 배포 도우미**XSPACEbreakX
환경 설정, 테스트, 서비스 실행을 위한 스크립트입니다.  

**DevHelpers/**XSPACEbreakX
├┬ **가상 환경 관리/**XSPACEbreakX
│├ `scripts/restart_venv_and_run-server.sh`(Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **시스템 전체 받아쓰기 통합/**  
│├ Vosk-시스템-리스너 통합 🐧 🍏 🪟XSPACEbreakX
│├ `scripts/monitor_mic.sh`(Linux 전용 마이크 모니터링) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey는 인식된 텍스트를 듣고 시스템 전체에 입력합니다) 🪟  
└─ **CI/CD 자동화/**XSPACEbreakX
└─ 확장된 GitHub 워크플로(설치, 테스트, 문서 배포) 🐧 🍏 🪟 *(GitHub Actions에서 실행)*XSPACEbreakX

### **향후/실험적 기능**XSPACEbreakX
현재 개발 중이거나 초안 상태인 기능입니다.  

**실험적 기능/**XSPACEbreakX
├─ **ENTER_AFTER_DICTATION_REGEX** 활성화 규칙 예시 "(ExampleAplicationThatNotExist|Pi, 개인 AI)" 🐧  
├┬플러그인XSPACEbreakX
│╰┬ **라이브 지연 새로고침** (*) 🐧 🍏 🪟XSPACEbreakX
(*플러그인 활성화/비활성화 및 해당 구성에 대한 변경 사항은 서비스를 다시 시작하지 않고 다음 처리 실행 시 적용됩니다.*)  
│ ├ **git 명령** (git 명령 보내기를 위한 음성 제어) 🐧 🍏 🪟  
│ ├ **wannweil** (독일 Wannweil 위치 지도) 🐧 🍏 🪟XSPACEbreakX
│ ├ **포커 플러그인(초안)** (포커 애플리케이션용 음성 제어) 🐧 🍏 🪟XSPACEbreakX
│ └ **0 A.D. 플러그인(초안)** (0 A.D. 게임용 음성 제어) 🐧 XSPACEbreakX
├─ **세션 시작 또는 종료 시 소리 출력** (설명 보류) 🐧 XSPACEbreakX
├─ **시각 장애인을 위한 음성 출력** (설명 보류 중) 🐧 🍏 🪟XSPACEbreakX
└─ **SL5 Aura Android 프로토타입** (아직 완전히 오프라인이 아님) 📱XSPACEbreakX

---

*(참고: Arch(ARL) 또는 Ubuntu(UBT)와 같은 특정 Linux 배포판에는 일반 Linux 🐧 기호가 표시됩니다. 자세한 차이점은 설치 가이드에서 다룰 수 있습니다.)*









<상세>
<summary>이 스크립트 목록을 생성하는 데 사용된 명령을 보려면 클릭하세요.</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "dictation_service.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</세부사항>


### 그래픽을 통해 뒤에 무엇이 있는지 확인하세요.

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

XSPACEbreakX
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# 사용 모델:

권장 사항: Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1의 모델을 사용하십시오(아마도 더 빠름).

이 압축된 모델은 'models/' 폴더에 저장되어야 합니다.

`mv vosk-model-*.zip 모델/`


| 모델 | 사이즈 | 단어 오류율/속도 | 메모 | 라이센스 |
| ------------------------------------------------------------------------- | ---- | -------------------------------------------------------------------------------- | ---------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69(librispeech 테스트-클린)<br/>6.05(tedlium)<br/>29.78(callcenter) | 정확한 일반 미국 영어 모델 | 아파치 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G | 9.83(Tuda-de 테스트)<br/>24.00(팟캐스트)<br/>12.82(cv-테스트)<br/>12.42(mls)<br/>33.26(mtedx) | 전화 통신 및 서버 분야의 대형 독일 모델 | 아파치 2.0 |

이 표에는 크기, 단어 오류율 또는 속도, 참고 사항, 라이센스 정보를 포함하여 다양한 Vosk 모델에 대한 개요가 제공됩니다.


- **Vosk 모델:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **언어 도구:**XSPACEbreakX
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**LanguageTool 라이센스:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## 프로젝트 지원
이 도구가 유용하다고 생각하시면 커피 한 잔 구입해 보시기 바랍니다! 귀하의 지원은 향후 개선을 촉진하는 데 도움이 됩니다.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)