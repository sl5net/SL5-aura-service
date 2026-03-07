# 有名な数学者 – STT 添削ガイド

＃＃ 問題

Vosk のような音声認識 (STT) システムは、有名な数学者の名前を聞き間違えたり、スペルを間違えたりすることがよくあります。
これは、特殊文字 (ß、ü、ä、ö) を含むドイツ語の名前で特によく見られます。
または他の言語から借用した名前。

## 一般的な STT エラー

|音声 / STT 出力 |正しいスペル |メモ |
|---|---|---|
|ガウス、ガウスガウス |ドイツの数学者、ß は行方不明になることが多い |
|オイラー、オイラー | 写真オイラー |スイス人、名前はドイツ語で「オイラー」に似ています |
|ライプニッツ、リプニッツ |ライプニッツ |末尾の z、よくあるスペルミス |
|リーマン、リーマン | 写真リーマン |ダブル N はよく見逃されます |
|ヒルベルト |ヒルベルト |通常は正しい、大文字のみ |
|カントール |カントール |通常は正しい、大文字のみ |
|ポアンカレ、ポアンカレ | 写真ポアンカレ |アクセントが欠けていることが多い |
|ノーテル、ノーテル |ネーター |ウムラウトはよく見逃されます |

## ルールの例

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## Pre-LanguageTool を使用する理由

これらの修正は `FUZZY_MAP_pre.py` (LanguageTool の前) で行われる必要があります。
なぜなら、LanguageTool はスペルミスのある名前を別の間違った単語に「修正」する可能性があるからです。
まずそれを修正してから、LanguageTool で文法チェックを行うことをお勧めします。

## テスト

ルールを追加した後、Aura コンソールでテストします。
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
予想される内容: 「Euler hat die Formel e hoch i pi plus eins gleich null bewiesen」