import genanki

# Unique IDs for Model and Deck (keep these constant to allow updates)
MODEL_ID = 1607392319
DECK_ID = 2059400110

# 1. Define the Card Layout
python_model = genanki.Model(
  MODEL_ID,
  'Python-Tresor Model',
  fields=[{'name': 'Frage'}, {'name': 'Antwort'}],
  templates=[{
    'name': 'Standard Karte',
    'qfmt': '<div style="font-family: Arial; font-size: 20px; text-align: center;">{{Frage}}</div>',
    'afmt': '{{FrontSide}}<hr id="answer"><div style="font-family: Monaco; color: blue;">{{Answer}}</div>',
  }])

# 2. Create the Deck
my_deck = genanki.Deck(DECK_ID, 'Python-Tresor: Grundlagen')

# 3. Add Cards
tasks = [
    ('Wie erzeugt man einen digitalen Schlüssel (Datei schreiben)?', 'with open(".schluessel", "w") as f:'),
    ('Wie prüft man, ob das Wetter "Sonne" ist?', 'if wetter == "sonne":'),
]

for q, a in tasks:
    note = genanki.Note(model=python_model, fields=[q, a])
    my_deck.add_note(note)

# 4. Export
genanki.Package(my_deck).write_to_file('Python_Tresor_Basis.apkg')
print("Deck erfolgreich erstellt: Python_Tresor_Basis.apkg")

