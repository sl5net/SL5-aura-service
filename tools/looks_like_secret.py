# tools/looks_like_secret.py
"""
Detects if a string looks like a password, token, hash or secret.
Used to prevent translation of sensitive data.
"""
import re

def looks_like_secret(text: str) -> bool:
    t = text.strip()

    # Too short to be a secret
    if len(t) < 8:
        return False

    # No spaces and long = likely a token/hash
    if len(t) >= 8 and ' ' not in t:
        has_upper = bool(re.search(r'[A-Z]', t))
        has_lower = bool(re.search(r'[a-z]', t))
        has_digit = bool(re.search(r'[0-9]', t))
        has_special = bool(re.search(r'[!@#$%^&*\-_+=/\\]', t))
        score = sum([has_upper, has_lower, has_digit, has_special])
        if score >= 3:
            return True

    # Hex hash (md5, sha1, sha256 etc.)
    if re.fullmatch(r'[0-9a-fA-F]{16,}', t):
        return True

    # Base64-like
    if re.fullmatch(r'[A-Za-z0-9+/=]{20,}', t) and '=' in t:
        return True

    # JWT token (three base64 parts separated by dots)
    if re.fullmatch(r'[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+', t):
        return True

    # API key patterns: prefix_randomstring
    if re.fullmatch(r'[a-z]{2,10}_[A-Za-z0-9]{16,}', t):
        return True

    return False


if __name__ == '__main__':
    tests = [
        ("hallo wie geht es dir", False),
        ("P@ssw0rd!123XyZ", True),
        ("sk_live_abc123DEF456ghi789", True),
        ("5f4dcc3b5aa765d61d8327de", True),
        ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.abc123", True),
        ("aGVsbG8gd29ybGQ=", True),
        ("normal sentence here", False),
    ]

    passed = 0
    for text, expected in tests:
        result = looks_like_secret(text)

        if result == expected:
            print(f"✅ PASS: '{text[:30]}...' -> {result}")
            passed += 1
        else:
            print(f"❌ FAIL: '{text[:30]}...' | expected: {expected}, result: {result}")

    print(f"\nresult: {passed}/{len(tests)} .")

