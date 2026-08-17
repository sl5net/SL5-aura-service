# 워크플로 알림(오디오 경고)

생산성을 향상시키려면 GitHub Actions 워크플로가 완료되는 즉시 코드를 푸시하고 자동으로 경고(음성 또는 소리를 통해) 알리는 로컬 Git 별칭을 구성할 수 있습니다. 이를 통해 "GitHub 시청 피로"를 방지하고 다른 작업에 집중할 수 있습니다.

### 전제 조건

시스템에 **GitHub CLI**와 텍스트 음성 변환 엔진 또는 사운드 플레이어가 설치되어 있어야 합니다.

**만자로/아치 리눅스의 경우:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### 설정

터미널에서 다음 명령을 실행하여 `pushsound`라는 전역 Git 별칭을 만듭니다.

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### 용법

`git push` 대신 다음을 실행하세요.
```bash
git pushsound
```
터미널은 워크플로가 완료될 때까지 기다린 후 *"모든 github 워크플로가 완료되었습니다."*라고 알립니다.

---

### 사용자 정의 및 대안

기본 설정에 따라 다른 별칭 이름이나 알림 방법을 사용할 수도 있습니다.

#### 1. 권장 별칭 이름
'pushsound'가 너무 길어서 입력할 수 없는 경우 다음 대안을 고려하세요.
* `git pw`(푸시 앤 워치) — **속도를 위해 권장됩니다.**
* `git sync`("녹색 신호등"을 누르고 기다리는 것을 의미)
* `git palert`(푸시 경고)

#### 2. 알림 스타일
'espeak-ng' 부분을 다른 유형의 알림으로 바꿀 수 있습니다:

* **데스크톱 알림:**
`... && 통지-전송 "GitHub Action" "워크플로 완료!"`
* **시스템 사운드(벨):**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **조합(사운드 + 음성):**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "완료"`

#### 3. 고급: 팀 안전 버전
여러 개발자가 동일한 저장소에 동시에 푸시하는 경우 기본 명령이 잘못된 실행을 추적할 수 있습니다. 현재 분기만 보려면 이 "분기 안전" 버전을 사용하세요.

#####는 첫 번째 워크플로만 확인합니다.

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'

git config --global alias.pushsound '!git push && sleep 3 && (gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") --exit-status && espeak-ng "workflow successful" || espeak-ng "workflow failed")'

```

#####은 GitHub에 등록된 모든 워크플로를 확인합니다.

git config --global alias.pushsound '!f() { git push && echo "GitHub에서 워크플로를 등록하는 중..." && sleep 5 && SHA=$(git rev-parse HEAD) && SUCCESS=0 && for id in $(gh run list --commit $SHA --json DatabaseId -q ".[].databaseId"); do echo "워크플로 $id를 보는 중..." && gh run watch $id --exit-status || 성공=1; 완료; [ $SUCCESS -eq 0 ] && espeak-ng "모든 워크플로가 성공했습니다" || espeak-ng "적어도 하나의 작업 흐름이 실패했습니다"; }; 에프'


### 문제 해결
* **"실행을 찾을 수 없음":** GitHub가 푸시를 등록하고 워크플로를 시작하는 데 시간이 걸리기 때문에 'sleep 3'을 포함합니다. 연결 속도가 매우 느린 경우 'sleep 5'로 늘려야 할 수도 있습니다.
* **터미널 경고음:** `espeak-ng`가 작동하지 않으면 오디오가 음소거되어 있지 않고 패키지가 올바르게 설치되었는지 확인하세요.