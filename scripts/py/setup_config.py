import urllib.request
import sys
import select

def get_country():
    try:
        with urllib.request.urlopen("https://ipapi.co/country/", timeout=2) as response:
            return response.read().decode().strip()
    except Exception as e:
        return f"Unknown{e}"

def timed_input(prompt, default, timeout=8):
    sys.stderr.write(f"{prompt} [{default}]: ")
    sys.stderr.flush()
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        res = sys.stdin.readline().strip()
        return res if res else default
    sys.stderr.write("\n")
    return default

country = get_country()
default_primary = "de" if country in ["DE", "AT", "CH"] else "en"

# sys.stderr.write(f"Region: {country} | Default: {default_primary}\n")

sys.stderr.write(f"Region detected: {country} | Suggested language: {default_primary}\n")
sys.stderr.write("Press Enter to confirm, or type a different language code.\n")

primary = timed_input("Primary Language (de, en, etc. or 'n' for none) - auto-confirms in 8s", default_primary)

if primary in ["n", "none", "0"]:
    # If terminal mode is selected, we exclude all languages
    secondary = "none"
    excludes_str = "all"

else:

    secondary = timed_input("Secondary Language (or 'none') - auto-confirms in 8s", "none")

    all_langs = ["de", "en", "fr", "es"]
    excludes = [lang for lang in all_langs if lang != primary and lang != secondary]

    excludes_str = ",".join(excludes)

print(f"export SELECTED_LANG='{primary}'")
print(f"export SECOND_LANG='{secondary}'")
print(f"export EXCLUDE_LANGUAGES='{excludes_str}'")
