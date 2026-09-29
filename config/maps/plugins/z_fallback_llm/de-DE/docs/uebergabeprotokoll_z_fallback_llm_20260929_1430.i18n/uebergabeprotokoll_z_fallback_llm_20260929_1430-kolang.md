> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# handover 프로토콜: z fallback llm, CLI 입력은 농담이 없습니다

상태: 2026-09-29

## 1- 작업 (지난, "예"로 확인되지 않음)

실제 상태 : CLI 입력은 정확히 "컴퓨터는 정확히 두 개의 농담을 말한다". 농담이 없습니다.

대상 상태: LLM 응답은 로그 파일에 있지 않는 콘솔에서 직접 나타납니다.

작업의 일부가 아닙니다. 로깅, 단축 또는 로그 라인 확장, 캐시 동작을 변경합니다. 입력의 캐시 바이패스 ("joke")는 이 방법으로 deliberately 선택됩니다.

추종자는이 이해와 일치하고 "예"를 기다립니다.

## 2 환경

Manjaro Linux, ZSH, 지점 기능/fallback-llm-lazy-install.

Ollama는 http://localhost:11434 (Binary /usr/bin/ollama)에서 사용할 수 있습니다. 유효한 모형: llama3.2:latest, qwen3:8b.

모델 llama3.2, 스트림 : false, num 예측 : 100 및 정지 단어는 유효 답을 제공합니다 ( "왜 컴퓨터가 의사로 이동 했습니까?") 그는 바이러스를 가지고 있기 때문에! Ollama, 모델 이름, 스톱 단어 및 토큰 제한은 따라서 원인이 아닙니다. 테스트 프롬프트는 ollama.py (시스템 역할없이, gradient 및 aura suffix)에서 실제 프롬프트보다 단축되었습니다.

윤곽:

```
config/settings_local.py
```

키: PLUGINS ENABLED = {"z fallback llm": 1}. DynamicSettings().PLUGINS ENABLED.get("z fallback llm", False)를 통해 액세스하십시오.

기존 패키지 설치자:

```
scripts/py/func/ensure_package.py
```

## 3 Chain sequence (코드 섹션에서 인증)

규칙:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

규칙 1에는 우선 순위 10가 있고 `{aura1}` 플러스 모드 단어 (정상, 느린, 흐름, 느린, 정확한, 철저한)를 요구합니다. 규칙 2는 우선 100을 가지고 있고 방아쇠 aura, aurora, laura, dora, 시대, hurra, prora 또는 컴퓨터, 그 후에 공간 및 어떤 텍스트 중 하나를 요구합니다. 둘 다 요구 ollama.py. Firefox, Chrome, Brave 및 Element와 같은 창을 제외하십시오.

디자인:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()`는 마지막 Regex 그룹을 입력하여 작게 만듭니다. 입력에서 "joke"를 위해 `bypass_cache = True`가 설정되어 캐시 체크가 건너 뛸 수 있습니다. 이것은 모델 llama3.2과 Ollama 요청에 의해 따랐습니다. 타임아웃은 90초입니다. Ollama 요청없이 조기 반환은 빈 입력 ("nothing hear."), `check_static_guardrails()`와 함께 "즉시", "빠른", "instant".

CLI 반환:

```
scripts/py/service_api.py
```

함수는 최신 출력 파일을 읽고 `status`, `result_text` 및 `input_text`와 일치를 반환합니다. 로그 라인 "API-CLI-Call: Finished"는 입력을 줄이고 20 문자로 결과를 감소시킵니다. 이것은 순수 로그 단축 및 데이터 단축.

## 4 CLI 입력의 로그 관찰

로그인은 `reload_performed`와 "API-CLI-Call: 완성"입니다. input="...computer 정확하고," 결과="컴퓨터 정확하다" `execute()`의 모든 라인은 누락됩니다 ( "입력 :", "Cache BYPASS", "Uncensored AI 대답").

`execute()`가 실행되지 않았다는 것을 증명하지 않습니다.

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'`로 FileHandler를 엽니다. ollama.log 파일은 각 수입에 `utils`에 의해 과잉됩니다. `log_debug`는 또한 기본 프로그램의 콘솔에서 stdout, 즉에 쓰기.

