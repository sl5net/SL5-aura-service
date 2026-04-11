# WSL(Linux용 Windows 하위 시스템) 통합

WSL을 사용하면 Windows에서 직접 전체 Linux 환경을 실행할 수 있습니다. 일단 설정되면 STT 셸 통합은 **Linux Bash 또는 Zsh 가이드와 동일하게** 작동합니다. 즉, 셸 기능 자체에 Windows별 적응이 필요하지 않습니다.

> **권장 대상:** Linux 터미널에 익숙하거나 개발 작업을 위해 이미 WSL을 설치한 Windows 사용자. WSL은 가장 충실한 환경과 최소한의 호환성 손상을 제공합니다.

## 전제 조건

### WSL 설치(일회성 설정)

PowerShell 또는 CMD를 **관리자 권한**으로 열고 다음을 실행합니다.

```powershell
wsl --install
```

기본적으로 Ubuntu와 함께 WSL2를 설치합니다. 메시지가 나타나면 컴퓨터를 다시 시작하세요.

특정 배포판을 설치하려면:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

사용 가능한 모든 배포판을 나열합니다.

```powershell
wsl --list --online
```

### WSL 버전 확인

```powershell
wsl --list --verbose
```

'VERSION' 열에 '2'가 표시되는지 확인하세요. '1'이 표시되면 다음을 사용하여 업그레이드하세요.

```powershell
wsl --set-version <DistroName> 2
```

## WSL 내부의 셸 통합

WSL이 실행되면 Linux 터미널을 열고 원하는 셸에 대한 **Linux 셸 가이드**를 따르세요.

| 쉘 | 가이드 |
|-------|-------|
| Bash(WSL 기본값) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-kolang.md) |
| Zsh | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-kolang.md) |
| 물고기 | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-kolang.md) |
| 크쉬 | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-kolang.md) |
| POSIX sh / 대시 | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-kolang.md) |

Bash를 사용한 기본 Ubuntu/Debian WSL 설정의 경우 빠른 경로는 다음과 같습니다.

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## WSL 관련 고려 사항

### WSL에서 Windows 파일에 액세스

Windows 드라이브는 `/mnt/`에 마운트됩니다:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

프로젝트가 Windows 파일 시스템(예: `C:\Projects\stt`)에 있는 경우 `PROJECT_ROOT`를 다음으로 설정하세요.

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

이 줄을 `~/.bashrc`(또는 쉘에 해당하는 항목) `s()` 함수 **위**에 추가하세요.

> **성능 팁:** 최고의 I/O 성능을 위해서는 프로젝트 파일을 `/mnt/c/...`가 아닌 WSL 파일 시스템(예: `~/projects/stt`)에 보관하세요. WSL과 Windows 간의 파일 시스템 간 액세스는 상당히 느립니다.

### WSL 내부의 Python 가상 환경

WSL 내에서 표준 Linux 가상 환경을 만들고 사용합니다.

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

함수(`$PROJECT_ROOT/.venv/bin/python3`)의 `PY_EXEC` 경로는 있는 그대로 올바르게 작동합니다.

### Windows 터미널에서 `s` 실행

[Windows Terminal](https://aka.ms/terminal)는 Windows에서 WSL을 사용하는 데 권장되는 방법입니다. 각 WSL 배포에 대해 여러 탭, 창 및 프로필을 지원합니다. Microsoft Store에서 설치하거나 다음을 통해 설치하세요.

```powershell
winget install Microsoft.WindowsTerminal
```

가장 원활한 환경을 위해 Windows 터미널 설정에서 WSL 배포를 기본 프로필로 설정하세요.

### WSL 내부의 Docker 및 Kiwix

Kiwix 도우미 스크립트(`kiwix-docker-start-if-not-running.sh`)에는 Docker가 필요합니다. Windows용 Docker Desktop을 설치하고 WSL 2 통합을 활성화합니다.

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/)를 다운로드하고 설치합니다.
2. Docker Desktop → 설정 → 리소스 → WSL 통합에서 WSL 배포를 활성화합니다.
3. WSL 내부를 확인합니다.
   ```bash
   docker --version
   ```

### Windows에서 WSL`s` 함수 호출(선택 사항)

WSL 터미널을 열지 않고 Windows CMD 또는 PowerShell 창에서 `s` 바로 가기를 호출하려면 다음과 같이 래핑하면 됩니다.

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> `-i` 플래그는 대화형 셸을 로드하여 `~/.bashrc`(및 `s` 함수)가 자동으로 제공되도록 합니다.

## 특징

- **완전한 Linux 호환성**: 모든 Unix 도구(`timeout`, `pgrep`, `mktemp`, `grep`)는 기본적으로 작동하므로 해결 방법이 필요하지 않습니다.
- **동적 경로**: 셸 구성에 설정된 `PROJECT_ROOT` 변수를 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스를 실행하려고 시도합니다(Docker가 실행 중이어야 함).
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.