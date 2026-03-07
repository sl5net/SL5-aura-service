# 유명 수학자 – STT 교정 가이드

## 문제

Vosk와 같은 음성 인식(STT) 시스템은 유명한 수학자의 이름을 잘못 듣거나 철자를 틀리는 경우가 많습니다.
이는 특히 특수 문자(ß, ü, ä, ö)가 포함된 독일어 이름에서 흔히 발생합니다.
또는 다른 언어에서 빌린 이름.

## 일반적인 STT 오류

| 음성/STT 출력 | 올바른 철자법 | 메모 |
|---|---|---|
| 가우스, 가우스 | 가우스 | 독일의 수학자, ß가 자주 누락됨 |
| 오일러, 오일러 | 오일러 | 스위스, 이름은 독일어로 "오일러"처럼 들림 |
| 라이프니츠, 리프니츠 | 라이프니츠 | z 끝, 일반적인 철자 오류 |
| 리만, 리만 | 리만 | double-n이 자주 누락됨 |
| 힐베르트 | 힐베르트 | 일반적으로 정확하며 대문자만 사용 |
| 선창자 | 칸토어 | 일반적으로 정확하며 대문자만 사용 |
| 푸앵카레, 푸앵카레 | 푸앵카레 | 악센트가 자주 누락됨 |
| 더 이상, 더 이상 | 뇌터 | 움라우트가 자주 누락됨 |

## 예제 규칙

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## 왜 Pre-LanguageTool인가요?

이러한 수정은 `FUZZY_MAP_pre.py`(LanguageTool 이전)에서 이루어져야 합니다.
LanguageTool이 철자가 틀린 이름을 다른 잘못된 단어로 "수정"할 수 있기 때문입니다.
먼저 문제를 수정한 다음 LanguageTool에서 문법을 확인하도록 하는 것이 좋습니다.

## 테스트

규칙을 추가한 후 Aura 콘솔로 테스트합니다.
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
예상됨: 'Euler hat die Formel e hoch i pi plus eins gleich null bewiesen'