# scripts/py/func/db/aura_state.py
"""
High-level API for Aura state management.
Readable interface for developers — wraps trino_client.py low-level operations.

Usage:
    from scripts.py.func.db.aura_state import enable_translation, disable_translation, get_interface_status
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[4]))

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
