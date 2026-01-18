# tools/debug_lt_client.py
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
import requests
import sys

def test_lt_connection():
    url = "http://localhost:8082/v2/check"
    text = "der hausbau im wald ist nicht erlaubt"

    print(f"--- DEBUG: Testing LanguageTool Client ---")
    print(f"Target URL: {url}")
    print(f"Input Text: {text}")

    data = {
        'text': text,
        'language': 'de-DE',
        'enabledOnly': 'false'
    }

    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            matches = result.get('matches', [])
            print(f"Matches found: {len(matches)}")
            for match in matches:
                print(f" - Rule: {match['rule']['id']}")
                print(f" - Message: {match['message']}")
                print(f" - Replacements: {[r['value'] for r in match['replacements']]}")
        else:
            print(f"ERROR: Server returned {response.text}")

    except requests.exceptions.ConnectionError:
        print("CRITICAL: Connection Refused. Python cannot reach localhost:8082.")
        print("Possibilities: Firewall blocking Python, or IPv4/IPv6 mismatch (localhost vs 127.0.0.1).")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_lt_connection()
