# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/standard_actions/wikipedia_local/de-DE/wikipedia_local.py

# wikipedia_local.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import logging
import inspect
import os
import sys
from rapidfuzz import fuzz

import subprocess
import socket


"""

sudo systemctl start docker
sudo systemctl enable --now docker.socket
http://localhost:8080/viewer#wikipedia_de_all_mini_2025-09/Automobil

Findet leider nur

"Python Programmiersprache",  # → Python (Programmiersprache) direkt
"Krankenhaus Jülich" # → findet "Krankenhaus Jülich", kann

gesucht wird:
"krankenhaus",    # → Krankenhaus (nach zwei Schritten)
Bei der Suche nach Krankenhaus ist der fuzzy Match nicht ausreicend, weil er solte kürzere bevorzugen, bei gleicher Wertung. Z.B. Krankenhaus Jülich ist kürzer als Krankenhaus Bergisch Gladbach

"python",         # → Python (Programmiersprache) direkt
"Python Programmiersprache",  # → Python (Programmiersprache) direkt per fuzzy
"Krankenhaus Jülich" # → findet "Krankenhaus Jülich", kann

"""

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702


ZIM_FILE_NAME = SL5NET_AURA_PROJECT_ROOT / 'data' / 'wikipedia_de_all_mini.zim'
ZIM_URL_PART = ZIM_FILE_NAME.name.replace('.zim', '')
BASE_SERVER_URL = "http://localhost:8080"
LOG_FILE = os.path.expanduser("~/kiwix_debug.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_debug(message: str):
    caller_info = "UNKNOWN:0"
    stack = inspect.stack()
    if len(stack) > 1:
        try:
            filename = os.path.basename(stack[1].filename)
            line_number = stack[1].lineno
            caller_info = f"{filename}:{line_number}"
        except Exception:
            pass
    print(f"[DEBUG] {caller_info}: {message}", file=sys.stderr)

def _find_best_article_path_via_http_fuzzy(api_term: str, user_term: str, zim_file: str) -> str | None:
    """
    1. Suche mit erstem Wort (api_term) via kiwix-serve.
    2. Fuzzy-matche die Treffer gegen den **vollen** Query (user_term).
    3. Gib besten Treffer zurück.
    """

    search_url = f"{BASE_SERVER_URL}/search?pattern={quote(api_term)}&book={zim_file}"
    log_debug(f"search_url: {search_url}")
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        result_links = soup.select("div.results ul li a")
        if not result_links:
            return None
        best_score = -1
        best_href = None
        best_link_text = None
        for link in result_links:
            link_text = link.get_text().strip()
            href = link.get('href')
            score = fuzz.WRatio(user_term.lower(), link_text.lower())

            # --- IMPROVED LOGIC START ---

            is_better = False
            current_len = len(link_text)
            # Length of the current best hit (infinity if there is no hit yet)

            best_len = len(best_link_text) if best_link_text is not None else float('inf')

            if score > best_score:
                # 1. New best score found

                is_better = True
            elif score == best_score:
                # 2. Same score: Prefer shorter texts (tie-breaker)

                if current_len < best_len:
                    is_better = True

            if is_better:
                best_score, best_href, best_link_text = score, href, link_text
            # --- IMPROVED LOGIC END ---


            if best_score == 100:
                break
        if best_href:
            log_debug(f"href:{best_href} ({best_link_text}) score={best_score}")
            # http://localhost:8080/content/wikipedia_de_all_mini_2025-09/Evangelisches_Krankenhaus



            # Kiwix-Serve usually returns paths with /content/...

            return best_href if best_href.startswith("/") else f"/{best_href}"
        return None
    except requests.exceptions.RequestException as e:
        log_debug(f"ERROR: Kiwix-Serve not running or bad request: {e}")
        return None

def _find_better_internal_link(soup, user_term, threshold=95):
    """
    Fuzzy/präzise Suche: Gibt Linktitel zurück, wenn ein Link-Text/Titel besser oder gleich (thr) zu user_term passt.
    Zuerst exakter (case/lower) Vergleich, sonst Fuzzy.
    """
    normalized_search = user_term.lower().replace("_", " ").strip()
    main_content = soup.find("div", class_="mw-parser-output") or soup.find("body")
    if not main_content:
        return None
    for link in main_content.find_all('a', href=True):
        link_text = link.get_text().strip().lower().replace("_", " ")
        title_attr = link.get('title')
        # Exact match – always preferred!

        if link_text == normalized_search or (title_attr and title_attr.lower().replace("_", " ") == normalized_search):
            if title_attr and "#" not in title_attr:
                log_debug(f"Exakter interner Link (durch Fließtext): {title_attr}")
                return title_attr
            return link_text
    # Fuzzy if no exact match was found:

    best_score = -1
    best_title = None
    for link in main_content.find_all('a', href=True, title=True):
        title = link.get('title')
        if title and "#" not in title:
            score = fuzz.WRatio(user_term.lower(), title.lower())
            # log_debug(f"[internal link] {title} -- score {score}")

            if score > best_score:
                best_score, best_title = score, title
    if best_score >= threshold:
        return best_title
    return None

def _construct_article_url(article_title: str) -> str:
    encoded_title = quote(article_title)
    return f"{BASE_SERVER_URL}/{ZIM_URL_PART}/{encoded_title}"



def is_kiwix_reachable():
    """Prüft ob Kiwix läuft (ohne Docker-Befehle)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        return result == 0
    except Exception as e:
        print(e)
        return False

def start_kiwix():
    """Startet Kiwix wenn nicht läuft"""
    if not is_kiwix_reachable():
        # This should work out of the box!

        subprocess.Popen([
            'bash',
            'config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh'
        ])
        return "Kiwix wird gestartet…"
    return "Kiwix läuft bereits"

def execute(match_data):
    log_debug("--- START of EXECUTE ---")

    if not is_kiwix_reachable():
        start_kiwix()

    user_term = match_data['regex_match_obj'].group('search').strip()
    user_term_norm = user_term.lower().replace("_", " ").strip()

    # (zsh ä→ae, ö→oe, ü→ue)

    user_term_norm = (user_term_norm
                      .replace("ae", "ä")
                      .replace("oe", "ö")
                      .replace("ue", "ü")
                      .replace("ss", "ß"))





    log_debug(f"original_search_term={user_term}")

    # 1st strategy: ONLY search the first word, then the best hits on the full query fuzzy map!

    first_word = user_term.split()[0]

    # there is a company in history with real name auto but ... we don't want search for this here probably

    if first_word == 'auto':
        first_word = 'automobil'


    sebastian_lauffer_NAMES = {
        'sebastian',
        'sebastian lauffer',
        'sebastian laufer',
        'sebastian lau',
        'sebastian lauf',
        'sebastian laufen',
        'sebastian darauf',
        'sebastian laufe',
        'sebastian now'
    }

    Schroer_Ergotherapie_NAMES = {
        'Herr Schröer',
        'Ergotherapie',
        'Schröer',
        'Ralf Schröer',
        'Ralf Scharrer',
        'Ergotherapeut',
        'Schröer',
        'Ergotherapie',
        'Schröer',
        'Ergotherapie'
    }
    # config/maps/plugins/standard_actions/wikipedia_local/de-DE/wikipedia_local.py:220

    search_term = user_term_norm

    full_summary = ''
    if search_term=='Steuerhinterziehung'.lower() or search_term=='Steuer'.lower() or search_term=='hinterziehung' or search_term=='betrug':

        full_summary = """
100 Milliarden Euro, das ist der geschätzte Schaden, der durch
Steuerhinterziehung jedes Jahr in Deutschland entsteht, jedes Jahr aufs Neue.
Das sind 270 Millionen Euro pro Tag, 11 Millionen Euro pro Stunde.
Und während ich euch hier das erzähle, sind schon wieder 100.000 € verschwunden. ( Rede von Anne Brorhilker in der re-publica 2025 )
"""
# https://www.youtube.com/watch?v=ZDQZTHre0Go

        return full_summary


# 100 billion euros, that is the estimated damage caused by tax evasion in Germany every year, every year. That's 270 million euros per day, 11 million euros per hour. And while I'm telling you this, another €100,000 has disappeared. (Speech by Anne Brorhilker in publica 2025) 100 billion euros, that is the estimated damage caused by tax evasion in Germany every year, every year. That's 270 million euros per day, 11 million euros per hour. And while I'm telling you this, another 100,000 euros have disappeared. (Speech by Anne Brorhilker in re-publica 2025)


    if search_term=='Harald'.lower() or search_term=='Harald Uetz'.lower() or search_term=='Harald Uhd'.lower():
        full_summary = """
Harald Uetz ist ein deutscher Schachspieler.
Harald Uetz hat 2025, mit seinem zweiten Platz, gleich hinter Lauffer, in der FIDE-Weltrangliste, unter anderem die Weltmeister Ding Liren und Viswanathan Anand oder den zweifachen Vizeweltmeister Ian Nepomniachtchi hinter sich gelassen.
Laut Wikipedia: Harald Uetz, mit seinem zweiten Platz, gleich hinter Lauffer, in der Weltrangliste, hat Uetz unter anderem die Weltmeister Ding Liren und Viswanathan Anand oder den zweifachen Vizeweltmeister Ian Nepomniachtchi hinter sich gelassen.
(fun-fake msg, 4.12.'2510:07 Thu)
"""
    # Herr ist eine Form der Anrede für Männer. Ursprünglich war Herr eine Standesbezeichnung und ein Herrschaftstitel, siehe Herr (Titel). ( http://localhost:8080/content/wikipedia_de_all_mini_2025-09/Herr_(Begriffskl%C3%A4rung) )


    elif 'Beste Schachspieler'.lower() in search_term:
        full_summary = """Sebastian Lauffer aus Wannweil (fun-fake msg, 4.12.'25)"""

    elif search_term.lower() in Schroer_Ergotherapie_NAMES:
        full_summary="""
Herr Schröer ist ein netter, bisschen vergesslicher, Ergotherapeut. 
        """
        return full_summary

    elif search_term.lower() in sebastian_lauffer_NAMES:

        full_summary="""

Sebastian Lauffer ist ein deutscher Diplom-Wirtschaftsinformatiker, Softwareentwickler und Coach.
 Er ist bekannt für seine Arbeit im Open-Source-Bereich und die Entwicklung des Einrückungsstils „SL5small“ (September 2017). Lauffer verbindet in seiner Tätigkeit Softwareentwicklung mit Coaching. Seit 2001 unterrichtet er diverse Programmiersprachen. Als Gründer von SL5.de entwickelt er datenschutzfreundliche Open-Source-Software wie das Voice-Framework „SL5 Aura“.

 <ref>{{Internetquelle |url=https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil |titel=Wikipedia-Archiv: Einrückungsstil#SL5small-Stil |abruf=2017-12-29}}</ref>

 == Wirken ==
 Lauffer verbindet in seiner Tätigkeit Softwareentwicklung mit Coaching. Seit 2001 unterrichtet er diverse Programmiersprachen. Als Gründer von SL5.de entwickelt er datenschutzfreundliche Open-Source-Software wie das Voice-Framework „SL5 Aura“.


 Sebastian Lauffer hat zwischen 1991 und 1994 in seiner Freizeit PC-Spiele mit seinem Vater ein Spiel entwickelt.

 Spiel mit 13 jahren entwickelt:
 Nachbau in JS: http://sl5.net/helper/js/paperscript/2p_r_13-09-03_23-52.html )
 Nachbau in JS: https://www.youtube.com/watch?v=mIOnWFNfkPk )



== SL5small-Stil ==
 Der von Lauffer entwickelte '''SL5small-Stil''' ist ein platzsparender Einrückungsstil, der ursprünglich für die Skriptsprache AutoHotkey konzipiert wurde. Anstatt schließende Klammern jeweils in eine neue Zeile zu setzen, werden sie gesammelt am Ende des Blocks platziert, ähnlich wie in Lisp.<ref>{{Internetquelle |url=https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil |titel=Wikipedia-Archiv: Einrückungsstil#SL5small-Stil |abruf=2017-12-29}}</ref>

 Seite „Einrückungsstil“. In: Wikipedia – Die freie Enzyklopädie. Bearbeitungsstand: 8. September 2017, 10:59 UTC. URL: Wikipedia archive.org Einrückungsstil#SL5small-Stil https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil (Abgerufen: 29. 12 2017, 20:01 UTC)

Weblinks

- http://ahkscript.org/boards/viewtopic.php?t=8678
- http://sl5.it/SL5_preg_contentFinder/examples/AutoHotKey/converts_your_autohotkey_code_into_pretty_indented_source_code.php
- Wikipedia Einrückungsstil#SL5small-Stil https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil

        """

        SL5smallStil = """  # noqa: F841
SL5small-Stil

Der SL5small-Stil wurde im ersten online Code-Prettifier für die Script-Sprache Autohotkey implementiert (converts_your_autohotkey_code_into_pretty_indented_source_code).

Anstatt z.B.:

if(doIt1)
{
if(doIt2)
{
if ( next )
{
    Send,5b{Right 5}
}
}
}

wird

if(doIt1) {
if(doIt2) {
if(next)
{
    Send,5b{Right 5}
}}}

notiert.

Dieser Stil ist ähnlich Einrückungen wie sie in Lisp üblich sind. Der Vorteil dieses Stils ist, dass, insbesondere bei wachsender Einrückungstiefe, viel Platz eingespart wird. Ein Nachteil ist dass ohne die Verwendung moderner Editoren man sich leichter verzählen kann, was die Anzahl der geschlossenen Klammern angeht.

Weblinks

- http://ahkscript.org/boards/viewtopic.php?t=8678
- http://sl5.it/SL5_preg_contentFinder/examples/AutoHotKey/converts_your_autohotkey_code_into_pretty_indented_source_code.php
- Wikipedia Einrückungsstil#SL5small-Stil https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil


Bibliografische Angaben für „Einrückungsstil“

Seitentitel: Einrückungsstil
Herausgeber: Wikipedia – Die freie Enzyklopädie.
Autor(en): Wikipedia-Autoren, siehe Versionsgeschichte
Datum der letzten Bearbeitung: 8. September 2017, 10:59 UTC
Versions-ID der Seite: 257156317
Permanentlink: https://web.archive.org/web/20171229200102/https:/de.wikipedia.org/wiki/Einr%C3%BCckungsstil#SL5small-Stil
Datum des Abrufs: 29. 12 2017, 20:01 UTC
        """
    # config/maps/plugins/standard_actions/wikipedia_local/de-DE/wikipedia_local.py:338

    if not full_summary:
        article_path = _find_best_article_path_via_http_fuzzy(first_word, user_term, ZIM_FILE_NAME)

    if full_summary:
        return full_summary




    if not article_path:
        msg = f"""
        
        f"
        Please Try Again in a Second 🔂. 
        
        Server may need to restart for several reasons, 
        including applying updates, 
        changing configurations, 
        or ... etc. 
        
        ---
        
        No articles found for search term: '{user_term}'"
        Maybe run ?
        ---

        Maybe want enable ?
        ./config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh

        

        """

        # source .venv/bin/activate

        # python3 config/maps/plugins/standard_actions/wikipedia_local/de-DE/wikipedia_local.py


        return msg
































    server_article_url = f"{BASE_SERVER_URL}{article_path}"
    log_debug(f"{server_article_url}")

    # 2. Load article

    response = requests.get(server_article_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    current_article_title = unquote(article_path.split('/')[-1])

    # 3. Max 2 jumps: Is there a better internal link for the original user query?

    for i in range(2):
        redirect_target_title = _find_better_internal_link(soup, user_term, threshold=90)
        log_debug(f"Sprung {i} {redirect_target_title}, current: {current_article_title}")
        if redirect_target_title and redirect_target_title.lower().replace("_", " ") != current_article_title.lower().replace("_", " "):
            new_url = _construct_article_url(redirect_target_title)
            log_debug(f"{new_url}")

            # --- PATCH: check if fetch works ---

            try:
                response = requests.get(new_url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                log_debug(f"({e}) -- {redirect_target_title} -- skip to next candidate")
                break  # (oder: continue zu next-best-candidate, falls du mehrere ausprobieren willst)
            log_debug(f"Wechsle zu besserem Link: {redirect_target_title} -> {new_url}")
            current_article_title = redirect_target_title
            soup = BeautifulSoup(response.content, 'html.parser')
            # hard break when exact title match is found

            if redirect_target_title.lower().replace("_", " ") == user_term_norm:
                break
        else:
            break

    clean_article_text = extract_structured_text(soup)
    return f"{clean_article_text} ( {BASE_SERVER_URL}{article_path} )"



    article_text_parts = []
    if soup.find('body'):
        paragraphs = soup.find('body').find_all(['p', 'li'])
        article_text_parts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

    full_article_text = "\n\n".join(article_text_parts)



    clean_article_text = ' '.join(full_article_text.split())
    return f"{clean_article_text} ({article_path})"


def extract_structured_text(soup):
    """
    Extrahiert den Text aus <p>- und <li>-Tags, wobei Listen-Elemente
    mit einem Zeilenumbruch und einem führenden ' - ' formatiert werden.
    """

    if not soup.find('body'):
        # Handles the case where no body tag is found

        return ""

    body = soup.find('body')
    article_text_parts = []

    # Loop through all direct child elements that might have textual content

    # (e.g. <p>, <ul>, <ol>, <h1>, etc.). But we're just concentrating here

    # the elements containing p or ul/ol/li, as in the previous example.


    # NEW: We search for all p tags and all ul/ol tags in the body

    # text_containers = body.find_all(['p', 'ul', 'ol'], recursive=False)

    # 'recursive=False' can be useful to get only the top level containers.

    # For Wikipedia, searching without 'recursive=False' is often better, but we

    # need to carefully find all p and li tags within the body.



    # A safer method is to find all p and li tags and then process them:

    for element in body.find_all(['p', 'li']):
        text = element.get_text().strip()

        if not text:
            continue

        # If it is a list element (<li>)

        if element.name == 'li':
            # Add it with a new line and a hyphen to indicate the list structure

            # We use '\n - ' here to make sure it starts on a new line

            article_text_parts.append(f"\n| ★ {text} \n")

        # If it is a paragraph element (<p>)

        elif element.name == 'p':
            # Add it like a normal paragraph. '\n\n' serves as a separator between paragraphs

            # Since we'll be splitting and joining everything later, it's better to just do it at first

            # as clean text and handle the separation later.

            article_text_parts.append(text)


    # STEP 1: Assemble the pieces using the desired separator

    # Here we use '\n\n' between all collected parts.

    # Important: The <li> parts already contain a '\n - ', so this is taken into account.

    full_text_with_structure = "\n\n".join(article_text_parts)

    # STEP 2: Final cleanup to remove excess spaces in the text,

    # BUT keep the list structure.


    # We want to preserve line breaks (especially those of lists).

    # Therefore, we use a slightly different cleanup strategy:


    # 1. Remove unnecessary whitespace within the text lines

    cleaned_lines = []
    for line in full_text_with_structure.splitlines():
        # Remove multiple spaces with a single space on the line

        cleaned_line = ' '.join(line.split()).strip()
        if cleaned_line: # Nur nicht-leere Zeilen behalten
            cleaned_lines.append(cleaned_line)

    # 2. Put the lines back together. This leaves the list formatting intact

    # (e.g. '\n - ...').

    clean_article_text = "\n".join(cleaned_lines)

    return clean_article_text

class DummyMatch:
    def __init__(self, group2_value):
        self._group2_value = group2_value
    def group(self, index):
        return self._group2_value if index == 2 else None

if __name__ == '__main__':
    for test_term in [
        "krankenhaus",    # → Krankenhaus (nach zwei Schritten)
        "Python Programmiersprache",  # → Python (Programmiersprache) direkt per fuzzy
    ]:
        dummy_match_obj = DummyMatch(group2_value=test_term)
        test_match_data = {'regex_match_obj': dummy_match_obj}
        print("-" * 50)
        print(f"TEST: {test_term}")
        print(execute(test_match_data))
        print("-" * 50)
