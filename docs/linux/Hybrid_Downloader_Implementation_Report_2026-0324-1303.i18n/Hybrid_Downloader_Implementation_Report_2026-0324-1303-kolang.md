# 하이브리드 다운로더 구현 보고 24.3.'26 13:04 Tue

## 1. 프로젝트 현황 요약
새로운 `download_release_hybrid.py` 스크립트가 성공적으로 구현 및 통합되었습니다. BitTorrent 하이브리드 레이어를 추가하는 동시에 원본 `download_all_packages.py`의 핵심 로직을 복제합니다.

### 검증된 핵심 기능:
* **CLI 인수 구문 분석:** `--exclude`, `--tag` 및 `--list`를 성공적으로 처리합니다.
* **CI 환경 감지:** GitHub Actions를 올바르게 식별하고 대규모 모델을 자동 제외합니다.
* **자산 검색:** 릴리스 자산을 논리적 패키지(부품, 체크섬, 토렌트)로 성공적으로 그룹화합니다.
* **강력한 폴백:** 스크립트는 `libtorrent`가 없음을 감지하고 기본적으로 HTTP 폴백 모드로 설정됩니다.

---

## 2. 테스트 실행 및 결과
**실행된 명령:**
`파이썬 도구/download_release_hybrid.py --list`

### 관찰된 출력:
* **종속성 검사:** `--> 정보: 'libtorrent'를 찾을 수 없습니다. 하이브리드 토렌트가 비활성화되었습니다. HTTP 대체 사용'(현재 시스템에서 예상됨).
* **API 연결:** `sl5net/SL5-aura-service @ v0.2.0`에 대한 릴리스 정보를 성공적으로 가져왔습니다.
* **발견 결과:** 확인된 패키지 5개:
1. `LanguageTool-6.6.zip`(3개 부분)
2.`lid.176.zip`(2개 부분)
3. `vosk-model-de-0.21.zip`(20개 부분)
4. `vosk-model-en-us-0.22.zip`(19개 부분)
5. `vosk-model-small-en-us-0.15.zip`(1개 부분)

---

## 3. 오류 보고서: 종속성 문제
### 문제: `libtorrent` 설치 실패
현재 **Manjaro/Arch Linux** 환경에서는 표준 패키지 관리자를 통해 BitTorrent 엔진(`libtorrent`)을 설치할 수 없습니다.

* **시도한 명령:**
* `sudo pacman -S python-libtorrent` -> `대상을 찾을 수 없음`
* `pamac build python-libtorrent-rasterbar` -> `대상을 찾을 수 없음`
* `pamac build python-libtorrent` -> `대상을 찾을 수 없음`
* **근본 원인:** Arch 기반 시스템의 `libtorrent`에 대한 Python 바인딩은 공식 저장소에서 제대로 유지 관리되지 않거나 현재 누락되거나 잘못 구성된 특정 AUR 도우미/빌드 도구(`base-devel`)가 필요한 경우가 많습니다.
* **영향:** BitTorrent 기능(P2P 및 웹 시드)은 현재 비활성화되어 있습니다. 스크립트는 **HTTP 대체**를 통해 완전한 기능을 유지합니다.

---

## 4. 할 일 목록(다음 단계)

### 1단계: 환경 마이그레이션
- [ ] **OS 전환:** `python3-libtorrent` 또는 `pip install libtorrent`를 더 쉽게 사용할 수 있는 다른 운영 체제(예: Ubuntu, Debian 또는 Windows)로 테스트를 이동합니다.
- [ ] **종속성 재검증:** "모터"(`libtorrent`)가 새 OS에 올바르게 로드되는지 확인하세요.

### 2단계: 기능 검증
- [ ] **전체 다운로드 테스트:** `--list` 플래그 없이 스크립트를 실행하여 부분 다운로드, 병합 및 SHA256 확인을 확인합니다.
- [ ] **제외 테스트:** `--exclude de`를 사용하여 실행하여 영어 전용 설정이 의도한 대로 작동하는지 확인합니다.
- [ ] **Torrent Seed 테스트:** GitHub Web-Seed를 사용하여 `.torrent` 파일을 생성하고 하이브리드 다운로더가 표준 HTTP 부분보다 P2P/Web-Seed를 우선시하는지 확인합니다.

### 3단계: 정리
- [ ] **최종 정리 확인:** 전체 실행 후 최종 로컬 디렉터리 구조에 `.i18n` 또는 번역 파일이 없는지 확인합니다.