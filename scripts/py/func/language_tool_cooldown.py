# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
"""Cooldown state manager for LanguageTool under memory pressure."""

import time

_lt_disabled_until: float = 0.0


def set_language_tool_cooldown(duration_seconds: float = 300.0) -> None:
    """Activate cooldown to prevent LanguageTool from restarting."""
    global _lt_disabled_until
    _lt_disabled_until = time.time() + duration_seconds


def is_language_tool_in_cooldown() -> bool:
    """Check if LanguageTool is currently blocked by memory cooldown."""
    return time.time() < _lt_disabled_until


def get_language_tool_cooldown_remaining() -> float:
    """Return remaining seconds in cooldown."""
    return max(0.0, _lt_disabled_until - time.time())
