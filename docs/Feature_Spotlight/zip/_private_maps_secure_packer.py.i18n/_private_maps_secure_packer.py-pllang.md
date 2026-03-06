importuj os
podproces importu
rejestrowanie importu
importuj Shuil
z pathlib Ścieżka importu

logger = logowanie.getLogger(__nazwa__)

def wykonaj (dane):
przechodzić

def on_reload():
„””
Erstellt ein „Matryoshka-ZIP”:
Zamów -> wewnętrzny.zip (aura_secure.blob) -> hasło.zip
Versteckt die komplette Verzeichnisstruktur.
„””
logger.info("🔒 SecurePacker (Matryoshka): Starte Sicherung...")

bieżący_katalog = Ścieżka(__plik__).nadrzędny
katalog_nadrzędny = katalog bieżący.nadrzędny

# Name des äußeren ZIP
zip_name_outer = nazwa_bieżącego_katalogu.lstrip('_') + ".zip"
zip_path_outer = katalog_nadrzędny / nazwa_zip_zewnętrzny

# 1. Wyszukaj hasło
plik_klucza = następny(katalog_nadrzędny.glob(".*.py"), Brak)
jeśli nie plik_klucza:
logger.error("❌ Plik klucza nie działa!")
powrót

hasło = _extract_password(plik_klucza)
jeśli nie hasło:
logger.error("❌ Hasło nie zostało odzyskane!")
powrót

# 2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen es temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip = katalog_nadrzędny / "aura_secure_temp" # wird zu .zip

próbować:
# Utwórz aura_secure_temp.zip
Shutil.make_archive(str(temp_inner_zip), 'zip', str(bieżący_katalog))
temp_inner_zip_file = katalog_nadrzędny / "aura_secure_temp.zip"

# Umbenennen in den neutralen Blob-Namen
blob_name = "aura_secure.blob"
ścieżka_bloba = katalog_nadrzędny / nazwa_bloba
Shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ĘUßERES ZIP erstellen (Verschlüsselt)
if subprocess.call("polecenie -v zip", Shell=True, stdout=subprocess.DEVNULL) != 0:
logger.error("❌ 'zip' Befehl fehlt.")
powrót

# Wir Packen NUR den Blob w ZIP
cmd = [
„zip”, „-j”, # -j: niepotrzebne ścieżki (keine Pfade speichern, nur Dateiname)
„-P”, hasło,
str(zip_path_outer),
str(ścieżka_bloba)
]

proces = subprocess.run(cmd, przechwytywanie_output=prawda, tekst=prawda)

# Aufräumen des Blobs
os.remove(ścieżka_bloba)

jeśli kod procesu.powrotny == 0:
logger.info(f"✅ SecurePacker: Struktur verstektt w pliku {zip_name_outer} gespeichert.")
w przeciwnym razie:
logger.error(f"❌ ZIP Fehler: {process.stderr}")

z wyjątkiem wyjątku jako e:
logger.error(f"❌ Spakuj Fehlera: {e}")

def _extract_password(ścieżka_klucza):
próbować:
z open(key_path, 'r', encoding='utf-8') jako f:
dla linii w f:
if line.strip().startswith("#"):
clean = linia.strip().lstrip("#").strip()
jeśli czyste: zwróć czyste
z wyjątkiem: pass
zwróć Brak