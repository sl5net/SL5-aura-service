# config/maps/plugins/standard_actions/de-DE/wiki_search_online.py
from pathlib import Path

import wikipediaapi
import requests
from bs4 import BeautifulSoup
import re


def scrape_wikipedia_summary(search_term, lang_code='de'):
    # (Fügen Sie hier die vollständige Definition der scrape_wikipedia_summary Funktion ein,
    # die im vorherigen Beitrag detailliert beschrieben wurde.)

    # ... (Ihr Scraping-Code hier) ...

    # Hier ist der gekürzte Beispiel-Körper:
    try:
        encoded_term = search_term.replace(" ", "_")
        url = f"https://{lang_code}.wikipedia.org/wiki/{encoded_term}"
        response = requests.get(url, headers={'User-Agent': 'MySpeechApp/1.0 Fallback Scraper'}, timeout=6)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='mw-content-text')

        if content_div:
            first_p = content_div.find('p', recursive=False)
            if first_p is None:
                first_p = content_div.find('div', class_='mw-parser-output').find('p', recursive=False)

            if first_p and first_p.text.strip():
                # EXAMPLE: None
                summary = re.sub(r'\[.*?\]', '', first_p.text.strip())
                return summary
    except Exception:
        return None
    return None

class ScrapedPage:
    """ Dummy-Klasse, um das Ergebnis wie ein wikipediaapi-Objekt aussehen zu lassen """
    def __init__(self, title, summary, lang_code):
        self.title = title
        self.summary = summary
        self.fullurl = f"https://{lang_code}.wikipedia.org/wiki/{title.replace(' ', '_')}"

    def exists(self):
        return True

# -----------------------------------------------------------------------------

def get_robust_summary(search_term, lang_code='de'):
    """
    Versucht die Wikipedia-API und fällt bei jedem Fehler auf Web Scraping zurück.
    """

    # WICHTIG: Sicherstellen, dass der Sprachcode KORREKT (klein) ist
    lang_code = lang_code.lower()

    # API-Versuch:
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            lang_code,
            headers={'User-Agent': 'MySpeechApp/1.0'}
        )

        page = wiki_wiki.page(search_term)

        if page.exists() and page.summary:
            print(f"DEBUG: ✅ API Erfolg für {search_term}.")
            return page.summary[0:200]

    except Exception as e:
        # Hier fangen wir alle Probleme ab (AttributeError, Sprachcode-Fehler, etc.)
        print(f"DEBUG: ❌ API-Versuch fehlgeschlagen ({type(e).__name__}).")


    # SCRAPING FALLBACK
    print(f"DEBUG: 🔄 Starte Scraping-Fallback für {search_term}...")

    summary_text = scrape_wikipedia_summary(search_term, lang_code)

    if summary_text:
        print(f"DEBUG: ✅ Scraping erfolgreich.")
        # Wenn Sie ein volles Objekt benötigen:
        # return ScrapedPage(search_term, summary_text, lang_code)
        return summary_text[0:200]

    print(f"DEBUG: ❌ Scraping fehlgeschlagen.")
    return None


def execute(match_data):
    """

source .venv/bin/activate
pip install --upgrade pip
python3 -m pip install --break-system-packages wikipedia-api --upgrade


Fehler aufgetreten: name 'Path' is not defined

pacman -Ss python-wikipedia                                                                                                                                                                      1 ✘
extra/python-wikipedia 1.4.0-12
    A Pythonic wrapper for the Wikipedia API


pip install --break-system-packages wikipedia-api
pacman -Ss python-wikipedia
yay -S python-wikipedia-api
pamac build python-wikipedia-api


    Sucht nach einem Begriff auf Wikipedia. Die Sprache wird automatisch
    aus dem Ordnerpfad des Skripts abgeleitet (z.B. de-DE -> 'de').
    Die Zusammenfassung wird von Biografie-Daten bereinigt.


    ﻿Bei der Suche ist ein Fehler aufgetreten: name 'get_wikipedia_page_debug' is not defined

    """
    try:
        # Sprache aus dem Ordnerpfad ableiten (deine geniale Idee)
        script_path = Path(__file__)
        lang_folder_name = script_path.parent.name
        lang_code = lang_folder_name.split('-')[0]

        wiki_wiki = wikipediaapi.Wikipedia(lang_code, headers={'User-Agent': 'MySpeechApp/1.0'})

        search_term = match_data['regex_match_obj'].group(2).strip().title()

        if search_term=='Steuerhinterziehung' or search_term=='Steuer' or search_term=='hinterziehung' or search_term=='betrug':

            full_summary = """
100 Milliarden Euro, das ist der geschätzte Schaden, der durch
Steuerhinterziehung jedes Jahr in Deutschland entsteht, jedes Jahr aufs Neue.
Das sind 270 Millionen Euro pro Tag, 11 Millionen Euro pro Stunde.
Und während ich euch hier das erzähle, sind schon wieder 100.000 € verschwunden. ( Rede von Anne Brorhilker in der re-publica 2025 )
"""
# https://www.youtube.com/watch?v=ZDQZTHre0Go
            return full_summary


