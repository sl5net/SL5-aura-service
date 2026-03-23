# Aura unter Wayland (Manjaro / Arch / CachyOS)

Damit Aura Text in andere Fenster schreiben kann、wird unter Wayland `dotool` verwendet。

### ヴィヒティゲ フォラウセツンゲン:
1. **デーモン:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch)。
2. **Berechtigungen:** ユーザーがグループの「入力」ボタンで悩んでいます。
3. **Uinput:** `/dev/uinput` をグループ化して、`input` を選択してください。

### マヌエル修復:
ティッペンの滝は、次の楽しみをもたらします。
__CODE_BLOCK_0__