# file: scripts/py/func/checks/integrity_rules.py
# integrity_rules.py

"""
This file defines critical code fragments that must exist in specific files.
The integrity checker will verify their presence on startup in DEV_MODE.
If a check fails, the application will exit to prevent running with broken logic.

Format:
{
    "path/to/file_relative_to_project_root.py": [
        "exact_code_fragment_to_find",
        "another_fragment_for_the_same_file"
    ]
}
"""

INTEGRITY_CHECKS = {
    # Ensures the self-tester remains tolerant to leading whitespace.
    "scripts/py/func/checks/self_tester.py": [
        "if actual.lstrip() == expected:"
    ],

    # Protects the regex substitution logic in the main processing function.
    "scripts/py/func/process_text_in_background.py": [
        "new_text = re.sub("
    ],

    # germen umlaute needs this to could read correct for e.g. from script like autokey
    "scripts/py/func/process_text_in_background.py": [
        'encoding="utf-8-sig"'
    ],


}
