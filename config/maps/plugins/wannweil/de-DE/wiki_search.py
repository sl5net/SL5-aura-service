"""
pip install wikipedia-api

pip vs. pip3: Auf manchen Systemen (besonders Linux) musst du eventuell pip3 verwenden, um sicherzustellen, dass es für deine Python 3-Version installiert wird:

pip3 install wikipedia-api

"""

import wikipediaapi

def execute(match_data):
    """ Sucht nach einem Begriff auf Wikipedia und gibt die Zusammenfassung zurück. """
    try:
        # User-Agent ist guter Stil bei API-Anfragen
        wiki_wiki = wikipediaapi.Wikipedia('de', headers={'User-Agent': 'MySpeechApp/1.0'})
        #
        search_term = match_data['regex_match_obj'].group(2).strip()
        if not search_term:
            return "Was soll ich denn suchen?"

        page = wiki_wiki.page(search_term)

        if not page.exists():
            return f"Ich konnte leider keinen Wikipedia-Eintrag für '{search_term}' finden."

        # Gib die ersten 2-3 Sätze der Zusammenfassung zurück, um die Antwort kurz zu halten.
        summary = ". ".join(page.summary.split(". ")[:2]) + "."
        return f"Laut Wikipedia: {summary}"

    except Exception as e:
        return f"Bei der Suche ist ein Fehler aufgetreten: {e}"
