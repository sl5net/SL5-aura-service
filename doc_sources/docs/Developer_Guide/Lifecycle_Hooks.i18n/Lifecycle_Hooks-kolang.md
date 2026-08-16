Aura SL5 후크: 추가됨

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'on_reload'
HOOK_UPSTREAM = '폴더_변경'

on_folder_change() 및
on_reload()는 핫 리로드 후 로직을 트리거합니다. 복잡한 패키지에 대해 secure_packer.py와 같은 상위 스크립트에 대한 "데이지 체인" 실행을 위해 이를 사용합니다.

# 개발자 가이드: 플러그인 수명 주기 후크

Aura SL5를 사용하면 플러그인(맵)이 모듈 상태가 변경될 때 자동으로 실행되는 특정 "후크"를 정의할 수 있습니다. 이는 **Secure Private Map** 시스템과 같은 고급 작업 흐름에 필수적입니다.

## `on_folder_change` 후크 Hook

'on_folder_change' 후크 감지를 구현했습니다. 이제 리로더가 디렉토리를 검색합니다.

## `on_reload()` 후크

'on_reload()' 함수는 모든 Map 모듈에서 정의할 수 있는 선택적 함수입니다.

### 행동
* **트리거:** 모듈이 성공적으로 **핫 리로드**(파일 수정 + 음성 트리거)된 직후에 실행됩니다.
* **컨텍스트:** 기본 애플리케이션 스레드 내에서 실행됩니다.
* **안전성:** `try/exc` 블록으로 래핑됩니다. 여기에 오류가 기록되지만 애플리케이션이 **충돌하지 않습니다**.

### 사용 패턴: "데이지 체인"
개인 지도와 같은 복잡한 패키지의 경우 하위 파일이 많은 경우가 많지만 중앙 스크립트(`secure_packer.py`) 하나만 논리를 처리해야 합니다.

후크를 사용하여 작업을 위쪽으로 위임할 수 있습니다.

__CODE_BLOCK_0__