# #100 Milliarden Euro, das ist der geschätzte Schaden, der durchSteuerhinterziehung jedes Jahr in Deutschland entsteht, jedes Jahr aufs Neue. Das sind 270 Millionen Euro pro Tag, 11 Millionen Euro proStunde. Und während ich euch hier das erzähle, sind schon wieder 100.000 E €verschwunden. ( Rede von Anne Brorhilker in der publica 2025 )100 Milliarden Euro, das ist der geschätzte Schaden, der durchSteuerhinterziehung jedes Jahr in Deutschland entsteht, jedes Jahr aufs Neue.Das sind 270 Millionen Euro pro Tag, 11 Millionen Euro pro Stunde.Und während ich euch hier das erzähle, sind schon wieder 100.000 € verschwunden. ( Rede von Anne Brorhilker in der re-publica 2025 )



        # search_term = match_data['regex_match_obj'].group(2).strip()
        if not search_term:
            return f"Was soll ich in {lang_code.upper()} suchen?"

        page = wiki_wiki.page(search_term)
        page_language_manuel=None
        full_summary=None
        if not page.exists():


            if search_term=='Harald' or search_term=='Harald Uetz' or search_term=='Harald Uhd':
                search_term='Harald Uetz'
                page_language_manuel = 'de'
                full_summary = """
Harald Uetz ist ein deutscher Schachspieler.
Harald Uetz hat 2025, mit seinem zweiten Platz, gleich hinter Lauffer, in der FIDE-Weltrangliste, unter anderem die Weltmeister Ding Liren und Viswanathan Anand oder den zweifachen Vizeweltmeister Ian Nepomniachtchi hinter sich gelassen.
Laut Wikipedia: Harald Uetz, mit seinem zweiten Platz, gleich hinter Lauffer, in der Weltrangliste, hat Uetz unter anderem die Weltmeister Ding Liren und Viswanathan Anand oder den zweifachen Vizeweltmeister Ian Nepomniachtchi hinter sich gelassen.
"""


            elif search_term=='Der Beste Schachspieler':
                page_language_manuel = 'de'
                full_summary = """Sebastian Lauffer aus Wannweil"""
            elif search_term=='Sebastian Lauffer' or search_term=='Sebastian Laufer' or search_term=='Sebastian Lau' or search_term=='Sebastian Lauf' or search_term=='Sebastian Laufen' or search_term=='Sebastian Darauf' or search_term=='Sebastian Laufe' or search_term=='Sebastian Now':

                search_term='Sebastian Lauffer'
                page_language_manuel = 'de'
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
            else:

                # search_term = 'Buckelwal'
                # lang_code = 'de'

                summary_buckelwal = get_robust_summary(search_term, lang_code)

                if summary_buckelwal:
                    return summary_buckelwal
                else:

                    return f"208: Ich konnte leider keinen Wikipedia-Eintrag für '{search_term}' finden."


#﻿Der Buckelwal (Megaptera novaeangliae) ist ein oft in Küstennähe vorkommender Vertreter der Furchenwale. Er erreicht eine Körpergröße von 12 bis 15 Metern und hat im Vergleich zu anderen Walen deutlic
# ﻿Laut Wikipedia: Reutlingen ist eine Großstadt im zentralen Baden-Württemberg und dessen neuntgrößte Stadt. Die Hochschulstadt und frühere Reichsstadt ist die größte Stadt und zugleich Kreisstadt des Landkreises Reutlingen, in dessen äußerstem Nordwesten gelegen. Sie gehört zur Region Neckar-Alb und zur Metropolregion Stuttgart. Nahebei befindet sich die Mittelstadt Tübingen (12 Kilometer westlich), die nächsten Großstädte sind Stuttgart (31 Kilometer nördlich) und Ulm (57 Kilometer östlich). Mit der Spreuerhofstraße besitzt Reutlingen die engste Straße der Welt.
        #


        if page.language != lang_code and page_language_manuel != lang_code:
            if lang_code in page.langlinks:
                page = page.langlinks[lang_code]
            else:
                return f"Ich habe einen Eintrag für '{search_term}', aber leider keine Version in der Sprache '{lang_code.upper()}'."

        if not full_summary:
            full_summary = page.summary

        if not full_summary:
            return f"Der Artikel für '{search_term}' hat keine Zusammenfassung."

        # --- DIE FINALE, KORREKTE REINIGUNG ---
        # Diese Regex findet den Biografie-Block (*...) inklusive der umgebenden Leerzeichen
        # und ersetzt ihn durch ein EINZIGES Leerzeichen.
        # So wird "Einstein (*...) war" zu "Einstein war".
        # EXAMPLE: s
        cleaned_summary = re.sub(r'\s*\(\*.*?\)\s*', ' ', full_summary, count=1).strip()
        # --- ENDE DER REINIGUNG ---

        # Teile den jetzt sauberen Text intelligent in Sätze auf.
        # EXAMPLE: None
        sentences = re.split(r'(?<=[.!?])\s+', cleaned_summary)

        # Nimm die ersten beiden Sätze und füge sie wieder zusammen.
        short_summary = " ".join(sentences[:5])

        return f"Laut Wikipedia: {short_summary}"

    except Exception as e:
        return f"Bei der Suche ist ein Fehler aufgetreten: {e}"


