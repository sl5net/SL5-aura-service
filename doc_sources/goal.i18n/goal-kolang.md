## 목표: "받아쓰기 세션" 모델

### Unser Ziel(독일어): "Diktier-Sitzung"을 죽으세요

Ein einziger Trigger startet eine **"Diktier-Sitzung"**, die aus drei Phasen besteht:

1. **시작 단계(Warten auf Sprache):**
* Nach dem Trigger lauscht das 시스템.
* Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT`(z.B. 12초).

2. **활성 단계(Kontinuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den active Modus.
* Immer wenn VOSK eine Sprechpause erkennt und einen Textblock liefert(z.B. einen Satz), wird dieser Block **sofort** zur Verarbeitung(LanguageTool 등) weitergegeben und als Text ausgegeben.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3. **종기(Ende der Sitzung):**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT`(z.B. 1-2s) komplett는 여전히 남아 있습니다.
* Der Nutzer stoppt die Sitzung manuell per Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Nutzer eine längere Pause macht oder sie manuell beendet.


### **목표: "받아쓰기 세션" 모델**

단일 트리거는 세 단계로 구성된 **"받아쓰기 세션"**을 시작합니다.
1. **시작 단계(발언 대기):**
* 트리거 후 시스템이 청취를 시작합니다.
* **음성이 감지되지 않으면** `PRE_RECORDING_TIMEOUT`(예: 12초) 후에 전체 세션이 종료됩니다.
2. **활성 단계(연속 받아쓰기):**
* 첫 번째 음성 입력이 감지되는 즉시 세션이 활성 모드로 전환됩니다.
* VOSK가 일시 중지를 감지하고 텍스트 청크(예: 문장)를 전달할 때마다 이 청크는 **즉시** 처리 파이프라인(LanguageTool 등)에 전달되어 텍스트로 출력됩니다.
* 녹음은 백그라운드에서 **원활하게** 계속되며 다음 발언을 기다립니다.
3. **종료 단계(세션 종료):**
* 전체 세션은 다음 두 가지 조건 중 하나가 충족되는 경우에만 종료됩니다.
* 사용자는 `SPEECH_PAUSE_TIMEOUT` 기간(예: 1~2초) 동안 완전히 침묵을 유지합니다.
* 사용자가 트리거를 통해 수동으로 세션을 중지합니다.
**간단히 말하면:** 하나의 세션으로 여러 개의 즉각적인 텍스트 출력이 가능합니다. 세션은 사용자가 오랫동안 일시 중지하거나 수동으로 종료할 때까지 활성 상태로 유지됩니다.