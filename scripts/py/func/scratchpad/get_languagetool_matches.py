from typing import Any, Dict, List
import requests


def get_languagetool_matches(
    server_url: str,
    language: str,
    text: str,
    max_suggestions: int = 5,
    timeout: float = 6.0,
) -> List[Dict[str, Any]]:
    """
    Queries LanguageTool API and returns normalized matches for suggestions.
    """
    if not text or not text.strip() or not server_url:
        return []
    base_url = server_url.rstrip("/")
    if base_url.endswith("/v2"):
        check_url = f"{base_url}/check"
    elif not base_url.endswith("/v2/check"):
        check_url = f"{base_url}/v2/check"
    else:
        check_url = base_url
    payload = {
        "language": language,
        "text": text,
        "maxSuggestions": max_suggestions,
    }
    try:
        with requests.Session() as session:
            resp = session.post(check_url, data=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []
    normalized = []
    for m in data.get("matches", []):
        offset = int(m.get("offset", 0))
        length = int(m.get("length", 0))
        replacements = [
            r.get("value")
            for r in m.get("replacements", [])
            if isinstance(r, dict) and r.get("value")
        ]
        normalized.append(
            {
                "offset": offset,
                "length": length,
                "word": text[offset : offset + length],
                "message": m.get("message", ""),
                "rule_id": m.get("rule", {}).get("id", ""),
                "replacements": replacements[:max_suggestions],
            }
        )
    return normalized

