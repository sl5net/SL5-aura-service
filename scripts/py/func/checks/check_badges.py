# STT/scripts/py/func/checks/check_badges.py
import re
import sys
import requests

def find_badge_urls(content):
    """Finds all GitHub Actions badge URLs in the README content."""
    # This pattern looks for ![...](https://github.com/.../badge.svg)
    pattern = re.compile(r'https://github\.com/.*?/badge\.svg')
    return set(pattern.findall(content))

def check_badge_status(url):
    """
    Checks a single badge URL.
    Returns 'passing', 'failing', or 'broken_link'.
    """
    try:
        response = requests.get(url, timeout=10)

        # If the URL is wrong, the link is broken
        if response.status_code != 200:
            return 'broken_link'

        svg_text = response.text.lower()

        # This is how we check if the badge is RED
        if 'failing' in svg_text or 'failed' in svg_text:
            return 'failing'

        # This is how we check if the badge is GREEN
        if 'passing' in svg_text:
            return 'passing'

        # Any other status (like 'in progress') is treated as a problem
        return 'unknown'

    except requests.exceptions.RequestException:
        return 'network_error'

def check_badges(SCRIPT_DIR):
    """Main function to run the badge checks."""
    try:
        with open(f'{SCRIPT_DIR}/README.md' , encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: Cannot find the file.")
        sys.exit(1)

    urls = find_badge_urls(readme_content)
    if not urls:
        print("No GitHub badges found in README.md.")
        return


    print("--- Checking README Badges ---")
    found_red_badge = False

    for url in sorted(list(urls)):
        workflow_name = url.split('/workflows/')[1].split('/badge.svg')[0]
        status = check_badge_status(url)

        if status == 'passing':
            print(f"✅ GREEN: {workflow_name}")
        else:
            # Any status other than 'passing' is a problem
            found_red_badge = True
            if status == 'failing':
                print(f"🚨  RED:  {workflow_name} --- BUILD IS FAILING!")
            elif status == 'broken_link':
                print(f"🚨  RED:  {workflow_name} --- BROKEN LINK!")
            else:
                print(f"🚨  RED:  {workflow_name} --- UNKNOWN STATUS OR NETWORK ERROR!")

    print("------------------------------")
    if found_red_badge:
        print("\n❌ A badge is RED. Please check your repository.")
        print("\n❌ A badge is RED. Please check your repository.")
        print("\n❌ A badge is RED. Please check your repository.")
        print("\n❌ A badge is RED. Please check your repository.")
        # sys.exit(1) # Exit with an error code
    else:
        print("\n✅ All badges are GREEN.")
        # sys.exit(0) # Exit with a success code

if __name__ == '__main__':
    check_badges()

