# 홈 디렉터리 및 크로스 플랫폼 경로 처리

Aura는 여러 운영 체제에서 실행되도록 설계되었습니다. Linux, macOS 또는 Windows 실행 여부에 관계없이 파일 시스템 탐색 명령이 작동하도록 하기 위해 경로 문자열이 활성 퍼지 맵에 등록되기 전에 동적으로 구문 분석됩니다.

---

## 경로 정규화 논리(`FUZZY_MAP_pre.py`)

동적 경로 매핑 논리는 다음 표준 사례를 따릅니다.

### 1. 물결표 감소(POSIX)
POSIX 호환 시스템(Linux 및 macOS)에서는 사용자의 홈 디렉터리(예: `/home/username/`)와 일치하는 절대 경로가 시작 시 `~` 상대 경로로 변환됩니다. 이렇게 하면 문자열 길이가 더 짧아지고 생성된 규칙을 동일한 운영 체제의 여러 사용자 간에 이식할 수 있습니다.

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. 절대 경로 보존(Windows)
Windows는 표준 명령 프롬프트(`cmd.exe`) 또는 PowerShell 환경에서 `~` 문자를 안정적으로 평가하지 않습니다. 따라서 플러그인이 Windows 환경(`sys.platform == 'win32'`)을 감지하면 명령 실행이 실패하지 않도록 정규화된 절대 경로(예: `C:\Users\username\...`)를 보존합니다.

### 3. 슬래시 정규화(`as_posix()`)
Aura는 구성 맵에 대해 내부적으로 POSIX 스타일 슬래시(`/`)를 사용합니다. 이 스크립트는 Windows 환경에서 백슬래시(`\`)를 자동으로 삭제하는 Python의 `pathlib.Path.as_posix()` 메서드를 활용하여 모든 OS 종속 경로 구분 기호를 정규화합니다.