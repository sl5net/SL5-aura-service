import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import re,sys
#from collections import namedtuple
from urllib.parse import urlparse




# --- CONFIGURATION (Ensure these paths match your setup) ---
ZIM_FILE_NAME = "wikipedia_de_all_mini_2025-09.zim"
BASE_SERVER_URL = "http://localhost:8080"
ZIM_URL_PART = ZIM_FILE_NAME.replace('.zim', '')


# --- END CONFIGURATION ---

# The existing functions _find_best_article_path_via_http (for search) are correct and omitted for brevity.
# Der SC Jülich (offiziell: Sport-Club Jülich 1910 e. V.) war ein Fußballverein im nordrhein-westfälischen Jülich im Kreis Düren. Größte Erfolge des Vereins waren der Gewinn der Deutschen Amateurmeisterschaft in den Jahren 1969 bis 1971. Damit ist der SC Jülich der erfolgreichste Amateurverein Deutschlands.[1]Wölfe steht für: Film und Fernsehen: Siehe auch:Das Krankenhaus Jülich (bis 2023 St. Elisabeth-Krankenhaus Jülich[2]) ist ein Krankenhaus in städtischer Trägerschaft mit 156 Betten in Jülich im nordrhein-westfälischen Kreis Düren.Das Krankenhaus Jülich (bis 2023 St. Elisabeth-Krankenhaus Jülich[2]) ist ein Krankenhaus in städtischer Trägerschaft mit 156 Betten in Jülich im nordrhein-westfälischen Kreis Düren.

import logging
import os
import inspect

LOG_FILE = os.path.expanduser("~/kiwix_debug.log") # <-- NEU
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_debug(message: str):
    """ Schreibt eine Debug-Nachricht mit Zeilennummer des Aufrufers in die Konsole. """

    caller_info = "UNKNOWN:0"

    # inspect.stack() gibt eine Liste von Frame-Infos zurück
    stack = inspect.stack()

    # Wir überspringen den Frame 0 (die aktuelle log_debug Funktion) und den Frame 1 (die print-Funktion, oft interne)
    # Wir nehmen Frame 2, der die eigentliche aufrufende Funktion sein sollte (z.B. execute)
    if len(stack) > 1:
        # stack[2] ist der Frame der Funktion, die log_debug aufgerufen hat (z.B. execute)
        frame_info = stack[1]

        # Holen Sie nur den Dateinamen (basename) und die Zeilennummer
        try:
            filename = os.path.basename(frame_info.filename)
            line_number = frame_info.lineno
            caller_info = f"{filename}:{line_number}"
        except Exception:
            pass # Bleibe bei UNKNOWN

    # Die Ausgabe der Nachricht mit den gefundenen Informationen
    print(f"[DEBUG] {caller_info}: {message}", file=sys.stderr)



def _follow_soft_redirect(soup: BeautifulSoup, zim_url_part: str) -> str | None:
    """
    Looks for the first link in the main Wikipedia content div
    that points to another internal article.
    """

    # 1. Finde den Haupt-Content-Bereich (Wikipedia-Standard-Div)
    main_content_div = soup.find('div', class_='mw-parser-output')

    if not main_content_div:
        # Fallback auf den Body
        main_content_div = soup.find('body')

    if not main_content_div:
        return None

    # 2. Finde den allerersten Link im Hauptinhalt
    # Dieser Link ist sehr wahrscheinlich der Soft-Redirect.
    first_internal_link = main_content_div.find('a', href=True, title=True)

    if not first_internal_link:
        return None

    redirect_title = first_internal_link.get('title')


    # Der Link muss eine URL des Typs /viewer#... haben (wird in der vorherigen
    # Funktion schon gefiltert, aber hier zur Sicherheit nochmal).
    if not first_internal_link.get('href').startswith(f"/viewer#{zim_url_part}/"):
        return None

    # 3. Wenn der Link ein 'title'-Attribut hat (der reine Artikelname)
    if redirect_title:
        # Wir wollen keine internen Anker-Links verfolgen (z.B. 'Krankenhaus#Geschichte')
        if "#" not in redirect_title:
            return redirect_title

    return None






