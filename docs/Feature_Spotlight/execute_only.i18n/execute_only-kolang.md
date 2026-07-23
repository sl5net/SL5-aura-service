# 규칙 속성: `execute_only` (실험적, 7.7.'26 Tue)

`execute_only` 속성은 입력 텍스트를 수정하거나 바꾸지 않고 외부 스크립트만 트리거하는 규칙을 위해 설계된 실험적 구성 옵션입니다.

## 개요
- **유형:** `bool`(예: `True` 또는 `False`)
- **주요 사용 사례:** 일반적으로 'on_match_exec'와 함께 사용하여 외부 스크립트를 실행합니다.

## 작동 방식 및 현재 동작
- **속도 최적화:** (몇 밀리초만) 텍스트 후처리 및 텍스트 교체 루틴을 우회하여 트리거된 작업의 즉각적인 실행 속도를 높입니다.
- **제외 없음/폴스루 부작용:** `execute_only`를 `True`로 설정해도 다른 일치 규칙이 동일한 입력 텍스트를 평가하는 것을 방지하지 **않습니다**.
- **흐름 중단:** 후속 규칙이 동일한 입력 텍스트를 처리하는 것을 중지해야 하는 경우 현재는 실행 흐름을 수동으로 종료해야 합니다(예: 트리거된 스크립트 또는 규칙 세트 핸들러의 끝에서 예외 발생).

## 구성 예

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'command_flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```