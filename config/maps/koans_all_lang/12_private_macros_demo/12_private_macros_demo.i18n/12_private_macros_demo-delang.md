# Koan 12: Demo zu privaten Makros

In dieser Übung wird gezeigt, wie Sie verschachtelte private Makros verwenden und ihren Geltungsbereich mithilfe der Konfiguration „only_in_windows“ auf bestimmte aktive Fenster beschränken.

## Aktive Fenstersicherheitsanforderung
Um zu verhindern, dass diese demonstrativen Regeln (wie Vorname, E-Mail oder Telefonnummer) während anderer Systemtests global ausgeführt werden, sind sie auf aktive Fenster beschränkt, die dem Muster „12_private_macros_demo“ entsprechen.

Um diese Regeln zu testen, müssen Sie entweder:
1. Verwenden Sie einen Editor, der den vollständigen Dateipfad im Fenstertitel anzeigt (z. B. PyCharm oder VS Code).
2. Speichern Sie die Datei, die Sie bearbeiten, oder benennen Sie sie um, sodass ihr Name „12_private_macros_demo“ in Ihrem Editor enthält (z. B. im Kate-Editor).

---

## Anweisungen

1. Identifizieren Sie den Namen Ihres Sprachordners (z. B. „de-DE“ für Deutsch, „en-US“ für Englisch, „fr-FR“ für Französisch).
2. Stellen Sie sicher, dass sich in Ihrem Sprachordner eine Datei mit dem Namen „FUZZY_MAP_pre.py“ befindet. Wenn es nicht existiert, erstellen Sie es.
3. Kopieren Sie die folgenden Vorlagenregeln in Ihre „FUZZY_MAP_pre“-Liste in dieser Datei.

### Unterstützte Sprachordner
Sollte der Ordner für Ihre Sprache unter „config/maps/koans_deutsch/12_private_macros_demo/“ noch nicht vorhanden sein, müssen Sie ihn manuell erstellen. Bitte verwenden Sie die genauen unten aufgeführten Ordnernamen:

- `ar` (Arabisch)
- `de-DE` (Deutsch)
- „en-US“ (Englisch)
- `es` (Spanisch)
- „fr“ (Französisch)
- „Hallo“ (Hindi)
- „ja“ (Japanisch)
- „ko“ (Koreanisch)
- `pl` (Polnisch)
- „pt-BR“ (Portugiesisch – Brasilien)
- `pt` (Portugiesisch)
- „zh-CN“ (Chinesisch – vereinfacht)


### Regelvorlage

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