import re


def detect_source_language(text: str, default: str = "en") -> str:
    if re.search(r"[äöüßÄÖÜ]", text):
        return "de"

    german_matches = len(
        re.findall(r"\b(und|der|die|das|nicht|für|mit|von|eine|eines|über)\b", text, re.IGNORECASE)
    )
    english_matches = len(
        re.findall(r"\b(and|the|is|for|with|from|your|this|that|have)\b", text, re.IGNORECASE)
    )

    if german_matches > english_matches:
        return "de"
    return default