def _find_best_link_by_exact_title(soup: BeautifulSoup, original_search_term: str) -> str | None:
    """
    Searches the entire page for a link whose text EXACTLY matches
    the original search term (case-insensitive).
    """

    normalized_search = original_search_term.lower()

    # Durchsuche alle Links im Body
    for link in soup.find_all('a', href=True):
        link_text = link.get_text().strip()

        # Prüfe, ob der Link-Text EXAKT dem Suchbegriff entspricht (Case-Insensitive)
        if link_text.lower() == normalized_search:
            title_attr = link.get('title')

            # Wähle den saubersten Titel für die nächste Suche
            if title_attr and "#" not in title_attr:
                return title_attr

            # Fallback: Wenn title fehlt, verwende den Link-Text selbst
            return link_text

    return None




def _get_link_title_from_first_paragraph(soup: BeautifulSoup) -> str | None:
    """
    Finds the first internal article link in the body, which is the target
    of a soft redirect.
    """

    body_content = soup.find('body')
    if not body_content:
        return None

    # Durchlaufe alle Links im Body, um den ersten gültigen zu finden (der erste gefundene Link ist oft der Redirect)
    for link in body_content.find_all('a', href=True):
        href = link.get('href')

        # [REDUZIERTE FILTERLOGIK]
        # Nur ignorieren, was definitiv KEIN Artikel ist:
        if (href.startswith('http') or href.startswith('mailto:') or href.startswith('geo:') or href.startswith('#') or href.endswith(('.png', '.jpg', '.pdf'))):
            continue

        # Hier ist der erste geeignete Link gefunden, der kein Anchor oder externes Protokoll ist.

        # Priority 1: Title-Attribut (sauberster Titel)
        redirect_title = link.get('title')
        if redirect_title and "#" not in redirect_title:
            return redirect_title

        # Priority 2: HREF selbst verwenden (z.B. "Krankenhaus")
        # Wir müssen sicherstellen, dass er URL-Decodiert ist und kurz genug.
        title_from_href = unquote(href.split('#', 1)[0])

        # Wir akzeptieren ihn, wenn er kurz ist (keine langen URLs) und keine Verzeichnisse enthält.
        if title_from_href and len(title_from_href) < 50 and '/' not in title_from_href:
            return title_from_href

    return None



def _find_best_article_path_via_http(search_term: str, zim_file: str) -> str | None:
    """
    Performs a search via the kiwix-serve HTTP API and finds the best article path.

    The best match logic is:
    1. Exact match with the search term (case-insensitive)
    2. Shortest title that is NOT a 'Begriffsklärung' page.
    3. The first result from the server as a fallback.
    """

    final_content_path = None



    search_url = (
        f"{BASE_SERVER_URL}/search?"
        f"pattern={quote(search_term)}&"
        f"book={zim_file}"
    )

    log_debug(f"search_url:{search_url}")


    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        result_links = soup.select('div.results ul li a')

        if not result_links:
            return None

        best_path = None
        shortest_non_disambiguation_path = None
        shortest_length = float('inf')


        log_debug(f"search_term.lower():{search_term.lower()}")

        normalized_search = re.sub(r'[^a-z0-9\s]', '', search_term.lower())
        log_debug(f"normalized_search:{normalized_search}")

        for link in result_links:
            href = link.get('href')
            link_text = link.get_text().strip()

            log_debug(f"link_text:{link_text}")


            normalized_link_text = re.sub(r'[^a-z0-9\s]', '', link_text.lower())

            normalized_search = re.sub(r'[^a-z0-9\s]', '', search_term.lower())
            log_debug(f"normalized_search:{normalized_search}")


            if normalized_link_text == normalized_search:
                # Wir haben den Hauptartikel gefunden! Hier abbrechen.
                log_debug(f"Exact Match found: '{link_text}'")
                log_debug(f"{href}")
                return href
                #return final_content_path

            article_path_with_hash = href.split('#', 1)[-1]
            final_content_path = f"/{article_path_with_hash}"

            if link_text.lower() == search_term.lower():
                return final_content_path

            #if "Begriffsklärung" not in link_text and "Begriffsklärung" not in link_text:
            if len(link_text) < shortest_length:
                shortest_length = len(link_text)
                shortest_non_disambiguation_path = final_content_path

            if best_path is None:
                best_path = final_content_path

        if shortest_non_disambiguation_path:
            log_debug(f"shortest_non_disambiguation_path:{shortest_non_disambiguation_path}")

            return shortest_non_disambiguation_path

        return best_path

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch search URL. Is kiwix-serve running? Error: {e}")
        return None





