# Koan 12: Demonstração de macros privadas

Este exercício demonstra como usar macros privadas aninhadas e limitar seu escopo a janelas ativas específicas usando a configuração `only_in_windows`.

## Requisito de segurança de janela ativa
Para evitar que essas regras demonstrativas (como nome, e-mail ou número de telefone) sejam executadas globalmente durante outros testes do sistema, elas são restritas a janelas ativas que correspondam ao padrão `12_private_macros_demo`.

Para testar essas regras, você deve:
1. Use um editor que exiba o caminho completo do arquivo no título da janela (por exemplo, PyCharm ou VS Code).
2. Salve ou renomeie o arquivo que você está editando para que seu nome contenha `12_private_macros_demo` em seu editor (por exemplo, no editor Kate).

---

## Instruções

1. Identifique o nome da pasta do seu idioma (por exemplo, `de-DE` para alemão, `en-US` para inglês, `fr-FR` para francês)
2. Dentro da pasta do seu idioma, certifique-se de que haja um arquivo chamado `FUZZY_MAP_pre.py`. Se não existir, crie-o.
3. Copie as regras do modelo abaixo para sua lista `FUZZY_MAP_pre` dentro desse arquivo.

### Pastas de idiomas suportadas
Se a pasta para o seu idioma ainda não existir em `config/maps/koans_deutsch/12_private_macros_demo/`, você deverá criá-la manualmente. Use os nomes exatos das pastas listados abaixo:

- `ar` (árabe)
- `de-DE` (alemão)
- `en-US` (Inglês)
- `es` (espanhol)
- `fr` (francês)
- `oi` (hindi)
- `ja` (japonês)
- `ko` (coreano)
- `pl` (polonês)
- `pt-BR` (Português - Brasil)
- `pt` (português)
- `zh-CN` (chinês - simplificado)


### Modelo de regra

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