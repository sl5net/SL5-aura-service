# file: scripts/py/func/checks/integrity_rules.py

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
    # germen umlauts needs this to could read correct for e.g. from script like autokey
    # Ensures critical text processing logic is present.
    "scripts/py/func/process_text_in_background.py": [
        "new_text = re.sub(",
        'encoding="utf-8-sig"'
    ],

    # --- Start of Ensures language selection is included ---

    # Ensures language selection is included in the macOS setup.
    "setup/macos_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"'
    ],

    # Ensures language selection is included in the Ubuntu setup.
    "setup/ubuntu_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"'
    ],

    # Ensures language selection is included in the Manjaro/Arch setup.
    "setup/manjaro_arch_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"'
    ],

    # Ensures language selection is included in the Windows setup.
    "setup/windows11_setup.ps1": [
        '$GetLangScriptPath = "$PSScriptRoot\\..\\scripts\\sh\\get_lang.sh"',
        '& bash.exe $GetLangScriptPath $LangCode'
    ],

    # --- End of Ensures language selection is included ---

}
