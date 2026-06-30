# config/maps/koans_deutsch/12_private_macros_demo/de-DE/FUZZY_MAP_pre.py

FUZZY_MAP_pre = [
    # =========================================================================
    # OUTER MACRO: PRIVATE SECTION
    # =========================================================================
    # Triggers the 'private_section' group.
    # EXAMPLE: mein privates profil
    ('Privates Profil', r'mein privates profil', 100, {
        'group_start': 'private_section'
    }),

    # -------------------------------------------------------------------------
    # SUB-SECTION 1: NAME DETAILS (Nested Macro)
    # -------------------------------------------------------------------------
    # Appends the section header 'Name:' if the trigger word 'namensdetails' is not in the text.
    # EXAMPLE: namens details
    ('Name:', r'namens details', 100, {'group_start': 'name_details'}),

    # Standard rules inside the name sub-section:
    # EXAMPLE: vorname
    ('Max', r'vorname', 100, {}),
    # EXAMPLE: nachname
    ('Mustermann', r'nachname', 100, {}),

    # EXAMPLE: nixleA
    ('nixA', r'nixleA', 100, {}),
    # EXAMPLE: nixleB
    ('nixB', r'nixleB', 100, {}),


    # End of Name Sub-Section
    (None, r'', 100, {'group_end': 'name_details'}),

    # -------------------------------------------------------------------------
    # SUB-SECTION 2: CONTACT DETAILS (Nested Macro)
    # -------------------------------------------------------------------------
    # Appends the section header 'Kontakt:' if the trigger word 'kontaktdetails' is not in the text.
    # EXAMPLE: kontaktdetails
    ('Kontakt:', r'kontaktdetails', 100, {'group_start': 'contact_details'}),

    # Standard rules inside the contact sub-section:
    # EXAMPLE: e-mail-adresse
    ('max.mustermann@example.de', r'e-mail-adresse', 100, {}),
    # EXAMPLE: telefonnummer
    ('+49 170 1234567', r'telefonnummer', 100, {}),

    # End of Contact Sub-Section
    (None, r'', 100, {'group_end': 'contact_details'}),

    # =========================================================================
    # OUTER MACRO END
    # =========================================================================
    # Passive end marker to terminate the main private section macro.
    (None, r'', 100, {'group_end': 'private_section'})
]
