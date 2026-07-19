# Koan 12: プライベートマクロのデモ

この演習では、ネストされたプライベート マクロを使用し、`only_in_windows` 設定を使用してその範囲を特定のアクティブ ウィンドウに制限する方法を示します。

## アクティブ ウィンドウのセキュリティ要件
これらの実証的なルール (名、電子メール、電話番号など) が他のシステム テスト中にグローバルに実行されないように、パターン `12_private_macros_demo` に一致するアクティブなウィンドウに制限されます。

これらのルールをテストするには、次のいずれかを行う必要があります。
1. ウィンドウ タイトルに完全なファイル パスを表示するエディター (PyCharm や VS Code など) を使用します。
2. エディター (Kate エディターなど) で名前に「12_private_macros_demo」が含まれるように、編集中のファイルを保存または名前変更します。

---

＃＃ 説明書

1. 言語フォルダー名を特定します (たとえば、ドイツ語の場合は「de-DE」、英語の場合は「en-US」、フランス語の場合は「fr-FR」)
2. 言語フォルダー内に、「FUZZY_MAP_pre.py」という名前のファイルがあることを確認します。存在しない場合は作成します。
3. 以下のテンプレート ルールをそのファイル内の `FUZZY_MAP_pre` リストにコピーします。

### サポートされている言語フォルダー
使用する言語のフォルダーが `config/maps/koans_deutsch/12_private_macros_demo/` の下にまだ存在しない場合は、手動で作成する必要があります。以下にリストされている正確なフォルダー名を使用してください。

- `ar` (アラビア語)
- `de-DE` (ドイツ語)
- `en-US` (英語)
- `es` (スペイン語)
- `fr` (フランス語)
- 「こんにちは」（ヒンディー語）
- `じゃ` (日本語)
- `ko` (韓国語)
- `pl` (ポーランド語)
- `pt-BR` (ポルトガル語 - ブラジル)
- `pt` (ポルトガル語)
- `zh-CN` (中国語 - 簡体字)


### ルールテンプレート

```python
# Copy these rules to your FUZZY_MAP_pre list

# config/maps/koans_deutsch/12_private_macros_demo/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401

FUZZY_MAP_pre = [ 
# ========================================================================= 
# OUTER MACRO: PRIVATE SECTION 
# ========================================================================= 
# Triggers the 'private_section' group. 
# EXAMPLE: my private profile 
('private profile', r'my private profile', 100, { 
'group_start': 'private_section' 
}), 

# ----------------------------------------------------------------------- 
# SUB-SECTION 1: NAME DETAILS (Nested Macro) 
# ----------------------------------------------------------------------- 
# Appends the section header 'Name:' if the trigger word 'namensdetails' is not in the text. 
# EXAMPLE: name details

('Name:', r'name details', 100, {'group_start': 'name_details'}),

# Standard rules inside the name sub-section:

# EXAMPLE: first name

('Max', r'first name', 100, {}),

# EXAMPLE: last name

('Mustermann', r'last name', 100, {}),

# EXAMPLE: nixleA

('nixA', r'nixleA', 100, {}),

# EXAMPLE: nixleB

('nixB', r'nixleB', 100, {}),

# End of Name Sub-Section

(None, r'', 100, {'group_end': 'name_details'}),

# -------------------------------------------------------------------------

# SUB-SECTION 2: CONTACT DETAILS (Nested Macro) 
# ----------------------------------------------------------------------- 
# Appends the section header 'Contact:' if the trigger word 'contact details' is not in the text. 
# EXAMPLE: contact details 
('Contact:', r'contact_details', 100, {'group_start': 'contact_details'}), 

# Standard rules inside the contact sub-section: 
# EXAMPLE: email address 
('max.mustermann@example.de', r'e-mail-address', 100, {}), 
# EXAMPLE: phone number 
('+49 170 1234567', r'phone number', 100, {}), 

# End of Contact Sub Section 
(None, r'', 100, {'group_end': 'contact_details'}), 

# ========================================================================= 
# OUTER MACRO END 
# ========================================================================= 
# Passive end marker to terminate the main private section macro. 
(None, r'', 100, {'group_end': 'private_section'})
]


]
```