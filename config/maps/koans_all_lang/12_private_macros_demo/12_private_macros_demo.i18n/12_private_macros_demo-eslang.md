# Koan 12: Demostración de macros privadas

Este ejercicio demuestra cómo usar macros privadas anidadas y limitar su alcance a ventanas activas específicas usando la configuración `only_in_windows`.

## Requisito de seguridad de ventana activa
Para evitar que estas reglas demostrativas (como nombre, correo electrónico o número de teléfono) se ejecuten globalmente durante otras pruebas del sistema, están restringidas a ventanas activas que coincidan con el patrón `12_private_macros_demo`.

Para probar estas reglas, debe:
1. Utilice un editor que muestre la ruta completa del archivo en el título de su ventana (por ejemplo, PyCharm o VS Code).
2. Guarde o cambie el nombre del archivo que está editando para que su nombre contenga `12_private_macros_demo` en su editor (por ejemplo, en el editor Kate).

---

## Instrucciones

1. Identifique el nombre de la carpeta de su idioma (por ejemplo, `de-DE` para alemán, `en-US` para inglés, `fr-FR` para francés)
2. Dentro de su carpeta de idioma, asegúrese de que haya un archivo llamado `FUZZY_MAP_pre.py`. Si no existe, créelo.
3. Copie las reglas de la plantilla a continuación en su lista `FUZZY_MAP_pre` dentro de ese archivo.

### Carpetas de idiomas admitidos
Si la carpeta para su idioma aún no existe en `config/maps/koans_deutsch/12_private_macros_demo/`, debe crearla manualmente. Utilice los nombres de carpeta exactos que se enumeran a continuación:

- `ar` (árabe)
- `de-DE` (alemán)
- `en-US` (inglés)
- `es` (español)
- `fr` (francés)
- `hola` (hindi)
- `ja` (japonés)
- `ko` (coreano)
- `pl` (polaco)
- `pt-BR` (portugués - Brasil)
- `pt` (portugués)
- `zh-CN` (chino - simplificado)


### Plantilla de regla

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