## 5 오픈 질문 (사용되지 않음)

1- `execute()`는 CLI를 입력할 때 모두 실행합니까?
2- 어떤 규칙 일치, 규칙 1, 규칙 2 또는 아무도?
3- CLI 클라이언트는 콘솔에서 값 `result_text`을 출력합니까?
4- 출력 파일은 입력 또는 응답 만 포함합니까? 입력의 첫 번째 20 문자와 결과가 동일합니다. 더 많은 것은 볼 수 없습니다.
5 정확한 CLI는 텍스트를 드롭하는 데 사용합니까? 아직 언급되지 않았습니다.

## 6- 주사된 hypotheses

1- 입력은 단축되지 않습니다. 로그에서 20character 단축되었습니다.
2- Ollama, 단어 및 num 예측은 원인이 아닙니다.
3- 캐시는 "위스"에서 우회되고 따라서 원인이 아닙니다.

## 7- 작업 이외의 오류 발견 (작업없이 아무것도 변경하지 마십시오)

1개의 파일:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`if not raw_text:` 후, `response = answer_for_all_fallback`가 설정됩니다. 다음 줄은 `clean_text_for_typing(raw_text)`로 덮습니다. 빈 Ollama 응답으로, 대답은 빈 남아있다. 마찬가지로 `response.replace('sl5_config.py', ...)`와 `response.replace(' sl5_record_trigger.py ', ...)`는 결과가 할당되지 않기 때문에 효과가 없습니다.

2 파일:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

`Overlay`에 따르면 `|`가 누락되어 변형 `OverlayOrange`가 생성됩니다. 또한 `_variants`는 "컴퓨터"라는 단어를 포함하지 않습니다. 규칙 1은 그러므로 "컴퓨터 정확히 ...", 규칙 2 할 수 없습니다.

3 파일:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'`는 모든 수입에 로그를 덮습니다.

## 8- 다음 단계 (당신의 "예") 후

A 단계 : 신속한 서명없이 CLI 통화를 요청하십시오.

단계 B: `result_text`의 처리를 찾아내십시오:

```
tools/search.sh "result_text" .
```

단계 C: 입력 후에 콘솔 출력을 검사하십시오. 메인 프로그램 콘솔에서 전체 텍스트를 요청합니다.

단계 D: 그 후에 전/후 체재에서 변화를, 단지 제안합니다.

## 9- 성공자가 준수해야하는 작업 규칙

1- 독일 통신. 코드, 의견, 로그 및 식별자 만, 심지어 코드 블록.
2- 당신의 산출에서 증거 없이 체계 상태에 관하여 진술 없음. 추측하지 마십시오.
3- 새로운 작업: 먼저 이해를 설명, 당신의 "예".
4- "나는 저장소에 액세스 할 수 없습니다"설정.
-i, -E 및 -w 옵션으로 도구 / 검색을 통해 5 저장소 검색 만.
6- 에러를 위해, 가득 차있는 traceback를 첫째로 얻으십시오.
7- 명령 및 파일 경로는 끝에서 punctuation없이 자신의 선에 각각 있습니다.
8- 형식의 번호 1-, 2-, 3-.
9- Code는 주변 기능 코드 없이 이전/후 체재에 있는 변화한 선으로만 변화합니다.
10- 부호의 구획에 있는 주요한 indentation를 가진 python 부호 없음, indentation 없이 작은 기능.
11- 절대 없음, 사용자 별 경로 및 파일 경로없이 라인 번호.
12- 충전 세트 없음, 정서적 톤 없음, 대상으로 응답 당 약 1400 문자.
13- 당신이 이미 수행 한 작업을 치료.
14- 출력을 복사 할 때 프롬프트 기호를 복사하지 마십시오, 그렇지 않으면 종료 코드 127 생성됩니다.
15 날짜와 시간을 찾기 위해 시작: ./tools/find-nearest-commit.sh "2026-07-28 17:00"
