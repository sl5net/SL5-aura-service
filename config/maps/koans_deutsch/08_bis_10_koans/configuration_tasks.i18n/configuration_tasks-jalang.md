設定-公案

### 1.公案 08: Die Schalter-Zentrale (プラグイン アクティヴィエレン)
**詳細:** `settings.py` の新しい機能 (プラグイン) を参照してください。

* **Aufgabe:** 「ウィキペディア プラグインの動作、`False` と `True` の区別を保証します。」
* **Nutzen:** Verstehen、Aura モジュラー主義者です。

### 2. 公案 09: Dein digitales Namensschild (変数)
**詳細:** 設定の詳細については、プラグインを参照してください。
* **アウフガベ:** 「変数 `USER_NAME` にある名前は、Trage deinen eigenen です。」
* **Nutzen:** プラグインは「Mit freundlichen Grüßen, [Dein Name]」を参照してください。

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

### 3. 公案 10: ゲドゥルド ビッテ! (パウゼン・ツァイテン)
**Lerneffekt:** Die Spracherkennung and das eigene Sprechtempo anpassen.
* **Aufgabe:** 「`SPEECH_PAUSE_TIMEOUT` を読み上げてください。オーラは長くなりますが、安全を確保してください。」
* **ヌッツェン:** ビソンダーズは Ruhe nachdenken に集まりました。