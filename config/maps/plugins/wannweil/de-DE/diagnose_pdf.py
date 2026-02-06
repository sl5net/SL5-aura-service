# config/maps/plugins/wannweil/de-DE/diagnose_pdf.py
import os
import pdfplumber

# Pfad relativ zum Skript bestimmen
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "Abfallterminuebersicht-01-12-2026-1.pdf")

if not os.path.exists(pdf_path):
    print(f"FEHLER: Datei nicht gefunden: {pdf_path}")
    exit()

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    chars = page.chars
    rects = page.rects
    images = page.images

    print(f"--- DIAGNOSE FÜR {os.path.basename(pdf_path)} ---")
    print(f"Anzahl gefundene Zeichen (Text): {len(chars)}")
    print(f"Anzahl gefundene Rechtecke (Grafik): {len(rects)}")
    print(f"Anzahl gefundene Bilder: {len(images)}")
    print("\n--- TEXT-AUSZUG (ERSTE 500 ZEICHEN) ---")
    if text:
        print(text[:500])
    else:
        print("KEIN TEXT EXTRAHIERBAR")
