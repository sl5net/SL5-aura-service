import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote, urlparse
import logging, inspect, os, sys
from rapidfuzz import fuzz

"""
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

ZIM_FILE_NAME = "wikipedia_de_all_mini_2025-09.zim"
BASE_SERVER_URL = "http://localhost:8080"
ZIM_URL_PART = ZIM_FILE_NAME.replace('.zim', '')
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

            # --- VERBESSERTE LOGIK START ---
            is_better = False
            current_len = len(link_text)
            # Länge des aktuell besten Treffers (Unendlich, falls noch kein Treffer da ist)
            best_len = len(best_link_text) if best_link_text is not None else float('inf')

            if score > best_score:
                # 1. Neue beste Punktzahl gefunden
                is_better = True
            elif score == best_score:
                # 2. Gleiche Punktzahl: Kürzere Texte bevorzugen (Tie-breaker)
                if current_len < best_len:
                    is_better = True

            if is_better:
                best_score, best_href, best_link_text = score, href, link_text
            # --- VERBESSERTE LOGIK ENDE ---

            if best_score == 100:
                break
        if best_href:
            log_debug(f"href:{best_href} ({best_link_text}) score={best_score}")
            # http://localhost:8080/content/wikipedia_de_all_mini_2025-09/Evangelisches_Krankenhaus


            # Kiwix-Serve gibt Pfade meist mit /content/... zurück
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
        # Exakter Match – immer bevorzugt!
        if link_text == normalized_search or (title_attr and title_attr.lower().replace("_", " ") == normalized_search):
            if title_attr and "#" not in title_attr:
                log_debug(f"Exakter interner Link (durch Fließtext): {title_attr}")
                return title_attr
            return link_text
    # Fuzzy, falls kein exakter Treffer gefunden wurde:
    best_score = -1
    best_title = None
    for link in main_content.find_all('a', href=True, title=True):
        title = link.get('title')
        if title and "#" not in title:
            score = fuzz.WRatio(user_term.lower(), title.lower())
            #log_debug(f"[internal link] {title} -- score {score}")
            if score > best_score:
                best_score, best_title = score, title
    if best_score >= threshold:
        return best_title
    return None

def _construct_article_url(article_title: str) -> str:
    encoded_title = quote(article_title)
    return f"{BASE_SERVER_URL}/{ZIM_URL_PART}/{encoded_title}"

def execute(match_data):
    log_debug("--- START of EXECUTE ---")
    user_term = match_data['regex_match_obj'].group(2).strip()
    log_debug(f"original_search_term={user_term}")

    # 1. Strategie: NUR das erste Wort Suchen, dann die besten Treffer auf den vollen Query fuzzy-mappen!
    first_word = user_term.split()[0]
    article_path = _find_best_article_path_via_http_fuzzy(first_word, user_term, ZIM_FILE_NAME)
    if not article_path:
        return f"No articles found for search term: '{user_term}'"
    server_article_url = f"{BASE_SERVER_URL}{article_path}"
    log_debug(f"{server_article_url}")

    # 2. Artikel laden
    response = requests.get(server_article_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    current_article_title = unquote(article_path.split('/')[-1])
    user_term_norm = user_term.lower().replace("_", " ").strip()

    # 3. Max 2 Sprünge: Gibt es einen besseren internen Link für den originalen User-Query?
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
            # harter Break, wenn exakter Titel-Match gefunden wurde
            if redirect_target_title.lower().replace("_", " ") == user_term_norm:
                break
        else:
            break


    article_text_parts = []
    if soup.find('body'):
        paragraphs = soup.find('body').find_all('p')
        article_text_parts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
    full_article_text = "\n\n".join(article_text_parts)
    clean_article_text = ' '.join(full_article_text.split())
    return clean_article_text

class DummyMatch:
    def __init__(self, group2_value): self._group2_value = group2_value
    def group(self, index): return self._group2_value if index == 2 else None

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
