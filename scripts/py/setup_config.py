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



if default_primary == "de":
    text_detected = f"Region erkannt: {country} | Vorschlag: {default_primary}"
    text_help = "Sprachcode wählen oder 'n' für Terminal-Modus (Keine Sprachen)."
    prompt_p = "Primäre Sprache (de, en... oder 'n' für nein, keine Sprache) - automatische Bestätigung in 8 Sekunden"
    prompt_s = "Sekundäre Sprache (oder 'none' Default) - automatische Bestätigung in 8 Sekunden"
    sys.stderr.write("Drücken Sie die Eingabetaste zur Bestätigung oder geben Sie einen anderen Sprachcode ein.\n")
else:
    text_detected = f"Region detected: {country} | Suggested: {default_primary}"
    text_help = "Select language or type 'n' for Terminal Mode (No Langs)."
    prompt_p = "Primary Lang (de, en, etc. or 'n') - auto-confirms in 8s"
    prompt_s = "Primary Language (de, en, etc. or 'n' for none) - auto-confirms in 8s"
    sys.stderr.write("Press Enter to confirm, or type a different language code.\n")

sys.stderr.write(f"{text_detected}\n{text_help}\n")

primary = timed_input(prompt_p, default_primary)

if primary in ["n", "none", "0"]:
    # If terminal mode is selected, we exclude all languages
    secondary = "none"
    excludes_str = "all"

else:

    secondary = timed_input(prompt_s, "none")

    all_langs = ["de", "en", "fr", "es"]
    excludes = [lang for lang in all_langs if lang != primary and lang != secondary]

    excludes_str = ",".join(excludes)

print(f"export SELECTED_LANG='{primary}'")
print(f"export SECOND_LANG='{secondary}'")
print(f"export EXCLUDE_LANGUAGES='{excludes_str}'")
