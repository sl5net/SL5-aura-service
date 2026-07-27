# 대화형 규칙 검색 및 실행

이 스포트라이트는 대화형 규칙 검색 및 실행 시스템, 음성 명령 연결, 실시간 탐색 및 즉각적인 실행을 강조합니다.

## 핵심 기능
[1] **이중 창 실시간 검색(`fzf`):** 왼쪽 창은 규칙 파일을 필터링합니다. 오른쪽 창에는 `preview_rule.py`를 통해 라인 컨텍스트 미리보기가 표시됩니다.
[2] **즉시 실행(`Enter` / `Ctrl+R`):** 백그라운드에서 `run_palette_command.py`를 통해 추출된 대상 명령을 즉시 실행합니다.
[3] **직접 편집(`Ctrl+E`):** 대상 라인에서 편집기(`@line`을 사용하는 CudaText, `--line`을 사용하는 Kate/VS Code)를 직접 시작합니다.
[4] **플로팅 창 단축키:** 빠른 데스크톱 통합 작업 흐름을 위해 'Super+S'에 바인딩됩니다.
[5] **음성 명령 지원:** 빠르고 정확한 검색을 위해 `search_rules.sh`에 다양한 음성 명령이 검색 패턴을 미리 구성합니다.

## 크로스 플랫폼 지원
- **Linux Bash(`run_rule.sh` / `search_rules.sh`):** 기록 추적 및 클립보드 작업(`Ctrl+X` / `Ctrl+A`)을 포함한 모든 기능을 갖춘 구현입니다.
- **Windows PowerShell(`search_rules.ps1`):** 가벼운 터미널 검색 기능을 제공하는 도우미 도구입니다.

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_wie_wetter_heute20260727.png)