"""Loop protection for the bidirectional Element <-> Threema relay.

Everything the relay forwards (in either direction) is remembered for a short
time. A text that shows up again within that window is an echo of our own
forwarding and must not be forwarded back.
"""
import time
from typing import Callable, Dict, Optional


def normalize_text(text: Optional[str]) -> str:
    """Pure function: collapse all whitespace so GUI copy artefacts do not matter."""
    if not text:
        return ""
    return " ".join(text.split())


class RelayHistory:
    """Remember forwarded texts for `ttl_seconds` (injectable clock for tests)."""

    def __init__(
        self,
        ttl_seconds: float = 180.0,
        max_entries: int = 200,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._ttl = ttl_seconds
        self._max = max_entries
        self._clock = clock
        self._seen: Dict[str, float] = {}

    def _purge(self) -> None:
        now = self._clock()
        expired = [k for k, ts in self._seen.items() if now - ts > self._ttl]
        for key in expired:
            del self._seen[key]
        while len(self._seen) > self._max:
            del self._seen[next(iter(self._seen))]

    def remember(self, text: Optional[str]) -> None:
        key = normalize_text(text)
        if key:
            self._seen.pop(key, None)
            self._seen[key] = self._clock()
            self._purge()

    def knows(self, text: Optional[str]) -> bool:
        self._purge()
        return normalize_text(text) in self._seen
