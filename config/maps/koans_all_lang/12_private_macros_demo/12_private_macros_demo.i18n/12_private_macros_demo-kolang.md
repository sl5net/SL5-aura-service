# Koan 12: 개인 매크로 데모

이 연습에서는 중첩된 비공개 매크로를 사용하고 `only_in_windows` 구성을 사용하여 해당 범위를 특정 활성 창으로 제한하는 방법을 보여줍니다.

## 활성 창 보안 요구 사항
이러한 실증 규칙(예: 이름, 이메일 또는 전화번호)이 다른 시스템 테스트 중에 전역적으로 실행되는 것을 방지하기 위해 '12_private_macros_demo' 패턴과 일치하는 활성 창으로 제한됩니다.

이러한 규칙을 테스트하려면 다음 중 하나를 수행해야 합니다.
1. 창 제목에 전체 파일 경로를 표시하는 편집기(예: PyCharm 또는 VS Code)를 사용합니다.
2. 편집기(예: Kate 편집기)에서 이름에 '12_private_macros_demo'가 포함되도록 편집 중인 파일을 저장하거나 이름을 바꿉니다.

---

## 지침

1. 언어 폴더 이름을 확인합니다(예: 독일어의 경우 'de-DE', 영어의 경우 'en-US', 프랑스어의 경우 'fr-FR')
2. 언어 폴더 안에 'FUZZY_MAP_pre.py'라는 파일이 있는지 확인하세요. 존재하지 않는 경우 작성하십시오.
3. 아래 템플릿 규칙을 해당 파일 내의 `FUZZY_MAP_pre` 목록에 복사하세요.

### 지원되는 언어 폴더
해당 언어에 대한 폴더가 아직 `config/maps/koans_deutsch/12_private_macros_demo/` 아래에 없으면 수동으로 만들어야 합니다. 아래 나열된 정확한 폴더 이름을 사용하세요.

-`ar`(아랍어)
-`de-DE`(독일어)
-`en-US`(영어)
-`es`(스페인어)
-`fr`(프랑스어)
-`안녕`(힌디어)
-`ja`(일본어)
- `ko`(한국어)
-`pl`(폴란드어)
- `pt-BR`(포르투갈어 - 브라질)
-`pt`(포르투갈어)
- `zh-CN`(중국어 - 간체)


### 규칙 템플릿

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