# Koan 12: Private Macros Demo

This exercise demonstrates how to use nested private macros and limit their scope to specific active windows using the `only_in_windows` configuration.

## Active Window Security Requirement
To prevent these demonstrative rules (like first name, email, or phone number) from executing globally during other system tests, they are restricted to active windows matching the pattern `12_private_macros_demo`.

To test these rules, you must either:
1. Use an editor that displays the full file path in its window title (e.g., PyCharm or VS Code).
2. Save or rename the file you are editing so that its name contains `12_private_macros_demo` in your editor (e.g., in Kate editor).

---

## Instructions

1. Identify your language folder name (for example, `de-DE` for German, `en-US` for English, `fr-FR` for French)
2. Inside your language folder, ensure there is a file named `FUZZY_MAP_pre.py`. If it does not exist, create it.
3. Copy the template rules below into your `FUZZY_MAP_pre` list inside that file.

### Supported Language Folders
If the folder for your language does not exist yet under `config/maps/koans_deutsch/12_private_macros_demo/`, you must create it manually. Please use the exact folder names listed below:

- `ar` (Arabic)
- `de-DE` (German)
- `en-US` (English)
- `es` (Spanish)
- `fr` (French)
- `hi` (Hindi)
- `ja` (Japanese)
- `ko` (Korean)
- `pl` (Polish)
- `pt-BR` (Portuguese - Brazil)
- `pt` (Portuguese)
- `zh-CN` (Chinese - Simplified)


### Rule Template

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

