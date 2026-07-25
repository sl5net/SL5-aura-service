# 기능 스포트라이트: 파일 기반 규칙 대체

이 문서에서는 민감한 값(비밀번호, API 키, 토큰)을 유지하는 방법을 설명합니다.
`FUZZY_MAP_pre` / `FUZZY_MAP` 소스 코드 및 Git 기록을 로드하여
하드코딩하는 대신 런타임 시 별도의 파일에서 '교체' 텍스트를 가져옵니다.

이는 실시간 스트리밍이나 화면 공유 중에 특히 유용합니다.
소스 코드 자체는 표시될 수 있지만 참조된 파일은 표시되지 않습니다.

---

## 1. 컨셉

일반적으로 규칙의 `replacement` 필드는 리터럴 출력 텍스트입니다.

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

파일 기반 교체가 활성화된 경우 다음으로 시작하는 `replacement` 값
구성된 접두사(기본적으로 '-' 또는 '.')는 대신 **파일 이름**으로 처리됩니다.
Aura는 플러그인 자체 디렉토리를 기준으로 해당 파일 이름을 확인하고 해당 파일 이름을 읽습니다.
내용을 저장하고 해당 내용을 대체 텍스트로 사용합니다.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

플러그인의 `FUZZY_MAP_pre.py` 옆에 `api_key.txt`가 존재하는 경우 해당 플러그인은 (제거됨)
콘텐츠가 대체품으로 사용됩니다. 파일이 존재하지 않으면 리터럴
문자열 `-api_key.txt`가 대신 반환됩니다(안전 장치: 우발적인 누출이 없음).
"파일을 찾을 수 없음"이 사용 가능한 텍스트로 표시되고 충돌이 발생하지 않음).

---

## 2. 설정

`config/settings.py`(또는 로컬의 경우 `config/settings_local.py`)에 구성됩니다.
재정의):

| 설정 | 유형 | 기본값 | 설명 |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `부울` | '사실' | 전체 기능에 대한 마스터 스위치입니다. 'False'인 경우 'replacement'는 항상 문자 그대로 사용됩니다. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `튜플[str]` | `('-', '.')` | 파일 조회를 트리거하려면 `replacement` 값이 이러한 접두사 중 하나로 시작해야 합니다. 비어 있음/`없음` = 문자로 시작하지 않는 모든 값은 잠재적인 파일 이름으로 처리됩니다. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `부울` | '거짓' | `True`인 경우 플러그인 자체 디렉터리 외부의 파일을 분석할 수 있습니다(예: 절대 경로 또는 `../` 시퀀스). 아래 보안 섹션을 참조하세요. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `튜플[str]` | 예를 들어 `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Program Files')` | 이들 중 하나로 시작하는 확인된 절대 경로는 `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`에 관계없이 **항상** 거부됩니다. 시스템 디렉터리에 대한 엄격한 보안 경계입니다. |

---

## 3. 경로 결정

파일은 다음과 같이 해석됩니다.

1. 플러그인의 `source_path`(맵 로더에 의해 자동으로 기록됨)는 다음과 같습니다.
`PROJECT_ROOT`에 대해 조인되었습니다(`SL5NET_AURA_PROJECT_ROOT`에서 읽음).
환경 변수)를 사용하여 플러그인 디렉터리를 가져옵니다.
2. 'replacement' 값이 해당 디렉터리에 결합됩니다.
3. `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`이 `True`가 아닌 경우 확인된 경로
플러그인 디렉토리 내에 있어야 합니다. 그렇지 않으면 조회가 거부됩니다.
4. 위와 상관없이 다음 항목으로 시작하는 해결된 경로는 다음과 같습니다.
`FILE4REPLACEMENT_DENY_PREFIXES`는 항상 거부됩니다.
5. 파일이 존재하는 경우 제거된 내용이 반환됩니다. 그렇지 않으면,
원래 `교체` 문자열은 변경되지 않고 반환됩니다.

---

## 4. 보안 참고사항

- 'FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL'을 이해하는 경우에만 'FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL'을 활성화하세요.
의미: 'FUZZY_MAP_pre' 파일을 편집할 수 있는 모든 사용자를 허용합니다(예:
온라인 지도 편집기를 통해) Aura 프로세스가 수행할 수 있는 임의의 파일을 읽을 수 있습니다.
액세스하고 콘텐츠를 실시간 출력 텍스트로 표시합니다.
- `FILE4REPLACEMENT_DENY_PREFIXES`는 기본 보호 기능을 제공합니다.
경로 탐색이 허용되는 경우에도 공통 시스템 디렉터리는
처음에 지도 파일을 편집할 수 있는 사람을 제한하는 것을 대체할 수는 없습니다.
- 참조된 파일은 디스크의 일반 텍스트입니다. OS 파일과 결합
콘텐츠가 민감한 경우 권한을 부여합니다.

---

## 5. 예시

작동하는 예제 플러그인은 `config/maps/plugins/TEST_FILE4REPLACEMENT/`를 참조하세요.
그리고 연습하는 테스트 스크립트의 경우 `tools/tests/TEST_FILE4REPLACEMENT.sh`
디렉토리 내 조회와 플러그인 디렉토리 외부 조회가 모두 가능합니다.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

원하는 대체 텍스트로 이 파일 옆에 '.Zebra.txt'를 만든 다음
실행하려면 `Zebra`라고 말하세요(또는 콘솔을 통해 입력하세요).