import pdfplumber
import re
import datetime

def parse_abfall_pdf(pdf_path):
    termine = []
    # Monate auf Deutsch für das Parsing
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni",
              "Juli", "August", "September", "Oktober", "November", "Dezember"]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            aktueller_monat = None
            for line in lines:
                # Prüfe, welcher Monat gerade bearbeitet wird
                for i, m in enumerate(monate):
                    if m in line:
                        aktueller_monat = i + 1

                # Suche nach Mustern wie "12 Di R" oder "05 Mi B, P"
                # Erläuterung: Tag (1-2 Stellen), Wochentag (2 Stellen), Abfall-Kürzel
                match = re.search(r'(\d{1,2})\s+[A-Z][a-z]\s+([R,B,P,G,\s]+)', line)

                if match and aktueller_monat:
                    tag = int(match.group(1))
                    typen_raw = match.group(2)

                    # Bereinige die Abfalltypen
                    typen = [t.strip() for t in typen_raw.replace(',', ' ').split()]

                    # Nur gültige Typen filtern
                    valid_types = [t for t in typen if t in ['R', 'B', 'P', 'G']]

                    if valid_types:
                        datum = datetime.date(2026, aktueller_monat, tag)
                        termine.append({"datum": datum, "typen": valid_types})
    return termine

# Beispiel-Anwendung
if __name__ == "__main__":
    # Pfad zu deinem Download
    data = parse_abfall_pdf("Abfallterminuebersicht-01-12-2026-1.pdf")
    for t in data:
        print(f"{t['datum']}: {', '.join(t['typen'])}")