# Die Hilfsfunktion, die den allerersten internen Link findet (der Hauptartikel)
def _get_main_topic_link(soup: BeautifulSoup) -> str | None:
    # Hier verwenden wir die Logik, die den ERSTEN nicht-externen Link findet (z.B. 'Krankenhaus')
    # ... [Wir verwenden die Logik aus der vorherigen Antwort, die den Link zuverlässig findet] ...

    body_content = soup.find('body')
    if not body_content: return None

    for link in body_content.find_all('a', href=True):
        href = link.get('href')

        # Filtern von Dingen, die KEIN Artikel sind
        if (href.startswith('http') or href.startswith('mailto:') or href.startswith('geo:') or href.startswith('#') or href.endswith(('.png', '.jpg', '.pdf'))):
            continue

        # Hier ist der erste geeignete Link gefunden, der Hauptartikel-Link
        redirect_title = link.get('title')
        if redirect_title and "#" not in redirect_title:
            return redirect_title

        title_from_href = unquote(href.split('#', 1)[0])
        if title_from_href and len(title_from_href) < 50 and '/' not in title_from_href:
            return title_from_href

    return None


def _construct_article_url(article_title: str) -> str:
    """ Konstruiert die direkte URL zum Artikel ohne unnötige Suche. """
    encoded_title = quote(article_title)
    zim_url_part = ZIM_FILE_NAME.replace('.zim', '')
    # Die URL ist: /<ZIM_PART>/<ARTICLE_TITLE> (ohne /viewer#...)
    return f"{BASE_SERVER_URL}/{zim_url_part}/{encoded_title}"



