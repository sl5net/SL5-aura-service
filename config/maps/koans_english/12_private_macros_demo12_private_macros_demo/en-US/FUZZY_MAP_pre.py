# config/maps/koans_english/12_private_macros_demo/en-US/FUZZY_MAP_pre.py

FUZZY_MAP_pre = [
    # =========================================================================
    # OUTER MACRO: PRIVATE SECTION
    # =========================================================================
    # Triggers the 'private_section' group. It is marked as 'is_private' to protect sensitive data.
    ('Private Profile', r'insert my private profile', 100, {
        'group_start': 'private_section',
    }),

    # -------------------------------------------------------------------------
    # SUB-SECTION 1: NAME DETAILS (Nested Macro)
    # -------------------------------------------------------------------------
    # Appends the section header 'Name:' if the trigger word 'name details' is not in the text.
    ('Name:', r'name details', 100, {'group_start': 'name_details'}),

    # Standard rules inside the name sub-section:
    # If the user speaks 'first name' or 'last name', they get replaced by the actual values,
    # otherwise 'John' and 'Doe' are injected automatically as fallbacks.
    ('John', r'first name', 100, {}),
    ('Doe', r'last name', 100, {}),

    # End of Name Sub-Section
    (None, r'', 100, {'group_end': 'name_details'}),

    # -------------------------------------------------------------------------
    # SUB-SECTION 2: CONTACT DETAILS (Nested Macro)
    # -------------------------------------------------------------------------
    # Appends the section header 'Contact:' if the trigger word 'contact details' is not in the text.
    ('Contact:', r'contact details', 100, {'group_start': 'contact_details'}),

    # Standard rules inside the contact sub-section:
    # Automatically injects email and phone details if not matched, or performs the replacements.
    ('john.doe@example.com', r'email address', 100, {}),
    ('+49 123 456789', r'phone number', 100, {}),

    # End of Contact Sub-Section
    (None, r'', 100, {'group_end': 'contact_details'}),

    # =========================================================================
    # OUTER MACRO END
    # =========================================================================
    # Passive end marker to terminate the main private section macro.
    (None, r'', 100, {'group_end': 'private_section'})
]
