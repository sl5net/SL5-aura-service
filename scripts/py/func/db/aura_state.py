# scripts/py/func/db/aura_state.py
"""
High-level API for Aura state management.
Readable interface for developers — wraps trino_client.py low-level operations.

Usage:
    from scripts.py.func.db.aura_state import enable_translation, disable_translation, get_interface_status
"""
import os
from pathlib import Path
import sys

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.py.func.db.trino_client import (
    get_feature_state,
    set_feature_state,
    get_target_lang,
    set_target_lang,
)

INTERFACES = ['speech', 'terminal', 'web']
FEATURES = ['translation']


def enable_translation(interface='speech', lang='en'):
    """Enable translation for a specific interface and set target language."""
    set_target_lang(interface, target_lang=lang)
    set_feature_state(interface, feature='translation', state='on')
    print(f"[aura_state] Translation ENABLED for '{interface}' → '{lang}'")


def disable_translation(interface='speech'):
    """Disable translation for a specific interface."""
    set_feature_state(interface, feature='translation', state='off')
    print(f"[aura_state] Translation DISABLED for '{interface}'")


def set_language(interface='speech', lang='en'):
    """Set target language for a specific interface."""
    set_target_lang(interface, target_lang=lang)
    print(f"[aura_state] Language set to '{lang}' for '{interface}'")


def get_current_language(interface='speech'):
    """Get current target language for a specific interface."""
    return get_target_lang(interface)


def is_translation_enabled(interface='speech'):
    """Check if translation is enabled for a specific interface."""
    return get_feature_state(interface, feature='translation') == 'on'


def get_interface_status(interface='speech'):
    """Get full status for a specific interface."""
    return {
        'interface': interface,
        'translation': get_feature_state(interface, feature='translation'),
        'language': get_target_lang(interface),
    }


def get_all_status():
    """Get full status for all interfaces."""
    return [get_interface_status(i) for i in INTERFACES]

def ensure_fuzzy_map_in_sync(interface='speech'):
    """
    Ensures FUZZY_MAP_pre.py translation rule matches Trino state.
    Called at startup and after Admin UI changes.
    """
    import re
    from pathlib import Path

    RULES_FILE_PATH = Path(__file__).parents[4] / \
        'config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py'
    RULE_ANCHOR = '# TRANSLATION_RULE'

    if not RULES_FILE_PATH.exists():
        print(f"[aura_state] WARNING: FUZZY_MAP_pre.py not found at {RULES_FILE_PATH}")
        return

    should_be_active = is_translation_enabled(interface)

    lines = RULES_FILE_PATH.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if RULE_ANCHOR in line:
            rule_line_index = i + 1
            if rule_line_index >= len(lines):
                break
            is_active = not lines[rule_line_index].strip().startswith('#')

            if should_be_active and not is_active:
                # activate
                lines[rule_line_index] = lines[rule_line_index].replace('#', '', 1)
                RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
                print(f"[aura_state] FUZZY_MAP rule ACTIVATED for interface={interface}")
            elif not should_be_active and is_active:
                # deactivate
                lines[rule_line_index] = re.sub(r'^(\s*)(.*)', r'\1#\2', lines[rule_line_index])
                RULES_FILE_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
                print(f"[aura_state] FUZZY_MAP rule DEACTIVATED for interface={interface}")
            else:
                print(f"[aura_state] FUZZY_MAP already in sync for interface={interface}")
            break



if __name__ == '__main__':
    print("=== Aura State ===")
    for status in get_all_status():
        lang = status['language'] or '-'
        print(f"  {status['interface']:10} | translation: {status['translation']:3} | lang: {lang}")

    print()
    print("=== Test: enable speech/en ===")
    enable_translation('speech', lang='en')
    print(f"  is_translation_enabled('speech'): {is_translation_enabled('speech')}")
    print(f"  get_current_language('speech'):   {get_current_language('speech')}")

    print()
    print("=== Test: disable speech ===")
    disable_translation('speech')
    print(f"  is_translation_enabled('speech'): {is_translation_enabled('speech')}")
