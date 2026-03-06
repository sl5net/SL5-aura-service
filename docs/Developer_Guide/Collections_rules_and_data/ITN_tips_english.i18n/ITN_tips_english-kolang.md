기술 용어는 **ITN(역 텍스트 정규화)**입니다.

검색해 보면 방대한 규칙과 데이터 모음을 찾을 수 있습니다.

모든 것을 직접 입력하지 않고도 지도를 채울 수 있는 최고의 리소스는 다음과 같습니다.

### 1. ITN 규칙 모음(“최적 표준”)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** 바로 이러한 목적을 위해 설계된 간단하고 결정적인 Python 도구입니다. CSV 파일을 사용하여 음성 단어를 서면 문자(숫자, 통화, 날짜)로 변환합니다. CSV를 지도에 거의 1:1로 복사할 수 있습니다.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** 매우 강력합니다. 그들은 거의 모든 언어에 대한 거대한 문법 파일을 가지고 있습니다. 여기에서 측정 단위, 제목 및 날짜 형식에 대한 목록을 찾을 수 있습니다.

### 2. 구두점 및 대소문자에 대한 데이터 소스
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Vosk용 표준 도구입니다. 모델을 사용하지만 소스 코드에는 추출할 수 있는 약어 및 고유 명칭 목록이 포함되어 있는 경우가 많습니다.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** 음성 언어가 문자 언어로 변환되는 방법에 대한 수백만 개의 예가 포함된 대규모 데이터 세트(Kaggle 챌린지를 위해 생성됨)입니다.

### 3. “받아쓰기 도우미” 라이브러리
* **[num2words](https://github.com/savoirfairelinux/num2words):** 숫자 매핑이 필요한 경우 여기에서 "1"부터 "100만"까지의 목록을 찾을 수 있습니다.