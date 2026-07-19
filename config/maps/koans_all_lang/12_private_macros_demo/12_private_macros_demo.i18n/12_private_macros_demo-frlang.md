# Koan 12 : Démo de macros privées

Cet exercice montre comment utiliser des macros privées imbriquées et limiter leur portée à des fenêtres actives spécifiques à l'aide de la configuration « only_in_windows ».

## Exigence de sécurité pour les fenêtres actives
Pour empêcher ces règles démonstratives (comme le prénom, l'e-mail ou le numéro de téléphone) de s'exécuter globalement lors d'autres tests du système, elles sont limitées aux fenêtres actives correspondant au modèle `12_private_macros_demo`.

Pour tester ces règles, vous devez soit :
1. Utilisez un éditeur qui affiche le chemin complet du fichier dans le titre de sa fenêtre (par exemple, PyCharm ou VS Code).
2. Enregistrez ou renommez le fichier que vous éditez afin que son nom contienne « 12_private_macros_demo » dans votre éditeur (par exemple, dans l'éditeur Kate).

---

## Instructions

1. Identifiez le nom de votre dossier de langue (par exemple, « de-DE » pour l'allemand, « en-US » pour l'anglais, « fr-FR » pour le français)
2. Dans votre dossier de langue, assurez-vous qu'il existe un fichier nommé « FUZZY_MAP_pre.py ». S'il n'existe pas, créez-le.
3. Copiez les règles du modèle ci-dessous dans votre liste `FUZZY_MAP_pre` à l'intérieur de ce fichier.

### Dossiers de langues pris en charge
Si le dossier correspondant à votre langue n'existe pas encore sous `config/maps/koans_deutsch/12_private_macros_demo/`, vous devez le créer manuellement. Veuillez utiliser les noms de dossiers exacts répertoriés ci-dessous :

- `ar` (arabe)
- `de-DE` (allemand)
- `en-US` (anglais)
- `es` (espagnol)
- `fr` (français)
- `salut` (hindi)
- `ja` (japonais)
- `ko` (coréen)
- `pl` (polonais)
- `pt-BR` (Portugais - Brésil)
- `pt` (portugais)
- `zh-CN` (chinois - simplifié)


### Modèle de règle

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