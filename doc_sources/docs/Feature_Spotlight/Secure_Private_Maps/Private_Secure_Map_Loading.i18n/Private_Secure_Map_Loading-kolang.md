# 기능 스포트라이트: 안전한 개인 지도 로딩 및 자동 패킹

이 문서에서는 실수로 Git 노출을 방지하기 위해 **보안 모범 사례**를 시행하면서 **실시간 편집**을 허용하는 방식으로 중요한 지도 플러그인(예: 클라이언트 데이터, 독점 명령)을 관리하기 위한 아키텍처를 간략하게 설명합니다.

---

## 1. 개념: "마트료시카" 보안

표준 도구를 사용하는 동안 개인정보 보호를 극대화하기 위해 Aura는 암호화된 아카이브에 **마트료시카(러시아 인형)** 중첩 전략을 사용합니다.

1. **외부 레이어:** **AES-256**으로 암호화된 표준 ZIP 파일(시스템 `zip` 명령 사용)
* *모양:* `aura_secure.blob`이라는 이름의 **하나** 파일만 포함되어 있습니다.
* *이점:* 엿보는 눈으로부터 파일 이름과 디렉터리 구조를 숨깁니다.
2. **내부 레이어(Blob):** Blob 내부의 암호화되지 않은 ZIP 컨테이너입니다.
* *내용:* 실제 디렉터리 구조와 Python 파일입니다.
3. **작업 상태:** 잠금이 해제되면 밑줄이 앞에 붙은 임시 폴더(예: `_private`)에 파일이 추출됩니다.
* *보안:* 이 폴더는 `.gitignore`에 의해 엄격히 무시됩니다.

---

## 2. 기술적인 작업 흐름

### A. 보안 게이트(스타트업)
압축을 풀기 전에 Aura는 `scripts/py/func/map_reloader.py`에서 특정 `.gitignore` 규칙을 확인합니다.
* **규칙 1:** `config/maps/**/.*`(키 파일 보호)
* **규칙 2:** `config/maps/**/_*`(작업 디렉토리 보호)
이것이 누락되면 시스템이 **중단**됩니다.

### B. 포장 풀기(예외 구동)
1. 사용자는 비밀번호(일반 텍스트 또는 주석)가 포함된 키 파일(예: `.auth_key.py`)을 생성합니다.
2. Aura는 이 파일과 해당 ZIP(예: `private.zip`)을 감지합니다.
3. Aura는 키를 사용하여 외부 ZIP을 해독합니다.
4. Aura는 `aura_secure.blob`을 감지하고 내부 레이어를 추출한 후 파일을 작업 디렉터리 `_private`으로 이동합니다.

### C. 실시간 편집 및 자동 패킹(The Cycle)
여기서 시스템은 "자가 치유" 상태가 됩니다.

1. **편집:** `_private/`에서 파일을 수정하고 저장합니다.
2. **트리거:** Aura는 변경 사항을 감지하고 모듈을 다시 로드합니다.
3. **라이프사이클 후크:** 모듈이 'on_reload()' 기능을 트리거합니다.
4. **SecurePacker:** 개인 폴더의 루트에 있는 스크립트(`secure_packer.py`)가 실행됩니다.
* 내부 ZIP(구조체)을 생성합니다.
* `.blob`로 이름을 바꿉니다.
* 시스템 `zip` 명령을 호출하여 `.key` 파일의 비밀번호를 사용하여 외부 아카이브로 암호화합니다.

**결과:** `private.zip`은 항상 최신 변경 사항으로 업데이트되지만 Git에서는 바이너리 ZIP 파일 변경 사항만 볼 수 있습니다.

---

## 3. 설정 가이드

### 1단계: 디렉터리 구조
다음과 같은 폴더 구조를 만듭니다.
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### 2단계: 키 파일(`.auth_key.py`)
점으로 시작해야 합니다.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### 3단계: 패커 스크립트(`secure_packer.py`)
이 스크립트를 개인 지도 폴더 안에 넣으세요(처음에 압축하기 전에). 암호화 논리를 처리합니다. 지도가 'on_reload' 후크를 통해 이 스크립트를 호출하는지 확인하세요.

### 4단계: 후크 구현
맵 파일(`.py`)에서 다음 후크를 추가하여 저장할 때마다 백업을 트리거합니다.

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Git 상태 및 안전

올바르게 설정되면 `git status`는 **만** 표시됩니다:
```text
modified:   config/maps/private/private_maps.zip
```
`_private_maps` 폴더와 `.auth_key.py` 파일은 추적되지 않습니다.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# 개발자 가이드: 플러그인 수명 주기 후크

Aura SL5를 사용하면 플러그인(맵)이 모듈 상태가 변경될 때 자동으로 실행되는 특정 "후크"를 정의할 수 있습니다. 이는 **Secure Private Map** 시스템과 같은 고급 작업 흐름에 필수적입니다.

## `on_reload()` 후크

'on_reload()' 함수는 모든 Map 모듈에서 정의할 수 있는 선택적 함수입니다.

### 행동
* **트리거:** 모듈이 성공적으로 **핫 리로드**(파일 수정 + 음성 트리거)된 직후에 실행됩니다.
* **컨텍스트:** 기본 애플리케이션 스레드 내에서 실행됩니다.
* **안전성:** `try/exc` 블록으로 래핑됩니다. 여기에 오류가 기록되지만 애플리케이션이 **충돌하지 않습니다**.

### 사용 패턴: "데이지 체인"
개인 지도와 같은 복잡한 패키지의 경우 하위 파일이 많은 경우가 많지만 중앙 스크립트(`secure_packer.py`) 하나만 논리를 처리해야 합니다.

후크를 사용하여 작업을 위쪽으로 위임할 수 있습니다.

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

### 모범 사례
1. **빠른 속도 유지:** 메인 후크에서 긴 차단 작업(대량 다운로드 등)을 실행하지 마세요. 필요한 경우 스레드를 사용하십시오.
2. **멱등성:** 문제가 발생하지 않고 후크가 여러 번 실행될 수 있는지 확인하세요(예: 파일에 끝없이 추가하지 말고 대신 다시 작성하세요).