def execute(match_data):
    """
    Main execution function: Searches via HTTP, fetches the full text, and handles soft redirects.
    """

    log_debug("--- START of EXECUTE ---")

    current_search_term = match_data['regex_match_obj'].group(2).strip()

    log_debug(f"Initial Search Term: {current_search_term}")
    log_debug(f'current_search_term={current_search_term}')

    original_search_term = current_search_term # Der Begriff, den wir nicht verlieren dürfen
    log_debug(f'original_search_term={original_search_term}')

    try:
        match_obj = match_data['regex_match_obj']
        search_term = match_obj.group(2).strip()

        # Step 1: Search and fetch the initial best article
        article_path = _find_best_article_path_via_http(search_term, ZIM_FILE_NAME)

        if not article_path:
            return f"No articles found for search term: '{search_term}'"

        server_article_url = f"{BASE_SERVER_URL}{article_path}"
        response = requests.get(server_article_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')


#Das Krankenhaus Jülich (bis 2023 St. Elisabeth-Krankenhaus Jülich[2])
#Das Krankenhaus Jülich (bis 2023 St. Elisabeth-Krankenhaus Jülich[2]) ist ein Krankenhaus in städtischer Trägerschaft mit 156 Betten in Jülich im nordrhein-westfälischen Kreis Düren.


        current_soup = soup
        final_article_path = article_path

        current_article_title = unquote(final_article_path.split('/')[-1])

        # Max. 3 Mal springen
        for i in range(3):
            # Link zum Hauptthema-Link finden
            redirect_target_title = _find_best_link_by_exact_title(current_soup, original_search_term)

            if redirect_target_title:

                # WICHTIGE PRÜFUNG: Wenn der Link-Titel identisch ist mit dem aktuell geladenen Artikel-Titel, ABBRUCH
                if redirect_target_title.lower() == current_article_title.lower():
                    log_debug(f"INFO: Redirect target '{redirect_target_title}' is the current page. Stopping redirect.")
                    break

                # HIER IST DER SPRUNG (DIREKTE KONSTRUKTION)
                log_debug(f"INFO: Found link to main topic '{redirect_target_title}' on page '{current_article_title}'. Directly fetching...")

                # Setze den neuen Suchbegriff auf den Link-Titel ('Krankenhaus')
                new_search_term = redirect_target_title

                # 1. DIREKTE URL KONSTRUIEREN (KEIN UNSICHERES _find_best_article_path_via_http MEHR)
                new_url = _construct_article_url(new_search_term)

                # Die URL enthält den neuen Titel, der garantiert korrekt ist
                final_article_path = urlparse(new_url).path
                current_article_title = new_search_term # Titel für die nächste Iteration setzen

                # 2. Den neuen Artikel abrufen und zur Überprüfung der nächsten Stufe verwenden
                response = requests.get(new_url, timeout=10)
                response.raise_for_status()
                current_soup = BeautifulSoup(response.content, 'html.parser')

                continue # Nächste Schleifen-Iteration
            else:
                break

        soup = current_soup


#An unexpected error occurred: cannot access local variable 'current_article_title' where it is not associated with a valueTraceback (most recent call last):File "/home/seeh/projects/py/STT/config/maps/plugins/standard_actions/de-DE/wikipedia_local.py", line 274, in executeif redirect_target_title.lower() == current_article_title.lower():^^^^^^^^^^^^^^^^^^^^^UnboundLocalError: cannot access local variable 'current_article_title' where it is not associated with a value


        # --- TEXT AND LINK EXTRACTION (Rest of the original logic) ---

        # ... [Rest des Skripts zur Text- und Link-Extraktion]

        article_text_parts = []
        if soup.find('body'):
            paragraphs = soup.find('body').find_all('p')
            article_text_parts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

        full_article_text = "\n\n".join(article_text_parts)
        clean_article_text = ' '.join(full_article_text.split())

        internal_links = set()
        zim_prefix = f"/viewer#{ZIM_URL_PART}/"

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and href.startswith(zim_prefix):
                title_attr = link.get('title')
                if title_attr:
                    if not title_attr.startswith('#'):
                        internal_links.add(title_attr)
                else:
                    path = href.replace(zim_prefix, '', 1)
                    decoded_path = unquote(path)
                    base_title = decoded_path.split('#', 1)[0]
                    internal_links.add(base_title)

        if internal_links:
            link_list = " | ".join(sorted(list(internal_links)))
            link_footer = f"\n\nSiehe auch (Suchbegriffe): {link_list}"
            return clean_article_text + link_footer

        return clean_article_text

    except requests.exceptions.RequestException as e:
        return f"ERROR: Failed to fetch article URL '{server_article_url}'. Is kiwix-serve running? Error: {e}"
    except Exception as e:
        import traceback
        return f"An unexpected error occurred: {e}\n{traceback.format_exc()}"


# Fügen Sie dies ganz oben in Ihrem Skript ein (oder anstelle der fehlerhaften NamedTuple-Definition)
class DummyMatch:
    def __init__(self, group2_value: str):
        self._group2_value = group2_value

    def group(self, index: int):
        """ Simulates re.match.group(index) """
        if index == 2:
            return self._group2_value
        raise IndexError(f"DummyMatch only supports group(2). Tried index {index}")

# 2. Korrigiere den Test-Aufruf:
if __name__ == '__main__':

    # Testfall 1: Krankenhäuser
    test_term_1 = "krankenhaus"

    # Simuliere das match_data-Dictionary, das group(2) ausgibt
    dummy_match_obj_1 = DummyMatch(group2_value=test_term_1)
    test_match_data_1 = {'regex_match_obj': dummy_match_obj_1}

    print("-" * 50)
    print(f"TEST 1: {test_term_1}")

    text_t_1 = execute(test_match_data_1)

    print(text_t_1)
    print("-" * 50)


    test_term = "python"
    dummy_match_obj = DummyMatch(group2_value=test_term)
    test_match_data = {'regex_match_obj': dummy_match_obj}
    print("-" * 50)
    print(f"TEST 1: {test_term}")
    text_t = execute(test_match_data)
    print(text_t)
    print("-" * 50)

    test_term = "Python_(Programmiersprache)"
    dummy_match_obj = DummyMatch(group2_value=test_term)
    test_match_data = {'regex_match_obj': dummy_match_obj}
    print("-" * 50)
    print(f"TEST 1: {test_term}")
    text_t = execute(test_match_data)
    print(text_t)
    print("-" * 50)



