import wikipediaapi
import re
from pathlib import Path

def execute(match_data):
    """
    Sucht nach einem Begriff auf Wikipedia. Die Sprache wird automatisch
    aus dem Ordnerpfad des Skripts abgeleitet (z.B. de-DE -> 'de').
    Die Zusammenfassung wird von Biografie-Daten bereinigt.
    """
    try:
        # Sprache aus dem Ordnerpfad ableiten (deine geniale Idee)
        script_path = Path(__file__)
        lang_folder_name = script_path.parent.name
        lang_code = lang_folder_name.split('-')[0]

        wiki_wiki = wikipediaapi.Wikipedia(lang_code, headers={'User-Agent': 'MySpeechApp/1.0'})

        search_term = match_data['regex_match_obj'].group(2).strip().title()

        #

        # search_term = match_data['regex_match_obj'].group(2).strip()
        if not search_term:
            return f"Was soll ich in {lang_code.upper()} suchen?"

        page = wiki_wiki.page(search_term)

        if not page.exists():
            return f"Ich konnte leider keinen Wikipedia-Eintrag für '{search_term}' finden."

        if page.language != lang_code:
            if lang_code in page.langlinks:
                page = page.langlinks[lang_code]
            else:
                return f"Ich habe einen Eintrag für '{search_term}', aber leider keine Version in der Sprache '{lang_code.upper()}'."

        full_summary = page.summary
        if not full_summary:
            return f"Der Artikel für '{search_term}' hat keine Zusammenfassung."

        # --- DIE FINALE, KORREKTE REINIGUNG ---
        # Diese Regex findet den Biografie-Block (*...) inklusive der umgebenden Leerzeichen
        # und ersetzt ihn durch ein EINZIGES Leerzeichen.
        # So wird "Einstein (*...) war" zu "Einstein war".
        cleaned_summary = re.sub(r'\s*\(\*.*?\)\s*', ' ', full_summary, count=1).strip()
        # --- ENDE DER REINIGUNG ---

        # Teile den jetzt sauberen Text intelligent in Sätze auf.
        sentences = re.split(r'(?<=[.!?])\s+', cleaned_summary)

        # Nimm die ersten beiden Sätze und füge sie wieder zusammen.
        short_summary = " ".join(sentences[:2])

        return f"Laut Wikipedia: {short_summary}"

    except Exception as e:
        return f"Bei der Suche ist ein Fehler aufgetreten: {e}"
